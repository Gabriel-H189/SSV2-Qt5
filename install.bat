@echo off
color 7
title Seagull Scaring V2 installer
cls

echo ---------------------------------------------------------------------------------------------------------
echo                                        =-.                                      
echo                                       .+:=.                                     
echo                                      .=. .-:                                    
echo                                     .+.    -:                                   
echo                                     +.      =:                                  
echo                                  ..-+::::---:+::::::..                          
echo                   ..:-::-:-:::::::....   .         .::-::::-:--::::.            
echo .......:::::::-=:-::.      :                                     ..:---.        
echo ==-::::..     +        =.      :=                                     .=.       
echo   .:-:::::::::=+-..    .-::::::-                                       -:       
echo                 .-==--::..                                            .+.       
echo                        .::::::=::::::...                       .   .:--.        
echo                              :=    .+-:::::::*:::::::::::::::::+:::-.           
echo                              +.     .--.   .=:                 =                
echo                             .+        .=. .+.                  =.               
echo                             :-         .+.=.                   .+               
echo                    :::::::::--          .++                     +               
echo                            .:.                        .-:::::::::			Seagull Scaring V2 installer
echo																			By Gabriel Alonso-Holt
echo --------------------------------------------------------------------------------------------------------

set /p choice="Do you want to install Seagull Scaring V2? (y/n)"
if %choice% == y goto install
if %choice% == n goto quit

:install
if not exist .venv (

	echo Venv does not exist, creating and activating .venv
	python -m venv .venv
	.venv\Scripts\activate.bat
	echo Success
	
)

if not exist media echo Sounds not present!

echo Installing dependencies...
pip install -r requirements.txt

echo Installation complete.

set /p choice2="Run Seagull Scaring V2? (y/n) "

if %choice2% == y goto run
if %choice2% == n goto quit2

:run
echo Running Seagull Scaring V2...
python main.pyw

:quit
echo Installation cancelled.
exit /b

:quit2
echo Installation complete.
exit /b