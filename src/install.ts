import * as path from 'path'
import * as vscode from 'vscode'
import * as fs from 'fs'
import * as def from './definitions'

export var config: any = undefined
export const PYTHON: string = "python3"
export const PIP: string = "pip3"

const WSL_VERSION_MIN = "4.3"
const ERROR_COLOR = "indianred"

const FIND_WSL = "findWsl"
const CHANGE_WORKSPACE = "changeWorkspace"
const EOS_REPOSITORY = "eosRepository"
const CONFIGURATION = "configuration"
const START_WITH_EOSIDE = "startWithEosIde"
const MENU = "menu"

export var isError = false
var htmlBody: any = undefined

function errorConditions(){
    const spawn = require("child_process").spawnSync;
    htmlBody = ''

    if(def.IS_WINDOWS){
        const process = spawn("bash.exe", ["--version"])
        let version = process.stdout.toString().match(/version\s{1}(.*)\./)[1]
        if(process.status){
            errorMsg(
`It seems that Windows Subsystem Linux is not in the System, or the 
<em>bash.exe</em> executable is not in the System path.<br> 
EOSIde cannot do without WSL.`)
            isError = true
            return            
        }
        if(version >= WSL_VERSION_MIN){
            conditionMsg(
            `<em>Windows Subsystem Linux</em> version ${version} detected.`)
        } else {
            errorMsg(
`The version of the WSL installation is <em>${version}</em>, while the 
minimum is <em>${WSL_VERSION_MIN}</em>.<br>
EOSIde cannot do without proper WSL.`)
            isError = true
            return
        }        
    }

    {
        const process = def.IS_WINDOWS 
            ? spawn("bash.exe", ["-c", `${exports.PYTHON} -V`])
            : spawn(`${exports.PYTHON}`, ["-V"])
        if(!process.status){
            conditionMsg(
`<em>${process.stdout.toString().trim()}</em> detected.`)
        } else{
            let msg = 
`It seams that <em>${exports.PYTHON}</em> is not in the System, as the 
<em>python3</em> executable is not in the System path.<br>
EOSIde cannot do without <em>${exports.PYTHON}</em>.`

            if(def.IS_WINDOWS){
                msg +=
`
<br>
Note that the Python has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg)
            isError = true
            return
        }
    }

    {
        const process = def.IS_WINDOWS 
            ? spawn("bash.exe", ["-c", `${exports.PIP} -V`])
            : spawn(`${exports.PIP}`, ["-V"])
        if(!process.status){
            conditionMsg(
`<em>${process.stdout.toString().trim()}</em> detected.`)
        } else{
            let msg = 
`It seams that <em>${exports.PIP}</em> is not in the System, as the 
<em>python3</em> executable is not in the System path.<br>
EOSIde cannot do without <em>${exports.PIP}</em>.`

            if(def.IS_WINDOWS){
                msg +=
`
<br>
Note that the Python Pip has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg)
            isError = true
            return
        }
    }

    {
        let cl = `${exports.PYTHON} -c 'import eosfactory'`
        let clExe = def.IS_WINDOWS
            ? `bash.exe -c "${cl}"`
            : `"${cl}"`
        const process = spawn(clExe, [], {shell: true})
        if(!process.status){
            conditionMsg(`<em>eosfactory</em> package detected.`)
        } else {
            let msg =
`It seems that <em>eosfactory</em> package is not installed in 
the System.<br>
EOSIde cannot do without <em>eosfactory</em>.
`
            if(def.IS_WINDOWS){
                msg += 
`<br>
Note that the package has to be installed in the Windows Subsystem Linux.`
            }
            errorMsg(msg)
            isError = true
            return
        }
    }
    {
        let cl = `${exports.PYTHON} -m eosfactory.config --json`
        let clExe = def.IS_WINDOWS
            ? `bash.exe -c "${cl}"`
            : `"${cl}"`
        const process = spawn(clExe, [], {shell: true})
        if(!process.status){
            conditionMsg(`<em>EOSFactory</em> configuration file detected`)
        } else {
            errorMsg(
`It seems that the eosfactory package is corrupted, as its configuration 
file cannot be found.`)
            isError = true
            return
        }
        exports.config = JSON.parse(process.stdout)
        conditionMsg(
`Configuration file is ${def.wslMapLinuxWindows(exports.config["CONFIG_FILE"])}`)

        if(def.IS_WINDOWS){
            if(!exports.config["WSL_ROOT"] && !writeRoot()){
                errorMsg(
`Cannot determine the root of the WSL.<br>
EOSIde cannot do without it.`)
                setWslRoot()
                isError = true
                return
            } else {
                conditionMsg(`<em>WSL</em> root directory detected.<br>`)
            } 
        }        
    }
    passed()
}


function conditionMsg(msg:string){
    htmlBody += `<li>${msg}</li>\n`
}


function errorMsg(msg:string){
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


function passed(){
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
    ${def.wslMapLinuxWindows(exports.config["EOSIO_CONTRACT_WORKSPACE"])}
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

    public static createOrShow(extensionPath: string) {
        if(def.IS_WINDOWS && (!exports.config || !root())){
            // In Windows and Linux Subsystem is not installed
        }

        const column = vscode.window.activeTextEditor 
            ? vscode.window.activeTextEditor.viewColumn : undefined

        // If we already have a panel, show it.
        if (InstallPanel.currentPanel) {
            InstallPanel.currentPanel._panel.reveal(column)
            return
        }

        // Otherwise, create a new panel.
        const panel = vscode.window.createWebviewPanel(
                InstallPanel.viewType, "Install", 
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

        InstallPanel.currentPanel = new InstallPanel(panel, extensionPath)
    }

    protected constructor(
        panel: vscode.WebviewPanel,
        extensionPath: string
    ) {
        super(panel, extensionPath)
        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview()

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
                                if(def.writeJson(
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
                case CHANGE_WORKSPACE:{
                    let defaultUri = def.wslMapLinuxWindows(
                                   exports.config["EOSIO_CONTRACT_WORKSPACE"])

                    vscode.window.showOpenDialog({
                        canSelectMany: false,
                        canSelectFiles: false,
                        canSelectFolders: true,
                        defaultUri: vscode.Uri.file(defaultUri),
                        openLabel: 'Open'
                    }).then(fileUri => {
                        if (fileUri && fileUri[0]) {
                            exports.config["EOSIO_CONTRACT_WORKSPACE"] 
                                = def.wslMapWindowsLinux(fileUri[0].fsPath)
                            if(!def.writeJson(
                                exports.config["CONFIG_FILE"], exports.config)){
                                    this.update()
                            } 
                        }
                    })
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
                                    = def.wslMapWindowsLinux(fileUri[0].fsPath)
                                if(!def.writeJson(
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
                                .update("eoside.startWithEosIde",!vscode.workspace.getConfiguration()
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

    public update(){
        htmlBody = ''
        errorConditions()
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
        const process = spawn(cl, [], {shell: true})
        if(process.status){
            return -1
        }
        try{
            var basePath = process.stdout.toString().match(/REG_SZ(.*)/)[1].trim()
        } catch(err){
            return -1
        }
        
    } 
    {
        let cl = `bash.exe -c whoami`
        const process = spawn(cl, [], {shell: true})
        var user = process.stdout.toString()
        if(process.status){
            return -1
        }
    }
    exports.config["WSL_ROOT"] = `${basePath}`//\\home\\${user}`
    return def.writeJson(exports.config["CONFIG_FILE"], exports.config)
}

errorConditions()
