import * as path from 'path'
import * as fs from 'fs'
import * as vscode from 'vscode'
import * as def from './definitions'


export default class ReleaseNotes extends def.Panel {
    /**
     * Track the currently panel. Only allow a single panel to exist at a time.
     */
    public static currentPanel: ReleaseNotes | undefined
    public static readonly viewType = "ReleaseNotes"

    
    public static createOrShow() {

        const column = vscode.window.activeTextEditor 
            ? vscode.window.activeTextEditor.viewColumn : undefined

        // If we already have a panel, show it.
        if (ReleaseNotes.currentPanel) {
            ReleaseNotes.currentPanel._panel.reveal(column)
        } else {
            // Otherwise, create a new panel.
            const panel = vscode.window.createWebviewPanel(
                    ReleaseNotes.viewType, "ReleaseNotes", 
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
            ReleaseNotes.currentPanel = new ReleaseNotes(panel)
        }
    }


    protected constructor(panel: vscode.WebviewPanel) {
        super(panel)
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
        ReleaseNotes.currentPanel = undefined
    }


    private _getHtmlForWebview() {
        var version = ''
        var packageFile = JSON.parse(fs.readFileSync(
                        path.join(def.getExtensionPath(), "package.json"), 'utf8'))
        if (packageFile) {
            version = packageFile.version
        }
        const htmlBase = vscode.Uri.file(path.join(
            def.getExtensionPath(), def.RESOURCE_DIR, '/')).with({scheme: 'vscode-resource'})
    
        var html = fs.readFileSync(
                    path.join(def.getExtensionPath(), "media", "releasenotes.html")).toString()
        return html.replace("${version}", version)
                    .replace("${nonce", def.getNonce())
                    .replace("htmlBase", htmlBase.toString())
    }
}
