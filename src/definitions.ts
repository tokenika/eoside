import * as path from 'path'
import * as child_process from 'child_process'
import * as vscode from 'vscode'
import * as extension from './extension'

export const IS_WINDOWS = (vscode.env.appRoot.indexOf("\\") != -1)
export const RESOURCE_DIR: string = "media"
export const SHELL_PATH = "bash.exe"
export const HEADER_SIZE = "20px"
export const PYTHON = "python3"

const SCRIPTS = "scripts.js"
const STYLES = "styles.css"


export function getExtensionPath(){
    return extension.extensionPath
}

export abstract class Panel{
    public readonly _extensionPath: string
    public readonly _panel: vscode.WebviewPanel
    protected _disposables: vscode.Disposable[] = []

    protected constructor(
        panel: vscode.WebviewPanel
    ){
        this._panel = panel
        this._extensionPath = getExtensionPath()

        // Listen for when the panel is disposed
        // This happens when the user closes the panel or when the panel 
        // is closed programmatically C:\Users\cartman\AppData\Roaming\npm\node_modules\vscode
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

export function getTerminal(name: string, showTerminal=false, reset=false){
    if(reset){
        for(let i = 0; i < (<any>vscode.window).terminals.length; i++){
            let terminal = (<any>vscode.window).terminals[i]
            if( !terminal._disposed && terminal.name === name){terminal.dispose()
            }
        }
    }        
   
    for(let i = 0; i < (<any>vscode.window).terminals.length; i++){
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

    var terminal = IS_WINDOWS 
            ? vscode.window.createTerminal(name, exports.SHELL_PATH)
            : vscode.window.createTerminal(name)
    if(showTerminal){
        terminal.show()
    } else{
        terminal.hide()
    }
    return terminal
}


export function getNonce() {
    var text = ""
    const possible 
            = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length))
    }
    return text
}


export function clickable(id:string, title:string, text:string, clazz:string){
    return `<label id="${id}" 
                title="${title}" class="clickable ${clazz}">
                ${text}
            </label><br>`
}

export function callEosfactory(cl:string){
    var clExe: string   
    if(exports.IS_WINDOWS){
        clExe = `cmd.exe /c bash.exe -c \"${cl}\"`
    } else{
        clExe = cl
    }
    const proc = child_process.spawnSync(clExe, [], {shell: true})
    var stderr = proc.stderr.toString().replace(
        /[\u001b\u009b][[()#?]*(?:[0-9]{1,4}(?:[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, '')
    var stdout = proc.stdout.toString().replace(
        /[\u001b\u009b][[()#?]*(?:[0-9]{1,4}(?:[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, '')    
    if(proc.status){
        vscode.window.showErrorMessage(`
Command line is 
${clExe}.
Error message is 
${stderr ? stderr : stdout}
            `)
    }
    return proc
}


export function javaPath(convPath:string){
    convPath = convPath.replace(/\\/gi, "/")
    return convPath.replace(convPath[0], convPath[0].toUpperCase())
}


export function htmlForWebview(
    extensionPath: string, title: string, htmlContents: string){

const htmlBase = vscode.Uri.file(path.join(
extensionPath, RESOURCE_DIR, '/')).with({scheme: 'vscode-resource'})
const cssPageUri = vscode.Uri.file(path.join(
extensionPath, RESOURCE_DIR, STYLES)).with({scheme: 'vscode-resource'})
const scriptUri = vscode.Uri.file(path.join(
extensionPath, RESOURCE_DIR, SCRIPTS)).with({scheme: 'vscode-resource'})
const nonce = getNonce()

var html = `
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>${title}</title>
        <base href="${htmlBase}">
        <link rel="stylesheet" href="${cssPageUri}">
        <meta charset="utf-8">

        <!--
        Use a content security policy to only allow loading images from https 
        or from our extension directory,
        and only allow scripts that have a specific nonce.
        -->
        <meta http-equiv="Content-Security-Policy" content="
        default-src 'none';
        script-src 'nonce-${nonce}' 'unsafe-inline';
        style-src 'unsafe-inline';
        img-src vscode-resource: https:; 
        ">

        <meta name="theme-color" content="#000000">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>EOSIDE install page</title>
    </head>
        <body class="body">
        <script nonce="${nonce}" src="${scriptUri}"></script>
        ${htmlContents}
        </body>

</html>
`
return html
}


