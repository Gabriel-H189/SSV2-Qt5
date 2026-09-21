!include "MUI.nsh"

OutFile "SSV2-Qt5_Setup.exe"
Name "Seagull Scaring V2 (Qt Edition)"
InstallDir $ProgramFiles64\SSV2-Qt5
BrandingText "Gabriel Alonso-Holt"

; Images
!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "wizard.bmp"
!define MUI_ICON "setup.ico"

!define MUI_WELCOMEPAGE_TEXT "Setup will guide you through the installation process of Seagull Scaring V2 (Qt Edition).\n\nYou should close all other applications before continuing.\n\nClick Next to continue and Cancel to exit the Setup Wizard."

Function LaunchLink
	ExecShell "" "$SMPROGRAMS\SeagullScaringV2 (Qt Edition).lnk"
FunctionEnd

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.rtf"
!define MUI_LICENSEPAGE_CHECKBOX

!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!define MUI_ABORTWARNING

!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_NOTCHECKED
!define MUI_FINISHPAGE_RUN_TEXT "Start Seagull Scaring V2 (Qt Edition)"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"

!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_LICENSE "license.rtf"
!insertmacro MUI_UNPAGE_DIRECTORY
!insertmacro MUI_UNPAGE_INSTFILES
!define MUI_UNFINISHPAGE_NOAUTOCLOSE
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Main program"

	SetOutPath $INSTDIR

	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5" "DisplayName" "Seagull Scaring V2 (Qt Edition)"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5" "DisplayVersion" "2.1.2"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5" "Publisher" "Gabriel Alonso-Holt"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5" "DisplayIcon" "$INSTDIR\seagull.ico"
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5" "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5" "NoRepair" 1
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5" "UninstallString" "$INSTDIR\uninstall.exe"

	File SSV2-Qt5.exe
	File ssv2cfg.ini
	File seagull.png
	File seagull.ico
	File ssv2_log.txt
	File config_docs.txt
	File readme.txt
	File License.rtf

	CreateShortcut "$SMPROGRAMS\SeagullScaringV2 (Qt Edition).lnk" "$INSTDIR\SSV2-Qt5.exe"

	WriteUninstaller $INSTDIR\uninstall.exe

SectionEnd

Section "Gabriel's Seagull Sound Pack"

	File /r media

SectionEnd

Section "Desktop shortcut"

	CreateShortcut "$DESKTOP\SeagullScaringV2 (Qt Edition).lnk" "$INSTDIR\SSV2-Qt5.exe"

SectionEnd

Section "Uninstall"

	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SSV2-Qt5"

	Delete $INSTDIR\SSV2-Qt5.exe
	Delete $INSTDIR\ssv2cfg.ini
	Delete $INSTDIR\seagull.png
	Delete $INSTDIR\seagull.ico
	Delete $INSTDIR\ssv2_log.txt
	Delete $INSTDIR\config_docs.txt
	Delete $INSTDIR\License.rtf
	Delete $INSTDIR\Readme.txt
	Delete $INSTDIR\media\seagull.wav
	Delete $INSTDIR\media\alarm_seagull.wav
	Delete $INSTDIR\media\confused_seagull.wav
	Delete $INSTDIR\media\sad_seagull.wav
	Delete $INSTDIR\media\disgust_seagull.wav
	Delete $INSTDIR\media\Seagull_2.wav
	Delete $INSTDIR\media\sea_gull.wav
	Delete $INSTDIR\media\robot_seagull.wav
	Delete "$DESKTOP\SeagullScaringV2 (Qt Edition).lnk"
	Delete "$SMPROGRAMS\SeagullScaringV2 (Qt Edition).lnk"
	RMDir /r $INSTDIR\media

	Delete $INSTDIR\uninstall.exe
	RMDir $INSTDIR

SectionEnd