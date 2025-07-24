# core/overlay_visuals.py
# Funciones para renderizar información visual sobre los frames.

import cv2
import datetime

def draw_bounding_boxes(frame, bounding_boxes, color=(0, 255, 0), thickness=2):
    """
    Dibuja bounding boxes en un frame.

    Args:
        frame (numpy.ndarray): El frame sobre el cual dibujar.
        bounding_boxes (list): Lista de bounding boxes (x, y, w, h).
        color (tuple): Color del recuadro en BGR.
        thickness (int): Grosor de la línea.
    """
    for (x, y, w, h) in bounding_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

def draw_hud(frame, num_objects, config):
    """
    Dibuja un Head-Up Display (HUD) con información relevante.

    Args:
        frame (numpy.ndarray): El frame sobre el cual dibujar.
        num_objects (int): Número de objetos detectados.
        config (dict): Diccionario de configuración para el HUD.
    """
    if not config.get('enabled', True):
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = config.get('font_scale', 0.7)
    color = tuple(config.get('color', [255, 255, 255]))
    thickness = config.get('thickness', 1)
    
    # Información de estado
    status_text = f"Status: {config.get('status_text', 'LIVE')}"
    cv2.putText(frame, status_text, (10, 30), font, font_scale, color, thickness)

    # Contador de objetos
    objects_text = f"Objetos detectados: {num_objects}"
    cv2.putText(frame, objects_text, (10, 60), font, font_scale, color, thickness)
    
    # Fecha y hora
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), font, 0.5, color, thickness)
