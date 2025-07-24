# gui_app.py
# Interfaz gráfica de usuario para el pipeline de Captura de Movimiento.

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
from PIL import Image, ImageTk
import threading
import os
import subprocess
import sys
import json
from datetime import datetime
import webbrowser

# Asumimos que los otros módulos del proyecto están en sus carpetas correctas
from core.pose_estimation import PoseEstimator
from core.hand_estimation import HandEstimator
from core.face_estimation import FaceEstimator
from core.video_capture import VideoCapture

class MotionCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Xlerion - Video 2 Anim")
        self.root.geometry("1280x800")

        self.capture_source = None
        self.csv_path = ""
        self.processing_thread = None
        self.stop_processing = False
        self.current_theme = 'dark'
        self.sessions_file = "sessions.json"

        self.capture_mode = tk.StringVar(value="Pose Corporal")
        self.detection_confidence = tk.DoubleVar(value=0.5)
        self.tracking_confidence = tk.DoubleVar(value=0.5)
        self.model_complexity = tk.IntVar(value=1)

        self.setup_translations()
        self.ui_elements = {}

        self.themes = {
            'light': {
                'bg': "#FFFFFF", 'fg': "#888888", 'frame_bg': '#ffffff',
                'button_bg': '#0078D7', 'button_fg': '#ffffff', 'button_active': '#005a9e',
                'header_fg': "#0088ff", 'canvas_bg': "#F7F7F7", 'status_bg': "#353535",
                'tree_bg': '#ffffff', 'tree_fg': "#272727", 'tree_selected': '#0078D7',
                'link_fg': '#0066cc', 'border': '#d0d0d0'
            },
            'dark': {
                'bg': "#000000", 'fg': "#00FFEA", 'frame_bg': "#181818",
                'button_bg': '#0078D7', 'button_fg': "#ffffff", 'button_active': '#005a9e',
                'header_fg': "#00ffea", 'canvas_bg': "#000000", 'status_bg': "#242424",
                'tree_bg': "#020202", 'tree_fg': "#00f7ff", 'tree_selected': '#005a9e',
                'link_fg': "#15dcff", 'border': "#00ffff"
            }
        }

        self.setup_styles()
        self.setup_ui()
        self.apply_theme()
        self.change_language('es') 
        self.load_sessions()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

    def setup_ui(self):
        # --- Menú Superior ---
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Guía de Uso", command=self.show_help_dialog)
        
        self.about_menu = tk.Menu(self.menubar, tearoff=0)
        self.about_menu.add_command(label="Créditos", command=self.show_credits_dialog)

        self.menubar.add_cascade(label="Ayuda", menu=self.help_menu)
        self.menubar.add_cascade(label="Acerca de", menu=self.about_menu)


        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        sessions_frame = ttk.Frame(self.paned_window, padding="5")
        self.paned_window.add(sessions_frame, weight=1)
        sessions_header = ttk.Frame(sessions_frame)
        sessions_header.pack(fill=tk.X)
        self.ui_elements['sessions_label'] = ttk.Label(sessions_header, text="Sesiones Guardadas", font=('Helvetica', 14, 'bold'))
        self.ui_elements['sessions_label'].pack(side=tk.LEFT, pady=5)
        self.ui_elements['refresh_button'] = ttk.Button(sessions_header, text="Refrescar", command=self.load_sessions)
        self.ui_elements['refresh_button'].pack(side=tk.RIGHT)
        tree_frame = ttk.Frame(sessions_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.sessions_tree = ttk.Treeview(tree_frame, columns=("video", "csv", "bvh"), show="headings")
        self.sessions_tree.pack(side='left', fill='both', expand=True)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.sessions_tree.yview)
        self.sessions_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self.sessions_tree.bind("<<TreeviewSelect>>", self.on_session_select)
        action_frame = ttk.Frame(sessions_frame)
        action_frame.pack(fill=tk.X, pady=5)
        self.ui_elements['open_folder_button'] = ttk.Button(action_frame, text="Abrir Carpeta", command=self.open_session_folder, state=tk.DISABLED)
        self.ui_elements['open_folder_button'].pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.ui_elements['delete_session_button'] = ttk.Button(action_frame, text="Eliminar Sesión", command=self.delete_session, state=tk.DISABLED)
        self.ui_elements['delete_session_button'].pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.ui_elements['clear_all_button'] = ttk.Button(action_frame, text="Limpiar Todo", command=self.clear_all_sessions)
        self.ui_elements['clear_all_button'].pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.main_frame = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(self.main_frame, weight=3)
        top_bar = ttk.Frame(self.main_frame)
        top_bar.pack(fill=tk.X)
        lang_frame = ttk.Frame(top_bar)
        lang_frame.pack(side=tk.RIGHT, padx=5, pady=5)
        self.lang_btn_es = ttk.Button(lang_frame, text="ES", command=lambda: self.change_language('es'), width=3)
        self.lang_btn_es.pack(side=tk.LEFT)
        self.lang_btn_en = ttk.Button(lang_frame, text="EN", command=lambda: self.change_language('en'), width=3)
        self.lang_btn_en.pack(side=tk.LEFT)
        self.lang_btn_ja = ttk.Button(lang_frame, text="JA", command=lambda: self.change_language('ja'), width=3)
        self.lang_btn_ja.pack(side=tk.LEFT)
        self.theme_button = ttk.Button(top_bar, text="🌙", command=self.toggle_theme, width=3)
        self.theme_button.pack(side=tk.RIGHT, pady=5)
        self.ui_elements['app_title'] = ttk.Label(top_bar, text="Xlerion - Video 2 Anim")
        self.ui_elements['app_title'].pack(side=tk.TOP, fill=tk.X, expand=True, pady=5)
        
        self.control_frame = ttk.Frame(self.main_frame, padding="10", relief="groove", borderwidth=1)
        self.control_frame.pack(fill=tk.X, pady=5)

        self.ui_elements['header1'] = ttk.Label(self.control_frame, text="Etapa 1: Captura de Datos")
        self.ui_elements['header1'].grid(row=0, column=0, columnspan=5, pady=5, sticky="w")
        self.ui_elements['select_video_button'] = ttk.Button(self.control_frame, text="Seleccionar Video", command=self.select_video_file)
        self.ui_elements['select_video_button'].grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.ui_elements['no_source_label'] = ttk.Label(self.control_frame, text="Ninguna fuente seleccionada", wraplength=300)
        self.ui_elements['no_source_label'].grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky="w")
        self.ui_elements['webcam_capture_button'] = ttk.Button(self.control_frame, text="Capturar desde Webcam", command=self.start_webcam_capture)
        self.ui_elements['webcam_capture_button'].grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.ui_elements['delay_label'] = ttk.Label(self.control_frame, text="Retardo (s):")
        self.ui_elements['delay_label'].grid(row=2, column=1, padx=(10,0), pady=5, sticky="e")
        self.timer_spinbox = ttk.Spinbox(self.control_frame, from_=0, to=10, width=5, command=lambda: self.timer_spinbox.selection_clear())
        self.timer_spinbox.set(3)
        self.timer_spinbox.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.ui_elements['start_capture_button'] = ttk.Button(self.control_frame, text="Iniciar Captura", command=self.start_capture_thread, state=tk.DISABLED)
        self.ui_elements['start_capture_button'].grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        self.ui_elements['stop_capture_button'] = ttk.Button(self.control_frame, text="Detener Captura", command=self.stop_capture)

        self.ui_elements['settings_frame'] = ttk.LabelFrame(self.control_frame, text="Ajustes de Detección")
        self.ui_elements['settings_frame'].grid(row=0, column=5, rowspan=4, padx=20, pady=5, sticky="ns")
        self.ui_elements['capture_mode_label'] = ttk.Label(self.ui_elements['settings_frame'], text="Modo de Captura:")
        self.ui_elements['capture_mode_label'].grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.capture_mode_combo = ttk.Combobox(self.ui_elements['settings_frame'], textvariable=self.capture_mode, state="readonly")
        self.capture_mode_combo.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)
        self.ui_elements['det_conf_label'] = ttk.Label(self.ui_elements['settings_frame'], text="Confianza de Detección:")
        self.ui_elements['det_conf_label'].grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ttk.Scale(self.ui_elements['settings_frame'], from_=0.1, to=1.0, orient=tk.HORIZONTAL, variable=self.detection_confidence).grid(row=3, column=0, sticky="ew", padx=5)
        ttk.Label(self.ui_elements['settings_frame'], textvariable=self.detection_confidence).grid(row=3, column=1, sticky="w", padx=5)
        self.ui_elements['track_conf_label'] = ttk.Label(self.ui_elements['settings_frame'], text="Confianza de Seguimiento:")
        self.ui_elements['track_conf_label'].grid(row=4, column=0, sticky="w", padx=5, pady=2)
        ttk.Scale(self.ui_elements['settings_frame'], from_=0.1, to=1.0, orient=tk.HORIZONTAL, variable=self.tracking_confidence).grid(row=5, column=0, sticky="ew", padx=5)
        ttk.Label(self.ui_elements['settings_frame'], textvariable=self.tracking_confidence).grid(row=5, column=1, sticky="w", padx=5)
        self.ui_elements['model_comp_label'] = ttk.Label(self.ui_elements['settings_frame'], text="Complejidad del Modelo:")
        self.ui_elements['model_comp_label'].grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.model_complexity_combo = ttk.Combobox(self.ui_elements['settings_frame'], textvariable=self.model_complexity, values=[0, 1], state="readonly", width=10)
        self.model_complexity_combo.grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.ui_elements['model_comp_note'] = ttk.Label(self.ui_elements['settings_frame'], text="(0=Rápido, 1=Normal)")
        self.ui_elements['model_comp_note'].grid(row=8, column=0, sticky="w", padx=5, pady=2)

        self.ui_elements['header2'] = ttk.Label(self.control_frame, text="Etapa 2: Conversión de CSV a BVH")
        self.ui_elements['header2'].grid(row=4, column=0, columnspan=5, pady=10, sticky="w")
        self.ui_elements['no_csv_label'] = ttk.Label(self.control_frame, text="Ningún archivo CSV seleccionado")
        self.ui_elements['no_csv_label'].grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.ui_elements['export_button'] = ttk.Button(self.control_frame, text="Exportar Animación", command=self.show_export_dialog, state=tk.DISABLED)
        self.ui_elements['export_button'].grid(row=5, column=2, padx=5, pady=5, sticky="ew")

        action_bar = ttk.Frame(self.control_frame)
        action_bar.grid(row=6, column=0, columnspan=6, pady=10, sticky="ew")
        self.ui_elements['clear_selection_button'] = ttk.Button(action_bar, text="Limpiar Selección", command=self.clear_selections)
        self.ui_elements['clear_selection_button'].pack(side=tk.RIGHT, padx=5)
        self.ui_elements['close_program_button'] = ttk.Button(action_bar, text="Cerrar Programa", command=self.on_closing)
        self.ui_elements['close_program_button'].pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=10)
        self.status_bar = ttk.Label(self.main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def clear_selections(self):
        self.capture_source = None
        self.csv_path = ""
        self.ui_elements['no_source_label'].config(text=self.translations[self.current_lang]['no_source_label'])
        self.ui_elements['no_csv_label'].config(text=self.translations[self.current_lang]['no_csv_label'])
        self.ui_elements['start_capture_button'].config(state=tk.DISABLED)
        self.ui_elements['export_button'].config(state=tk.DISABLED)
        if self.sessions_tree.selection(): self.sessions_tree.selection_remove(self.sessions_tree.selection()[0])
        self.canvas.delete("all")
        self.update_status(self.translations[self.current_lang]['status_cleaned'])

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.theme_button.config(text="☀️" if self.current_theme == 'dark' else "🌙")
        title_fg_color = theme['header_fg'] if self.current_theme == 'light' else theme['fg']
        
        self.style.configure(".", background=theme['bg'], foreground=theme['fg'])
        self.style.configure("TFrame", background=theme['bg'])
        self.style.configure("AppTitle.TLabel", background=theme['bg'], foreground=title_fg_color, font=('Helvetica', 16, 'bold'), anchor='center')
        self.style.configure("Header.TLabel", background=theme['frame_bg'], foreground=theme['header_fg'], font=('Helvetica', 14, 'bold'))
        self.style.configure("TLabel", background=theme['frame_bg'], foreground=theme['fg'], font=('Helvetica', 10))
        self.style.configure("Status.TLabel", background=theme['status_bg'], foreground=theme['fg'])
        self.style.configure("TButton", padding=6, relief="flat", background=theme['button_bg'], foreground=theme['button_fg'], font=('Helvetica', 10, 'bold'))
        self.style.map("TButton", background=[('active', theme['button_active'])])
        self.style.configure("Groove.TFrame", background=theme['frame_bg'], bordercolor=theme['border'], relief='groove')
        self.style.configure("Treeview", background=theme['tree_bg'], foreground=theme['tree_fg'], fieldbackground=theme['tree_bg'], rowheight=25)
        self.style.map("Treeview", background=[('selected', theme['tree_selected'])])
        self.style.configure("TLabelframe", background=theme['frame_bg'], bordercolor=theme['fg'])
        self.style.configure("TLabelframe.Label", background=theme['frame_bg'], foreground=theme['fg'])

        self.root.configure(bg=theme['bg'])
        self.main_frame.configure(style="TFrame")
        self.ui_elements['app_title'].configure(style="AppTitle.TLabel")
        self.ui_elements['sessions_label'].configure(background=theme['bg'], foreground=theme['fg'])
        self.control_frame.configure(style="Groove.TFrame")
        self.ui_elements['header1'].configure(style="Header.TLabel")
        self.ui_elements['header2'].configure(style="Header.TLabel")
        self.ui_elements['no_source_label'].configure(style="TLabel")
        self.ui_elements['no_csv_label'].configure(style="TLabel")
        self.status_bar.configure(style="Status.TLabel")
        self.canvas.configure(bg=theme['canvas_bg'])
        
        for widget in self.control_frame.winfo_children():
            if isinstance(widget, (ttk.Label, ttk.LabelFrame)):
                widget.configure(style="TLabel" if "Etapa" not in str(widget.cget("text")) else "Header.TLabel")

    def load_sessions(self):
        for i in self.sessions_tree.get_children(): self.sessions_tree.delete(i)
        if not os.path.exists(self.sessions_file): return
        with open(self.sessions_file, 'r') as f:
            try:
                sessions = json.load(f)
                for session_id, data in sorted(sessions.items()):
                    video = os.path.basename(data.get('video_path', 'N/A')) if data.get('video_path') != 0 else self.translations[self.current_lang]['webcam_capture']
                    csv = os.path.basename(data.get('csv_path', 'N/A')) if data.get('csv_path') else 'N/A'
                    bvh = os.path.basename(data.get('bvh_path', 'N/A')) if data.get('bvh_path') else 'N/A'
                    self.sessions_tree.insert("", "end", iid=session_id, values=(video, csv, bvh))
            except json.JSONDecodeError: self.update_status("Error al leer el archivo de sesiones.")
        self.on_session_select(None)

    def save_session(self, session_id, data_to_update):
        sessions = {}
        if os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'r') as f:
                try: sessions = json.load(f)
                except json.JSONDecodeError: pass
        if session_id in sessions: sessions[session_id].update(data_to_update)
        else: sessions[session_id] = data_to_update
        with open(self.sessions_file, 'w') as f: json.dump(sessions, f, indent=4)
        self.load_sessions()

    def on_session_select(self, event):
        selected_items = self.sessions_tree.selection()
        if selected_items:
            self.ui_elements['open_folder_button'].config(state=tk.NORMAL)
            self.ui_elements['delete_session_button'].config(state=tk.NORMAL)
            session_id = selected_items[0]
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
                session_data = sessions.get(session_id)
                if session_data:
                    self.capture_source = session_data.get('video_path', '')
                    self.csv_path = session_data.get('csv_path', '')
                    self.ui_elements['no_source_label'].config(text=os.path.basename(self.capture_source) if isinstance(self.capture_source, str) else self.translations[self.current_lang]['webcam_capture'])
                    self.ui_elements['no_csv_label'].config(text=os.path.basename(self.csv_path) if self.csv_path else "N/A")
                    self.ui_elements['start_capture_button'].config(state=tk.NORMAL if self.capture_source is not None else tk.DISABLED)
                    self.ui_elements['export_button'].config(state=tk.NORMAL if self.csv_path else tk.DISABLED)
                    self.update_status(self.translations[self.current_lang]['status_session_loaded'].format(session_id))
        else:
            self.ui_elements['open_folder_button'].config(state=tk.DISABLED)
            self.ui_elements['delete_session_button'].config(state=tk.DISABLED)

    def select_video_file(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")])
        if path:
            self.capture_source = path
            self.ui_elements['no_source_label'].config(text=os.path.basename(path))
            self.ui_elements['start_capture_button'].config(state=tk.NORMAL)
            self.update_status(self.translations[self.current_lang]['status_video_selected'].format(os.path.basename(path)))
    
    def start_webcam_capture(self):
        self.capture_source = 0
        self.ui_elements['no_source_label'].config(text=self.translations[self.current_lang]['status_webcam_prep'])
        try: seconds = int(self.timer_spinbox.get())
        except (ValueError, tk.TclError): seconds = 0
        self.toggle_capture_controls(capturing=True)
        if seconds > 0: self.run_countdown(seconds)
        else: self.start_capture_thread(from_countdown=False)

    def run_countdown(self, seconds):
        if self.stop_processing: self.toggle_capture_controls(capturing=False); return
        if seconds > 0:
            self.update_canvas_with_text(str(seconds))
            self.root.after(1000, lambda: self.run_countdown(seconds - 1))
        else:
            self.update_canvas_with_text("REC", color="red")
            self.root.after(500, lambda: self.start_capture_thread(from_countdown=True))

    def start_capture_thread(self, from_countdown=False):
        if self.capture_source is None: messagebox.showerror(self.translations[self.current_lang]['error_title'], self.translations[self.current_lang]['error_no_source']); return
        if not from_countdown: self.toggle_capture_controls(capturing=True)
        self.stop_processing = False
        self.processing_thread = threading.Thread(target=self.process_video)
        self.processing_thread.start()

    def stop_capture(self):
        self.stop_processing = True
        self.update_status(self.translations[self.current_lang]['status_stopping'])

    def toggle_capture_controls(self, capturing):
        state = tk.DISABLED if capturing else tk.NORMAL
        self.ui_elements['select_video_button'].config(state=state)
        self.ui_elements['webcam_capture_button'].config(state=state)
        self.ui_elements['start_capture_button'].grid_remove()
        if capturing: self.ui_elements['stop_capture_button'].grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        else: self.ui_elements['stop_capture_button'].grid_remove()
        if not capturing: self.ui_elements['start_capture_button'].grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    def show_export_dialog(self):
        if not self.csv_path:
            messagebox.showerror(self.translations[self.current_lang]['error_title'], self.translations[self.current_lang]['error_no_csv'])
            return
        ExportDialog(self.root, self)

    def start_bvh_conversion(self):
        bvh_path = filedialog.asksaveasfilename(defaultextension=".bvh", filetypes=[("BVH files", "*.bvh")], initialfile=f"{os.path.splitext(os.path.basename(self.csv_path))[0]}.bvh")
        if not bvh_path: return
        self.ui_elements['export_button'].config(state=tk.DISABLED)
        self.update_status(self.translations[self.current_lang]['status_converting'])
        command = [sys.executable, "csv_to_bvh.py", self.csv_path, bvh_path]
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.update_status(self.translations[self.current_lang]['status_conversion_ok'].format(bvh_path))
            session_id = self.get_session_id_from_csv(self.csv_path)
            if session_id: self.save_session(session_id, {'bvh_path': bvh_path})
            messagebox.showinfo(self.translations[self.current_lang]['success_title'], self.translations[self.current_lang]['success_conversion'].format(result.stdout))
        except subprocess.CalledProcessError as e:
            self.update_status(self.translations[self.current_lang]['status_conversion_error'])
            messagebox.showerror(self.translations[self.current_lang]['error_title_conversion'], self.translations[self.current_lang]['error_conversion'].format(e.stderr))
        finally: self.ui_elements['export_button'].config(state=tk.NORMAL)
    
    def get_session_id_from_csv(self, csv_path):
        basename = os.path.basename(csv_path)
        if basename.endswith("_mocap_data.csv") or basename.endswith("_mocap_pose_data.csv") or basename.endswith("_mocap_hand_data.csv"):
             return os.path.splitext(basename)[0].replace("_mocap_data", "").replace("_mocap_pose_data", "").replace("_mocap_hand_data", "")
        return os.path.splitext(basename)[0]

    def process_video(self):
        is_webcam = isinstance(self.capture_source, int)
        captured_data = []
        estimator = None
        video_source = None
        try:
            det_conf, track_conf, model_comp, mode = self.detection_confidence.get(), self.tracking_confidence.get(), self.model_complexity.get(), self.capture_mode.get()
            video_source = VideoCapture(self.capture_source)
            if mode == self.translations['es']['capture_mode_values'][0]: estimator = PoseEstimator(min_detection_confidence=det_conf, min_tracking_confidence=track_conf, model_complexity=model_comp if model_comp < 3 else 2)
            elif mode == self.translations['es']['capture_mode_values'][1]: estimator = HandEstimator(min_detection_confidence=det_conf, min_tracking_confidence=track_conf, model_complexity=model_comp if model_comp < 2 else 1)
            else: estimator = FaceEstimator(min_detection_confidence=det_conf, min_tracking_confidence=track_conf)
            frame_number = 0; csv_writer, csv_file, output_csv_path = None, None, ""
            while not self.stop_processing:
                ret, frame = video_source.get_frame()
                if not ret: break
                annotated_frame, results = estimator.process_frame(frame)
                if mode == self.translations['es']['capture_mode_values'][1] and results.multi_hand_landmarks:
                    frame_landmarks = []
                    for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        for idx, landmark in enumerate(hand_landmarks.landmark): frame_landmarks.append([frame_number, hand_no, idx, landmark.x, landmark.y, landmark.z])
                    if is_webcam: captured_data.extend(frame_landmarks)
                    else:
                        if frame_number == 0:
                            base, _ = os.path.splitext(self.capture_source); output_csv_path = f"{base}_mocap_hand_data.csv"
                            csv_file = open(output_csv_path, 'w', newline=''); import csv; csv_writer = csv.writer(csv_file); csv_writer.writerow(['frame', 'hand_id', 'landmark_id', 'x', 'y', 'z'])
                        csv_writer.writerows(frame_landmarks)
                elif mode == self.translations['es']['capture_mode_values'][0] and results.pose_landmarks:
                    frame_landmarks = []
                    for idx, landmark in enumerate(results.pose_landmarks.landmark): frame_landmarks.append([frame_number, idx, landmark.x, landmark.y, landmark.z, landmark.visibility])
                    if is_webcam: captured_data.extend(frame_landmarks)
                    else:
                        if frame_number == 0:
                            base, _ = os.path.splitext(self.capture_source); output_csv_path = f"{base}_mocap_pose_data.csv"
                            csv_file = open(output_csv_path, 'w', newline=''); import csv; csv_writer = csv.writer(csv_file); csv_writer.writerow(['frame', 'landmark_id', 'x', 'y', 'z', 'visibility'])
                        csv_writer.writerows(frame_landmarks)
                elif mode == self.translations['es']['capture_mode_values'][2] and results.multi_face_landmarks:
                    frame_landmarks = []
                    for face_no, face_landmarks in enumerate(results.multi_face_landmarks):
                        for idx, landmark in enumerate(face_landmarks.landmark): frame_landmarks.append([frame_number, face_no, idx, landmark.x, landmark.y, landmark.z])
                    if is_webcam: captured_data.extend(frame_landmarks)
                    else:
                        if frame_number == 0:
                            base, _ = os.path.splitext(self.capture_source); output_csv_path = f"{base}_mocap_face_data.csv"
                            csv_file = open(output_csv_path, 'w', newline=''); import csv; csv_writer = csv.writer(csv_file); csv_writer.writerow(['frame', 'face_id', 'landmark_id', 'x', 'y', 'z'])
                        csv_writer.writerows(frame_landmarks)
                self.update_canvas(annotated_frame)
                self.update_status(self.translations[self.current_lang]['status_processing'].format(frame_number))
                frame_number += 1
            if is_webcam: self.root.after(0, self.schedule_webcam_save, captured_data, mode)
            else:
                if csv_file: csv_file.close()
                session_id = os.path.splitext(os.path.basename(self.capture_source))[0]
                session_data = {'video_path': self.capture_source, 'csv_path': output_csv_path, 'timestamp': datetime.now().isoformat()}
                self.save_session(session_id, session_data)
                self.root.after(0, self.finalize_capture, output_csv_path)
        except Exception as e:
            messagebox.showerror(self.translations[self.current_lang]['error_title_processing'], self.translations[self.current_lang]['error_processing'].format(e))
            self.root.after(0, self.toggle_capture_controls, False)
        finally:
            if estimator: estimator.close()
            if video_source: video_source.release()

    def finalize_capture(self, output_path):
        self.toggle_capture_controls(capturing=False)
        self.update_status(self.translations[self.current_lang]['status_done'].format(output_path))
        messagebox.showinfo(self.translations[self.current_lang]['done_title'], self.translations[self.current_lang]['done_message'].format(output_path))

    def schedule_webcam_save(self, data, mode):
        self.toggle_capture_controls(capturing=False)
        if not data: self.update_status(self.translations[self.current_lang]['status_no_pose']); return
        output_csv_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title=self.translations[self.current_lang]['dialog_save_capture'])
        if output_csv_path:
            with open(output_csv_path, 'w', newline='') as f:
                import csv; writer = csv.writer(f)
                if mode == self.translations['es']['capture_mode_values'][0]: writer.writerow(['frame', 'landmark_id', 'x', 'y', 'z', 'visibility'])
                elif mode == self.translations['es']['capture_mode_values'][1]: writer.writerow(['frame', 'hand_id', 'landmark_id', 'x', 'y', 'z'])
                else: writer.writerow(['frame', 'face_id', 'landmark_id', 'x', 'y', 'z'])
                writer.writerows(data)
            session_id = f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            session_data = {'video_path': 0, 'csv_path': output_csv_path, 'timestamp': datetime.now().isoformat()}
            self.save_session(session_id, session_data)
            self.update_status(self.translations[self.current_lang]['status_webcam_saved'].format(output_csv_path))
            messagebox.showinfo(self.translations[self.current_lang]['saved_title'], self.translations[self.current_lang]['saved_message'])
        else:
            self.update_status(self.translations[self.current_lang]['status_webcam_unsaved'])

    def open_session_folder(self):
        selected_items = self.sessions_tree.selection()
        if not selected_items: return
        session_id = selected_items[0]
        with open(self.sessions_file, 'r') as f:
            sessions = json.load(f)
            session_data = sessions.get(session_id)
            if session_data and session_data.get('csv_path'):
                folder_path = os.path.dirname(session_data['csv_path'])
                if sys.platform == "win32": os.startfile(folder_path)
                elif sys.platform == "darwin": subprocess.Popen(["open", folder_path])
                else: subprocess.Popen(["xdg-open", folder_path])
            else: messagebox.showwarning(self.translations[self.current_lang]['warning_title'], self.translations[self.current_lang]['warning_no_path'])

    def delete_session(self):
        selected_items = self.sessions_tree.selection()
        if not selected_items: return
        if not messagebox.askyesno(self.translations[self.current_lang]['confirm_delete_title'], self.translations[self.current_lang]['confirm_delete_message']): return
        sessions = {}
        with open(self.sessions_file, 'r') as f: sessions = json.load(f)
        for item in selected_items:
            if item in sessions: del sessions[item]
        with open(self.sessions_file, 'w') as f: json.dump(sessions, f, indent=4)
        self.load_sessions()
        self.update_status(self.translations[self.current_lang]['status_deleted'])

    def clear_all_sessions(self):
        if not messagebox.askyesno(self.translations[self.current_lang]['confirm_clear_title'], self.translations[self.current_lang]['confirm_clear_message']): return
        if os.path.exists(self.sessions_file): os.remove(self.sessions_file)
        self.load_sessions()
        self.update_status(self.translations[self.current_lang]['status_all_deleted'])

    def update_canvas(self, frame):
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 2 or canvas_h < 2: return
        h, w, _ = frame.shape
        aspect_ratio = w / h
        new_w, new_h = (int(canvas_h * aspect_ratio), canvas_h) if canvas_w / canvas_h > aspect_ratio else (canvas_w, int(canvas_w / aspect_ratio))
        resized_frame = cv2.resize(frame, (new_w, new_h))
        img = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        self.photo = ImageTk.PhotoImage(image=img_pil)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_w/2, canvas_h/2, anchor=tk.CENTER, image=self.photo)

    def update_canvas_with_text(self, text, color="white"):
        self.canvas.delete("all")
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        self.canvas.create_text(canvas_w/2, canvas_h/2, text=text, font=('Helvetica', 100, 'bold'), fill=color)

    def update_status(self, text):
        self.status_bar.config(text=text)

    def on_closing(self):
        if messagebox.askokcancel(self.translations[self.current_lang]['exit_title'], self.translations[self.current_lang]['exit_message']):
            self.stop_processing = True
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join()
            self.root.destroy()

    def change_language(self, lang):
        self.current_lang = lang
        lang_dict = self.translations[lang]
        for key, widget in self.ui_elements.items():
            if key in lang_dict:
                widget.config(text=lang_dict[key])
        
        self.sessions_tree.heading("video", text=lang_dict['treeview_col1'])
        self.sessions_tree.heading("csv", text=lang_dict['treeview_col2'])
        self.sessions_tree.heading("bvh", text=lang_dict['treeview_col3'])
        
        self.capture_mode_combo['values'] = lang_dict['capture_mode_values']

        self.style.configure("Accent.TButton", background=self.themes[self.current_theme]['button_active'])
        self.lang_btn_es.config(style="TButton")
        self.lang_btn_en.config(style="TButton")
        self.lang_btn_ja.config(style="TButton")
        getattr(self, f"lang_btn_{lang}").config(style="Accent.TButton")
        
        self.menubar.entryconfig(1, label=lang_dict['menu_help'])
        self.menubar.entryconfig(2, label=lang_dict['menu_about'])
        self.help_menu.entryconfig(0, label=lang_dict['menu_guide'])
        self.about_menu.entryconfig(0, label=lang_dict['menu_credits'])

        self.load_sessions()

    def show_help_dialog(self):
        messagebox.showinfo(self.translations[self.current_lang]['menu_guide'], self.translations[self.current_lang]['help_text'])

    def show_credits_dialog(self):
        CreditsDialog(self.root, self)

    def setup_translations(self):
        self.translations = {
            'es': {
                'app_title': "Xlerion - Video 2 Anim",
                'sessions_label': "Sesiones Guardadas", 'refresh_button': "Refrescar",
                'treeview_col1': "Fuente Original", 'treeview_col2': "Archivo CSV", 'treeview_col3': "Archivo BVH",
                'open_folder_button': "Abrir Carpeta", 'delete_session_button': "Eliminar Sesión", 'clear_all_button': "Limpiar Todo",
                'header1': "Etapa 1: Captura de Datos", 'select_video_button': "Seleccionar Video",
                'no_source_label': "Ninguna fuente seleccionada", 'webcam_capture_button': "Capturar desde Webcam",
                'delay_label': "Retardo (s):", 'start_capture_button': "Iniciar Captura", 'stop_capture_button': "Detener Captura",
                'settings_frame': "Ajustes de Detección", 'capture_mode_label': "Modo de Captura:",
                'capture_mode_values': ["Pose Corporal", "Manos (Alta Precisión)", "Rostro y Gestos"],
                'det_conf_label': "Confianza de Detección:", 'track_conf_label': "Confianza de Seguimiento:",
                'model_comp_label': "Complejidad del Modelo:", 'model_comp_note': "(0=Rápido, 1=Normal)",
                'header2': "Etapa 2: Conversión de CSV a BVH", 'no_csv_label': "Ningún archivo CSV seleccionado",
                'export_button': "Exportar Animación", 'clear_selection_button': "Limpiar Selección", 'close_program_button': "Cerrar Programa",
                'status_ready': "Listo", 'status_cleaned': "Selección limpiada. Listo para empezar.",
                'status_session_loaded': "Sesión '{}' cargada.", 'status_video_selected': "Video seleccionado: {}",
                'status_webcam_prep': "Preparando Webcam...", 'status_stopping': "Deteniendo captura...",
                'status_converting': "Iniciando conversión a BVH...", 'status_conversion_ok': "¡Conversión a BVH completada! Archivo guardado en {}",
                'status_conversion_error': "Error durante la conversión a BVH.", 'status_processing': "Procesando frame: {}",
                'status_done': "Procesamiento finalizado. Datos guardados en {}", 'status_no_pose': "Captura detenida. No se detectó ninguna pose.",
                'dialog_save_capture': "Guardar datos de captura", 'status_webcam_saved': "Datos de webcam guardados en {}",
                'saved_title': "Guardado", 'saved_message': "Datos de captura guardados exitosamente.",
                'status_webcam_unsaved': "Captura detenida. Datos no guardados.",
                'error_title': "Error", 'error_no_source': "Por favor, selecciona un video o inicia la captura desde la webcam.",
                'error_no_csv': "Por favor, selecciona un archivo CSV primero.", 'success_title': "Éxito",
                'success_conversion': "Conversión completada.\n\n{}", 'error_title_conversion': "Error de Conversión",
                'error_conversion': "Ocurrió un error:\n\n{}", 'error_title_processing': "Error en Procesamiento",
                'error_processing': "Ocurrió un error: {}", 'done_title': "Proceso Terminado",
                'done_message': "La captura de datos ha finalizado.\nEl archivo CSV se ha guardado en:\n{}",
                'warning_title': "Advertencia", 'warning_no_path': "No se encontró una ruta de archivo para esta sesión.",
                'confirm_delete_title': "Confirmar Eliminación", 'confirm_delete_message': "¿Estás seguro de que quieres eliminar la(s) sesión(es) seleccionada(s)?",
                'status_deleted': "Sesión(es) eliminada(s).", 'confirm_clear_title': "Confirmar Limpieza Total",
                'confirm_clear_message': "ADVERTENCIA: ¿Estás seguro de que quieres eliminar TODAS las sesiones guardadas? Esta acción no se puede deshacer.",
                'status_all_deleted': "Todas las sesiones han sido eliminadas.", 'exit_title': "Salir", 'exit_message': "¿Estás seguro de que quieres salir?",
                'webcam_capture': "Webcam Capture",
                'menu_help': "Ayuda", 'menu_guide': "Guía de Uso", 'menu_about': "Acerca de", 'menu_credits': "Créditos",
                'help_text': "1. Selecciona un modo de captura.\n2. Ajusta los parámetros de detección.\n3. Elige un video o usa la webcam para iniciar la captura.\n4. Una vez generado un CSV, selecciónalo desde la lista de sesiones.\n5. Exporta la animación a formato BVH (solo para Pose Corporal).",
                'credits_title': "Créditos y Licencia",
                'credits_created_by': "Creado por:",
                'credits_developer_title': "Creador de Videojuegos y Desarrollador",
                'credits_collaboration': "Desarrollado en colaboración con la IA de Google.",
                'credits_license': "Licencia MIT - 2025",
                'credits_support_title': "Apoya el Desarrollo",
                'credits_professional_title': "Redes Profesionales",
                'credits_portfolio_title': "Portafolios y Proyectos"
            },
            'en': {
                'app_title': "Xlerion - Video 2 Anim",
                'sessions_label': "Saved Sessions", 'refresh_button': "Refresh",
                'treeview_col1': "Original Source", 'treeview_col2': "CSV File", 'treeview_col3': "BVH File",
                'open_folder_button': "Open Folder", 'delete_session_button': "Delete Session", 'clear_all_button': "Clear All",
                'header1': "Stage 1: Data Capture", 'select_video_button': "Select Video",
                'no_source_label': "No source selected", 'webcam_capture_button': "Capture from Webcam",
                'delay_label': "Delay (s):", 'start_capture_button': "Start Capture", 'stop_capture_button': "Stop Capture",
                'settings_frame': "Detection Settings", 'capture_mode_label': "Capture Mode:",
                'capture_mode_values': ["Body Pose", "Hands (High Precision)", "Face & Gestures"],
                'det_conf_label': "Detection Confidence:", 'track_conf_label': "Tracking Confidence:",
                'model_comp_label': "Model Complexity:", 'model_comp_note': "(0=Fast, 1=Normal)",
                'header2': "Stage 2: CSV to BVH Conversion", 'no_csv_label': "No CSV file selected",
                'export_button': "Export Animation", 'clear_selection_button': "Clear Selection", 'close_program_button': "Close Program",
                'status_ready': "Ready", 'status_cleaned': "Selection cleared. Ready to start.",
                'status_session_loaded': "Session '{}' loaded.", 'status_video_selected': "Video selected: {}",
                'status_webcam_prep': "Preparing Webcam...", 'status_stopping': "Stopping capture...",
                'status_converting': "Starting BVH conversion...", 'status_conversion_ok': "BVH conversion complete! File saved to {}",
                'status_conversion_error': "Error during BVH conversion.", 'status_processing': "Processing frame: {}",
                'status_done': "Processing finished. Data saved to {}", 'status_no_pose': "Capture stopped. No pose detected.",
                'dialog_save_capture': "Save capture data", 'status_webcam_saved': "Webcam data saved to {}",
                'saved_title': "Saved", 'saved_message': "Capture data saved successfully.",
                'status_webcam_unsaved': "Capture stopped. Data not saved.",
                'error_title': "Error", 'error_no_source': "Please select a video or start webcam capture first.",
                'error_no_csv': "Please select a CSV file first.", 'success_title': "Success",
                'success_conversion': "Conversion complete.\n\n{}", 'error_title_conversion': "Conversion Error",
                'error_conversion': "An error occurred:\n\n{}", 'error_title_processing': "Processing Error",
                'error_processing': "An error occurred: {}", 'done_title': "Process Finished",
                'done_message': "Data capture has finished.\nThe CSV file has been saved to:\n{}",
                'warning_title': "Warning", 'warning_no_path': "No file path found for this session.",
                'confirm_delete_title': "Confirm Deletion", 'confirm_delete_message': "Are you sure you want to delete the selected session(s)?",
                'status_deleted': "Session(s) deleted.", 'confirm_clear_title': "Confirm Clear All",
                'confirm_clear_message': "WARNING: Are you sure you want to delete ALL saved sessions? This action cannot be undone.",
                'status_all_deleted': "All sessions have been deleted.", 'exit_title': "Exit", 'exit_message': "Are you sure you want to exit?",
                'webcam_capture': "Webcam Capture",
                'menu_help': "Help", 'menu_guide': "User Guide", 'menu_about': "About", 'menu_credits': "Credits",
                'help_text': "1. Select a capture mode.\n2. Adjust the detection parameters.\n3. Choose a video or use the webcam to start capturing.\n4. Once a CSV is generated, select it from the sessions list.\n5. Export the animation to BVH format (only for Body Pose).",
                'credits_title': "Credits & License",
                'credits_created_by': "Created by:",
                'credits_developer_title': "Game Creator and Developer",
                'credits_collaboration': "Developed in collaboration with Google's AI.",
                'credits_license': "MIT License - 2025",
                'credits_support_title': "Support the Development",
                'credits_professional_title': "Professional Networks",
                'credits_portfolio_title': "Portfolios & Projects"
            },
            'ja': {
                'app_title': "Xlerion - ビデオからアニメへ",
                'sessions_label': "保存されたセッション", 'refresh_button': "更新",
                'treeview_col1': "元のソース", 'treeview_col2': "CSVファイル", 'treeview_col3': "BVHファイル",
                'open_folder_button': "フォルダを開く", 'delete_session_button': "セッションを削除", 'clear_all_button': "すべてクリア",
                'header1': "ステージ1：データキャプチャ", 'select_video_button': "ビデオを選択",
                'no_source_label': "ソースが選択されていません", 'webcam_capture_button': "ウェブカメラからキャプチャ",
                'delay_label': "遅延 (秒):", 'start_capture_button': "キャプチャ開始", 'stop_capture_button': "キャプチャ停止",
                'settings_frame': "検出設定", 'capture_mode_label': "キャプチャモード:",
                'capture_mode_values': ["全身ポーズ", "手（高精度）", "顔とジェスチャー"],
                'det_conf_label': "検出信頼度:", 'track_conf_label': "追跡信頼度:",
                'model_comp_label': "モデルの複雑さ:", 'model_comp_note': "(0=高速, 1=通常)",
                'header2': "ステージ2：CSVからBVHへの変換", 'no_csv_label': "CSVファイルが選択されていません",
                'export_button': "アニメーションをエクスポート", 'clear_selection_button': "選択をクリア", 'close_program_button': "プログラムを閉じる",
                'status_ready': "準備完了", 'status_cleaned': "選択がクリアされました。準備完了です。",
                'status_session_loaded': "セッション「{}」が読み込まれました。", 'status_video_selected': "ビデオが選択されました: {}",
                'status_webcam_prep': "ウェブカメラを準備中...", 'status_stopping': "キャプチャを停止中...",
                'status_converting': "BVH変換を開始中...", 'status_conversion_ok': "BVH変換が完了しました！ファイルは{}に保存されました",
                'status_conversion_error': "BVH変換中にエラーが発生しました。", 'status_processing': "フレームを処理中: {}",
                'status_done': "処理が完了しました。データは{}に保存されました", 'status_no_pose': "キャプチャが停止しました。ポーズは検出されませんでした。",
                'dialog_save_capture': "キャプチャデータを保存", 'status_webcam_saved': "ウェブカメラデータが{}に保存されました",
                'saved_title': "保存済み", 'saved_message': "キャプチャデータが正常に保存されました。",
                'status_webcam_unsaved': "キャプチャが停止しました。データは保存されませんでした。",
                'error_title': "エラー", 'error_no_source': "ビデオを選択するか、ウェブカメラからキャプチャを開始してください。",
                'error_no_csv': "最初にCSVファイルを選択してください。", 'success_title': "成功",
                'success_conversion': "変換が完了しました。\n\n{}", 'error_title_conversion': "変換エラー",
                'error_conversion': "エラーが発生しました:\n\n{}", 'error_title_processing': "処理エラー",
                'error_processing': "エラーが発生しました: {}", 'done_title': "処理完了",
                'done_message': "データキャプチャが完了しました。\nCSVファイルは次の場所に保存されました:\n{}",
                'warning_title': "警告", 'warning_no_path': "このセッションのファイルパスが見つかりませんでした。",
                'confirm_delete_title': "削除の確認", 'confirm_delete_message': "選択したセッションを削除してもよろしいですか？",
                'status_deleted': "セッションが削除されました。", 'confirm_clear_title': "すべてクリアの確認",
                'confirm_clear_message': "警告：保存されているすべてのセッションを削除してもよろしいですか？この操作は元に戻せません。",
                'status_all_deleted': "すべてのセッションが削除されました。", 'exit_title': "終了", 'exit_message': "本当に終了しますか？",
                'webcam_capture': "ウェブカメラキャプチャ",
                'menu_help': "ヘルプ", 'menu_guide': "使用ガイド", 'menu_about': "バージョン情報", 'menu_credits': "クレジット",
                'help_text': "1. キャプチャモードを選択します。\n2. 検出パラメータを調整します。\n3. ビデオを選択するか、ウェブカメラを使用してキャプチャを開始します。\n4. CSVが生成されたら、セッションリストから選択します。\n5. アニメーションをBVH形式にエクスポートします（全身ポーズのみ）。",
                'credits_title': "クレジットとライセンス",
                'credits_created_by': "作成者:",
                'credits_developer_title': "ゲームクリエーター兼開発者",
                'credits_collaboration': "GoogleのAIとの協力で開発されました。",
                'credits_license': "MITライセンス - 2025",
                'credits_support_title': "開発をサポート",
                'credits_professional_title': "専門的なネットワーク",
                'credits_portfolio_title': "ポートフォリオとプロジェクト"
            }
        }

if __name__ == "__main__":
    try: from PIL import Image, ImageTk
    except ImportError:
        print("Error: La librería Pillow no está instalada.")
        print("Por favor, instálala ejecutando: pip install Pillow")
        sys.exit(1)
    
    class ExportDialog(tk.Toplevel):
        def __init__(self, parent, app_instance):
            super().__init__(parent)
            self.app = app_instance
            self.title(self.app.translations[self.app.current_lang]['export_button'])
            self.geometry("600x450")
            
            ttk.Label(self, text=self.app.translations[self.app.current_lang]['export_button'], font=('Helvetica', 14, 'bold')).pack(pady=10)
            
            ttk.Button(self, text="Exportar a .BVH", command=self.export_bvh).pack(pady=5, padx=20, fill=tk.X)

            info_frame = ttk.LabelFrame(self, text="Otros Formatos (FBX, GLTF)")
            info_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
            
            info_text = "Para exportar a otros formatos como FBX o GLTF, sigue estos pasos:\n\n1. Exporta tu animación a .BVH usando el botón de arriba.\n2. Abre el programa gratuito Blender.\n3. Importa el archivo .BVH (`File > Import > .bvh`).\n4. Exporta la animación al formato deseado (`File > Export > .fbx / .gltf`)."
            ttk.Label(info_frame, text=info_text, wraplength=350, justify=tk.LEFT).pack(pady=10, padx=10)

        def export_bvh(self):
            self.destroy()
            self.app.start_bvh_conversion()
            
    class CreditsDialog(tk.Toplevel):
        def __init__(self, parent, app_instance):
            super().__init__(parent)
            self.app = app_instance
            lang = self.app.current_lang
            theme = self.app.themes[self.app.current_theme]

            self.title(self.app.translations[lang]['credits_title'])
            self.geometry("450x800")
            self.configure(bg=theme['bg'])

            main_frame = ttk.Frame(self, style="TFrame")
            main_frame.pack(padx=60, pady=80, fill=tk.BOTH, expand=True)

            ttk.Label(main_frame, text="Xlerion - Video 2 Anim", font=('Helvetica', 16, 'bold'), style="TLabel").pack()
            ttk.Label(main_frame, text=self.app.translations[lang]['credits_created_by'], style="TLabel").pack(pady=(10,0))
            ttk.Label(main_frame, text="Miguel Rodriguez Martinez", font=('Helvetica', 12, 'bold'), style="TLabel").pack()
            ttk.Label(main_frame, text=self.app.translations[lang]['credits_developer_title'], style="TLabel").pack()
            
            def create_link(parent, text, url, icon=""):
                frame = ttk.Frame(parent, style="TFrame")
                link = ttk.Label(frame, text=f"{icon} {text}", foreground=theme['link_fg'], cursor="hand2", style="TLabel")
                link.pack(side=tk.LEFT)
                link.bind("<Button-1>", lambda e: webbrowser.open_new(url))
                return frame

            # --- Links ---
            ttk.Label(main_frame, text=self.app.translations[lang]['credits_professional_title'], font=('Helvetica', 11, 'bold'), style="TLabel").pack(pady=(20, 5))
            create_link(main_frame, "LinkedIn (Personal)", "https://www.linkedin.com/in/mikerodriguez84", "🔗").pack(anchor='w')
            create_link(main_frame, "LinkedIn (Xlerion)", "https://www.linkedin.com/company/xlerion/", "🔗").pack(anchor='w')
            
            ttk.Label(main_frame, text=self.app.translations[lang]['credits_support_title'], font=('Helvetica', 11, 'bold'), style="TLabel").pack(pady=(20, 5))
            create_link(main_frame, "Patreon", "https://www.patreon.com/c/xlerion", "❤️").pack(anchor='w')
            create_link(main_frame, "Indiegogo", "https://www.indiegogo.com/individuals/32112766", "💡").pack(anchor='w')
            create_link(main_frame, "Kickstarter", "https://www.kickstarter.com/profile/xlerionstudios", "🚀").pack(anchor='w')

            ttk.Label(main_frame, text=self.app.translations[lang]['credits_portfolio_title'], font=('Helvetica', 11, 'bold'), style="TLabel").pack(pady=(20, 5))
            create_link(main_frame, "ArtStation", "https://www.artstation.com/xlerion", "🎨").pack(anchor='w')
            create_link(main_frame, "Itch.io", "https://xlerion.itch.io/", "🎮").pack(anchor='w')
            create_link(main_frame, "Facebook", "https://www.facebook.com/xlerionultimate", "👍").pack(anchor='w')
            create_link(main_frame, "GitHub", "https://github.com/MikeHell84", "💻").pack(anchor='w')

            ttk.Label(main_frame, text=self.app.translations[lang]['credits_collaboration'], style="TLabel").pack(pady=(20,0))
            ttk.Label(main_frame, text=self.app.translations[lang]['credits_license'], style="TLabel").pack()

            ttk.Button(main_frame, text="Cerrar", command=self.destroy).pack(pady=20)


    root = tk.Tk()
    app = MotionCaptureApp(root)
    root.mainloop()
