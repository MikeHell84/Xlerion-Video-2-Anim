# core/video_capture.py
# Módulo para gestionar la captura de video desde una fuente (webcam o archivo).

import cv2

class VideoCapture:
    """
    Clase para encapsular la lógica de captura de video con OpenCV.
    Puede manejar tanto cámaras en vivo como archivos de video.
    """
    def __init__(self, source):
        """
        Inicializa el objeto de captura de video.

        Args:
            source (int or str): El índice de la cámara (ej. 0) o la ruta a un archivo de video.
        """
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise IOError(f"No se puede abrir la fuente de video: {source}")
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Fuente de video iniciada con resolución: {self.width}x{self.height}")

    def get_frame(self):
        """
        Captura un único frame desde la fuente de video.

        Returns:
            tuple: Una tupla conteniendo (bool, numpy.ndarray).
                   El booleano es True si el frame se leyó correctamente, False en caso contrario
                   (por ejemplo, al final de un video).
                   El ndarray es el frame de imagen capturado.
        """
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        """
        Libera el recurso de la fuente de video.
        """
        if self.cap.isOpened():
            self.cap.release()
            print("Recurso de video liberado.")

    def __del__(self):
        """
        Destructor para asegurar que la fuente se libere al eliminar el objeto.
        """
        self.release()
