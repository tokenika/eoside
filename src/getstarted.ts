import * as path from 'path'
import * as vscode from 'vscode'
import * as fs from 'fs'

import * as def from './definitions'
import * as inst from './install'

const TEMPLATE: string = "template"
const TEMPLATE_DIR: string = "templates"
const RECENT: string = "recent"
const RECENT_JSON: string = RECENT + ".json"
const GET_STARTED: string = "getstarted"
const GET_STARTED_JSON: string = GET_STARTED + ".json"
const OPEN: string = "open"

export default class GetStartedPanel extends def.Panel {
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: GetStartedPanel | undefined
    public static readonly viewType = "EOS IDE"
    private static c_cpp_prop_updated = false

    public static createOrShow(
                        extensionPath: string, checkFolders:boolean=true) {

        if(vscode.workspace.workspaceFolders 
                && !GetStartedPanel.c_cpp_prop_updated){

            GetStartedPanel.c_cpp_prop_updated = true
            let c_cpp_prop_path = path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath, 
                    ".vscode", "c_cpp_properties.json")

            if(fs.existsSync(c_cpp_prop_path)){
                let cl = 'python3 -m eosfactory.core.vscode '
                + `--c_cpp_prop_path \\"${c_cpp_prop_path}\\" `
                + `--root \\"${inst.root()}\\" `
                def.callEosfactory(cl, (stdout:string, stderr:string) =>{})
            }
        }

        if(checkFolders){
            if(
                vscode.workspace.workspaceFolders 
                    || !vscode.workspace.getConfiguration()
                                                    .eoside.startWithEosIde){
                return
            }
        }

        const column = vscode.window.activeTextEditor 
            ? vscode.window.activeTextEditor.viewColumn : undefined

        // If we already have a panel, show it.
        if (GetStartedPanel.currentPanel) {
            GetStartedPanel.currentPanel._panel.reveal(column)
            return
        }

        // Otherwise, create a new panel.
        const panel = vscode.window.createWebviewPanel(
                GetStartedPanel.viewType, "EOS IDE", 
                column || vscode.ViewColumn.One, {
            // Enable javascript in the webview
            enableScripts: true,

            // And restrict the webview to only loading content from our 
            // extension's `media` directory.
            localResourceRoots: [
                vscode.Uri.file(path.join(extensionPath, def.RESOURCE_DIR))
            ]
            }
        )

        GetStartedPanel.currentPanel = new GetStartedPanel(
                                                        panel, extensionPath)        
    }

    protected constructor(
        panel: vscode.WebviewPanel,
        extensionPath: string
    ) {
        super(panel, extensionPath)
        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview()

        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(message => {
            switch (message.title) {
                case TEMPLATE:
                    Templates.createOrGet(this._extensionPath)
                        .action(message.id)
                    break
                case RECENT:
                    Recent.createOrGet(this._extensionPath).open(message.id)
                    break
                case GET_STARTED:
                    GetStarted.createOrGet(this._extensionPath)
                        .open(message.id)
                    break
                case OPEN:
                    if(message.id === "open_folder"){
                        vscode.commands.executeCommand('vscode.openFolder')
                    }
                    break
            }
        }, null, this._disposables)
    }

    public dispose() {
        super.dispose()
        GetStartedPanel.currentPanel = undefined
    }

    private _getHtmlForWebview() {
        const scriptPathOnDisk = vscode.Uri.file(path.join(
            this._extensionPath, def.RESOURCE_DIR, 'getstarted.js'))

        // And the uri we use to load this script in the webview
        const scriptUri = scriptPathOnDisk.with({ scheme: 'vscode-resource' })

        if(vscode.workspace.workspaceFolders){
            var folder = path.join(
                        vscode.workspace.workspaceFolders[0].uri.fsPath, 
                        "CMakeLists.txt")
        }

        const htmlUri = vscode.Uri.file(
            path.join(this._extensionPath, def.RESOURCE_DIR, 'startpage.html'))

        const htmlBase = vscode.Uri.file(path.join(
                            this._extensionPath, def.RESOURCE_DIR, '/'))
                            .with({ scheme: 'vscode-resource' })

        return fs.readFileSync(htmlUri.fsPath).toString()
                .replace(/\$\{nonce\}/gi, def.getNonce())
                .replace(/\$\{scriptUri\}/gi, scriptUri.toString())
                .replace(/\$\{getstartedList\}/gi, 
                    GetStarted.createOrGet(this._extensionPath).list())                
                .replace(/\$\{templateList\}/gi, 
                    Templates.createOrGet(this._extensionPath).templateList())
                .replace(/\$\{recentList\}/gi, 
                    Recent.createOrGet(this._extensionPath).recentList())
                .replace(/\$\{htmlBase\}/gi, htmlBase.toString())
    }
}

class Templates {
    public static instance: Templates | undefined

    public static createOrGet(extensionPath:string) {
        if(! Templates.instance){
            Templates.instance = new Templates(extensionPath)
        }
        return Templates.instance
    }

    private readonly _extensionPath: string

    private constructor(extensionPath:string){
        this._extensionPath = extensionPath
    }

    public templateList(){
        let templateDir = vscode.Uri.file(path.join(
            this._extensionPath, TEMPLATE_DIR)).fsPath
        var list:string = ""
        fs.readdirSync(templateDir).forEach((template:string) => {
            list += def.clickable(
                template, TEMPLATE, template.replace(/_/gi, " "))
          })

        return list
    }

    public action(templateName:string){
        const options: vscode.OpenDialogOptions = {
            canSelectMany: false,
            canSelectFiles: false,
            canSelectFolders: true,
            defaultUri: vscode.Uri.file("C:\\Workspaces\\EOS\\contracts"),
            openLabel: 'Open'
        }
        vscode.window.showOpenDialog(options).then(fileUri => {
            if (fileUri && fileUri[0]) {
                let templateDir = vscode.Uri.file(path.join(
                    this._extensionPath, 
                    TEMPLATE_DIR, templateName)).fsPath
                console.log('Selected file: ' + fileUri[0].fsPath)
                
                let cl = 'python3 -m eosfactory.create_project '          
                    + `\\"${fileUri[0].fsPath}\\" \\"${templateDir}\\" ` 
                    + `--include \\"${eosideInclude()}\\" `
                    + `--libs \\"${eosideLibs()}\\" `
                    + `--silent `

                def.callEosfactory(cl, (stdout:string, stderr:string) =>{
                    if(!stderr){
                        Recent.createOrGet(
                            this._extensionPath).add(fileUri[0].fsPath)

                        var openFolder = async function(){
                            return await vscode.commands.executeCommand(
                                'vscode.openFolder', fileUri[0])
                        }
                        openFolder()                        
                    }
                })                          
            }
        })
    }
}

class GetStarted {
    public static instance: GetStarted | undefined
    public static createOrGet(extensionPath:string) {
        if(!GetStarted.instance){
            GetStarted.instance = new GetStarted(extensionPath)
        }
        GetStarted.instance.read()
        return GetStarted.instance
    }

    private readonly _file: string
    public json: Map<string, string> = new Map()

    private constructor(extensionPath:string){
        this._file = vscode.Uri.file(path.join(
            extensionPath, GET_STARTED_JSON)).fsPath
    } 

    private read(){
        var json: Object = {}
        try {
            let json = JSON.parse(fs.readFileSync(this._file, 'utf8'))
            this.json = new Map<string, string>(json)
        } catch(err){
            if(err.code !== "ENOENT"){
                vscode.window.showErrorMessage(err)
                console.log(err)                
            }

        }
    }

    public list() {
        var list:string = ""
        for(let entry of this.json.entries()){
            list += def.clickable(entry[1], GET_STARTED, entry[0])
        }
        return list
    }

    public open(url:string) {
        require('openurl').open(url)
    }
}


class Recent {
    public static instance: Recent | undefined
    public static createOrGet(extensionPath:string) {
        if(!Recent.instance){
             Recent.instance = new Recent(extensionPath)
        }
        Recent.instance.read()
        return Recent.instance
    }

    private readonly _file: string
    public list: string[] = []

    private constructor(extensionPath:string){
        this._file = vscode.Uri.file(path.join(
            extensionPath, RECENT_JSON)).fsPath
    }

    private read(){
        var list: string[] = []
        try {
            list = JSON.parse(fs.readFileSync(this._file, 'utf8'))
        } catch(err){

        }
        
        this.list = []
        for(var i = 0; i < list.length; i++){
            if(fs.existsSync(list[i]) 
                    && fs.lstatSync(list[i]).isDirectory() 
                    && this.list.indexOf(list[i]) == -1){
                this.list.push(list[i])
            }
        }
        
        if(list.length != this.list.length){
            def.writeJson(this._file, this.list)
        }
    }

    public recentList() {
        var recentList:string = ""
        this.list.forEach(
            (recent:string) => {
                recentList += def.clickable(recent, RECENT, recent)
          })
        return recentList
    }

    public open(projectPath:string){
        var openFolder = async function(){
            return await vscode.commands.executeCommand(
                'vscode.openFolder', 
                vscode.Uri.file(projectPath))
        }
// vscode.workspace.updateWorkspaceFolders(0, 0, {uri: fileUri[0]})
        openFolder()        
    }

    public add(projectPath:string){
        if(this.list.indexOf(projectPath) == -1){
            this.list.push(projectPath)
            def.writeJson(this._file, this.list)            
        }
    }
}


export function eosideInclude(){
    if(!GetStartedPanel.currentPanel)
        return ""
    return def.javaPath(
            path.join(GetStartedPanel.currentPanel._extensionPath, "include"))
}


export function eosideLibs(){
    if(!GetStartedPanel.currentPanel)
        return

    const walkSync = (dir:string, filelist:string[] = []) => {
        fs.readdirSync(dir).forEach(file => {
        
            filelist = fs.statSync(path.join(dir, file)).isDirectory()
                ? walkSync(path.join(dir, file), filelist)
                : filelist.concat(
                                def.javaPath(path.join(dir, file)));
        
        });
        return filelist;
        }

    return walkSync(path.join(
                    GetStartedPanel.currentPanel._extensionPath, "libs")).join(", ")
}
