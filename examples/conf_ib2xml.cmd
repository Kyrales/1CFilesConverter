@ECHO OFF

SETLOCAL ENABLEDELAYEDEXPANSION

echo START: %date% %time%

chcp 65001 > nul

set RELATIVE_REPO_PATH=%~dp0..\..
set RELATIVE_SRC_PATH=src
set RELATIVE_SRC_CF_PATH=cf
set RELATIVE_SRC_CFE_PATH=cfe

FOR /F "usebackq tokens=1 delims=" %%i IN (`FORFILES /P "%RELATIVE_REPO_PATH%" /M "%RELATIVE_SRC_PATH%" /C "cmd /c echo @path"`) DO set SRC_PATH=%%i
IF not defined SRC_PATH (
    echo [ERROR] Path to source files "%RELATIVE_REPO_PATH%\%RELATIVE_SRC_PATH%" not found
    exit /b 1
)
set SRC_PATH=%SRC_PATH:"=%
set REPO_PATH=%SRC_PATH%
FOR /L %%i IN (1, 1, 10) DO (
    set REPO_PATH=!REPO_PATH:~0,-1!
    IF "!REPO_PATH:~-1,1!" equ "\" (
        set REPO_PATH=!REPO_PATH:~0,-1!
        goto script
    )
)
:script

IF exist "%REPO_PATH%\.env" (
    FOR /F "usebackq tokens=*" %%a in ("%REPO_PATH%\.env") DO (
        FOR /F "tokens=1,2 delims==" %%b IN ("%%a") DO (
            set "%%b=%%c"
        )
    )
)

FOR /F "usebackq tokens=1 delims=" %%i IN (`FORFILES /P "%SRC_PATH%" /M "%RELATIVE_SRC_CF_PATH%" /C "cmd /c echo @path"`) DO (
    set CONF_PATH=%%i
    set CONF_PATH=!CONF_PATH:"=!
    echo [INFO] Found main configuration folder "!CONF_PATH!"
)

IF exist "%V8_DST_PATH%" IF "%V8_CONF_XML_CLEAN_DST%" equ "1" (
    del /f /s /q "%V8_DST_PATH%\*.*" > nul
    rd /S /Q "%V8_DST_PATH%"
    set V8_CONF_XML_CLEAN_DST=0
)

IF defined V8_EXPORT_TOOL set V8_CONVERT_TOOL=%V8_EXPORT_TOOL%

set V8_CONNECTION_STRING=/S%V8_DB_SRV_ADDR%\%V8_IB_NAME%
IF /i "%V8_CONVERT_TOOL%" equ "designer" set V8_CONNECTION_STRING=/S%V8_SRV_ADDR%\%V8_IB_NAME%

echo.
echo ======
echo Export main configuration
echo ======

call %REPO_PATH%\tools\1CFilesConverter\scripts\conf2xml.cmd "%V8_CONNECTION_STRING%" "%CONF_PATH%"

if exist "%REPO_PATH%\.git" (
    set "GIT_COMMAND=git status --short -- "%CONF_PATH%""
    FOR /f "tokens=1,2 delims= " %%a in (' "!GIT_COMMAND!" ') do (
        IF "%%a" equ "D" (
            set PATH_TO_RESTORE=%%b
            set PATH_TO_RESTORE=!PATH_TO_RESTORE:/=\!
            set RESTORE_FILE=0
            FOR %%i IN (%V8_FILES_TO_KEEP%) DO IF "!PATH_TO_RESTORE!" equ "%RELATIVE_SRC_PATH%\%RELATIVE_SRC_CF_PATH%\%%i" set RESTORE_FILE=1
            IF "!RESTORE_FILE!" equ "1" git checkout HEAD "!PATH_TO_RESTORE!" > nul 2>&1
        )
    )
)

IF exist "%CONF_PATH%\ConfigDumpInfo.xml" del /Q /F "%CONF_PATH%\ConfigDumpInfo.xml"

echo FINISH: %date% %time%