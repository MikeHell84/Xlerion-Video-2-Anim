# pipelines/real_time_pipeline.py
# Flujo de trabajo completo para la detección de movimiento en tiempo real.

import cv2
from core.video_capture import VideoCapture
from core.motion_detection import MotionDetector
from core.region_tracking import get_bounding_boxes
from core.overlay_visuals import draw_bounding_boxes, draw_hud

def run_real_time(config):
    """
    Ejecuta el pipeline de captura y detección en tiempo real.

    Args:
        config (dict): Diccionario de configuración de la aplicación.
    """
    # --- Inicialización ---
    try:
        camera = VideoCapture(config['video_capture']['source_index'])
    except IOError as e:
        print(f"Error al inicializar la cámara: {e}")
        return

    detector = MotionDetector(config['motion_detection'])
    hud_config = config['overlay_visuals']['hud']
    
    print("Pipeline en tiempo real iniciado. Presiona 'q' para salir.")

    # --- Bucle Principal ---
    while True:
        ret, frame = camera.get_frame()
        if not ret:
            print("No se pudo obtener el frame de la cámara. Saliendo...")
            break

        # 1. Detección de movimiento
        contours = detector.detect(frame)

        # 2. Seguimiento de regiones (bounding boxes)
        bounding_boxes = get_bounding_boxes(contours)

        # 3. Visualización
        draw_bounding_boxes(frame, bounding_boxes, color=(0, 255, 0))
        draw_hud(frame, len(bounding_boxes), hud_config)

        # Mostrar el resultado
        cv2.imshow('Motion Capture - Real Time', frame)

        # Condición de salida
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- Limpieza ---
    camera.release()
    cv2.destroyAllWindows()
    print("Pipeline en tiempo real finalizado.")
