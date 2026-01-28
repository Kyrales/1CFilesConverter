@ECHO OFF
chcp 1251 > nul

REM Проверка наличия Python
where python >nul 2>&1
if ERRORLEVEL 1 (
    echo [ERROR] Python не найден в PATH. Установите Python или добавьте его в PATH.
    exit /b 1
)

REM Получаем путь к Python скрипту
set PYTHON_SCRIPT=%~dp0convert.py

REM Проверка наличия Python скрипта
if not exist "%PYTHON_SCRIPT%" (
    echo [ERROR] Python скрипт не найден: %PYTHON_SCRIPT%
    exit /b 1
)

REM Вызов Python скрипта с передачей всех параметров
python "%PYTHON_SCRIPT%"

REM Возвращаем код возврата Python скрипта
exit /b %ERRORLEVEL%
