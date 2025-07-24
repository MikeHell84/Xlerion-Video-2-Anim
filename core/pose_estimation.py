# core/pose_estimation.py
# Módulo para la estimación de pose humana usando MediaPipe.

import cv2
import mediapipe as mp

class PoseEstimator:
    """
    Clase para encapsular la lógica de estimación de pose con MediaPipe.
    """
    def __init__(self, static_image_mode=False, model_complexity=1, smooth_landmarks=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Inicializa el estimador de pose.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            smooth_landmarks=smooth_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def process_frame(self, frame):
        """
        Procesa un frame para detectar la pose.

        Args:
            frame (numpy.ndarray): El frame de imagen en formato BGR.

        Returns:
            tuple: Una tupla conteniendo el frame con el esqueleto dibujado y los resultados de la pose.
        """
        # Convertir la imagen de BGR a RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar la imagen y encontrar la pose
        results = self.pose.process(image_rgb)
        
        # Dibujar el esqueleto en el frame original
        annotated_image = frame.copy()
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
        return annotated_image, results

    def close(self):
        """
        Libera los recursos del modelo de pose.
        """
        self.pose.close()