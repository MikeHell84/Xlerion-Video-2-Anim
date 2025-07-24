# pipelines/video_file_pipeline.py
# Flujo de trabajo para la captura de datos de pose desde un archivo de video.

import cv2
import os
import csv
from core.video_capture import VideoCapture
from core.pose_estimation import PoseEstimator

def run_video_file(config, filepath):
    """
    Ejecuta el pipeline de estimación de pose en un archivo de video,
    guarda el video con el esqueleto dibujado y exporta los datos de landmarks a un CSV.
    """
    video_source = None
    video_writer = None
    estimator = None
    csv_file = None
    csv_writer = None
    
    try:
        # --- Inicialización ---
        print("[DEBUG] Inicializando recursos...")
        video_source = VideoCapture(filepath)
        estimator = PoseEstimator()
        
        # --- Configuración de rutas de salida ---
        base, ext = os.path.splitext(filepath)
        output_video_path = f"{base}_mocap_processed.mp4"
        output_csv_path = f"{base}_mocap_data.csv"
        
        print(f"[DEBUG] Ruta del video de salida: {output_video_path}")
        print(f"[DEBUG] Ruta del archivo CSV de salida: {output_csv_path}")

        # --- Configuración del escritor de video ---
        frame_width = int(video_source.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_source.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video_source.cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
        
        if not video_writer.isOpened():
            print("[ERROR] No se pudo abrir el escritor de video.")
            return

        # --- Preparar archivo CSV ---
        print(f"[DEBUG] Abriendo archivo CSV en modo escritura: {output_csv_path}")
        csv_file = open(output_csv_path, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        header = ['frame', 'landmark_id', 'x', 'y', 'z', 'visibility']
        csv_writer.writerow(header)
        print("[DEBUG] Cabecera del CSV escrita correctamente.")

        frame_number = 0
        poses_detected_count = 0
        
        # --- Bucle Principal ---
        print("\n[INFO] Comenzando el procesamiento del video...")
        while True:
            ret, frame = video_source.get_frame()
            if not ret:
                print("[INFO] Fin del archivo de video detectado.")
                break

            # 1. Estimar la pose
            annotated_frame, pose_results = estimator.process_frame(frame)

            # 2. Guardar los datos si se detectó una pose
            if pose_results.pose_landmarks:
                poses_detected_count += 1
                if poses_detected_count == 1:
                    print("[DEBUG] ¡Primera pose detectada! Escribiendo datos...")

                for idx, landmark in enumerate(pose_results.pose_landmarks.landmark):
                    row = [frame_number, idx, landmark.x, landmark.y, landmark.z, landmark.visibility]
                    csv_writer.writerow(row)

            # 3. Guardar el frame procesado
            video_writer.write(annotated_frame)

            # Mostrar resultado
            cv2.imshow(f'Motion Capture - {os.path.basename(filepath)}', annotated_frame)
            
            frame_number += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[INFO] Salida solicitada por el usuario.")
                break
        
        print(f"\n[INFO] Procesamiento completado. Total de frames con poses detectadas: {poses_detected_count}")

    except Exception as e:
        print(f"\n[ERROR FATAL] Ocurrió un error inesperado: {e}")
    
    finally:
        # --- Limpieza ---
        print("[DEBUG] Iniciando limpieza de recursos...")
        if video_source:
            video_source.release()
            print("[DEBUG] Fuente de video liberada.")
        if video_writer:
            video_writer.release()
            print("[DEBUG] Escritor de video liberado.")
        if estimator:
            estimator.close()
            print("[DEBUG] Estimador de pose cerrado.")
        if csv_file:
            csv_file.close()
            print("[DEBUG] Archivo CSV cerrado.")
        cv2.destroyAllWindows()
        print("\n[INFO] Proceso finalizado.")

