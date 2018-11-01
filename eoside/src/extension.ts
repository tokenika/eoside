// https://code.visualstudio.com/docs
// https://code.visualstudio.com/docs/extensionAPI/extension-points
// https://code.visualstudio.com/docs/extensions/publish-extension
// https://code.visualstudio.com/docs/editor/extension-gallery#_install-from-a-vsix

// - Open this folder in VS Code 1.25+
// - `npm install`
// - `npm run watch` or `npm run compile`
// - `F5` to start debugging

import * as path from 'path'
import * as vscode from 'vscode'
import fs = require('fs')

const TERMINAL: string = "eoside"
const SHELL_PATH = "bash.exe"
const TEMPLATE: string = "template"
const TEMPLATE_DIR: string = "templates"
const RESOURCE_DIR: string = "media"
const RECENT: string = "recent"
const RECENT_JSON: string = RECENT + ".json"
const GET_STARTED: string = "getstarted"
const GET_STARTED_JSON: string = GET_STARTED + ".json"
const OPEN: string = "open"
var IS_WINDOWS: boolean = false

export function activate(context: vscode.ExtensionContext) {

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.getStarted', () => {
            GetStartedPanel.createOrShow(context.extensionPath, false)
        }
    ))
    GetStartedPanel.createOrShow(context.extensionPath)
    // if(vscode.env.appRoot.indexOf("\\") != -1){
    //     IS_WINDOWS = true
    //     vscode.workspace.getConfiguration().update(
    //         "terminal.integrated.shell.windows", "bash.exe", true)        
    // }
}

/**
 * Manages webview panel
 */
class GetStartedPanel {
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: GetStartedPanel | undefined
    public static readonly viewType = 'Get Started'
    private readonly _panel: vscode.WebviewPanel
    public readonly _extensionPath: string
    private _disposables: vscode.Disposable[] = []

    public static createOrShow(
        extensionPath: string, checkFolders:boolean=true) {
        if(checkFolders && vscode.workspace.workspaceFolders){
            return
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
                GetStartedPanel.viewType, "Get Started EOS IDE", 
                column || vscode.ViewColumn.One, {
            // Enable javascript in the webview
            enableScripts: true,

            // And restrict the webview to only loading content from our 
            // extension's `media` directory.
            localResourceRoots: [
                vscode.Uri.file(path.join(extensionPath, RESOURCE_DIR))
            ]
            }
        )

        GetStartedPanel.currentPanel = new GetStartedPanel(
                                                        panel, extensionPath)        
    }

    private constructor(
        panel: vscode.WebviewPanel,
        extensionPath: string
    ) {
        this._panel = panel
        this._extensionPath = extensionPath

        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview()

        // Listen for when the panel is disposed
        // This happens when the user closes the panel or when the panel 
        // is closed programmatically
        this._panel.onDidDispose(
                            () => this.dispose(), null, this._disposables)
        // Update the content based on view changes
        this._panel.onDidChangeViewState(
            e => {}, null, this._disposables)

        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(message => {
            switch (message.title) {
                case TEMPLATE:
                    Templates.createOrGet(this._extensionPath)
                        .template(message.id)
                    return
                case RECENT:
                    Recent.createOrGet(this._extensionPath).open(message.id)
                    return
                case GET_STARTED:
                    GetStarted.createOrGet(this._extensionPath)
                        .open(message.id)
                case OPEN:
                    if(message.id === "open_folder"){
                        vscode.commands.executeCommand('vscode.openFolder')
                    }
            }
        }, null, this._disposables)
    }

    public dispose() {
        GetStartedPanel.currentPanel = undefined

        // Clean up our resources
        this._panel.dispose()

        while (this._disposables.length) {
            const x = this._disposables.pop()
            if (x) {
                x.dispose()
            }
        }
    }

    private _getHtmlForWebview() {
        const scriptPathOnDisk = vscode.Uri.file(path.join(
            this._extensionPath, RESOURCE_DIR, 'main.js'))

        // And the uri we use to load this script in the webview
        const scriptUri = scriptPathOnDisk.with({ scheme: 'vscode-resource' })

        if(vscode.workspace.workspaceFolders){
            var folder = path.join(
                        vscode.workspace.workspaceFolders[0].uri.fsPath, 
                        "CMakeLists.txt")
        }

        const htmlUri = vscode.Uri.file(
            path.join(this._extensionPath, RESOURCE_DIR, 'startpage.html'))

        const htmlBase = vscode.Uri.file(path.join(
                            this._extensionPath, RESOURCE_DIR, '/'))
                            .with({ scheme: 'vscode-resource' })

        var html = require('fs').readFileSync(htmlUri.fsPath).toString()
                                .replace(/\$\{nonce\}/gi, getNonce())
                                .replace(/\$\{scriptUri\}/gi, scriptUri)
                .replace(/\$\{getstartedList\}/gi, 
                    GetStarted.createOrGet(this._extensionPath).list())                
                .replace(/\$\{templateList\}/gi, 
                    Templates.createOrGet(this._extensionPath).templateList())
                .replace(/\$\{recentList\}/gi, 
                    Recent.createOrGet(this._extensionPath).recentList())
                                        .replace(/\$\{htmlBase\}/gi, htmlBase)
        return html
    }
}


function getTerminal(showTerminal: boolean = false){
    for(var i = 0; i < (<any>vscode.window).terminals.length; i++){
        let terminal = (<any>vscode.window).terminals[i]
        if( terminal.name === TERMINAL){
            if(showTerminal){
                terminal.show()
            } else{
                terminal.hide()
            }
            return terminal
        }
    }

    var terminal = vscode.window.createTerminal(
        TERMINAL, SHELL_PATH)
    if(showTerminal){
        terminal.show()
    } else{
        terminal.hide()
    }
    return terminal
}


function getNonce() {
    let text = ""
    const possible 
            = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length))
    }
    return text
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
            list += clickable(
                template, TEMPLATE, template.replace(/_/gi, " "))
          })

        return list
    }

    public template(templateName:string){
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
                let cl = 'python3 -m eosfactory.utils.create_project '                  
                    + `\\"${fileUri[0].fsPath}\\" \\"${templateDir}\\" --silent`

                let clExe: string   
                if(IS_WINDOWS){
                    clExe = `cmd.exe /c bash.exe -c \"${cl}\"`
                } else{
                    clExe = `\"${cl}\"`
                }

                const child_process = require("child_process");
                ((cmd) => {
                    child_process.exec(
                        cmd, 
                        (err:string, stdout:string, stderr:string) => {
                        if(!stderr){
                            Recent.createOrGet(
                                this._extensionPath).add(fileUri[0].fsPath)
    
                            var openFolder = async function(){
                                return await vscode.commands.executeCommand(
                                    'vscode.openFolder', fileUri[0])
                            }
        // vscode.workspace.updateWorkspaceFolders(0, 0, {uri: fileUri[0]})
                            openFolder()
                        } else {
                            vscode.window.showErrorMessage(stderr.replace(
                    /[\u001b\u009b][[()#?]*(?:[0-9]{1,4}(?:[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, 
                    ''))
                        }
                        console.log('stderr is:' + stderr)
                    }).on(
                        'exit', 
                        (code:number) => {}
                        )
                })(clExe)                            
            }
        })
    }
}


function clickable(id:string, title:string, text:string){
    return `<label id="${id}" 
                title=${title} class="clickable">
                ${text}
            </label><br>`
}


function writeJson(file:string, json:Object){
    try{
        fs.writeFileSync(
            file, JSON.stringify(json, undefined, 4))
    } catch(err){
        vscode.window.showErrorMessage(err)
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
            list += clickable(entry[1], GET_STARTED, entry[0])
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
            if(fs.existsSync(list[i]) && fs.lstatSync(list[i]).isDirectory()){
                this.list.push(list[i])
            }
        }
        
        if(list.length != this.list.length){
            writeJson(this._file, this.list)
        }
    }

    public recentList() {
        var recentList:string = ""
        this.list.forEach(
            (recent:string) => {
                recentList += clickable(recent, RECENT, recent)
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
        this.list.push(projectPath)
        writeJson(this._file, this.list)
    }
}


vscode.workspace.onDidOpenTextDocument(() => {
    vscode.window.showInformationMessage("onDidOpenTextDocument")
})