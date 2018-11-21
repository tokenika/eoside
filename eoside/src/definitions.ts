
import * as vscode from 'vscode'
import fs = require('fs')

export const IS_WINDOWS = (vscode.env.appRoot.indexOf("\\") != -1)
export const RESOURCE_DIR: string = "media"
export const SHELL_PATH = "bash.exe"

export abstract class Panel{
    public readonly _extensionPath: string
    public readonly _panel: vscode.WebviewPanel
    protected _disposables: vscode.Disposable[] = []

    protected constructor(
        panel: vscode.WebviewPanel,
        extensionPath: string
    ){
        this._panel = panel
        this._extensionPath = extensionPath
        // Listen for when the panel is disposed
        // This happens when the user closes the panel or when the panel 
        // is closed programmatically
        this._panel.onDidDispose(
            () => this.dispose(), null, this._disposables)
        // Update the content based on view changes
        this._panel.onDidChangeViewState(
        e => {}, null, this._disposables)
    }

    public dispose() {
        // Clean up our resources
        this._panel.dispose()

        while (this._disposables.length) {
            const x = this._disposables.pop()
            if (x) {
                x.dispose()
            }
        }
    }
}


export function writeJson(file:string, json:Object){
    file = wslMapLinuxWindows(file)
    try{
        fs.writeFileSync(file, JSON.stringify(json, undefined, 4))
    } catch(err){
        vscode.window.showErrorMessage(
`Cannot write to the config file of EOSFactory. The path tried is
${file}.
Error message is
${err}`)
        return -1
    }
    return 0
}


export function getTerminal(
        name: string, showTerminal=false, reset=false){
    if(reset){
        for(var i = 0; i < (<any>vscode.window).terminals.length; i++){
            let terminal = (<any>vscode.window).terminals[i]
            if( !terminal._disposed && terminal.name === name){terminal.dispose()
            }
        }         
    }        
   
    for(var i = 0; i < (<any>vscode.window).terminals.length; i++){
        let terminal = (<any>vscode.window).terminals[i]
        if( !terminal._disposed && terminal.name === name){
            if(showTerminal){
                terminal.show()
            } else{
                terminal.hide()
            }
            return terminal
        }
    }

    var terminal = vscode.window.createTerminal(name, SHELL_PATH)
    if(showTerminal){
        terminal.show()
    } else{
        terminal.hide()
    }
    return terminal
}


export function getNonce() {
    let text = ""
    const possible 
            = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length))
    }
    return text
}


export function clickable(id:string, title:string, text:string){
    return `<label id="${id}" 
                title=${title} class="clickable">
                ${text}
            </label><br>`
}


export function callEosfactory(cl:string, result:Function){
    const child_process = require("child_process");

    let clExe: string   
    if(IS_WINDOWS){
        clExe = `cmd.exe /c bash.exe -c \"${cl}\"`
    } else{
        clExe = `\"${cl}\"`
    }

    child_process.exec(
        clExe, 
        (err:string, stdout:string, stderr:string) => {
        if(stderr){
            vscode.window.showErrorMessage(stderr.replace(
    /[\u001b\u009b][[()#?]*(?:[0-9]{1,4}(?:[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, 
    ''))
            console.log('stderr is:' + stderr)            
        }
        result(stdout)
    }).on(
        'exit', 
        (errorCode:number) => {}
        )
}

export function wslMapLinuxWindows(path:string){
    if(!IS_WINDOWS){
        return path
    }
    if(!path.includes("/mnt/")){
        return path
    }
    path = `${path[5].toUpperCase()}:${path.substr(6)}`
    return path.replace(/\//gi, "\\")
}

export function wslMapWindowsLinux(path:string){
    if(!IS_WINDOWS){
        return path
    }    
    if(!path.includes(":\\")){
        return path
    }
    path = path.replace(/\\/gi, "/")
    let drive = path[0]
    return path.replace(`${drive}:/`, `/mnt/${drive.toLowerCase()}/`)
}




