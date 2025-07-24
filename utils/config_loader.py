# utils/config_loader.py
# Módulo para cargar y validar archivos de configuración.

import yaml

def load_config(path):
    """
    Carga un archivo de configuración YAML.

    Args:
        path (str): La ruta al archivo YAML.

    Returns:
        dict: Un diccionario con los parámetros de configuración.
    """
    try:
        # --- CORRECCIÓN AQUÍ ---
        # Se añade encoding='utf-8' para asegurar la correcta lectura de caracteres especiales.
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"Configuración cargada exitosamente desde '{path}'.")
        return config
    except FileNotFoundError:
        print(f"Error: El archivo de configuración en '{path}' no fue encontrado.")
        raise
    except yaml.YAMLError as e:
        print(f"Error al parsear el archivo YAML: {e}")
        raise
