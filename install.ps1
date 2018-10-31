# Start Windows PowerShell with the "Run as administrator" option.
# set-executionpolicy remotesigned (A)


Write-Host "
###############################################################################
#   This script installs EOSIde. It needs to be executed from within 
#   the 'eoside' folder.
#   This file was downloaded from https://github.com/tokenika/eoside
###############################################################################
"

$ver=""
Try{
    $ver=$ver=(code -v)[0]
}
Catch{}

if(-Not $ver){
    Write-Host "
###############################################################################
# One prerequisite is that the Visual Studio Code is installed in the System
# with its 'code' binary is on the system path.
#
# The condition seems unfulfilled as the command 'code -v' does not return 
# any valid response.
#
# Exiting the installer...
###############################################################################
"
exit
}

$ubuntu=""
Try{
    $ubuntu=ubuntu run ubuntu run uname -a
}
Catch{}

if(-Not $ubuntu){
    Write-Host "
###############################################################################
# One prerequisite is that the WLS (Windows Linux Subsystem) is installed in 
# the System.
#
# The condition seems unfulfilled as the command 
# 'ubuntu run ubuntu run uname -a' does not return any valid response.
#
# Exiting the installer...
###############################################################################
"
exit
}




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

Write-Host "
         ______ ____   _____  _  _____   ______  
        |  ____/ __ \ / ____|| ||  __ \ |  ____| 
        | |__ | |  | | (___  | || |  | || |__
        |  __|| |  | |\___ \ | || |  | ||  __|
        | |___| |__| |____) || || |__| || |____ 
        |______\____/|_____/ |_||_____/ |______| 
                                                      
"

Write-Host "
To verify installation navigate to the 'eoside' folder and execute 
'eoside.ps1'.

# Alternatively, run 'code -n ""'.
# "