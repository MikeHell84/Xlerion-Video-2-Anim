# core/region_tracking.py
# Funciones para procesar regiones de movimiento, como bounding boxes.

import cv2

def get_bounding_boxes(contours):
    """
    Calcula los bounding boxes para una lista de contornos.

    Args:
        contours (list): Lista de contornos detectados.

    Returns:
        list: Una lista de tuplas, donde cada tupla es (x, y, w, h)
              representando un bounding box.
    """
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bounding_boxes.append((x, y, w, h))
    return bounding_boxes
