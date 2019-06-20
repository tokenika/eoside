import * as path from 'path'
import * as vscode from 'vscode'
import * as fs from 'fs'
import * as def from './definitions'
import * as inst from './install'
import * as deb from './nativedebugger'

const INCLUDE = "includePath"
const LIBS = "libs"
const CODE_OPTIONS = "codeOptions"
const TEST_OPTIONS = "testOptions"
const CONTRACT_ACCOUNT = "contractAccount"
const UP = "up"
const ADD = "include"
const DOWN = "down"
const DELETE = "del"
const INSERT = "insert"
const CONTROL = "ctr"


export default class SetupPanel extends def.Panel{
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: SetupPanel | undefined
    public static readonly viewType = "Setup"

    public static createOrShow() {
        if(!vscode.workspace.workspaceFolders){
            vscode.window.showInformationMessage(
                            "Cannot open Setup View: Explorer is empty."
            )
            return
        }

        if(inst.isError){
            vscode.window.showErrorMessage("Installation is not completed.")
            return
        }

        let c_cpp_prop_path = path.join(
                            vscode.workspace.workspaceFolders[0].uri.fsPath, 
                            ".vscode", "c_cpp_properties.json")
        if(!fs.existsSync(c_cpp_prop_path)){
            vscode.window.showErrorMessage(`
            There is no C/CPP configuration file expected to be
            "${c_cpp_prop_path}"
            `)
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
                vscode.Uri.file(path.join(
                    def.getExtensionPath(), def.RESOURCE_DIR))
            ]
            }
        )

        SetupPanel.currentPanel = new SetupPanel(panel)        
    }

    private constructor(panel: vscode.WebviewPanel) {
        super(panel)

        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview()
        // Handle messages from the webview
        var prevMsg: any = undefined
        this._panel.webview.onDidReceiveMessage(message => {

            var caseSeletor = message.class.split(" ").length == 1
                    ? message.title: message.class.split(" ")[1].trim()

            switch (caseSeletor) {
                case INCLUDE:
                    Includes.createOrGet(this._extensionPath).action(message)
                    break
                case LIBS:
                    Libs.createOrGet(this._extensionPath).action(message)
                    break
                case CODE_OPTIONS:
                    CodeOptions.createOrGet(this._extensionPath).action(message)
                    break
                    case TEST_OPTIONS:
                    TestOptions.createOrGet(this._extensionPath).action(message)
                    break   
                case CONTROL:
                    if(SetupPanel.currentPanel){
                        switch(message.id) {
                            case "compile": {
                                    compile()
                                }
                                break
                            case "compileTest": {
                                    compile(true)
                                }
                                break
                            case "build": {
                                    build()
                                }
                                break
                            case "buildTest": {
                                    build(true)
                                }
                                break
                            case "EOSIDE":
                                vscode.commands.executeCommand(
                                                        "eoside.GetStarted")
                                break
                            case "bash": {
                                    bash()
                                }            
                                break
                            case "zip": {
                                    zip()
                                }            
                                break
                        }
                    }
                    break
                case CONTRACT_ACCOUNT:
                    ContractAccount.createOrGet(this._extensionPath)
                                                            .action(message)
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
        return def.htmlForWebview(
            this._extensionPath, "Setup EOSIDE", body(this._extensionPath))
    }
}


function body(extensionPath:string){
    var options = vscode.workspace.getConfiguration().eoside.testMode
        ? `
        <div class="row">
            <div class="leftcolumn">
                <button  class="btn ${CODE_OPTIONS}"; id="include"; 
                                title="Add a new code option.">&#8627</button>
                <label style="color: unset; font-size: ${def.HEADER_SIZE};">
                    Code Options
                </label>
                <br><br>
                ${CodeOptions.createOrGet(extensionPath).items()}
            </div>

            <div class="rightcolumn">
                <button  class="btn ${TEST_OPTIONS}"; id="include"; 
                                title="Add a new test option.">&#8627</button>
                <label style="color: unset; font-size: ${def.HEADER_SIZE};">
                    Test Options
                </label>
                <br><br>
                ${TestOptions.createOrGet(extensionPath).items()}
            </div>            
        </div>
        ` : `
        <div class="row">
            <button  class="btn ${CODE_OPTIONS}"; id="include"; 
                                title="Add a new code option.">&#8627</button>
            <label style="color: unset; font-size: ${def.HEADER_SIZE};">
                Code Options
            </label>
            <br><br>
            ${CodeOptions.createOrGet(extensionPath).items()}
        </div>
        `
    var testButtons = vscode.workspace.getConfiguration().eoside.testMode
    ? `
            <button
                class="ctr ctr"; 
                id="compileTest"; 
                title="Compile with the test options (ctrl/cmd+alt+c).">Compile Test</button>
            <button 
                class="ctr ctr"; 
                id="buildTest"; 
                title="Build with the test options (ctrl/cmd+alt+b).">Build and Run Test</button>  
    ` : ''

    return `
        <div class="row">
            <button
                class="ctr ctr"; 
                id="compile"; 
                title="Compile with the code options (ctrl/cmd+shift+c).">Compile</button>
            <button 
                class="ctr ctr"; 
                id="build"; 
                title="Build with the code options (ctrl/cmd+shift+b).">Build</button>    
            <button 
                class="ctr ctr"; 
                id="EOSIDE"; 
                title="Open the EOSIDE view (ctrl/cmd+alt+i).">EOSIDE</button>
                
            ${def.IS_WINDOWS ?`
                <button class="ctr ctr"; id="bash"; 
                title="Open a new bash terminal panel (ctrl/cmd+alt+x).">bash</button>
            `: ""}

            ${testButtons}

            <br><br>

            <button
                class="ctr ctr"; 
                id="zip"; 
                title="Create zipped distribution of the current project. (ctrl/cmd+alt+z)">
                Zip</button>
        </div>        

        <div class="row">
            <button class="btn ${INCLUDE}"; id="include"; 
                    title="Add a new include folder. Left mouse -- use dialog, right mouse -- use input box.">&#8627</button>
            <label style=" color: unset; font-size: ${def.HEADER_SIZE};">
                Include
            </label>
            ${def.IS_WINDOWS ?`
                <p>WSL root is ${inst.root()}</p>
            `: "<p></p>"}
            
            ${Includes.createOrGet(extensionPath).items()}
        </div>

        <div class="row">
            <button class="btn ${LIBS}"; id="include"; 
                title="Add a new library file. Left mouse -- use dialog, right mouse -- use input box.">&#8627</button>
            <label style=" color: unset; font-size: ${def.HEADER_SIZE};">
                Libs
            </label>
            ${def.IS_WINDOWS ?`
                <p>WSL root is ${inst.root()}</p>
            `: "<p></p>"}

            ${Libs.createOrGet(extensionPath).items()}
        </div>

        ${options}

        <div class="row">
            <button class="btn ${CONTRACT_ACCOUNT}"; id="change"; 
                title="Set a contract deployment account.">&#8627</button>
            <label style="color: unset; font-size: ${def.HEADER_SIZE};">
                Contract Account
            </label>
            <br><br>
            ${ContractAccount.createOrGet(extensionPath).items()}
        </div>
`
}


export function compile(test_options=false){
    let terminalName = "compile"
    if(vscode.workspace.workspaceFolders){
        let terminal = def.getTerminal(terminalName, true, true)
        let cl = 
            `${def.PYTHON} -m eosfactory.build ` 
            + `'${vscode.workspace.workspaceFolders[0].uri.fsPath}' `
            + `--c_cpp_prop `
            + `'${path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath,
                    ".vscode/c_cpp_properties.json")}' `
            + ' --compile'
        if(test_options && vscode.workspace.getConfiguration().eoside.testMode){
            cl += ' --test_options'
        }
        terminal.sendText(cl)
    }    
}


export function build(test_options=false){
    let terminalName = "build"
    if(vscode.workspace.workspaceFolders){
        let terminal = def.getTerminal(terminalName, true, true)
        let c_cpp_propertiesPath = path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath,
                    ".vscode/c_cpp_properties.json")
        let cl = 
            `${def.PYTHON} -m eosfactory.build` 
            + ` '${vscode.workspace.workspaceFolders[0].uri.fsPath}'`
            + ` --c_cpp_prop`
            + ` '${c_cpp_propertiesPath}'`
        if(test_options && vscode.workspace.getConfiguration().eoside.testMode){
            cl += " --test_options"
        }                    
        terminal.sendText(cl)

        if(test_options){
            deb.createEosideLaunchConfig(readProperties(c_cpp_propertiesPath))
            let cl = 
            `${def.PYTHON} -m eosfactory.build` 
            + ` '${vscode.workspace.workspaceFolders[0].uri.fsPath}'`
            + " --c_cpp_prop"
            + ` '${c_cpp_propertiesPath}'`
            + " --test_options"
            + " --execute"
            terminal.sendText(" ")
            terminal.sendText(cl)
        }
    }    
}


export function deploy(){
    var terminalName = "deploy"
    if(vscode.workspace.workspaceFolders){
        let terminal = def.getTerminal(terminalName, true, true)
        let cl = 
            `${def.PYTHON} -m eosfactory.deploy`
            + ` --dir` 
            + ` '${vscode.workspace.workspaceFolders[0].uri.fsPath}'`
            + ` --c_cpp_prop`
            + ` '${path.join(
                    vscode.workspace.workspaceFolders[0].uri.fsPath,
                    ".vscode/c_cpp_properties.json")}'`
        terminal.sendText(cl)
    }      
}


export function bash(){
    if(def.IS_WINDOWS){
        vscode.window.createTerminal("bash", def.SHELL_PATH).show()
    } else {
        vscode.window.createTerminal("bash").show()
    }
}


export function zip(){
    var terminalName = "zip"
    if(vscode.workspace.workspaceFolders){
        let terminal = def.getTerminal(terminalName, true, true)
        let cl = 
            `${def.PYTHON} -m eosfactory.pack_contract`
        terminal.sendText(cl)
    }      
}


function readProperties(c_cpp_propertiesPath: any){
        var json = null
        if(c_cpp_propertiesPath && fs.existsSync(c_cpp_propertiesPath)){
            try {
                json = JSON.parse(
                            fs.readFileSync(c_cpp_propertiesPath, 'utf8'))
            } catch(err){
                if(err.code !== "ENOENT"){
                    vscode.window.showErrorMessage(err)
                    console.log(err)                
                }
            }
        }
        return json        
    }

abstract class Base{
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
        this.json = readProperties(this._c_cpp_properties)
    }

    protected update(){
        if(this._c_cpp_properties) {
            inst.writeJson(this._c_cpp_properties, this.json)
            if(SetupPanel.currentPanel){
                SetupPanel.currentPanel.update()
            }            
        } 
    }    
}

abstract class Dependencies extends Base{

    protected abstract getEntries(): string[]
    protected abstract setEntries(entries: string[]): void

    private insertPath(index: number, path: any){
        if(path){
            console.log('Selected file: ' + path)
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
            }
    }

    protected insert(index: number, button=0, selectFiles: boolean=true){
        if(button == 0){
            let path = undefined
            vscode.window.showOpenDialog({
                canSelectMany: false,
                canSelectFiles: selectFiles,
                canSelectFolders: !selectFiles,
                defaultUri: vscode.Uri.file(inst.root()),
                openLabel: 'Open'
            }).then(fileUri => {
                if (!fileUri || !fileUri[0]) {
                    return
                }
                this.insertPath(index, def.javaPath(fileUri[0].fsPath))             
            })
        } else {
            vscode.window.showInputBox({
                placeHolder: "",
                ignoreFocusOut: true
            }).then((path) => {this.insertPath(index, path)})
        }

    }

    public action(message: any){        
        if(message.id === ADD){
            this.insert(-1, message.button)
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
            this.insert(Number(message.id.replace(INSERT, "")), message.button)
        }     
    }

    public items(clazz=""){
        var entries: string[] = []
        this.read()
        var temp = this.getEntries()
        if(temp){
            entries = temp
        }
        
        var root = inst.root()
        var pattern = new RegExp(root, 'i')
        if(root){
            for(let i = 0; i < entries.length; i++){

                entries[i] = entries[i].replace(pattern, "${root)");
            }            
        }

        var items = ""
        for(let i = 0; i < entries.length; i++){
            items += setupEntry(i, entries[i], clazz,)
        }
        return items;
    }    
}

class Includes extends Dependencies{
    public static instance: Includes | undefined

    public static createOrGet(extensionPath:string) {
        if(!Includes.instance){
            Includes.instance = new Includes(extensionPath)
        }
        return Includes.instance
    }

    protected getEntries() {
        return this.json["configurations"][0][INCLUDE]
                ? this.json["configurations"][0][INCLUDE].slice(): []
    }

    protected setEntries(entries: string[]){
        this.json["configurations"][0][INCLUDE] = entries
        this.json["configurations"][0]["browse"]["path"] = entries
    }

    public items(){
        return super.items(INCLUDE)
    }

    public insert(index: number, button: number){
        super.insert(index, button, false)
    }
}


class ContractAccount extends Base{
    public static instance: ContractAccount | undefined

    public static createOrGet(extensionPath:string) {
        if(! ContractAccount.instance){
            ContractAccount.instance = new ContractAccount(extensionPath)
        }
        
        return ContractAccount.instance
    }

    public items(){
        this.read()
        if(this.json.hasOwnProperty(CONTRACT_ACCOUNT)){
            let ca = this.json[CONTRACT_ACCOUNT]
            return ca["template"] + ": " + ca["accountName"] 
                        + " @ " + ca["url"]
        }
        return "Not set"
    }

    public action(message: any){
        let terminalName = "bash"
        if(vscode.workspace.workspaceFolders){
            let terminal = def.getTerminal(terminalName, true, true)            
            terminal.sendText(`${def.PYTHON} -m eosfactory.testnets`)
        }

        vscode.window.showInputBox({
                    placeHolder: "",
                    ignoreFocusOut: true,
                }).then((name) => {
            if(name){
                let proc = def.callEosfactory(
                            `${def.PYTHON} -m eosfactory.testnets --name ${name}`)
                if(!proc.status){
                    let args = proc.stdout.toString().split(" ")
                    this.read()
                    this.json[CONTRACT_ACCOUNT] = 
                        {
                            "template": args[0], 
                            "accountName": args[1],             
                            "url": args[2]
                        }
                    this.update()   
                }
            }
            })
    }
}

abstract class Options extends Dependencies{
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
}

class CodeOptions extends Options{
    public static instance: CodeOptions | undefined

    public static createOrGet(extensionPath:string) {
        if(! CodeOptions.instance){
            CodeOptions.instance = new CodeOptions(extensionPath)
        }
        return CodeOptions.instance
    }

    protected getEntries() {
        return CODE_OPTIONS in this.json["configurations"][0]
                    ? this.json["configurations"][0][CODE_OPTIONS].slice(): []
    }

    protected setEntries(entries: string[]){
        this.json["configurations"][0][CODE_OPTIONS] = entries
    }

    public items(){
        return super.items(CODE_OPTIONS)
    }
}


class TestOptions extends Options{
    public static instance: TestOptions | undefined

    public static createOrGet(extensionPath:string) {
        if(! TestOptions.instance){
            TestOptions.instance = new TestOptions(extensionPath)
        }
        return TestOptions.instance
    }

    protected getEntries() {
        return TEST_OPTIONS in this.json["configurations"][0]
                    ? this.json["configurations"][0][TEST_OPTIONS].slice(): []
    }

    protected setEntries(entries: string[]){
        this.json["configurations"][0][TEST_OPTIONS] = entries
    }

    public items(){
        return super.items(TEST_OPTIONS)
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
        return LIBS in this.json["configurations"][0]
                            ? this.json["configurations"][0][LIBS].slice(): []
    }    
    
    protected setEntries(entries: string[]){
        this.json["configurations"][0][LIBS] = entries
    }

    public items(){
        return super.items(LIBS)
    }

    public insert(index: number, button: number){
        super.insert(index, button, true)
    }
}


function setupEntry(index:number, text:string, clazz:string){
    return `
        <button class="btn ${clazz}"; id="${DOWN}${index}"; 
            title="Move the entry DOWN.">
            &#9660
        </button>
        <button class="btn ${clazz}"; id="${UP}${index}"; 
            title="Move the entry UP">
            &#9650
        </button>
        <button class="btn ${clazz}"; id="${DELETE}${index}"; 
            title="Remove the entry from the list.";>
            X
        </button>
        <button class="btn ${clazz}"; id="${INSERT}${index}"; 
            title="Insert a new entry after the current one. Left mouse -- use dialog, right mouse -- use input box." class="clickable open">
            &#8627
        </button>
        <label>${text}</label>
        <br>
    `
}