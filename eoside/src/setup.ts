import * as path from 'path'
import * as vscode from 'vscode'
import fs = require('fs')

import * as def from './definitions'

const INCLUDE: string = "include"
const LINK: string = "link"
const UP: string = "up"
const DOWN: string = "down"
const DELETE:string = "del"
const INSERT:string = "insert"

export default class SetupPanel {
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: SetupPanel | undefined
    public static readonly viewType = "Setup"

    public readonly _extensionPath: string    
    private readonly _panel: vscode.WebviewPanel
    private _disposables: vscode.Disposable[] = []

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
                case INCLUDE:
                    Includes.createOrGet(this._extensionPath).action(message)
                    return
                case LINK:
                    Libs.createOrGet(this._extensionPath).action(message)
                    return                
            }
        }, null, this._disposables)
    }

    public dispose() {
        SetupPanel.currentPanel = undefined

        // Clean up our resources
        this._panel.dispose()

        while (this._disposables.length) {
            const x = this._disposables.pop()
            if (x) {
                x.dispose()
            }
        }
    }

    public update(){
        this._panel.webview.html = this._getHtmlForWebview();
    }

    private _getHtmlForWebview() {
        const scriptPathOnDisk = vscode.Uri.file(path.join(
            this._extensionPath, def.RESOURCE_DIR, 'setup.js'))

        // And the uri we use to load this script in the webview
        const scriptUri = scriptPathOnDisk.with({ scheme: 'vscode-resource' })

        if(vscode.workspace.workspaceFolders){
            let folder = path.join(
                        vscode.workspace.workspaceFolders[0].uri.fsPath, 
                        "CMakeLists.txt")
        }

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
                Includes.createOrGet(this._extensionPath).itemList())
            .replace(
                /\$\{libList\}/gi, 
                Libs.createOrGet(this._extensionPath).itemList())
            .replace(
        /\$\{wslRoot\}/gi, 
        `WSL root is ${def.root()}`)
        
        return html
    }
}

abstract class Dependencies {

    protected readonly _extensionPath: string
    protected readonly _c_cpp_properties: string | undefined
    protected json: any = undefined
    protected entries: string[] = []

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
                let entries = this.entries
                let list: string[] = []
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
        if(message.id === INCLUDE){
            this.insert(-1, )
        }

        if(message.id.includes(DOWN)){
            let index = Number(message.id.replace(DOWN, ""))
            let entries = this.entries
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
            let entries = this.entries
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
            let entries = this.entries
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
}

class Includes extends Dependencies{
    public static instance: Includes | undefined

    public static createOrGet(extensionPath:string) {
        if(! Includes.instance){
            Includes.instance = new Includes(extensionPath)
        }
        return Includes.instance
    }

    protected setEntries(entries: string[]){
        this.json["configurations"][0]["includePath"] = entries
    }

    protected read(){
        super.read()
        this.entries = this.json["configurations"][0]["includePath"].slice()
    }

    public insert(index: number){
        super.insert(index, false)
    }

    public itemList(){
        let entries: string[] = ["${workspaceFolder}"]
        this.read()
        if(this.entries && this.entries){
            entries = this.entries
        }
        let root = def.root()
        for(let i = 0; i < entries.length; i++){
            entries[i] = entries[i].replace(root, "${root)");
        }

        let itemList = ""
        for(let i = 0; i < entries.length; i++){
            itemList += setupEntry(i, "include", entries[i])
        }
        return itemList;
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
    
    protected setEntries(entries: string[]){
        this.json["configurations"][0]["libs"] = entries
    }

    protected read(){
        super.read()
        this.entries = this.json["configurations"][0]["libs"].slice()
    }

    public insert(index: number){
        super.insert(index, true)
    }

    public itemList(){
        let entries: string[] = []
        this.read()
        if(this.entries && this.entries){
            entries = this.entries
        }
        let root = def.root()
        for(let i = 0; i < entries.length; i++){
            entries[i] = entries[i].replace(root, "${root)");
        }

        let itemList = ""
        for(let i = 0; i < entries.length; i++){
            itemList += setupEntry(i, "link", entries[i])
        }
        return itemList;
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
            title="${title}">del</button>
        <button class="btn"
            class="btn"; 
            id="${INSERT}${index}"; 
            title="${title}">&#8627</button>
        <label>${text}</label>
        <br>
    `
}