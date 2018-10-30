# Start Windows PowerShell with the "Run as administrator" option.
# set-executionpolicy remotesigned (A)


Write-Host "
###############################################################################
#   This script installs EOSIde. It needs to be executed from within 
#   the 'eoside' folder.
#   This file was downloaded from https://github.com/tokenika/eoside
###############################################################################
"

cd .\eoside\

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

cd ..

Write-Host '
         ______ ____   _____  _  _____   ______  
        |  ____/ __ \ / ____|| ||  __ \ |  ____| 
        | |__ | |  | | (___  | || |  | || |__
        |  __|| |  | |\___ \ | || |  | ||  __|
        | |___| |__| |____) || || |__| || |____ 
        |______\____/|_____/ |_||_____/ |______| 
                                                      
'