#!/bin/bash

printf "%s\n" "
###############################################################################
#   This script installs EOSIde. It needs to be executed from within 
#   the 'eoside' folder.
#   This file was downloaded from https://github.com/tokenika/eoside
###############################################################################
"

......................
......................

txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
txtrst=$(tput sgr0)
printf "${bldred}%s${txtrst}" '
         ______ ____   _____  _  _____   ______  
        |  ____/ __ \ / ____|| ||  __ \ |  ____| 
        | |__ | |  | | (___  | || |  | || |__
        |  __|| |  | |\___ \ | || |  | ||  __|
        | |___| |__| |____) || || |__| || |____ 
        |______\____/|_____/ |_||_____/ |______| 
                                                      
'
printf "%s\n" "
To verify installation navigate to the 'eoside' folder and execute 
'eoside.ps1'.

Alternatively, run 'code -n ""'.
"