# utils/diagnostics.py
# Scripts para pruebas offline y simulaciones.

import cv2

def check_camera_connection(max_cameras_to_check=5):
    """
    Verifica la conexión de las cámaras disponibles.

    Args:
        max_cameras_to_check (int): Número máximo de índices de cámara a probar.

    Returns:
        list: Una lista de índices de cámaras que se pudieron abrir correctamente.
    """
    available_cameras = []
    print("Iniciando diagnóstico de cámaras...")
    for i in range(max_cameras_to_check):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Cámara en índice {i} está disponible.")
            available_cameras.append(i)
            cap.release()
        else:
            print(f"No se encontró cámara en el índice {i}.")
    
    if not available_cameras:
        print("Diagnóstico finalizado: No se encontraron cámaras funcionales.")
    else:
        print(f"Diagnóstico finalizado: Cámaras disponibles en índices: {available_cameras}")
        
    return available_cameras

if __name__ == '__main__':
    # Este script se puede ejecutar directamente para un diagnóstico rápido.
    check_camera_connection()
