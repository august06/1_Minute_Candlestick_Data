@echo off
chcp 65001 > nul
echo =================================================================
echo   TỰ ĐỘNG GHÉP NẾN M1 TUẦN MỚI VA PUSH GITHUB
echo =================================================================
cd /d "%~dp0"
python merge_and_push.py
echo.
echo Hoan tat! Nhan phim bat ky de thoat...
pause > nul
