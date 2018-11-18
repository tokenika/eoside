
import * as vscode from 'vscode'
import fs = require('fs')

export const IS_WINDOWS = (vscode.env.appRoot.indexOf("\\") != -1)
export const RESOURCE_DIR: string = "media"
export const SHELL_PATH = "bash.exe"
export const PYTHON: string = "python3"

const NO_PYTHON = `cannot find ${PYTHON}`
const NO_EOSFACTORY = `eosfactory package is not installed!`
const NO_CONFIG = `eosfactory is corrupted!`
const NO_EOSIDE = `eoside package is not installed!`
const NO_WSL_ROOT = `WSL root is not set`

export var config: any = undefined
export var ERROR_MSG = ""

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
    try{
        fs.writeFileSync(
            file, JSON.stringify(json, undefined, 4))
    } catch(err){
        vscode.window.showErrorMessage(err)
    } 
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


export function getWslRoot(){
    const spawn = require("child_process").spawnSync;
    {
        let lxss="hkcu\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss"
        let cl = `REG QUERY ${lxss} -s -v BasePath`
        const process = spawn(cl, [], {shell: true})
        var basePath = process.stdout.toString().match(new RegExp("REG_SZ(.*)"))[1].trim()
    }
    {
        let cl = `bash.exe -c whoami`
        const process = spawn(cl, [], {shell: true})
        var user = process.stdout.toString()
    }

    console.log(`${basePath}\\home\\${user}`)
}

export function errorConditions(){
    const spawn = require("child_process").spawnSync;  
    {
        const process = IS_WINDOWS 
            ? spawn("bash.exe", ["-c", `${PYTHON} -V`])
            : spawn(`${PYTHON}`, ["-V"])
        if(process.status){
            ERROR_MSG = NO_PYTHON
            return
        }
    }
    {
        let cl = `${PYTHON} -c 'import eosfactory'`
        let clExe = IS_WINDOWS
            ? `bash.exe -c "${cl}"`
            : `"${cl}"`
        const process = spawn(clExe, [], {shell: true})
        if(process.status){
            ERROR_MSG = NO_EOSFACTORY
            return
        }
    }
    {
        let cl = `${PYTHON} -c 'import eoside'`
        let clExe = IS_WINDOWS
            ? `bash.exe -c "${cl}"`
            : `"${cl}"`
        const process = spawn(clExe, [], {shell: true})
        if(process.status){
            ERROR_MSG = NO_EOSIDE
            return
        }        
    }
    {
        let cl = `${PYTHON} -m eosfactory.core.config`
        let clExe = IS_WINDOWS
            ? `bash.exe -c "${cl}"`
            : `"${cl}"`
        const process = spawn(clExe, [], {shell: true})
        if(process.status){
            ERROR_MSG = NO_CONFIG
            return
        }
        config = JSON.parse(process.stdout)
        if(IS_WINDOWS){
            if(!config["WSL_ROOT"]){
                ERROR_MSG = NO_WSL_ROOT
                return
            }
        }         
    }    
}


export function root(){
    if(config){
        return config["WSL_ROOT"]
    }
    return ""
}

getWslRoot()
errorConditions()