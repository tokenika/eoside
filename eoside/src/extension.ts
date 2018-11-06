// https://code.visualstudio.com/docs
// https://code.visualstudio.com/docs/extensionAPI/extension-points
// https://code.visualstudio.com/docs/extensions/publish-extension
// https://code.visualstudio.com/docs/editor/extension-gallery#_install-from-a-vsix

// - Open this folder in VS Code 1.25+
// - `npm install`
// - `npm run watch` or `npm run compile`
// - `F5` to start debugging

import * as path from 'path'
import * as vscode from 'vscode'
import fs = require('fs')

import * as def from './definitions'
import GetStartedPanel from "./getstarted"
import SetupPanel from "./setup"

export function activate(context: vscode.ExtensionContext) {

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.EOSIde', () => {
            GetStartedPanel.createOrShow(context.extensionPath, false)
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Setup', () => {
            SetupPanel.createOrShow(context.extensionPath)
        }
    ))    

    GetStartedPanel.createOrShow(context.extensionPath)
    // if(def.IS_WINDOWS){
    //     vscode.workspace.getConfiguration().update(
    //         "terminal.integrated.shell.windows", "bash.exe", true)        
    // }    

}


