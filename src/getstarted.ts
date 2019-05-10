import * as path from 'path'
import * as vscode from 'vscode'
import * as fs from 'fs'

import * as def from './definitions'
import * as inst from './install'

const TEMPLATE: string = "template"
const RECENT: string = "recent"
const RECENT_JSON: string = RECENT + ".json"
const GET_STARTED: string = "getstarted"
const GET_STARTED_JSON: string = GET_STARTED + ".json"
const OPEN: string = "open"

export default class GetStartedPanel extends def.Panel {
    public static currentPanel: GetStartedPanel | undefined
    public static readonly viewType = "EOSIDE"

    public static createOrShow(checkFolders: boolean=true) {

        if(inst.isError){
            vscode.window.showErrorMessage("Installation is not completed.")
            return
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

        if (GetStartedPanel.currentPanel) {
            GetStartedPanel.currentPanel._panel.reveal(column)
            return
        }

        const panel = vscode.window.createWebviewPanel(
                GetStartedPanel.viewType, "EOSIDE", 
                column || vscode.ViewColumn.One, {
            // Enable javascript in the webview
            enableScripts: true,

            // And restrict the webview to only loading content from our 
            // extension's `media` directory.
            localResourceRoots: [
                vscode.Uri.file(path.join(
                                    def.getExtensionPath(), def.RESOURCE_DIR))
            ]
            }
        )

        GetStartedPanel.currentPanel = new GetStartedPanel(panel)        
    }

    protected constructor(panel: vscode.WebviewPanel) {
        super(panel)
        this._panel.webview.html = this._getHtmlForWebview()

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
                        if(message.button == 0){
                            vscode.window.showOpenDialog({
                                canSelectMany: false,
                                canSelectFiles: false,
                                canSelectFolders: true,
                                defaultUri: vscode.Uri.file(
                                                    inst.getContractWorkspace()),
                                openLabel: 'Open'
                            }).then(fileUri => {
                                if (fileUri && fileUri[0]) {
                                    vscode.commands.executeCommand(
                                        'vscode.openFolder', fileUri[0])
                                }
                            })
                        } else {
                            vscode.window.showInputBox({
                                placeHolder: "",
                                ignoreFocusOut: true
                            }).then(fileUri => {
                                if (fileUri && fileUri[0]) {
                                    vscode.commands.executeCommand(
                                        'vscode.openFolder', fileUri[0])
                                }
                            })                            
                        }
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
        return def.htmlForWebview(
            this._extensionPath, "Get Started", body(this._extensionPath))     
    }
}


function body(extensionPath:string){
    return `
        <div class="row">
            <div class="leftcolumn">
                <div>
                    <p style="color: unset; font-size: 35px;">Get Started</p>
                    ${GetStarted.createOrGet(extensionPath).list()}
                </div>
                <div>
                    <p style="color: unset; font-size: 35px;">Recent</p>
                    ${Recent.createOrGet(extensionPath).recentList()}
                </div>
            </div>

            <div class="rightcolumn">
                <div>
                    <p style="color: unset; font-size: 35px;">Open</p>
                    <label id="open_folder" title="open" class="clickable" >
                        Open folder...
                    </label><br>
                </div>
                <div>
                    <p style="color: unset; font-size: 35px;">New project</p>
                    ${Templates.createOrGet(extensionPath).templateList()}
                </div>
            </div>
        </div>
    `
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
        var templateDir = inst.config["TEMPLATE_DIR"]
        if(def.IS_WINDOWS){
            templateDir = inst.wslMapLinuxWindows(templateDir)
        }  
        templateDir = vscode.Uri.file(templateDir).fsPath

        var list:string = ""
        fs.readdirSync(templateDir).forEach((template:string) => {
            list += def.clickable(
                template, TEMPLATE, template.replace(/_/gi, " "))
          })

        return list
    }

    public action(templateName:string){
        vscode.window.showOpenDialog({
            canSelectMany: false,
            canSelectFiles: false,
            canSelectFolders: true,
            defaultUri: vscode.Uri.file(inst.getContractWorkspace()),
            openLabel: 'Open'
        }).then(fileUri => {
            if (fileUri && fileUri[0]) {
                let templateDir = inst.config["TEMPLATE_DIR"] + "/" 
                                                                + templateName
                console.log('Selected file: ' + fileUri[0].fsPath)
                
                let cl = `${def.PYTHON} -m eosfactory.create_project `          
                + `'${inst.wslMapWindowsLinux(fileUri[0].fsPath)}' `
                + `'${inst.wslMapWindowsLinux(templateDir)}' `
                cl += '--silent '

                if(!def.callEosfactory(cl).status){ // Is OK
                    Recent.createOrGet(
                                    this._extensionPath).add(fileUri[0].fsPath)
                    vscode.commands.executeCommand(
                                                'vscode.openFolder', fileUri[0])          
                }                     
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
        vscode.commands.executeCommand('vscode.open', vscode.Uri.parse(url))
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
        for(let i = 0; i < list.length; i++){
            if(fs.existsSync(list[i]) 
                    && fs.lstatSync(list[i]).isDirectory() 
                    && this.list.indexOf(list[i]) == -1){
                this.list.push(list[i])
            }
        }
        
        if(list.length != this.list.length){
            inst.writeJson(this._file, this.list)
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
        var openFolder = function(){
            return vscode.commands.executeCommand(
                'vscode.openFolder', 
                vscode.Uri.file(projectPath))
        }
        openFolder()        
    }

    public add(projectPath:string){
        if(this.list.indexOf(projectPath) == -1){
            this.list.push(projectPath)
            inst.writeJson(this._file, this.list)            
        }
    }
}


