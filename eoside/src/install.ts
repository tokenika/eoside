import * as path from 'path'
import * as vscode from 'vscode'

import * as def from './definitions'


export default class InstallPanel extends def.Panel {
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: InstallPanel | undefined
    public static readonly viewType = "EOS IDE"

    public static createOrShow(extensionPath: string) {
        if(def.IS_WINDOWS && (!def.config || !def.root())){
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
                InstallPanel.viewType, "EOS IDE", 
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
            }
        }, null, this._disposables)
    }

    public dispose() {
        super.dispose()
        InstallPanel.currentPanel = undefined
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

        var html = require('fs').readFileSync(htmlUri.fsPath).toString()
                                .replace(/\$\{nonce\}/gi, def.getNonce())
                                .replace(/\$\{scriptUri\}/gi, scriptUri)
        return html
    }
}
