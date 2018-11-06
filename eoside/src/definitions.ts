const TERMINAL: string = "eoside"
const SHELL_PATH = "bash.exe"

import * as vscode from 'vscode'
export var IS_WINDOWS = (vscode.env.appRoot.indexOf("\\") != -1)
export const RESOURCE_DIR: string = "media"
import fs = require('fs')

export function writeJson(file:string, json:Object){
    try{
        fs.writeFileSync(
            file, JSON.stringify(json, undefined, 4))
    } catch(err){
        vscode.window.showErrorMessage(err)
    } 
}

export function getTerminal(showTerminal: boolean = false){
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
        if(!stderr){
            result(stdout)
        } else {
            vscode.window.showErrorMessage(stderr.replace(
    /[\u001b\u009b][[()#?]*(?:[0-9]{1,4}(?:[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, 
    ''))
            console.log('stderr is:' + stderr)
        }
    }).on(
        'exit', 
        (code:number) => {}
        )
}

export var config: any = undefined

callEosfactory(
    'python3 -m eosfactory.core.config ', 
    (stdout:string) => {
        config = JSON.parse(stdout)        
    })

export function root(){
    if(config){
        return config["WSL_ROOT"]
    }
    return ""
}