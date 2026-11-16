@echo off
chcp 65001 > nul
echo =================================================================
echo   TỰ ĐỘNG GHÉP NẾN M1 TUẦN MỚI VÀ PUSH GITHUB
echo =================================================================
cd /d "%~dp0"
if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    "%LOCALAPPDATA%\Python\bin\python.exe" merge_and_push.py
) else if exist "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe" (
    "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe" merge_and_push.py
) else (
    python merge_and_push.py
)
echo.
echo Hoàn tất! Nhấn phím bất kỳ để thoát...
pause > nul
