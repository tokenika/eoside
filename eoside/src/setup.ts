import * as path from 'path'
import * as vscode from 'vscode'
import fs = require('fs')

import * as def from './definitions'

const INCLUDE: string = "includePath"
const LIBS: string = "libs"
const OPTIONS: string = "compilerOptions"
const UP: string = "up"
const ADD: string = "include"
const DOWN: string = "down"
const DELETE:string = "del"
const INSERT:string = "insert"
const CONTROL:string = "ctr"

export default class SetupPanel extends def.Panel{
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: SetupPanel | undefined
    public static readonly viewType = "Setup"

    public static createOrShow(extensionPath: string) {
        if(!vscode.workspace.workspaceFolders){
            return
        }

        let c_cpp_properties = path.join(
                            vscode.workspace.workspaceFolders[0].uri.fsPath, 
                            ".vscode", "c_cpp_properties.json")
        if(!fs.existsSync(c_cpp_properties)){
            return
        }

        const column = vscode.window.activeTextEditor 
            ? vscode.window.activeTextEditor.viewColumn : undefined

        // If we already have a panel, show it.
        if (SetupPanel.currentPanel) {
            SetupPanel.currentPanel._panel.reveal(column)
            return
        }

        // Otherwise, create a new panel.
        const panel = vscode.window.createWebviewPanel(
                SetupPanel.viewType, "Setup", 
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

        SetupPanel.currentPanel = new SetupPanel(panel, extensionPath)        
    }

    private constructor(
        panel: vscode.WebviewPanel,
        extensionPath: string
    ) {
        super(panel, extensionPath)

        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview()

        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(message => {
            switch (message.title) {
                case INCLUDE:
                    Includes.createOrGet(this._extensionPath).action(message)
                    break
                case LIBS:
                    Libs.createOrGet(this._extensionPath).action(message)
                    break
                case OPTIONS:
                    Options.createOrGet(this._extensionPath).action(message)
                    break
                case CONTROL:
                    if(SetupPanel.currentPanel){
                        action(message, SetupPanel.currentPanel)
                    }
                    break
            }
        }, null, this._disposables)
    }

    public dispose() {
        SetupPanel.currentPanel = undefined
        super.dispose()
    }

    public update(){
        this._panel.webview.html = this._getHtmlForWebview();
    }

    private _getHtmlForWebview() {
        const scriptPathOnDisk = vscode.Uri.file(path.join(
            this._extensionPath, def.RESOURCE_DIR, 'setup.js'))

        // And the uri we use to load this script in the webview
        const scriptUri = scriptPathOnDisk.with({ scheme: 'vscode-resource' })

        const htmlUri = vscode.Uri.file(
            path.join(this._extensionPath, def.RESOURCE_DIR, 'setup.html'))

        const htmlBase = vscode.Uri.file(path.join(
            this._extensionPath, def.RESOURCE_DIR, '/'))
                            .with({ scheme: 'vscode-resource' })
        
        
        let html = require('fs')
            .readFileSync(htmlUri.fsPath).toString()
            .replace(/\$\{nonce\}/gi, def.getNonce())
            .replace(/\$\{scriptUri\}/gi, scriptUri)
            .replace(
                /\$\{includeList\}/gi, 
                Includes.createOrGet(this._extensionPath).items())
            .replace(
                /\$\{libList\}/gi, 
                Libs.createOrGet(this._extensionPath).items())
            .replace(
                /\$\{optionList\}/gi, 
                Options.createOrGet(this._extensionPath).items())
            .replace(/\$\{wslRoot\}/gi, `WSL root is ${def.root()}`)

        if(def.IS_WINDOWS){
            html = html.replace(/\$\{bash\}/gi, 
            `
            <button 
            class="ctr"; 
            id="bash"; 
            title="ctr">bash</button>`)
        }
        
        return html
    }
}


export function compile(){
    let terminalName = "compile"
    if(vscode.workspace.workspaceFolders){
        let terminal = def.getTerminal(terminalName, true, true)
        let cl = `python3 -m eoside.utils.build '${
    vscode.workspace.workspaceFolders[0].uri.fsPath}' --compile`
        terminal.sendText(cl)
    }    
}


export function build(){
    let terminalName = "build"
    if(vscode.workspace.workspaceFolders){
        let terminal = def.getTerminal(terminalName, true, true)
        let cl = `python3 -m eoside.utils.build '${
            vscode.workspace.workspaceFolders[0].uri.fsPath}'`
        terminal.sendText(cl)
    }      
}


export function bash(){
    if(SetupPanel.currentPanel){
        SetupPanel.currentPanel._panel.reveal(vscode.ViewColumn.Two)
    }
    let terminal = vscode.window.createTerminal("bash", def.SHELL_PATH)
    terminal.show()
}

function action(message: any, panel: def.Panel){
    switch(message.id) {
        case "compile": {
                compile()
            }
            break
        case "build": {
                build()
            }
            break
        case "EOSIde":
            vscode.commands.executeCommand("eoside.EOSIde")
            break
        case "bash":            
            bash()
            break
    }
}

abstract class Dependencies {

    protected readonly _extensionPath: string
    protected readonly _c_cpp_properties: string | undefined
    protected json: any = undefined

    protected constructor(extensionPath:string){
        this._extensionPath = extensionPath
        if(vscode.workspace.workspaceFolders){
            this._c_cpp_properties = path.join(
                vscode.workspace.workspaceFolders[0].uri.fsPath, 
                ".vscode", "c_cpp_properties.json")
        }
    }

    protected read(){
        if(this._c_cpp_properties && fs.existsSync(this._c_cpp_properties)){
            try {
                this.json = JSON.parse(
                            fs.readFileSync(this._c_cpp_properties, 'utf8'))
            } catch(err){
                if(err.code !== "ENOENT"){
                    vscode.window.showErrorMessage(err)
                    console.log(err)                
                }
            }
        }
    }

    protected abstract getEntries(): string[]
    protected abstract setEntries(entries: string[]): void

    protected insert(index: number, selectFiles: boolean=true){
        let path = undefined
        const options: vscode.OpenDialogOptions = {
            canSelectMany: false,
            canSelectFiles: selectFiles,
            canSelectFolders: !selectFiles,
            defaultUri: vscode.Uri.file(def.root()),
            openLabel: 'Open'
        }
        vscode.window.showOpenDialog(options).then(fileUri => {
            if (!fileUri || !fileUri[0]) {
                return
            }
                console.log('Selected file: ' + fileUri[0].fsPath)
                path = fileUri[0].fsPath
                path = path.replace(/\\/gi, "/")
                path = path.replace(path[0], path[0].toUpperCase())
                let list: string[] = []
                let entries = this.getEntries()
                index = index == -1 ? entries.length : index + 1
                for(let i = 0, j = 0; i < entries.length + 1; i++){
                    if(i === index){
                        list[index] = path
                        continue
                    }
                    list[i] = entries[j++]
                }
                this.setEntries(list)
                this.update()                 
        })
    }

    protected update(){
        if(this._c_cpp_properties) {
            def.writeJson(this._c_cpp_properties, this.json)
            if(SetupPanel.currentPanel){
                SetupPanel.currentPanel.update()
            }            
        } 
    }

    public action(message: any){        
        if(message.id === ADD){
            this.insert(-1)
        }

        if(message.id.includes(DOWN)){
            let index = Number(message.id.replace(DOWN, ""))
            let entries = this.getEntries()
            if(index === entries.length - 1){
                return
            }            
            let newIndex = index + 1
            let temp = entries[newIndex]
            entries[newIndex] = entries[index]
            entries[index] = temp;
            this.setEntries(entries)
            this.update()
        }

        if(message.id.includes(UP)){
            let index = Number(message.id.replace(UP, ""))
            let entries = this.getEntries()
            if(index === 0){
                return
            }                 
            let newIndex = index - 1
            let temp = entries[newIndex]
            entries[newIndex] = entries[index]
            entries[index] = temp;
            this.setEntries(entries)
            this.update()
        }
        
        if(message.id.includes(DELETE)){
            let index = Number(message.id.replace(DELETE, ""))
            let entries = this.getEntries()
            let list: string[] = []
            for(let i = 0, j = 0; i < entries.length; i++){
                if(i !== index){
                    list[j++] = entries[i]
                }
            }              
            this.setEntries(list)
            this.update()
        }  
        
        if(message.id.includes(INSERT)){
            this.insert(Number(message.id.replace(INSERT, "")))
        }     
    }

    public items(title=""){
        let entries: string[] = ["${workspaceFolder}"]
        this.read()
        if(this.getEntries()){
            entries = this.getEntries()
        }
        let root = def.root()
        for(let i = 0; i < entries.length; i++){
            entries[i] = entries[i].replace(root, "${root)");
        }

        let items = ""
        for(let i = 0; i < entries.length; i++){
            items += setupEntry(i, title, entries[i])
        }
        return items;
    }    
}

class Includes extends Dependencies{
    public static instance: Includes | undefined

    public static createOrGet(extensionPath:string) {
        if(! Includes.instance){
            Includes.instance = new Includes(extensionPath)
        }
        return Includes.instance
    }

    protected getEntries() {
        return this.json["configurations"][0][INCLUDE].slice()
    }

    protected setEntries(entries: string[]){
        this.json["configurations"][0][INCLUDE] = entries
        this.json["configurations"][0]["browse"]["path"] = entries
    }

    public insert(index: number){
        super.insert(index, false)
    }

    public items(){
        return super.items(INCLUDE)
    }
}

class Options extends Dependencies{
    public static instance: Options | undefined

    public static createOrGet(extensionPath:string) {
        if(! Options.instance){
            Options.instance = new Options(extensionPath)
        }
        return Options.instance
    }

    protected getEntries() {
        return this.json["configurations"][0][OPTIONS].slice()
    }

    protected setEntries(entries: string[]){
        this.json["configurations"][0][OPTIONS] = entries
    }

    public insert(index: number){
        vscode.window.showInputBox().then((option) => {
            if(option){
                let list: string[] = []
                let entries = this.getEntries()
                index = index == -1 ? entries.length : index + 1
                for(let i = 0, j = 0; i < entries.length + 1; i++){
                    if(i === index){
                        list[index] = option
                        continue
                    }
                    list[i] = entries[j++]
                }
                this.setEntries(list)
                this.update()   
            }
        })       
    }

    public items(){
        return super.items(OPTIONS)
    }
}


class Libs extends Dependencies{
    public static instance: Libs | undefined

    public static createOrGet(extensionPath:string) {
        if(! Libs.instance){
            Libs.instance = new Libs(extensionPath)
        }
        return Libs.instance
    }

    protected getEntries() {
        return this.json["configurations"][0][LIBS].slice()
    }    
    
    protected setEntries(entries: string[]){
        this.json["configurations"][0][LIBS] = entries
    }

    public insert(index: number){
        super.insert(index, true)
    }

    public items(){
        return super.items(LIBS)
    }
}



function setupEntry(index:number, title:string, text:string){
    return `
        <button 
            class="btn"; 
            id="${DOWN}${index}"; 
            title="${title}">&#9660</button>
        <button class="btn"
            class="btn"; 
            id="${UP}${index}"; 
            title="${title}">&#9650</button>
        <button class="btn"
            class="btn"; 
            id="${DELETE}${index}"; 
            title="${title}";>X</button>
        <button class="btn"
            class="btn"; 
            id="${INSERT}${index}"; 
            title="${title}">&#8627</button>
        <label>${text}</label>
        <br>
    `
}