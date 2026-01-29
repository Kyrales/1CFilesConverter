@ECHO OFF
chcp 65001 > nul

REM Запуск GUI конвертера
python "%~dp0converter_gui.py"

pause
