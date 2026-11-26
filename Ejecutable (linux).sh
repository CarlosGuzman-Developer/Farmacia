#!/bin/bash

# Cambiar el título de la ventana de terminal (funciona en la mayoría de emuladores de terminal)
echo -ne "\033]0;Sistema Farmacias Cruz Azul\007"

# Asegurar que el script se ejecute en la carpeta donde está guardado
cd "$(dirname "$0")" || exit 1

VENV_DIR="Librerias"
SCRIPT_NAME="Login-menu.py"
REQ_FILE="requirements.txt"

# Función equivalente a 'pause' de Windows
pausar() {
    read -n 1 -s -r -p "Presiona cualquier tecla para continuar..."
    echo ""
}

echo "==================================================="
echo "       INICIANDO SISTEMA FARMACIAS CRUZ AZUL"
echo "==================================================="
echo ""

# 1. Verificar si existe el entorno virtual "Librerias"
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "[1/3] Entorno virtual no encontrado. Creando \"$VENV_DIR\"..."
    echo "Por favor, espere a que las librerías terminen de instalarse..."
    
    # En Linux se usa habitualmente python3
    python3 -m venv "$VENV_DIR"

    if [ $? -ne 0 ]; then
        echo "[ERROR] No se pudo crear el entorno virtual. Verifica que python3 y python3-venv estén instalados."
        pausar
        exit 1
    fi

    echo "[2/3] Activando entorno e instalando dependencias desde $REQ_FILE..."
    source "$VENV_DIR/bin/activate"

    if [ -f "$REQ_FILE" ]; then
        python -m pip install --upgrade pip
        pip install -r "$REQ_FILE"
        if [ $? -ne 0 ]; then
            echo "[ERROR] Hubo un problema al instalar las librerías."
            pausar
            exit 1
        fi
    else
        echo "[ADVERTENCIA] No se encontró el archivo \"$REQ_FILE\"."
    fi
    echo ""
    echo "Instalación completada con éxito."
    echo ""
else
    echo "[1/2] Entorno virtual \"$VENV_DIR\" detectado. Activando..."
    source "$VENV_DIR/bin/activate"
fi

# 2. Ejecutar el script principal de Python
echo "[Ejecutando] Iniciando \"$SCRIPT_NAME\"..."
echo ""
python "$SCRIPT_NAME"

# Si el programa se cierra por un error, pausar para poder leerlo
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] El programa se cerró inesperadamente."
    pausar
fi

deactivate