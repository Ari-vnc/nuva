@echo off
REM Script de Windows para configurar Cloud CDN
REM Este script ejecuta el setup-cdn.sh usando Git Bash

echo ========================================
echo Configuracion de Cloud CDN
echo ========================================
echo.

REM Verificar si Git Bash está instalado
where bash >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git Bash no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Git Bash desde: https://git-scm.com/download/win
    echo O ejecuta manualmente: bash setup-cdn.sh
    pause
    exit /b 1
)

echo Ejecutando script de configuracion...
echo.

bash setup-cdn.sh

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Configuracion completada exitosamente!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Error durante la configuracion
    echo ========================================
)

echo.
pause
