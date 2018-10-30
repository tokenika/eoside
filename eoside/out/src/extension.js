"use strict";
// https://code.visualstudio.com/docs
// https://code.visualstudio.com/docs/extensionAPI/extension-points
// https://code.visualstudio.com/docs/extensions/publish-extension
// https://code.visualstudio.com/docs/editor/extension-gallery#_install-from-a-vsix
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const path = require("path");
const vscode = require("vscode");
const fs = require("fs");
const TERMINAL = "eoside";
const SHELL_PATH = "bash.exe";
const TEMPLATE = "template";
const TEMPLATE_DIR = "templates";
const RESOURCE_DIR = "media";
const RECENT = "recent";
const RECENT_JSON = RECENT + ".json";
const GET_STARTED = "getstarted";
const GET_STARTED_JSON = GET_STARTED + ".json";
const OPEN = "open";
var IS_WINDOWS = false;
function activate(context) {
    context.subscriptions.push(vscode.commands.registerCommand('eoside.getStarted', () => {
        GetStartedPanel.createOrShow(context.extensionPath);
    }));
    GetStartedPanel.createOrShow(context.extensionPath);
    if (vscode.env.appRoot.indexOf("\\") != -1) {
        IS_WINDOWS = true;
        vscode.workspace.getConfiguration().update("terminal.integrated.shell.windows", "bash.exe", true);
    }
}
exports.activate = activate;
/**
 * Manages webview panel
 */
class GetStartedPanel {
    constructor(panel, extensionPath) {
        this._disposables = [];
        this._panel = panel;
        this._extensionPath = extensionPath;
        // Set the webview's html content
        this._panel.webview.html = this._getHtmlForWebview();
        // Listen for when the panel is disposed
        // This happens when the user closes the panel or when the panel 
        // is closed programmatically
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        // Update the content based on view changes
        this._panel.onDidChangeViewState(e => { }, null, this._disposables);
        // Handle messages from the webview
        this._panel.webview.onDidReceiveMessage(message => {
            switch (message.title) {
                case TEMPLATE:
                    Templates.createOrGet(this._extensionPath)
                        .template(message.id);
                    return;
                case RECENT:
                    Recent.createOrGet(this._extensionPath).open(message.id);
                    return;
                case GET_STARTED:
                    GetStarted.createOrGet(this._extensionPath)
                        .open(message.id);
                case OPEN:
                    if (message.id === "open_folder") {
                        vscode.commands.executeCommand('vscode.openFolder');
                    }
            }
        }, null, this._disposables);
    }
    static createOrShow(extensionPath) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn : undefined;
        // If we already have a panel, show it.
        if (GetStartedPanel.currentPanel) {
            GetStartedPanel.currentPanel._panel.reveal(column);
            return;
        }
        // Otherwise, create a new panel.
        const panel = vscode.window.createWebviewPanel(GetStartedPanel.viewType, "Get Started EOS IDE", column || vscode.ViewColumn.One, {
            // Enable javascript in the webview
            enableScripts: true,
            // And restrict the webview to only loading content from our 
            // extension's `media` directory.
            localResourceRoots: [
                vscode.Uri.file(path.join(extensionPath, RESOURCE_DIR))
            ]
        });
        GetStartedPanel.currentPanel = new GetStartedPanel(panel, extensionPath);
    }
    static revive(panel, extensionPath) {
        GetStartedPanel.currentPanel = new GetStartedPanel(panel, extensionPath);
    }
    dispose() {
        GetStartedPanel.currentPanel = undefined;
        // Clean up our resources
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }
    _getHtmlForWebview() {
        const scriptPathOnDisk = vscode.Uri.file(path.join(this._extensionPath, RESOURCE_DIR, 'main.js'));
        // And the uri we use to load this script in the webview
        const scriptUri = scriptPathOnDisk.with({ scheme: 'vscode-resource' });
        if (vscode.workspace.workspaceFolders) {
            var folder = path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, "CMakeLists.txt");
        }
        const htmlUri = vscode.Uri.file(path.join(this._extensionPath, RESOURCE_DIR, 'startpage.html'));
        const htmlBase = vscode.Uri.file(path.join(this._extensionPath, RESOURCE_DIR, '/'))
            .with({ scheme: 'vscode-resource' });
        var html = require('fs').readFileSync(htmlUri.fsPath).toString()
            .replace(/\$\{nonce\}/gi, getNonce())
            .replace(/\$\{scriptUri\}/gi, scriptUri)
            .replace(/\$\{getstartedList\}/gi, GetStarted.createOrGet(this._extensionPath).list())
            .replace(/\$\{templateList\}/gi, Templates.createOrGet(this._extensionPath).templateList())
            .replace(/\$\{recentList\}/gi, Recent.createOrGet(this._extensionPath).recentList())
            .replace(/\$\{htmlBase\}/gi, htmlBase);
        return html;
    }
}
GetStartedPanel.viewType = 'Get Started';
function getTerminal(showTerminal = false) {
    for (var i = 0; i < vscode.window.terminals.length; i++) {
        let terminal = vscode.window.terminals[i];
        if (terminal.name === TERMINAL) {
            if (showTerminal) {
                terminal.show();
            }
            else {
                terminal.hide();
            }
            return terminal;
        }
    }
    var terminal = vscode.window.createTerminal(TERMINAL, SHELL_PATH);
    if (showTerminal) {
        terminal.show();
    }
    else {
        terminal.hide();
    }
    return terminal;
}
function getNonce() {
    let text = "";
    const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
class Templates {
    static createOrGet(extensionPath) {
        if (!Templates.instance) {
            Templates.instance = new Templates(extensionPath);
        }
        return Templates.instance;
    }
    constructor(extensionPath) {
        this._extensionPath = extensionPath;
    }
    templateList() {
        let templateDir = vscode.Uri.file(path.join(this._extensionPath, TEMPLATE_DIR)).fsPath;
        var list = "";
        fs.readdirSync(templateDir).forEach((template) => {
            list += clickable(template, TEMPLATE, template.replace(/_/gi, " "));
        });
        return list;
    }
    template(templateName) {
        const options = {
            canSelectMany: false,
            canSelectFiles: false,
            canSelectFolders: true,
            defaultUri: vscode.Uri.file("C:\\Workspaces\\EOS\\contracts"),
            openLabel: 'Open'
        };
        vscode.window.showOpenDialog(options).then(fileUri => {
            if (fileUri && fileUri[0]) {
                let templateDir = vscode.Uri.file(path.join(this._extensionPath, TEMPLATE_DIR, templateName)).fsPath;
                console.log('Selected file: ' + fileUri[0].fsPath);
                let cl = 'python3 -m eosfactory.utils.create_project '
                    + `\\"${fileUri[0].fsPath}\\" \\"${templateDir}\\" --silent`;
                let clExe;
                if (IS_WINDOWS) {
                    clExe = `cmd.exe /c bash.exe -c \"${cl}\"`;
                }
                else {
                    clExe = `\"${cl}\"`;
                }
                const child_process = require("child_process");
                ((cmd) => {
                    child_process.exec(cmd, (err, stdout, stderr) => {
                        if (!stderr) {
                            Recent.createOrGet(this._extensionPath).add(fileUri[0].fsPath);
                            var openFolder = function () {
                                return __awaiter(this, void 0, void 0, function* () {
                                    return yield vscode.commands.executeCommand('vscode.openFolder', fileUri[0]);
                                });
                            };
                            // vscode.workspace.updateWorkspaceFolders(0, 0, {uri: fileUri[0]})
                            openFolder();
                        }
                        else {
                            vscode.window.showErrorMessage(stderr.replace(/[\u001b\u009b][[()#?]*(?:[0-9]{1,4}(?:[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, ''));
                        }
                        console.log('stderr is:' + stderr);
                    }).on('exit', (code) => { });
                })(clExe);
            }
        });
    }
}
function clickable(id, title, text) {
    return `<label id="${id}" 
                title=${title} class="clickable">
                ${text}
            </label><br>`;
}
function writeJson(file, json) {
    try {
        fs.writeFileSync(file, JSON.stringify(json, undefined, 4));
    }
    catch (err) {
        vscode.window.showErrorMessage(err);
    }
}
class GetStarted {
    constructor(extensionPath) {
        this.json = new Map();
        this._file = vscode.Uri.file(path.join(extensionPath, GET_STARTED_JSON)).fsPath;
    }
    static createOrGet(extensionPath) {
        if (!GetStarted.instance) {
            GetStarted.instance = new GetStarted(extensionPath);
        }
        GetStarted.instance.read();
        return GetStarted.instance;
    }
    read() {
        var json = {};
        try {
            let json = JSON.parse(fs.readFileSync(this._file, 'utf8'));
            this.json = new Map(json);
        }
        catch (err) {
            if (err.code !== "ENOENT") {
                vscode.window.showErrorMessage(err);
                console.log(err);
            }
        }
    }
    list() {
        var list = "";
        for (let entry of this.json.entries()) {
            list += clickable(entry[1], GET_STARTED, entry[0]);
        }
        return list;
    }
    open(url) {
        require('openurl').open(url);
    }
}
class Recent {
    constructor(extensionPath) {
        this.list = [];
        this._file = vscode.Uri.file(path.join(extensionPath, RECENT_JSON)).fsPath;
    }
    static createOrGet(extensionPath) {
        if (!Recent.instance) {
            Recent.instance = new Recent(extensionPath);
        }
        Recent.instance.read();
        return Recent.instance;
    }
    read() {
        var list = [];
        try {
            list = JSON.parse(fs.readFileSync(this._file, 'utf8'));
        }
        catch (err) {
        }
        this.list = [];
        for (var i = 0; i < list.length; i++) {
            if (fs.existsSync(list[i]) && fs.lstatSync(list[i]).isDirectory()) {
                this.list.push(list[i]);
            }
        }
        if (list.length != this.list.length) {
            writeJson(this._file, this.list);
        }
    }
    recentList() {
        var recentList = "";
        this.list.forEach((recent) => {
            recentList += clickable(recent, RECENT, recent);
        });
        return recentList;
    }
    open(projectPath) {
        var openFolder = function () {
            return __awaiter(this, void 0, void 0, function* () {
                return yield vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(projectPath));
            });
        };
        // vscode.workspace.updateWorkspaceFolders(0, 0, {uri: fileUri[0]})
        openFolder();
    }
    add(projectPath) {
        this.list.push(projectPath);
        writeJson(this._file, this.list);
    }
}
vscode.workspace.onDidOpenTextDocument(() => {
    vscode.window.showInformationMessage("onDidOpenTextDocument");
});
//# sourceMappingURL=extension.js.map