# csv_to_bvh.py
# Este script convierte los datos de landmarks de MediaPipe (guardados en un CSV)
# a un archivo de animación en formato BVH.

import csv
import numpy as np
from scipy.spatial.transform import Rotation as R
import argparse
import os

# --- Definición del Esqueleto y Landmarks de MediaPipe ---
# Mapea los nombres de las articulaciones a los índices de MediaPipe Pose
LANDMARK_MAP = {
    'Hips': (24, 23),  # Promedio de caderas
    'Spine': (12, 11), # Promedio de hombros
    'Chest': (12, 11), # Igual que Spine por simplicidad
    'Neck': (12, 11),  # Punto de partida para la cabeza
    'Head': (0, 0),    # Nariz
    'LeftShoulder': 11,
    'LeftArm': 13,
    'LeftForeArm': 15,
    'LeftHand': 19,
    'RightShoulder': 12,
    'RightArm': 14,
    'RightForeArm': 16,
    'RightHand': 20,
    'LeftUpLeg': 23,
    'LeftLeg': 25,
    'LeftFoot': 27,
    'LeftToeBase': 31,
    'RightUpLeg': 24,
    'RightLeg': 26,
    'RightFoot': 28,
    'RightToeBase': 32
}

# Define la jerarquía del esqueleto (hueso_hijo: hueso_padre)
# La raíz es 'Hips'
HIERARCHY = {
    'Spine': 'Hips',
    'Chest': 'Spine',
    'Neck': 'Chest',
    'Head': 'Neck',
    'LeftShoulder': 'Chest',
    'LeftArm': 'LeftShoulder',
    'LeftForeArm': 'LeftArm',
    'LeftHand': 'LeftForeArm',
    'RightShoulder': 'Chest',
    'RightArm': 'RightShoulder',
    'RightForeArm': 'RightArm',
    'RightHand': 'RightForeArm',
    'LeftUpLeg': 'Hips',
    'LeftLeg': 'LeftUpLeg',
    'LeftFoot': 'LeftLeg',
    'LeftToeBase': 'LeftFoot',
    'RightUpLeg': 'Hips',
    'RightLeg': 'RightUpLeg',
    'RightFoot': 'RightLeg',
    'RightToeBase': 'RightFoot'
}

# --- Funciones Auxiliares ---

def read_csv_data(filepath):
    """Lee los datos de landmarks desde el archivo CSV."""
    frames = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Saltar la cabecera
        for row in reader:
            frame_num = int(row[0])
            if frame_num not in frames:
                frames[frame_num] = {}
            landmark_id = int(row[1])
            frames[frame_num][landmark_id] = np.array([float(row[2]), float(row[3]), float(row[4])])
    return frames

def get_joint_position(frame_data, joint_name):
    """Obtiene la posición de una articulación, promediando si es necesario."""
    indices = LANDMARK_MAP[joint_name]
    if isinstance(indices, tuple):
        # Promediar las posiciones de dos landmarks
        pos1 = frame_data.get(indices[0], np.zeros(3))
        pos2 = frame_data.get(indices[1], np.zeros(3))
        return (pos1 + pos2) / 2.0
    else:
        return frame_data.get(indices, np.zeros(3))

def calculate_bone_vector(frame_data, child_joint, parent_joint):
    """Calcula el vector de un hueso."""
    child_pos = get_joint_position(frame_data, child_joint)
    parent_pos = get_joint_position(frame_data, parent_joint)
    return child_pos - parent_pos

def calculate_rotation(v_from, v_to):
    """Calcula la rotación en grados Euler (ZXY) para alinear v_from con v_to."""
    v_from = v_from / np.linalg.norm(v_from)
    v_to = v_to / np.linalg.norm(v_to)
    
    rotation = R.align_vectors(v_to[np.newaxis, :], v_from[np.newaxis, :])[0]
    euler_angles = rotation.as_euler('zxy', degrees=True)
    return euler_angles

# --- Funciones para Escribir el BVH ---

def write_bvh_hierarchy(f, joint_name, level=0):
    """Escribe recursivamente la jerarquía del esqueleto en el archivo BVH."""
    indent = '  ' * level
    if joint_name == 'Hips':
        f.write(f"{indent}ROOT Hips\n")
    else:
        f.write(f"{indent}JOINT {joint_name}\n")
    
    f.write(f"{indent}{{\n")
    indent_inner = '  ' * (level + 1)
    
    # Escribir el OFFSET (longitud del hueso)
    # Esto es una simplificación; en un sistema real, se calcularía una vez desde una pose T.
    f.write(f"{indent_inner}OFFSET 0.00 0.00 0.00\n")
    
    if joint_name == 'Hips':
        f.write(f"{indent_inner}CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n")
    else:
        f.write(f"{indent_inner}CHANNELS 3 Zrotation Xrotation Yrotation\n")
        
    # Encontrar los hijos de la articulación actual y continuar recursivamente
    children = [j for j, p in HIERARCHY.items() if p == joint_name]
    for child in children:
        write_bvh_hierarchy(f, child, level + 1)
        
    # Escribir End Site para las articulaciones terminales
    if not children:
        f.write(f"{indent_inner}End Site\n")
        f.write(f"{indent_inner}{{\n")
        f.write(f"{indent_inner}  OFFSET 0.00 0.00 0.00\n")
        f.write(f"{indent_inner}}}\n")
        
    f.write(f"{indent}}}\n")


def write_bvh_motion(f, frames_data, frame_time):
    """Escribe la sección de movimiento del archivo BVH."""
    num_frames = len(frames_data)
    f.write(f"MOTION\n")
    f.write(f"Frames: {num_frames}\n")
    f.write(f"Frame Time: {frame_time:.6f}\n")

    # Define el orden de las articulaciones para escribir los datos
    joint_order = ['Hips']
    q = ['Hips']
    while q:
        parent = q.pop(0)
        children = sorted([j for j, p in HIERARCHY.items() if p == parent])
        joint_order.extend(children)
        q.extend(children)

    # Escribir los datos de rotación para cada frame
    for frame_num in sorted(frames_data.keys()):
        frame = frames_data[frame_num]
        line = []
        
        # Posición de la cadera (Hips)
        hips_pos = get_joint_position(frame, 'Hips') * 100 # Escalar a cm
        line.extend([f"{hips_pos[0]:.4f}", f"{hips_pos[1]:.4f}", f"{hips_pos[2]:.4f}"])
        
        # Rotación de la cadera (simplificado, se asume 0,0,0)
        line.extend(["0.00", "0.00", "0.00"])

        # Calcular y escribir rotaciones para las demás articulaciones
        for joint in joint_order:
            if joint == 'Hips': continue
            
            parent = HIERARCHY[joint]
            # Vector del hueso actual
            v_bone = calculate_bone_vector(frame, joint, parent)
            # Vector del hueso padre (simplificado como un vector hacia arriba)
            v_parent_dir = np.array([0, 1, 0]) # Asumimos que la pose T es vertical
            
            if np.linalg.norm(v_bone) > 1e-6:
                angles = calculate_rotation(v_parent_dir, v_bone)
                line.extend([f"{angle:.4f}" for angle in angles])
            else:
                line.extend(["0.00", "0.00", "0.00"])

        f.write(" ".join(line) + "\n")

# --- Función Principal ---

def main():
    parser = argparse.ArgumentParser(description="Convierte un archivo CSV de landmarks de MediaPipe a formato BVH.")
    parser.add_argument("csv_filepath", type=str, help="Ruta al archivo CSV de entrada.")
    parser.add_argument("bvh_filepath", type=str, help="Ruta al archivo BVH de salida.")
    parser.add_argument("--fps", type=int, default=30, help="Frames por segundo del video original.")
    args = parser.parse_args()

    print(f"Leyendo datos desde: {args.csv_filepath}")
    frames_data = read_csv_data(args.csv_filepath)
    if not frames_data:
        print("Error: No se encontraron datos en el archivo CSV.")
        return

    frame_time = 1.0 / args.fps

    print(f"Escribiendo archivo BVH en: {args.bvh_filepath}")
    with open(args.bvh_filepath, 'w') as f:
        f.write("HIERARCHY\n")
        write_bvh_hierarchy(f, 'Hips')
        write_bvh_motion(f, frames_data, frame_time)

    print("¡Conversión completada exitosamente!")

if __name__ == "__main__":
    main()
