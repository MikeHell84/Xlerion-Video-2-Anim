# core/hand_estimation.py
# Módulo para la estimación de landmarks de manos usando MediaPipe.

import cv2
import mediapipe as mp

class HandEstimator:
    """
    Clase para encapsular la lógica de estimación de manos con MediaPipe.
    """
    def __init__(self, static_image_mode=False, max_num_hands=2, model_complexity=1,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Inicializa el estimador de manos.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def process_frame(self, frame):
        """
        Procesa un frame para detectar las manos.

        Args:
            frame (numpy.ndarray): El frame de imagen en formato BGR.

        Returns:
            tuple: Una tupla conteniendo el frame con las manos dibujadas y los resultados.
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        annotated_image = frame.copy()
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
            
        return annotated_image, results

    def close(self):
        """
        Libera los recursos del modelo de manos.
        """
        self.hands.close()
