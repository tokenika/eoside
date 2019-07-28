import * as path from 'path'
import * as child_process from 'child_process'
import * as vscode from 'vscode'
import * as fs from 'fs'
import * as net from 'net'

import * as def from './definitions'

export var config: any = undefined
export const PIP: string = "pip3"

const WSL_VERSION_MIN = "4.3"
const EOSFACTORY_VERSION_MIN = "3.4.0"
const ERROR_COLOR = "indianred"
const WARNING_COLOR = "yellow"

const FIND_WSL = "findWsl"
const CHANGE_WORKSPACE = "changeWorkspace"
const BASH_COMMAND = "bashCommand"
const CONFIGURATION = "configuration"
const START_WITH_EOSIDE = "startWithEosIde"
const MENU = "menu"
const TITLE = '<p style="color: unset; font-size: 35px;">Installing EOSIDE</p>'
const NO_ERROR = 0
const IS_ERROR = 2
const IS_WARNING = 1

export var isError = NO_ERROR
var htmlContents: any = undefined
var firstErrMsg: any = undefined


export function verify(){
    exports.isError = NO_ERROR

    var error_codes = ""
    if(vscode.workspace.getConfiguration().eoside.specialEffects.length){
        error_codes = vscode.workspace.getConfiguration().eoside
                                                            .specialEffects[0]
    }

    // error_codes = "eosio,eosio_cdt,psutil,termcolor,wslroot,ubuntuversion,"
    // error_codes += "wslinstalled,python,pip,workspace,"
    // error_codes = "workspace,"

    htmlContents = TITLE
    firstErrMsg = ''

    if(def.IS_WINDOWS){

////////////////////////////////////////////////////////////////////////////////
// WSL bash.exe
////////////////////////////////////////////////////////////////////////////////
        let version = ""
        const proc = child_process.spawnSync("bash.exe", ["--version"])
        let match = proc.stdout.toString().match(/version\s{1}(.*)\./)
        if(match){
            version = match[1]
        }
        if(proc.status || !version || error_codes.includes("wslinstalled")){
            errorMsg(
`It seems that Windows Subsystem Linux is not in this System, <br>
or the <em>bash.exe</em> executable is not in the System path.<br> 
EOSIDE cannot do without WSL.`)
            exports.isError = IS_ERROR
        } else {
            if(version < WSL_VERSION_MIN){                
                errorMsg(
`The version of the WSL installation is <em>${version}</em>, while the 
minimum is <em>${WSL_VERSION_MIN}</em>.<br>
EOSIDE cannot do without proper WSL.`)
            exports.isError = IS_ERROR
            }            
        }
    }


////////////////////////////////////////////////////////////////////////////////
// Python
////////////////////////////////////////////////////////////////////////////////
    {
        const proc = def.IS_WINDOWS 
            ? child_process.spawnSync("bash.exe", ["-c", `${def.PYTHON} -V`])
            : child_process.spawnSync(`${def.PYTHON}`, ["-V"])
            
        if(proc.status || error_codes.includes("python")){
            let msg = 
`It seams that <em>${def.PYTHON}</em> is not in the System, as the 
<em>${def.PYTHON}</em> executable is not in the System path.<br>
EOSIDE cannot do without <em>${def.PYTHON}</em>.`

            if(def.IS_WINDOWS){
                msg +=
`
<br>
Note that the Python has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg)
            exports.isError = IS_ERROR
        }
    }


////////////////////////////////////////////////////////////////////////////////
// pip
////////////////////////////////////////////////////////////////////////////////
    {
        const proc = def.IS_WINDOWS 
            ? child_process.spawnSync("bash.exe", ["-c", `${exports.PIP} -V`])
            : child_process.spawnSync(`${exports.PIP}`, ["-V"])
        if(proc.status || error_codes.includes("pip")){
            let msg = 
`It seams that <em>${exports.PIP}</em> is not in the System, as the 
<em>${exports.PIP}</em> executable is not in the System path.<br>
EOSIDE cannot do without <em>${exports.PIP}</em>.`

            if(def.IS_WINDOWS){
                msg +=
`
<br>
Note that the Python Pip has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg)
            exports.isError = IS_ERROR
        }
    }


////////////////////////////////////////////////////////////////////////////////
// eosfactory
////////////////////////////////////////////////////////////////////////////////
    {
        let cl = `${def.PYTHON} -c 'import eosfactory'`
        let clExe = def.IS_WINDOWS
            ? `bash.exe -c "${cl}"`
            : `${cl}`
        const proc = child_process.spawnSync(clExe, [], {shell: true})

        if(proc.status || error_codes.includes("eosfactory")){

            let button = `
<button 
    style="text-align:left;"
    class="btn ${BASH_COMMAND}";
    class="btn"; 
    id="Install eosfactory"; 
    title="Install eosfactory. Click the button then ENTER in a newly created bash terminal window, to go."
>
    pip3 install --user eosfactory-tokenika
</button>`

            let msg =
`
It seems that <em>eosfactory</em> package is not installed in 
the System, or it is corrupted.<br>
EOSIDE cannot do without <em>eosfactory</em>.
Install it: ${button}
`
            if(def.IS_WINDOWS){
                msg += 
`<br>
Note that the package has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg )
            exports.isError = IS_ERROR
        } else {
            const proc = def.IS_WINDOWS
            ? child_process.spawnSync(
                    `bash.exe -c "${def.PYTHON}` 
                        + ' -m eosfactory.config --json --dont_set_workspace"', 
                    [], {shell: true})
            : child_process.spawnSync(`${def.PYTHON}`, 
                ['-m', 'eosfactory.config', '--json', 
                                                '--dont_set_workspace'])
            if(proc.status){
                errorMsg(
`It seems that the eosfactory package is not installed or corrupted, as its 
configuration file cannot be read.`)
                exports.isError = IS_ERROR
            } else {
                exports.config = JSON.parse(proc.stdout.toString());
                
                if(!isCurrentEOSFactoryBiggerThanMinimal()){
                    exports.isError = IS_ERROR
                    let button = `
                    <button 
                        style="text-align:left;"
                        class="btn ${BASH_COMMAND}";
                        class="btn"; 
                        id="Install eosfactory"; 
                        title="Install eosfactory. Click the button then ENTER in a newly created bash terminal window, to go."
                    >
                        pip3 install --user eosfactory-tokenika
                    </button>`
                    var msg = warning(
`The version of the detected EOSFactory package is ${exports.config["VERSION"]} while EOSIDE is tested with ${EOSFACTORY_VERSION_MIN}.
Install it the newest: ${button}
`)
                    statusMsg(msg)
                }
                
                statusMsg(
`EOSFactory v${exports.config["VERSION"]}`
                )
                statusMsg(
`EOSFactory configuration file is ${wslMapLinuxWindows(exports.config["CONFIG_FILE"])}`)
                var msg = ""

////////////////////////////////////////////////////////////////////////////////
// If EOSFactory is installed, EOSFactory checklist
////////////////////////////////////////////////////////////////////////////////
                {
                    const proc = def.IS_WINDOWS
                    ? child_process.spawnSync(
                        `bash.exe -c "${def.PYTHON}  -m eosfactory.config --html --error ${"dummy," + error_codes}"`, 
                                [], {shell: true})
                    : child_process.spawnSync(
                        `${def.PYTHON}`, ['-m', 'eosfactory.core.checklist', "--html"])
                    if(proc.stderr.toString()){
                        vscode.window.showErrorMessage(proc.stderr.toString())
                    }
                    let html = proc.stdout.toString()
                    html = html.replace(/\$\{ERROR_COLOR\}/gi, ERROR_COLOR)
                    html = html.replace(/\$\{WARNING_COLOR\}/gi, WARNING_COLOR)
                    html = html.replace(/\$\{FIND_WSL\}/gi, FIND_WSL)
                    html = html.replace(
                                /\$\{CHANGE_WORKSPACE\}/gi, CHANGE_WORKSPACE)
                    html = html.replace(/\$\{BASH_COMMAND\}/gi, BASH_COMMAND)
                    // vscode.window.showInformationMessage(html)
                    htmlContents += html
                    if(proc.status){
                        exports.isError = proc.status
                    }
                }  
            }
        }
    }
    setHtmlBody()
}

  
function statusMsg(msg:string){
    htmlContents += `<li>${msg}</li>\n`
}


function warning(msg:string){
    return `<em style="color: ${WARNING_COLOR}"> ${msg} </em>` 
}


function errorMsg(msg:string){
    if(!firstErrMsg){
        firstErrMsg = msg
    }
    htmlContents += `<p style="color: ${ERROR_COLOR}">ERROR: ${msg}</p>`
}

function changeWorkspace(){
    if(!exports.config){
        return
    }

    let contract_workspace = exports.config["EOSIO_CONTRACT_WORKSPACE"]
    var defaultUri = ""
    if(contract_workspace){
        defaultUri = wslMapLinuxWindows(contract_workspace)
    }
    
    vscode.window.showOpenDialog({
        canSelectMany: false,
        canSelectFiles: false,
        canSelectFolders: true,
        defaultUri: vscode.Uri.file(defaultUri),
        openLabel: 'Select workspace directory'
    }).then(fileUri => {
    if (fileUri && fileUri[0]) {
        exports.config["EOSIO_CONTRACT_WORKSPACE"] 
                                        = wslMapWindowsLinux(fileUri[0].fsPath)
        if(!writeJson( // OK, exit code is 0
            exports.config["CONFIG_FILE"], 
            {"EOSIO_CONTRACT_WORKSPACE": 
                                    wslMapWindowsLinux(fileUri[0].fsPath)})){
                                        InstallPanel.createOrShow()
                                    } 
    }
    })
}


function bashCommand(message:any){
    let lines = message.value.split("\n")
    let command = ""
    for(let i = 0; i < lines.length; i++){
        let line = lines[i].trim()
        if(line){
            line = line.replace(/\<br\>/gi, "\n")
            line = line.replace(/&amp;/gi, "&")
            command += line
        }
    }
    if(InstallPanel.currentPanel){
        command = 
`<< ////

ENTER to start the following command line. The last sub-command in the line 
issues a signal to the view 'Installing EOSIDE'

////
` + command
        command += " &&\\\n" + InstallPanel.currentPanel.updatingCommand()
    } else {
        command = 
`
<< ////

ENTER to start the following command line. Refresh the view 'Installing EOSIDE': (ctrl/cmd+alt+i) 
                        or (ctrl/cmd+shift+p + eoside install),
in order to see the newest installation status.

////
` + command
    }
     

    def.getTerminal(message.id, true, true).sendText(command.trim(), false)    
}


export function getContractWorkspace(){
    if(!exports.config){
        return null
    }
    var contractWorkspace = exports.config["EOSIO_CONTRACT_WORKSPACE"]
    if(contractWorkspace){
        contractWorkspace = def.IS_WINDOWS 
                                    ? wslMapLinuxWindows(contractWorkspace)
                                    : wslMapWindowsLinux(contractWorkspace)
    }
    return contractWorkspace
}


function setHtmlBody(){
    if(exports.isError >= IS_ERROR){
        return
    }

    htmlContents += 
`
        <p style="color: unset; font-size: ${def.HEADER_SIZE};">
            Contract Workspace
        </p>
        <p>
            <button class="btn"; id="${CHANGE_WORKSPACE}"; 
                                                    title="${CHANGE_WORKSPACE}">
                change
            </button>
            ${exports.config && exports.config["EOSIO_CONTRACT_WORKSPACE"] 
                ? wslMapLinuxWindows(exports.config["EOSIO_CONTRACT_WORKSPACE"])
                : "Not set"}
        </p>

        <p 
            style="color: unset; font-size: ${def.HEADER_SIZE};">
            Configuration
        </p>
        <p>
            <button class="btn"; id="${START_WITH_EOSIDE}"; 
                                                    title="${CONFIGURATION}">
                toggle
            </button>
            startWithEosIde = ${vscode.workspace.getConfiguration()
                                                    .eoside.startWithEosIde}
        </p>
        <p>
            <button class="btn"; id="${MENU}"; title="${CONFIGURATION}">
                toggle
            </button>
            menu = ${vscode.workspace.getConfiguration().eoside.menu}
        </p>
`
}


export default class InstallPanel extends def.Panel {
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: InstallPanel | undefined
    public static readonly viewType = "Install"

    public static createOrShow(show: boolean=true) {
        if(def.IS_WINDOWS && (!exports.config || !root())){
            // In Windows and Linux Subsystem is not installed
        }

        const column = vscode.window.activeTextEditor 
            ? vscode.window.activeTextEditor.viewColumn : undefined

        if(!show){
            verify()
            if(!exports.isError){
                return
            }
        }

        // If we already have a panel, show it.
        if (InstallPanel.currentPanel) {
            InstallPanel.currentPanel.update(show)
            InstallPanel.currentPanel._panel.reveal(column)
        } else {
            // Otherwise, create a new panel.
            const panel = vscode.window.createWebviewPanel(
                    InstallPanel.viewType, "Install", 
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
            InstallPanel.currentPanel = new InstallPanel(panel, show)
        }
    }

    private server: net.Server
    private port = ""

    public updatingCommand(){
        return `nc localhost ${this.port} <<< "Refresh the view 'Installing EOSIO'"`
    }

    protected constructor(panel: vscode.WebviewPanel, doUpdate: boolean=true) {
        super(panel)
        this.server = createServer(
`Refreshing the view 'Installing EOSIO...'
`)
        this.server.listen(() => {
            let addr = this.server.address()
            if(typeof addr !== 'string'){
                this.port = addr.port.toString()
            }  
      })
    
        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview()
        this.update(doUpdate)
        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(message => {

            var caseSeletor = message.class.split(" ").length == 1
                    ? message.title: message.class.split(" ")[1].trim()
////////////////////////////////////////////////////////////////////////////////
// On Message
////////////////////////////////////////////////////////////////////////////////
            switch (caseSeletor) {
                case BASH_COMMAND: {
                    bashCommand(message)
                    }
                    break
                case FIND_WSL: {
                    let defaultUri = process.env.appdata
                    defaultUri = defaultUri ? defaultUri: ""

                    vscode.window.showOpenDialog({
                        canSelectMany: false,
                        canSelectFiles: false,
                        canSelectFolders: true,
                        defaultUri: vscode.Uri.file(defaultUri),
                        openLabel: 'Open'
                    }).then(fileUri => {
                        let root = ""
                        if (fileUri && fileUri[0]) {
                            root = fileUri[0].fsPath
                            if(fs.existsSync(path.join(root, "home"))){
                                exports.config["WSL_ROOT"] = root
                                if(writeJson(
                                                exports.config["CONFIG_FILE"], 
                                                exports.config)){
                                    this.update()
                                }
                            } else {
                                vscode.window.showErrorMessage(
`The selected directory 
${root}
is not like the root of an Ubuntu file system as it
misses the 'home' directory.
`)
                            }
                        }
                    })
                    break
                }   
                case CHANGE_WORKSPACE: {
                    changeWorkspace()
                    break
                }
                case CONFIGURATION: {
                    switch (message.id) {
                        case START_WITH_EOSIDE: {
                            vscode.workspace.getConfiguration()
                                .update(
                                        "eoside.startWithEosIde",
                                        !vscode.workspace.getConfiguration()
                                    .eoside.startWithEosIde)
                                    .then(() => {this.update()})
                            break
                        }
                        case MENU: {
                            vscode.workspace.getConfiguration()
                                .update("eoside.menu", !vscode.workspace
                                .getConfiguration().eoside.menu)
                                .then(() => {this.update()})
                            break
                        }
                    }
                    break
                }
            }
        }, null, this._disposables)
    }

    public dispose() {
        super.dispose()
        this.server.close()
        InstallPanel.currentPanel = undefined
    }

    public update(doUpdate: boolean=true){
        if(!doUpdate){
            return
        }
        htmlContents = TITLE
        verify()
        this._panel.webview.html = this._getHtmlForWebview();
    }

    private _getHtmlForWebview() {
        return def.htmlForWebview(
                            this._extensionPath, "Install EOSIDE", htmlContents)
    }
}


export function root():string {
    if(exports.config){
        return exports.config["WSL_ROOT"]
    }
    return ""
}


export function writeRoot(){
    const spawn = require("child_process").spawnSync;
    {
        let lxss="hkcu\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss"
        let cl = `REG QUERY ${lxss} -s -v BasePath`
        const proc = spawn(cl, [], {shell: true})
        if(proc.status){
            return -1
        }
        try{
            var basePath = proc.stdout.toString().match(/REG_SZ(.*)/)[1].trim()
        } catch(err){
            return -1
        }
        
    } 
    // {
    //     let cl = `bash.exe -c whoami`
    //     const proc = spawn(cl, [], {shell: true})
    //     var user = proc.stdout.toString()
    //     if(proc.status){
    //         return -1
    //     }
    // }
    exports.config["WSL_ROOT"] = basePath
    return writeJson(exports.config["CONFIG_FILE"], exports.config)
}


export function writeJson(file:string, json:Object){
    file = wslMapLinuxWindows(file)
    try{
        fs.writeFileSync(file, JSON.stringify(json, undefined, 4))
    } catch(err){
        vscode.window.showErrorMessage(
`Cannot write. The path tried is
${file}.
Error message is
${err}`)
        return -1
    }
    return 0
}


export function wslMapLinuxWindows(originalPath:string){
    if(!def.IS_WINDOWS || originalPath.includes(":")){
        return originalPath
    }
    if(originalPath.includes("/mnt/")){
        var convPath = `${originalPath[5].toUpperCase()}:${originalPath.substr(6)}`
                                                        .replace(/\//gi, "\\")
    } else {
        convPath = path.join(root(), originalPath)
    }
    return convPath
}


export function wslMapWindowsLinux(originalPath:string){
    if(!def.IS_WINDOWS){
        return originalPath
    }    
    if(!originalPath.includes(":")){
        return originalPath
    }
    var convPath = originalPath.replace(/\\/gi, "/")

    if(convPath.includes(root())){
        convPath = convPath.replace(root(), "")
    } else {
        let drive = convPath[0]
        convPath = convPath.replace(
                                `${drive}:/`, `/mnt/${drive.toLowerCase()}/`)        
    }
    return convPath
}


function isCurrentEOSFactoryBiggerThanMinimal(){
    var versionMin = EOSFACTORY_VERSION_MIN.split('.')
    var version = exports.config["VERSION"].split('.')
     
    for(let i = 0; i < versionMin.length; i++){
        if(versionMin[i] > version[i]){
            return false
        }
    }

    return true
}


function createServer(msg:string){
//https://www.dev2qa.com/node-js-tcp-socket-client-server-example/    
    var server = net.createServer((client) => {
        client.setEncoding('utf-8');
        client.setTimeout(1000);
        // When receive client data.
        client.on('data', function (data) {
            client.end(msg)
            InstallPanel.createOrShow()
        })
        // When client send data complete.
        client.on('end', function () {
            // Get current connections count.
            server.getConnections(function (err, count) {
                if(err) {
                    console.error(JSON.stringify(err));
                }

            });
        });
        // When client timeout.
        client.on('timeout', function () {
            console.log('Client request time out.');
        })

        console.log("client connected")
    })
    return server
}


