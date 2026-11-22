@echo off
chcp 65001 > nul
title Sistema Farmacias Cruz Azul

:: Asegurar que el script se ejecute en la carpeta donde está guardado
cd /d "%~dp0"

set "VENV_DIR=Librerias"
set "SCRIPT_NAME=Login-menu.py"
set "REQ_FILE=requirements.txt"

echo ===================================================
echo        INICIANDO SISTEMA FARMACIAS CRUZ AZUL
echo ===================================================
echo.

:: 1. Verificar si existe el entorno virtual "librerías"
if not exist "%VENV_DIR%\Scripts\activate.bat" (
echo [1/3] Entorno virtual no encontrado. Creando "%VENV_DIR%"...
echo Por favor, espere a que las librerías terminen de instalarse...
python -m venv "%VENV_DIR%"

if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual. Verifica que Python este instalado y en el PATH.
    pause
    exit /b 1
)

echo [2/3] Activando entorno e instalando dependencias desde %REQ_FILE%...
call "%VENV_DIR%\Scripts\activate.bat"

if exist "%REQ_FILE%" (
    python -m pip install --upgrade pip
    pip install -r "%REQ_FILE%"
    if errorlevel 1 (
        echo [ERROR] Hubo un problema al instalar las librerias.
        pause
        exit /b 1
    )
) else (
    echo [ADVERTENCIA] No se encontro el archivo "%REQ_FILE%".
)
echo.
echo Instalacion completada con exito.
echo.


) else (
echo [1/2] Entorno virtual "%VENV_DIR%" detectado. Activando...
call "%VENV_DIR%\Scripts\activate.bat"
)

:: 2. Ejecutar el script principal de Python
echo [Ejecutando] Iniciando "%SCRIPT_NAME%"...
echo.
python "%SCRIPT_NAME%"

:: Si el programa se cierra por un error, pausar para poder leerlo
if errorlevel 1 (
echo.
echo [ERROR] El programa se cerro inesperadamente.
pause
)

deactivate