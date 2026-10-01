# build.ps1
param(
	[switch]$install
    ,[switch]$clean
)

if ($clean) {
    Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
    Remove-Item -Force SSV2-Qt5.spec, SSV2-Qt5.exe, SSV2-Qt5_Setup.exe -ErrorAction SilentlyContinue
    return
}

pyinstaller --onefile main_qt5.py -i seagull.ico -n SSV2-Qt5 --add-data="ssv2cfg.ini:." --add-data="seagull.png:." --noconsole
move-item -force -Path dist\SSV2-Qt5.exe -destination .\SSV2-Qt5.exe

if ($install) {
	makensis SSV2-Qt5.nsi /launch
}
