# utils/validator.py
# Funciones para validar el entorno y las dependencias.

def check_dependencies():
    """
    Verifica que las librerías esenciales estén instaladas.

    Returns:
        bool: True si todas las dependencias están presentes, False en caso contrario.
    """
    try:
        import cv2
        import numpy
        import yaml
        return True
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrate de tener instaladas las librerías 'opencv-python', 'numpy' y 'PyYAML'.")
        print("Puedes instalarlas con: pip install opencv-python numpy pyyaml")
        return False
