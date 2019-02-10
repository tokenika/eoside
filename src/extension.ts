// https://code.visualstudio.com/docs
// https://code.visualstudio.com/docs/extensionAPI/extension-points
// https://code.visualstudio.com/docs/extensions/publish-extension
// https://code.visualstudio.com/docs/editor/extension-gallery#_install-from-a-vsix

// - Open this folder in VS Code 1.25+
// - `npm install`
// - `npm run watch` or `npm run compile`
// - `F5` to start debugging
// "terminal.integrated.shell.windows": "bash.exe"

import * as vscode from 'vscode'

import * as setup from './setup'
import InstallPanel from "./install"
import GetStartedPanel from "./getstarted"
import SetupPanel from "./setup"

export function activate(context: vscode.ExtensionContext) {
    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Install', () => {
            InstallPanel.createOrShow(context.extensionPath)
        }
    ))

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

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Compile', () => {
            setup.compile()
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Build', () => {
            setup.build()
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Deploy', () => {
            setup.deploy()
        }
    )) 

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.bash', () => {
            setup.bash()
        }
    ))
       
    GetStartedPanel.createOrShow(context.extensionPath)

}


