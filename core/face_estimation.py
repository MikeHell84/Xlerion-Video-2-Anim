# core/face_estimation.py
# Módulo para la estimación de landmarks faciales usando MediaPipe.

import cv2
import mediapipe as mp

class FaceEstimator:
    """
    Clase para encapsular la lógica de estimación de malla facial con MediaPipe.
    """
    def __init__(self, static_image_mode=False, max_num_faces=1, refine_landmarks=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Inicializa el estimador de malla facial.
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=max_num_faces,
            refine_landmarks=refine_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def process_frame(self, frame):
        """
        Procesa un frame para detectar la malla facial.

        Args:
            frame (numpy.ndarray): El frame de imagen en formato BGR.

        Returns:
            tuple: Una tupla conteniendo el frame con la malla dibujada y los resultados.
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)
        
        annotated_image = frame.copy()
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Dibuja los contornos y teselación de la cara
                self.mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style())
                self.mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style())
            
        return annotated_image, results

    def close(self):
        """
        Libera los recursos del modelo de malla facial.
        """
        self.face_mesh.close()
