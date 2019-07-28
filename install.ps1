# Start Windows PowerShell with the "Run as administrator" option.
# set-executionpolicy remotesigned (A)
# https://eosfactory.io/eoside/html/_static/eoside-1.0.2.vsix


Write-Host "
# This script, downloaded from https://github.com/tokenika/eoside,
# installs EOSIDE, the Integrated Development Environment for EOSIO smart
contracts by Tokenika.
"

Write-Host "Checking the current directory ..."
$workingDirectory = Convert-Path (Resolve-Path -path ".")
If(![System.IO.File]::Exists("$workingDirectory\package.json")){
    Write-Host "
# It needs to be executed from within  the 'eoside' folder. This condition 
# seems unfulfilled as the command 'dir eoside\package.json' fails.
# 
"
}

$vsceVersion=$vsceVersion=npm list -g vsce
If ($vsceVersion -contains "(empty)"){
    npm install -g vsce
}

Remove-Item .\*.vsix
vsce package
$vsixFiles=Get-ChildItem .\*.vsix

# --install-extension (<extension-id> | <extension-vsix-path>)
#       Installs or updates the extension. 
#       Use `--force` argument to avoid prompts.
code --install-extension $vsixFiles[0]

Write-Host "
         ______   ____    _____  _  _____   ______  
        |  ____| / __ \  / ____|| ||  __ \ |  ____| 
        | |__   | |  | || (___  | || |  | || |__
        |  __|  | |  | | \___ \ | || |  | ||  __|
        | |___  | |__| | ____) || || |__| || |____ 
        |______| \____/ |_____/ |_||_____/ |______| 
                                                      
"

Write-Host "
To verify installation navigate to the 'eoside' folder and execute 
'eoside.ps1'.

# Alternatively, run 'code -n'.
# "