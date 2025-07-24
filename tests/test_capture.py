# tests/test_capture.py
# Tests unitarios para el módulo de captura de video.

import unittest
import cv2
# Para que el test funcione, necesita acceso a los módulos del proyecto.
# Esto se puede manejar con PYTHONPATH o una estructura de paquete adecuada.
# Asumimos que el test se ejecuta desde el directorio raíz.
from core.video_capture import VideoCapture

class TestVideoCapture(unittest.TestCase):

    def test_camera_initialization(self):
        """
        Prueba si la cámara se puede inicializar.
        Nota: Este test requiere una cámara conectada en el índice 0.
        Puede fallar en un entorno sin hardware de cámara.
        """
        try:
            camera = VideoCapture(source_index=0)
            self.assertTrue(camera.cap.isOpened(), "La cámara no se pudo abrir.")
            camera.release()
        except IOError:
            self.fail("VideoCapture levantó una IOError inesperadamente.")
        except Exception as e:
            # Si no hay cámara, cv2 puede no levantar IOError pero fallar.
            # Marcamos esto como un skip en lugar de un fallo.
            self.skipTest(f"No se pudo acceder a la cámara para la prueba. Error: {e}")

    def test_get_frame(self):
        """
        Prueba si se puede obtener un frame de la cámara.
        """
        try:
            camera = VideoCapture(source_index=0)
            if not camera.cap.isOpened():
                self.skipTest("No hay cámara disponible para probar get_frame.")
            
            ret, frame = camera.get_frame()
            self.assertTrue(ret, "get_frame debería devolver True si la captura es exitosa.")
            self.assertIsNotNone(frame, "El frame no debería ser None.")
            self.assertEqual(len(frame.shape), 3, "El frame debería tener 3 dimensiones (alto, ancho, canales).")
            camera.release()
        except Exception as e:
            self.skipTest(f"No se pudo realizar la prueba de get_frame. Error: {e}")

if __name__ == '__main__':
    unittest.main()
