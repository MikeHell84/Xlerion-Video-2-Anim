# pipelines/test_pipeline.py
# Flujo de trabajo para pruebas usando imágenes estáticas en lugar de video en vivo.

import cv2
import os
import time
from core.motion_detection import MotionDetector
from core.region_tracking import get_bounding_boxes
from core.overlay_visuals import draw_bounding_boxes, draw_hud

def run_test_pipeline(config):
    """
    Ejecuta el pipeline de detección usando imágenes de un directorio.

    Args:
        config (dict): Diccionario de configuración de la aplicación.
    """
    # --- Inicialización ---
    test_frames_dir = config['test_pipeline']['frames_directory']
    if not os.path.isdir(test_frames_dir):
        print(f"Error: El directorio de frames de prueba '{test_frames_dir}' no existe.")
        return

    image_files = sorted([
        os.path.join(test_frames_dir, f) for f in os.listdir(test_frames_dir)
        if f.endswith(('.png', '.jpg', '.jpeg'))
    ])

    if not image_files:
        print(f"No se encontraron imágenes en '{test_frames_dir}'.")
        return

    detector = MotionDetector(config['motion_detection'])
    hud_config = config['overlay_visuals']['hud']
    hud_config['status_text'] = 'TEST MODE' # Sobrescribir estado para el HUD

    print(f"Pipeline de prueba iniciado. Procesando {len(image_files)} frames. Presiona 'q' para salir.")

    # --- Bucle de Procesamiento ---
    for image_path in image_files:
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"No se pudo leer la imagen: {image_path}")
            continue

        # 1. Detección de movimiento
        contours = detector.detect(frame)

        # 2. Seguimiento de regiones
        bounding_boxes = get_bounding_boxes(contours)

        # 3. Visualización
        draw_bounding_boxes(frame, bounding_boxes, color=(255, 0, 0))
        draw_hud(frame, len(bounding_boxes), hud_config)

        # Mostrar el resultado
        cv2.imshow('Motion Capture - Test Mode', frame)

        # Pausa para simular un video y permitir la visualización
        if cv2.waitKey(config['test_pipeline']['delay_ms']) & 0xFF == ord('q'):
            break

    # --- Limpieza ---
    cv2.destroyAllWindows()
    print("Pipeline de prueba finalizado.")
