# tests/test_detection.py
# Tests para el módulo de detección de movimiento.

import unittest
import numpy as np
import cv2
from core.motion_detection import MotionDetector
from utils.config_loader import load_config

class TestMotionDetection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Carga la configuración y crea imágenes de prueba una vez para toda la clase.
        """
        # Cargar una configuración por defecto para las pruebas
        cls.config = load_config('configs/default_config.yaml')['motion_detection']
        
        # Crear imágenes sintéticas para la prueba
        # Frame de fondo (gris)
        cls.background_frame = np.full((100, 100, 3), 128, dtype=np.uint8)
        
        # Frame con un objeto en movimiento (un cuadrado blanco)
        cls.motion_frame = cls.background_frame.copy()
        cv2.rectangle(cls.motion_frame, (20, 20), (50, 50), (255, 255, 255), -1)

    def test_no_motion(self):
        """
        Prueba que no se detecte movimiento cuando los frames son idénticos.
        """
        detector = MotionDetector(self.config)
        # Alimentar el detector con el fondo para establecerlo como referencia
        for _ in range(10): # Simular varios frames estáticos
            _ = detector.detect(self.background_frame)
        
        # Ahora, detectar en un frame idéntico
        contours = detector.detect(self.background_frame)
        self.assertEqual(len(contours), 0, "No debería detectarse movimiento en un frame estático.")

    def test_motion_detected(self):
        """
        Prueba que se detecte movimiento cuando hay una diferencia significativa.
        """
        detector = MotionDetector(self.config)
        # Establecer el fondo
        for _ in range(10):
            _ = detector.detect(self.background_frame)
        
        # Introducir el frame con el objeto
        contours = detector.detect(self.motion_frame)
        
        # La configuración por defecto tiene un min_contour_area de 700.
        # El cuadrado es de 31x31 = 961. Debería ser detectado.
        self.assertGreaterEqual(len(contours), 1, "Debería detectarse al menos un contorno.")
        
        # Opcional: Verificar el área del contorno detectado
        if len(contours) > 0:
            area = cv2.contourArea(contours[0])
            self.assertGreater(area, self.config['min_contour_area'], 
                               "El área del contorno detectado debería ser mayor que el mínimo.")

if __name__ == '__main__':
    unittest.main()
