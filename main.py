# main.py
# Punto de entrada principal para la aplicación de captura de movimiento.

import argparse
import os
from utils.config_loader import load_config
from utils.logger import setup_logger
from utils.validator import check_dependencies
from pipelines.real_time_pipeline import run_real_time
from pipelines.test_pipeline import run_test_pipeline
# Importamos el nuevo pipeline
from pipelines.video_file_pipeline import run_video_file

def main():
    """
    Función principal que inicializa y ejecuta el pipeline seleccionado.
    """
    # --- Verificación de Dependencias ---
    print("Verificando dependencias...")
    if not check_dependencies():
        print("Error: Faltan dependencias clave. Por favor, instala OpenCV, NumPy y PyYAML.")
        return
    print("Dependencias verificadas correctamente.")

    # --- Configuración de Argumentos ---
    parser = argparse.ArgumentParser(description="Sistema de Captura de Movimiento.")
    parser.add_argument(
        '--mode',
        type=str,
        choices=['realtime', 'test', 'video'], # Añadimos el nuevo modo 'video'
        default='realtime',
        help="Modo de ejecución: 'realtime' para webcam, 'test' para imágenes, 'video' para un archivo de video."
    )
    parser.add_argument(
        '--config',
        type=str,
        default='configs/default_config.yaml',
        help="Ruta al archivo de configuración YAML."
    )
    # Nuevo argumento para la ruta del video
    parser.add_argument(
        '--filepath',
        type=str,
        default=None,
        help="Ruta al archivo de video para usar en modo 'video'."
    )
    args = parser.parse_args()

    # --- Carga de Configuración ---
    if not os.path.exists(args.config):
        print(f"Error: El archivo de configuración no se encuentra en '{args.config}'")
        return
    config = load_config(args.config)

    # --- Configuración del Logger ---
    logger = setup_logger(config['logging'])

    logger.info(f"Aplicación iniciada en modo: {args.mode}")
    logger.info(f"Configuración cargada desde: {args.config}")

    # --- Ejecución del Pipeline ---
    try:
        if args.mode == 'realtime':
            run_real_time(config)
        elif args.mode == 'test':
            run_test_pipeline(config)
        elif args.mode == 'video':
            if not args.filepath:
                print("Error: Debes proporcionar la ruta a un video con el argumento --filepath en modo 'video'.")
                logger.error("Intento de ejecución en modo video sin proporcionar --filepath.")
                return
            if not os.path.exists(args.filepath):
                print(f"Error: El archivo de video no se encuentra en '{args.filepath}'")
                return
            run_video_file(config, args.filepath)

    except Exception as e:
        logger.error(f"Se ha producido un error fatal en el pipeline: {e}", exc_info=True)
    finally:
        logger.info("La aplicación ha finalizado.")

if __name__ == "__main__":
    main()
