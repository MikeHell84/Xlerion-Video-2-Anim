@echo off
TITLE Xlerion - Video 2 Anim Launcher

ECHO ======================================================
ECHO  Lanzador de Xlerion - Video 2 Anim
ECHO ======================================================
ECHO.
ECHO Activando el entorno de Conda 'mocap_env'...
ECHO Por favor, espera...
ECHO.
CALL conda activate mocap_env

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

:: Run the GUI script
python gui_app.py

:: When you close the GUI, the script will terminate and the window will close automatically.
EXIT /B
