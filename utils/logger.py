# utils/logger.py
# Módulo para configurar un logging estructurado en formato JSON.

import logging
import logging.config
import json
import os
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    Formateador personalizado para logs en formato JSON.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.name,
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logger(config):
    """
    Configura y devuelve un logger basado en la configuración proporcionada.

    Args:
        config (dict): Diccionario de configuración para el logging.

    Returns:
        logging.Logger: Una instancia del logger configurado.
    """
    log_dir = config.get('directory', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file_name = config.get('file_name', f"{datetime.now().strftime('%Y%m%d')}_events.json")
    log_path = os.path.join(log_dir, log_file_name)

    logger = logging.getLogger(config.get('logger_name', 'MotionCaptureApp'))
    logger.setLevel(config.get('level', 'INFO').upper())

    # Evitar añadir manejadores duplicados
    if not logger.handlers:
        # Manejador para archivo
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)

        # Manejador para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)

    return logger
