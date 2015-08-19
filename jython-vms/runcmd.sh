#!/bin/zsh
scrPath="jython E:\sikulix-scripts\gmail_reg.sikuli\gmail_reg.py"
vboxmanage guestcontrol "win7-2 Clone" exec --image "cmd.exe" --environment "EMAIL=SOMEEMAIL@DOMAIN.com" --verbose --wait-stdout --wait-stderr --username User --password Passowrd01 -- /c $scrPath  
