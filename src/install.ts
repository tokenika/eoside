// var sync = require('child_process').spawnSync;
// var pyt = sync(`${def.PYTHON}`, ['-c', 'import eosfactory'])


import * as path from 'path'
import * as vscode from 'vscode'
import * as fs from 'fs'
import * as def from './definitions'

export var config: any = undefined
export const PIP: string = "pip3"

const WSL_VERSION_MIN = "4.3"
const ERROR_COLOR = "indianred"
const WARNING_COLOR = "yellow"

const FIND_WSL = "findWsl"
const CHANGE_WORKSPACE = "changeWorkspace"
const EOS_REPOSITORY = "eosRepository"
const CONFIGURATION = "configuration"
const START_WITH_EOSIDE = "startWithEosIde"
const MENU = "menu"

export var isError = true
export var isWarning = false
var htmlBody: any = undefined
var firstErrMsg: any = undefined
var c_cpp_prop_updated = false

export function verify(){
    const spawn = require("child_process").spawnSync;

    var forceError = false
    var forceSetDirectory = false
    try{
        forceError = vscode.workspace.getConfiguration().eoside
                                                            .specialEffects[0]
        forceSetDirectory = vscode.workspace.getConfiguration()
                                                    .eoside.specialEffects[1]
    } catch(err){
    }

    htmlBody = ''
    firstErrMsg = ''

    exports.isError = true
    exports.isWarning = false
    var isOK = true

    if(def.IS_WINDOWS){
        const proc = spawn("bash.exe", ["--version"])
        let version = proc.stdout.toString().match(/version\s{1}(.*)\./)[1]
        if(proc.status){
            errorMsg(
`It seems that Windows Subsystem Linux is not in this System, or the 
<em>bash.exe</em> executable is not in the System path.<br> 
EOSIDE cannot do without WSL.`)
            isOK = false           
        } else {
            if(version >= WSL_VERSION_MIN){
                statusMsg(
                `<em>Windows Subsystem Linux</em> version ${version} detected.`)
            } else {
                
                errorMsg(
`The version of the WSL installation is <em>${version}</em>, while the 
minimum is <em>${WSL_VERSION_MIN}</em>.<br>
EOSIDE cannot do without proper WSL.`)
            isOK = false
            }            
        }
    }

    {
        const proc = def.IS_WINDOWS 
            ? spawn("bash.exe", ["-c", `${def.PYTHON} -V`])
            : spawn(`${def.PYTHON}`, ["-V"])
            
        if(proc.status){
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
            isOK = false
        } else {
            statusMsg(
`<em>${proc.stdout.toString().trim()}</em> detected.`)
        } 
    }

    {
        const proc = def.IS_WINDOWS 
            ? spawn("bash.exe", ["-c", `${exports.PIP} -V`])
            : spawn(`${exports.PIP}`, ["-V"])
        if(proc.status){
            let msg = 
`It seams that <em>${exports.PIP}</em> is not in the System, as the 
<em>${def.PYTHON}</em> executable is not in the System path.<br>
EOSIDE cannot do without <em>${exports.PIP}</em>.`

            if(def.IS_WINDOWS){
                msg +=
`
<br>
Note that the Python Pip has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg)
            isOK = false
        } else {
            let msg = proc.stdout.toString().trim()
            msg = msg.substr(0, msg.indexOf("from"))
            statusMsg(
`<em>${msg}</em> detected.`)
        }
    }

    {
        let cl = `${def.PYTHON} -c 'import eosfactory'`
        let clExe = def.IS_WINDOWS
            ? `bash.exe -c "${cl}"`
            : `"${cl}"`
        const proc = spawn(clExe, [], {shell: true})

        if(proc.status){
            let msg =
`It seems that <em>eosfactory</em> package is not installed in 
the System, or it is corrupted.<br>
EOSIDE cannot do without <em>eosfactory</em>.
`
            if(def.IS_WINDOWS){
                msg += 
`<br>
Note that the package has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg)
            isOK = false
        } else {
            statusMsg(`<em>eosfactory</em> package detected.`)

            const proc = def.IS_WINDOWS
            ? spawn(
                    `bash.exe -c "${def.PYTHON}` 
                        + ' -m eosfactory.config --json --dont_set_workspace"', 
                    [], {shell: true})
            : spawn(`${def.PYTHON}`, 
                ['-m', 'eosfactory.config', '--json', 
                                                '--dont_set_workspace'])
            if(proc.status){
                errorMsg(
`It seems that the eosfactory package is not installed or corrupted, as its 
configuration file cannot be read.`)
                isOK = false
            } else {
                statusMsg(`<em>EOSFactory</em> configuration file detected`)
                exports.config = JSON.parse(proc.stdout);

                statusMsg(
`Configuration file is ${exports.config["CONFIG_FILE"]}`)
                var msg = ""
                if(exports.config["EOSIO_VERSION"][0]){
                    var msg = `eosio version ${exports.config["EOSIO_VERSION"][0]} detected.`
                    if(exports.config["EOSIO_VERSION"].length > 1){
                        exports.isWarning = true
                        msg += warning("NOTE: EOSFactory was tested with version " 
                            + `${exports.config["EOSIO_VERSION"][1]}`)
                    }
                
                } else {
                    exports.isWarning = true
                    msg = warning(
`Cannot determine that eosio is installed as nodeos does not response. EOSFactory expects eosio version ${exports.config["EOSIO_VERSION"][1]}`)
                }
                statusMsg(msg)

                if(exports.config["EOSIO_CDT_VERSION"][0]  && !forceError){
                    var msg = `eosio.cdt version ${exports.config["EOSIO_CDT_VERSION"][0]} detected.`
                    if(exports.config["EOSIO_CDT_VERSION"].length > 1){
                        exports.isWarning = true
                        msg += warning('NOTE: EOSFactory was tested with version '
                            + `${exports.config["EOSIO_CDT_VERSION"][1]}`)
                    }
                    statusMsg(msg)
                } else {
                    errorMsg(
`Cannot determine that eosio.cdt is installed as eosio-cpp does not response. 
EOSFactory expects eosio.cdt version ${exports.config["EOSIO_CDT_VERSION"][1]}`)
                    isOK = false
                }

                if(def.IS_WINDOWS){
                    if(!exports.config["WSL_ROOT"] && !writeRoot()){
                        errorMsg(
`Cannot determine the root of the WSL.<br>
EOSIDE cannot do without it.`)
                        setWslRoot()
                        isOK = false
                    } else {
                        statusMsg(`<em>WSL</em> root directory detected.<br>`)
                    } 
                }            
            }
            if(exports.config && (
                !exports.config["EOSIO_CONTRACT_WORKSPACE"] 
                                                        || forceSetDirectory)){
                isOK = false
                if(forceSetDirectory){
                    exports.config["EOSIO_CONTRACT_WORKSPACE"] = "Not set"
                }
                errorMsg(
`
Default workspace is not set. 
<button 
class="btn"; 
id="${CHANGE_WORKSPACE}"; 
title="${CHANGE_WORKSPACE}">
Set workspace.
</button>
`)
            }

        }
    }
 

    if(isOK){
        exports.isError = false
        if(vscode.workspace.workspaceFolders && !c_cpp_prop_updated){
            //Especially, update eosio.cdt version.
            c_cpp_prop_updated = true
            let c_cpp_prop_path = path.join(
                                    vscode.workspace.workspaceFolders[0].uri.fsPath, 
                                    ".vscode", "c_cpp_properties.json")
    
            if(fs.existsSync(c_cpp_prop_path)){
                let cl = `${def.PYTHON} -m eosfactory.core.vscode `
                + `--c_cpp_prop_path '${c_cpp_prop_path}' `
                + `--root '${root()}' `
    
                def.callEosfactory(cl)
            }
        }
    }
    setHtmlBody()
}

function statusMsg(msg:string){
    htmlBody += `<li>${msg}</li>\n`
}


function warning(msg:string){
    return `<em style="color: ${WARNING_COLOR}"> ${msg} </em>` 
}


function errorMsg(msg:string){
    if(!firstErrMsg){
        firstErrMsg = msg
    }
    htmlBody += `<p style="color: ${ERROR_COLOR}">ERROR: ${msg}</p>`
}


function setWslRoot(){
    htmlBody += 
`
<p>
You can indicate the WSL root in your system. Click the button below to open
file dialog. Then navigate to a directory containing the Ubuntu file system.
</p>
<p>
    <button 
        class="btn"; 
        id="${FIND_WSL}"; 
        title="${FIND_WSL}">find WSL root
    </button>
</p>
`
}


function setEosRepository(){
    htmlBody += 
`
<p>
You can indicate the EOS repository in your system. Click the button below to 
open file dialog. Then navigate to the repository's folder.
</p>
<p>
    <button 
        class="btn"; 
        id="${EOS_REPOSITORY}"; 
        title="${EOS_REPOSITORY}">find WSL root
    </button>
</p>
`
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
        openLabel: 'Open'
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


function setHtmlBody(){  
    htmlBody += 
`
<p 
        style="
        color: unset;
        font-size: ${def.HEADER_SIZE};">
    Contract Workspace
</p>
<p>
    <button 
            class="btn"; 
            id="${CHANGE_WORKSPACE}"; 
            title="${CHANGE_WORKSPACE}">
        change
    </button>
    ${exports.config && exports.config["EOSIO_CONTRACT_WORKSPACE"] ? exports.config
                                    ["EOSIO_CONTRACT_WORKSPACE"] : "Not set"}
</p>

<p 
        style="
        color: unset;
        font-size: ${def.HEADER_SIZE};">
    Configuration
</p>
<p>
    <button 
            class="btn"; 
            id="${START_WITH_EOSIDE}"; 
            title="${CONFIGURATION}">
        toggle
    </button>
    startWithEosIde = ${vscode.workspace.getConfiguration()
                                                    .eoside.startWithEosIde}
</p>
<p>
    <button 
            class="btn"; 
            id="${MENU}"; 
            title="${CONFIGURATION}">
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
            if(!exports.isError && !exports.isWarning){
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

    protected constructor(panel: vscode.WebviewPanel, doUpdate: boolean=true) {
        super(panel)
        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview()
        this.update(doUpdate)
        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(message => {
            switch (message.title) {
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
                case EOS_REPOSITORY: {
                        let defaultUri = def.IS_WINDOWS 
                            ? "": "/home"

                        vscode.window.showOpenDialog({
                            canSelectMany: false,
                            canSelectFiles: false,
                            canSelectFolders: true,
                            defaultUri: vscode.Uri.file(defaultUri),
                            openLabel: 'Open'
                        }).then(fileUri => {
                            if (fileUri && fileUri[0]) {
                                exports.config["EOSIO_SOURCE_DIR"] 
                                    = wslMapWindowsLinux(fileUri[0].fsPath)
                                if(!writeJson(
                                    exports.config["CONFIG_FILE"], 
                                                            exports.config)){
                                        this.update()
                                } 
                            }
                        })
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
        InstallPanel.currentPanel = undefined
    }

    public update(doUpdate: boolean=true){
        if(!doUpdate){
            return
        }
        htmlBody = ''
        verify()
        this._panel.webview.html = this._getHtmlForWebview();
    }

    private _getHtmlForWebview() {
        const scriptPathOnDisk = vscode.Uri.file(path.join(
            this._extensionPath, def.RESOURCE_DIR, 'install.js'))

        // And the uri we use to load this script in the webview
        const scriptUri = scriptPathOnDisk.with({ scheme: 'vscode-resource' })

        if(vscode.workspace.workspaceFolders){
            var folder = path.join(
                        vscode.workspace.workspaceFolders[0].uri.fsPath, 
                        "CMakeLists.txt")
        }

        const htmlUri = vscode.Uri.file(
            path.join(this._extensionPath, def.RESOURCE_DIR, 'install.html'))

        const htmlBase = vscode.Uri.file(path.join(
                            this._extensionPath, def.RESOURCE_DIR, '/'))
                            .with({ scheme: 'vscode-resource' })

        let html = fs.readFileSync(htmlUri.fsPath).toString()
                            .replace(/\$\{nonce\}/gi, def.getNonce())
                            .replace(/\$\{scriptUri\}/gi, scriptUri.toString())
                            .replace(/\$\{htmlBase\}/gi, htmlBase.toString())
                            .replace(/\$\{htmlBody\}/gi, htmlBody)                      
        return html
    }
}

export function root(){
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
    {
        let cl = `bash.exe -c whoami`
        const proc = spawn(cl, [], {shell: true})
        var user = proc.stdout.toString()
        if(proc.status){
            return -1
        }
    }
    exports.config["WSL_ROOT"] = `${basePath}`//\\home\\${user}`
    return writeJson(exports.config["CONFIG_FILE"], exports.config)
}


export function wslMapLinuxWindows(convPath:string){
    if(!def.IS_WINDOWS || convPath.includes(":")){
        return convPath
    }
    if(convPath.includes("/mnt/")){
        convPath = `${convPath[5].toUpperCase()}:${convPath.substr(6)}`
                                                        .replace(/\//gi, "\\")
    } else {
        convPath = path.join(root(), convPath)
    }
    return convPath
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


export function wslMapWindowsLinux(convPath:string){
    if(!exports.IS_WINDOWS){
        return convPath
    }    
    if(!convPath.includes(":")){
        return convPath
    }
    convPath = convPath.replace(/\\/gi, "/")
    if(convPath.includes("/mnt/")){
        let drive = convPath[0]
        convPath = convPath.replace(
                                `${drive}:/`, `/mnt/${drive.toLowerCase()}/`)
    } else {
        convPath = convPath.replace(root(), "")
    }
    return convPath
}