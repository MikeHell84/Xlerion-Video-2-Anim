# core/motion_detection.py
# Algoritmos para detectar movimiento entre frames.

import cv2
import numpy as np

class MotionDetector:
    """
    Gestiona la detección de movimiento usando sustracción de fondo.
    """
    def __init__(self, config):
        """
        Inicializa el detector de movimiento con parámetros de configuración.

        Args:
            config (dict): Diccionario de configuración para la detección.
        """
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=config.get('history', 500),
            varThreshold=config.get('var_threshold', 16),
            detectShadows=config.get('detect_shadows', True)
        )
        self.blur_ksize = tuple(config.get('blur_ksize', [5, 5]))
        self.threshold_val = config.get('threshold_val', 25)
        self.dilation_kernel_size = tuple(config.get('dilation_kernel_size', [3, 3]))
        self.min_contour_area = config.get('min_contour_area', 500)

    def detect(self, frame):
        """
        Detecta movimiento en un frame dado.

        Args:
            frame (numpy.ndarray): El frame actual para procesar.

        Returns:
            list: Una lista de contornos que representan las áreas de movimiento detectadas.
        """
        # 1. Aplicar sustracción de fondo
        fg_mask = self.bg_subtractor.apply(frame)

        # 2. Aplicar desenfoque para reducir el ruido
        blurred_mask = cv2.GaussianBlur(fg_mask, self.blur_ksize, 0)

        # 3. Umbralización para obtener una máscara binaria
        _, thresh_mask = cv2.threshold(
            blurred_mask, self.threshold_val, 255, cv2.THRESH_BINARY
        )

        # 4. Dilatación para rellenar agujeros en los objetos
        kernel = np.ones(self.dilation_kernel_size, np.uint8)
        dilated_mask = cv2.dilate(thresh_mask, kernel, iterations=2)

        # 5. Encontrar contornos en la máscara final
        contours, _ = cv2.findContours(
            dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # 6. Filtrar contornos pequeños
        significant_contours = [
            cnt for cnt in contours if cv2.contourArea(cnt) > self.min_contour_area
        ]

        return significant_contours
