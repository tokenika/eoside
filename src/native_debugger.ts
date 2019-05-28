import * as path from 'path'
import * as vscode from 'vscode'
import * as fs from 'fs'
import * as def from './definitions'
import * as inst from './install'

export function createEosideLaunchConfig(c_cpp_properties:any){
    const DEBUGGER_PATH = "/usr/bin/gdb"
    const MI_DEBUGGER_PATH = "/usr/bin/gdb"
    const BUILD = "build"
    const CONFIG_NAME = "eoside_native"

    try{
        if(!vscode.workspace.workspaceFolders){
            return
        }
        var workspace = vscode.workspace.workspaceFolders[0].uri.fsPath
        var testOptions = c_cpp_properties["configurations"][0]["testOptions"]
    } catch(err){
        return
    }

    for(let option in testOptions){
        let o = "-o"
        var program = null
        if(testOptions[option].indexOf(o) != -1){
            program = testOptions[option].replace(o, "").trim()
            if(!path.isAbsolute(program)){
                program = inst.wslMapWindowsLinux(
                                        path.join(workspace, BUILD, program))
            }
            break
        }
    }

    var cwd = inst.wslMapWindowsLinux(path.join(workspace, BUILD))
    var launchPath = path.join(workspace, ".vscode", "launch.json")

    if(!fs.existsSync(launchPath)){
        try{
            fs.writeFileSync(launchPath, `
{
    "version": "0.2.0",
    "configurations": [
        ]
}
        `)
        } catch(err){
            vscode.window.showErrorMessage(
`Cannot write file. The path tried is
${launchPath}.
Error message is
${err}`)
            return -1
        }
    }

    try {
        var launchJson = JSON.parse(
                    fs.readFileSync(launchPath, 'utf8'))
    } catch(err){
        vscode.window.showErrorMessage(
`Cannot read file. The path tried is
${launchPath}.
Error message is
            ${err}`)
            return -1               
    }

    var configEoside = 
    {
        "name": CONFIG_NAME,
        "type": "cppdbg",
        "request": "launch",
        "stopAtEntry": true,
        "environment": [],
        "MIMode": "gdb",
        "setupCommands": [
            {
                "description": "Enable pretty-printing for gdb",
                "text": "-enable-pretty-printing",
                "ignoreFailures": true
            }
        ],
        "miDebuggerPath": MI_DEBUGGER_PATH,
        "miDebuggerArgs": "-quiet",
        "program": program,
        "args": [],
        "cwd": cwd,
        ...(def.IS_WINDOWS ? {
            "externalConsole": true,
            "pipeTransport": {
                "pipeCwd": "",
                "pipeProgram": "c:\\windows\\sysnative\\bash.exe",
                "pipeArgs": [
                    "-c"
                ],
                "debuggerPath": DEBUGGER_PATH
            },
            "sourceFileMap": {
                "/mnt/c": "\${env:systemdrive}/",
                "/usr": inst.root().replace(/\//gi, "\\") + "\\usr\\"
        }}: {
            "externalConsole": false,
        })        
    }
    
    for(let index in launchJson["configurations"]){
        if(launchJson["configurations"][index]["name"] == CONFIG_NAME){
            launchJson["configurations"][index] = configEoside
            inst.writeJson(launchPath, launchJson)
            return 0
        }
    }

    launchJson["configurations"][launchJson["configurations"].length] 
                                                                = configEoside
    inst.writeJson(launchPath, launchJson)
    return 0
}

