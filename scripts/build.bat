@echo off
cd ..
IF EXIST build.spec pyinstaller --onefile build.spec

pause
exit