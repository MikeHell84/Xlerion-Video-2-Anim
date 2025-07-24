@echo off
TITLE Xlerion - Video 2 Anim Launcher

ECHO ======================================================
ECHO  Lanzador de Xlerion - Video 2 Anim
ECHO ======================================================
ECHO.
ECHO Activando el entorno de Conda 'mocap_env'...
ECHO Por favor, espera...
ECHO.

:: Llama al script de activación de Conda. Esto asume que 'conda init' ya se ha ejecutado.
CALL conda activate mocap_env

:: Comprueba si la activación del entorno fue exitosa.
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO *******************************************************************
    ECHO  ERROR: No se pudo activar el entorno 'mocap_env'.
    ECHO  Asegurate de que Miniconda/Anaconda esta instalado y que
    ECHO  el entorno 'mocap_env' fue creado correctamente.
    ECHO *******************************************************************
    ECHO.
    PAUSE
    EXIT /B
)

ECHO Entorno activado correctamente.
ECHO Iniciando la aplicacion grafica...
ECHO.

:: Ejecuta el script de la interfaz gráfica
python gui_app.py

:: Al cerrar la GUI, el script terminará y la ventana se cerrará automáticamente.
EXIT /B