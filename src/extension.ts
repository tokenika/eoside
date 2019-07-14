// https://code.visualstudio.com/docs
// https://code.visualstudio.com/docs/extensionAPI/extension-points
// https://code.visualstudio.com/docs/extensions/publish-extension
// https://code.visualstudio.com/docs/editor/extension-gallery#_install-from-a-vsix

// - Open this folder in VS Code 1.25+
// - `npm install`
// - `npm run watch` or `npm run compile`
// - `F5` to start debugging
// "terminal.integrated.shell.windows": "bash.exe"

// vsce create-publisher TOKENIKAPublisher human-friendly name: (TOKENIKA)
// E-mail: comtact@tokenika.ioPersonal Access Token: ****************************************************

// Successfully created publisher 'TOKENIKA'.

// vsce login TOKENIKA
// vsce publish

import * as path from 'path'
import * as fs from 'fs'
import * as vscode from 'vscode'

import * as setup from './setup'
import InstallPanel from "./install"
import GetStartedPanel from "./getstarted"
import SetupPanel from "./setup"
import ReleaseNotes from "./releasenotes"

export var extensionPath = ""

const RL_TRIGGER = ".releasenotes"

export function activate(context: vscode.ExtensionContext) {
    exports.extensionPath = context.extensionPath

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Install', () => {
            InstallPanel.createOrShow()
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.GetStarted', () => {
            GetStartedPanel.createOrShow(false)
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Setup', () => {
            SetupPanel.createOrShow()
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Compile', () => {
            setup.compile()
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.CompileTest', () => {
            setup.compile(true)
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Build', () => {
            setup.build()
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.BuildTest', () => {
            setup.build(true)
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

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.Zip', () => {
            setup.zip()
        }
    ))

    context.subscriptions.push(vscode.commands.registerCommand(
        'eoside.ReleaseNotes', () => {
            ReleaseNotes.createOrShow()
        }
    ))    

    
    InstallPanel.createOrShow(false)
    GetStartedPanel.createOrShow()

    var releaseFile = path.join(context.extensionPath, RL_TRIGGER)
    if(fs.existsSync(releaseFile) 
                && vscode.workspace.getConfiguration().eoside.showReleaseNotes){
        ReleaseNotes.createOrShow()
        
        try {
            fs.unlinkSync(releaseFile)
        } catch(err) {
        }
    }
}


