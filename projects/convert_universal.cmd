@ECHO OFF
chcp 65001 > nul

REM Проверка наличия Python
where python >nul 2>&1
if ERRORLEVEL 1 (
    echo [ERROR] Python не найден в PATH. Установите Python или добавьте его в PATH.
    exit /b 1
)

REM Получаем путь к Python скрипту (в той же папке где этот CMD)
set PYTHON_SCRIPT=%~dp0convert.py

REM Проверка наличия Python скрипта
if not exist "%PYTHON_SCRIPT%" (
    echo [ERROR] Python скрипт не найден: %PYTHON_SCRIPT%
    exit /b 1
)

REM Получаем абсолютный путь к папке проекта (первый параметр)
set PROJECT_PATH=%~f1

REM Проверка что передан параметр
if "%PROJECT_PATH%"=="" (
    echo [ERROR] Не указан путь к папке проекта
    echo Использование: convert_v2.cmd "путь_к_папке_проекта"
    exit /b 1
)

REM Проверка существования папки
if not exist "%PROJECT_PATH%" (
    echo [ERROR] Папка не существует: %PROJECT_PATH%
    exit /b 1
)

REM Вызов Python скрипта с передачей пути к папке проекта
python "%PYTHON_SCRIPT%" --env "%PROJECT_PATH%"

REM Возвращаем код возврата Python скрипта
exit /b %ERRORLEVEL%
