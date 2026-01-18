# src/interface/gui.py
"""
Módulo que implementa la Interfaz Gráfica de Usuario (GUI) de la aplicación.
Versión fusionada con estética "Green & Pink" y funcionalidad completa.
"""
import customtkinter as ctk
import tkinter
import base64
import io
from tkinter import filedialog
from PIL import Image
import os
import threading
import queue
import pathlib

from src.core import use_cases
from src.infrastructure.ocr_service import OcrService
from tkinterdnd2 import DND_FILES, TkinterDnD

# --- INCRUSTACIÓN DE ASSETS POR CÓDIGO ---
ICONO_DROP_B64 = base64.b64decode(
    b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAA'
    b'gIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAAsTAAAL'
    b'EwEAmpwYAAAAB3RJTUUH6AkMEy4TAca3lAAAA3RJREFUeNrtm21IVFcUx3/vuXPuvSPuDqOM4IOmBoMiIY2E'
    b'ijISFIn4gwpCF1G6iB6U6NJlF72J7gNB0yIa8kUUREZExEQw00JNSzSSzDA6g2NMzpnzvo/NoyI7jDNz4B94'
    b'eB+Hc8/97n/u+Z+7BwzDMAzDMAzDMAzDMAzDMAzDMAzDMAx/kGWs8BGxrgA8h/A+gDXCV4HUW8BWAL8AXgM4'
    b'A/gK4E8A/wT+A1ABWFXA3gC+x/gM8L3gVwFmA0gL/gC4G/AnANYBdhXwdcBfAasB/A04E/BLgH8BHgYMiQDP'
    b'gY3wF8BLDFgB/A9wK2Abgx4GvAr4M2ApAPwfuAfAiwL7AbwBPMbQG/jHwG8A/BuwFkAT+AngQcCG+gHiJoRW'
    b'AFwGHAfYEiAX+AnAuwLbA1wGHAyYEnhDwNcA/ALMBeA1gB2AtgE8AngA8CniMEX8EHAr4C9gEwNeAbwA+xJg'
    b'TwC/A+wFo/gK4E3AoYCuA1wBWAx4EHAlgB2BPgN+AA4E/AvwMeB3gXcC/gMHAUQBvAN4AvAB4EnA44F3AV4B'
    b'vAE8Bvgh4GvBZgH0BPgbcBPgY8BHAM8GvAG8B7AegBv+LgB8CjgfsBvAswA4AxwLuB3wU8HHAxwCvA/YAcCv'
    b'gOcA/gE8AngI8BjgScAewB4Bf/B0AfgRcCdgH4O+BrwCeBbwO+BNgLQDd+H0AlwMuBexy5J8AfgM4FHD3gB9'
    b'b5JcAjwL+DvBPgJsBeA/gIcBPAI8CjgLcCfgRYDfgRYBdgL0AfAxwI+CPgC8D3gK8Dngb8D7gC4AbAccDngf'
    b'8EfAswL4Afg7sBPApwIuAewA8BvgI4GuAuwD8CbgT8BPA1wBHAxYCrgScB3yM8TvA3wKuAeyK8QfgM8BHAL8Dv'
    b'A6YD+DXgN8C/gqYDuBfwLGAzYAvAZ4G/AHgNsBbANcDbgf8GbAfgD8H3AZwG2BPgL8H3AG4G8A/AfcBeAXgFs'
    b'A/Aj4D+DHgPzWl/wH4P+AvAfsBGIZhGIZhGIZhGIZhGIZhGIZhGIZhGIZhGIZh/i9b9qQy0m5/JAAAAABJRU5ErkJggg=='
)

# clase auxiliar para tooltips
class Tooltip:
    def __init__(self, widget, text, bg_color):
        self.widget = widget
        self.text = text
        self.bg_color = bg_color
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tkinter.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tkinter.Label(self.tooltip_window, text=self.text,
                              background=self.bg_color, relief='solid', borderwidth=1,
                              font=("Segoe UI", 10, "normal"), padx=8, pady=4)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

import ctypes
from ctypes import windll

class App(TkinterDnD.Tk):
    def __init__(self, ocr_service: OcrService):
        ctk.set_appearance_mode("Light")
        super().__init__()
        
        self.COLOR_BACKGROUND = "#F0FFF8"
        self.COLOR_FRAME = "#FFF0F7"
        self.COLOR_PRIMARY = "#F47A8D"
        self.COLOR_PRIMARY_HOVER = "#D86A7B"
        self.COLOR_SECONDARY = "#4FD1C5"
        self.COLOR_SECONDARY_HOVER = "#43B5A9"
        self.COLOR_DISABLED = "#D0D0D0"
        self.COLOR_TEXT = "#202020"
        self.COLOR_TEXT_SECONDARY = "#404040"
        self.FONT_BODY = ("Segoe UI", 13)
        self.FONT_TITLE = ("Segoe UI", 16, "bold")
        self.FONT_BUTTON = ("Segoe UI", 13, "bold")
        
        self.configure(bg=self.COLOR_BACKGROUND)
        self.overrideredirect(True)
        self.title("Extractor de Texto")
        
        self.geometry("1000x600")

        self.ocr_service = ocr_service
        self.batch_results: dict[str, str] = {}
        self.copy_in_progress = False
        self.image_paths_to_process: list[str] = []
        self.ocr_result_queue = queue.Queue()
        self.active_file_button = None

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self._on_drop)
        self._load_assets()
        
        self.minimize_functional_var = ctk.BooleanVar(value=True)
        self.adjust_720p_var = ctk.BooleanVar(value=True)
        self.show_taskbar_var = ctk.BooleanVar(value=True)
        
        self.adjust_720p_var.trace_add("write", self._on_720p_change)

        self._setup_ui()
        self.after(100, self._check_ocr_queue)
        
        self.after(200, self._set_taskbar_icon)

    def _set_taskbar_icon(self):
        """Hack para mostrar ventana en barra de tareas siendo frameless (overrideredirect=True)"""
        try:
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            
            hwnd = windll.user32.GetParent(self.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            
            self.wm_withdraw()
            self.after(10, self.wm_deiconify)
        except Exception as e:
            print(f"Advertencia: No se pudo configurar barra de tareas: {e}")

    def _minimize_window(self):
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()
        self.bind("<Map>", self._on_restore)
        
    def _on_restore(self, event):
        self.overrideredirect(True)
        self.unbind("<Map>")
        
    def _on_720p_change(self, *args):
        if self.adjust_720p_var.get():
            self.geometry("1000x600")

    def _load_assets(self):
        self.copy_icon = None
        self.save_icon = None
        self.drop_icon = None
        self.save_all_icon = None
        self.clean_text_icon = None
        try:
            assets_path = pathlib.Path(__file__).parent.parent.parent / "assets"
            
            self.copy_icon = ctk.CTkImage(Image.open(assets_path / "copy_icon.png"))
            self.save_icon = ctk.CTkImage(Image.open(assets_path / "save_icon.png"))
            self.save_all_icon = ctk.CTkImage(Image.open(assets_path / "save_all_icon.png"))
            self.clean_text_icon = ctk.CTkImage(Image.open(assets_path / "clean_text_icon.png"))

            drop_pil_image = Image.open(io.BytesIO(ICONO_DROP_B64))
            self.drop_icon = ctk.CTkImage(light_image=drop_pil_image, dark_image=drop_pil_image, size=(64, 64))
            
            if (assets_path / "app_icon.png").exists():
                 app_icon = Image.open(assets_path / "app_icon.png")
                 self.iconphoto(False, ctk.CTkImage(app_icon)._light_image)
            else:
                 self.iconphoto(False, drop_pil_image)
            
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar los iconos: {e}")

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main_container = ctk.CTkFrame(self, corner_radius=10, fg_color=self.COLOR_BACKGROUND)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)
        self._create_title_bar()
        self._create_controls_panel()
        self._create_main_workspace()
        self._create_status_bar()

    def _create_title_bar(self):
        self.title_bar = ctk.CTkFrame(self.main_container, height=40, corner_radius=0, fg_color=self.COLOR_FRAME)
        self.title_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.title_label = ctk.CTkLabel(self.title_bar, text="💗 Extractor de Texto - Green & Pink 💚", font=(self.FONT_BODY[0], 12, "bold"), text_color=self.COLOR_TEXT)
        self.title_label.pack(side="left", padx=15, pady=5)
        btn_style = {"font": (self.FONT_BODY[0], 16), "width": 40, "height": 30, "fg_color": "transparent", "text_color": self.COLOR_TEXT_SECONDARY}
        self.close_button = ctk.CTkButton(self.title_bar, text="✕", command=self._close_window, hover_color="#ff4d4d", **btn_style)
        self.close_button.pack(side="right")
        self.maximize_button = ctk.CTkButton(self.title_bar, text="▢", command=self._toggle_maximize, hover_color=self.COLOR_PRIMARY_HOVER, **btn_style)
        self.maximize_button.pack(side="right")
        self.minimize_button = ctk.CTkButton(self.title_bar, text="—", command=self._minimize_window, hover_color=self.COLOR_SECONDARY_HOVER, **btn_style)
        self.minimize_button.pack(side="right")
        self.title_bar.bind("<Button-1>", self._start_move)
        self.title_bar.bind("<B1-Motion>", self._do_move)
        self.title_label.bind("<Button-1>", self._start_move)
        self.title_label.bind("<B1-Motion>", self._do_move)

    def _create_controls_panel(self):
        self.top_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.top_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.top_frame.grid_columnconfigure(5, weight=1)
        btn_style = {"font": self.FONT_BUTTON, "corner_radius": 8, "height": 35, "text_color": "white"}
        self.select_image_button = ctk.CTkButton(self.top_frame, text="Seleccionar Imagen", command=self._select_image, fg_color=self.COLOR_PRIMARY, hover_color=self.COLOR_PRIMARY_HOVER, **btn_style)
        self.select_image_button.grid(row=0, column=0, padx=(10,5), pady=10)
        self.batch_button = ctk.CTkButton(self.top_frame, text="Procesar Carpeta", command=self._select_folder, fg_color=self.COLOR_PRIMARY, hover_color=self.COLOR_PRIMARY_HOVER, **btn_style)
        self.batch_button.grid(row=0, column=1, padx=5, pady=10)
        
        self.help_button = ctk.CTkButton(self.top_frame, text="Ayuda (?)", command=self._show_help_window, fg_color=self.COLOR_SECONDARY, hover_color=self.COLOR_SECONDARY_HOVER, **btn_style)
        self.help_button.grid(row=0, column=2, padx=5, pady=10)
        
        self.extract_button = ctk.CTkButton(self.top_frame, text="Extraer Texto", command=self._start_ocr_process, state="disabled", fg_color=self.COLOR_PRIMARY, hover_color=self.COLOR_PRIMARY_HOVER, **btn_style)
        self.extract_button.grid(row=0, column=6, padx=(5, 10), pady=10)

    def _create_main_workspace(self):
        self.main_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.main_frame.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.image_frame = ctk.CTkFrame(self.main_frame, fg_color=self.COLOR_FRAME, border_width=2, border_color=self.COLOR_PRIMARY)
        self.image_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        self.image_frame.grid_propagate(False)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.clear_image_button = ctk.CTkButton(self.image_frame, text="✕", font=(self.FONT_BODY[0], 20), width=30, height=30, corner_radius=15, fg_color="transparent", hover_color=self.COLOR_PRIMARY_HOVER, command=self._clear_image_selection, text_color=self.COLOR_TEXT_SECONDARY)
        self._create_image_label()
        self.results_container = ctk.CTkFrame(self.main_frame, fg_color=self.COLOR_FRAME, border_width=2, border_color=self.COLOR_SECONDARY)
        self.results_container.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        self.results_container.grid_columnconfigure(1, weight=3)
        self.results_container.grid_rowconfigure(0, weight=1)
        self.file_list_frame = ctk.CTkScrollableFrame(self.results_container, label_text="Archivos Procesados", label_font=self.FONT_BODY, fg_color="#FFFFFF", border_width=0)
        self.file_list_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.text_display_frame = ctk.CTkFrame(self.results_container, fg_color="transparent")
        self.text_display_frame.grid(row=0, column=1, rowspan=2, padx=(5, 10), pady=(0, 10), sticky="nsew")
        self.text_display_frame.grid_rowconfigure(0, weight=1)
        self.text_display_frame.grid_columnconfigure(0, weight=1)
        self.result_textbox = ctk.CTkTextbox(self.text_display_frame, wrap="word", font=self.FONT_BODY, fg_color="#FFFFFF", text_color=self.COLOR_TEXT, border_width=0)
        self.result_textbox.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="nsew")
        self.result_textbox.insert("0.0", "Bienvenido. Seleccione una imagen para comenzar.")
        
        self.actions_frame = ctk.CTkFrame(self.text_display_frame, fg_color="transparent")
        self.actions_frame.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="e")
        action_btn_style = {"width": 40, "height": 30, "corner_radius": 8, "text": ""}
        
        self.clean_text_button = ctk.CTkButton(self.actions_frame, image=self.clean_text_icon, command=self._clean_displayed_text, state="disabled", fg_color=self.COLOR_DISABLED, hover_color=self.COLOR_SECONDARY_HOVER, **action_btn_style)
        self.clean_text_button.pack(side="left", padx=(0, 5))
        Tooltip(self.clean_text_button, "Limpiar formato del texto", self.COLOR_FRAME)

        self.copy_button = ctk.CTkButton(self.actions_frame, image=self.copy_icon, command=self._copy_to_clipboard, state="disabled", fg_color=self.COLOR_DISABLED, hover_color=self.COLOR_SECONDARY_HOVER, **action_btn_style)
        self.copy_button.pack(side="left", padx=(0, 5))
        Tooltip(self.copy_button, "Copiar texto al portapapeles", self.COLOR_FRAME)
        
        self.save_button = ctk.CTkButton(self.actions_frame, image=self.save_icon, command=self._save_to_file, state="disabled", fg_color=self.COLOR_DISABLED, hover_color=self.COLOR_PRIMARY_HOVER, **action_btn_style)
        self.save_button.pack(side="left", padx=(0, 5))
        Tooltip(self.save_button, "Guardar texto en un archivo .txt", self.COLOR_FRAME)

        self.save_all_button = ctk.CTkButton(self.actions_frame, image=self.save_all_icon, command=self._save_all_results, state="disabled", fg_color=self.COLOR_DISABLED, hover_color=self.COLOR_PRIMARY_HOVER, **action_btn_style)
        self.save_all_button.pack(side="left")
        Tooltip(self.save_all_button, "Guardar todos los resultados en archivos .txt individuales", self.COLOR_FRAME)

    def _create_status_bar(self):
        self.status_frame = ctk.CTkFrame(self.main_container, fg_color=self.COLOR_FRAME)
        self.status_frame.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Listo.", text_color=self.COLOR_TEXT, font=self.FONT_BODY)
        self.status_label.pack(side="left", padx=15, pady=8)
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, mode='determinate', progress_color=self.COLOR_SECONDARY)
    
    def _create_image_label(self, image_object=None):
        for widget in self.image_frame.winfo_children():
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkFrame)):
                widget.destroy()
        if image_object:
            self.image_label = ctk.CTkLabel(self.image_frame, text="", image=image_object)
            self.image_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.image_label.image = image_object
            self.clear_image_button.lift()
        else:
            self.empty_state_frame = ctk.CTkFrame(self.image_frame, fg_color="transparent")
            self.empty_state_frame.grid(row=0, column=0, sticky="nsew")
            self.empty_state_frame.grid_columnconfigure(0, weight=1)
            self.empty_state_frame.grid_rowconfigure(0, weight=1)
            self.empty_state_frame.grid_rowconfigure(2, weight=1)
            if self.drop_icon:
                drop_icon_label = ctk.CTkLabel(self.empty_state_frame, text="", image=self.drop_icon)
                drop_icon_label.grid(row=0, column=0, sticky="s", pady=(0, 10))
            drop_text_label = ctk.CTkLabel(self.empty_state_frame, text="Arrastra una imagen aquí\no haz clic en 'Seleccionar Imagen'",
                                           font=(self.FONT_BODY[0], 16, "bold"), text_color="#B0B0B0")
            drop_text_label.grid(row=1, column=0, sticky="n")

    def _select_image(self):
        filepath = filedialog.askopenfilename(filetypes=(("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp"), ("Todos los archivos", "*.*")))
        if not filepath: return
        self.image_paths_to_process = [filepath]
        self._load_and_display_image(filepath)
    
    def _select_folder(self):
        folder_path = filedialog.askdirectory(title="Seleccionar Carpeta para Procesar")
        if not folder_path: return
        image_paths = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
        if image_paths:
            self.image_paths_to_process = image_paths
            self._load_and_display_image(image_paths[0])
            self._update_status(f"{len(image_paths)} imágenes cargadas. Listo para extraer.")
        else:
            self._update_status("Error: No se encontraron imágenes en la carpeta.")
            self.image_paths_to_process.clear()
        self._set_ui_state("normal")

    def _on_drop(self, event):
        filepath = event.data.strip('{}')
        if os.path.isfile(filepath):
            self.image_paths_to_process = [filepath]
            self._load_and_display_image(filepath)

    def _clear_image_selection(self):
        self.image_paths_to_process.clear()
        self.batch_results.clear()
        if self.active_file_button:
            self.active_file_button = None
        self.clear_image_button.place_forget()
        self._create_image_label()
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", "Bienvenido. Seleccione una imagen para comenzar.")
        self._clear_file_list()
        self._set_ui_state("normal")
        self._update_status("Listo.")
    
    def _load_and_display_image(self, filepath):
        try:
            pil_image = Image.open(filepath)
            self._update_status(f"Vista previa: {os.path.basename(filepath)}")
            self.clear_image_button.place(relx=1.0, rely=0.0, anchor="ne", x=-7, y=7)
            self.after(50, lambda: self._update_image_preview(pil_image))
            self._set_ui_state("normal")
        except Exception as e:
            self._update_status(f"Error al cargar la imagen: {e}")
            self.image_paths_to_process.clear()
            self._set_ui_state("normal")

    def _update_image_preview(self, pil_image):
        if not self.image_frame.winfo_exists(): return
        container_width, container_height = self.image_frame.winfo_width() - 40, self.image_frame.winfo_height() - 40
        if container_width <= 1 or container_height <= 1:
            self.after(100, lambda: self._update_image_preview(pil_image))
            return
        original_width, original_height = pil_image.size
        aspect_ratio = original_width / original_height
        new_width, new_height = (container_width, int(container_width / aspect_ratio)) if container_width / aspect_ratio <= container_height else (int(container_height * aspect_ratio), container_height)
        ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(new_width, new_height))
        self._create_image_label(image_object=ctk_image)

    def _start_ocr_process(self):
        if self.image_paths_to_process:
            self._start_batch_ocr_thread(self.image_paths_to_process)
        else:
            self._update_status("Error: Por favor, seleccione una imagen o carpeta primero.")

    def _start_batch_ocr_thread(self, image_paths):
        self._set_ui_state("disabled")
        self.result_textbox.delete("0.0", "end")
        self.batch_results.clear()
        if self.active_file_button:
            self.active_file_button = None
        self._clear_file_list()
        self.progress_bar.pack(side="right", padx=15, pady=8, fill="x", expand=True)
        self.progress_bar.set(0)
        
        selected_color = "auto"
        
        thread = threading.Thread(target=self._ocr_batch_worker, args=(image_paths, selected_color), daemon=True)
        thread.start()
        
    def _ocr_batch_worker(self, image_paths, color):
        total_images = len(image_paths)
        for i, image_path in enumerate(image_paths):
            progress_msg = f"Procesando {i+1}/{total_images}: {os.path.basename(image_path)}"
            self.ocr_result_queue.put(("progress", progress_msg))
            result = use_cases.extraer_texto_de_imagen(self.ocr_service, image_path, color)
            self.batch_results[image_path] = result.strip()
            progress_value = (i + 1) / total_images
            self.ocr_result_queue.put(("progress_update", progress_value))
        self.ocr_result_queue.put(("done", "Proceso finalizado."))

    def _check_ocr_queue(self):
        try:
            message_type, data = self.ocr_result_queue.get_nowait()
            if message_type == "progress": self._update_status(data)
            elif message_type == "progress_update": self.progress_bar.set(data)
            elif message_type == "done": self._process_ocr_result(data)
        except queue.Empty: pass
        finally: self.after(100, self._check_ocr_queue)

    def _process_ocr_result(self, final_message):
        self.progress_bar.set(1)
        self.progress_bar.pack_forget()
        self._update_status(final_message)
        self._populate_file_list()
        if self.batch_results:
            first_button = next(iter(self.file_list_frame.winfo_children()), None)
            if first_button:
                first_button.invoke()
        self.after(50, lambda: self._set_ui_state("normal"))

    def _clear_file_list(self):
        for widget in self.file_list_frame.winfo_children(): widget.destroy()

    def _populate_file_list(self):
        self._clear_file_list()
        self.active_file_button = None
        
        for filepath in self.batch_results.keys():
            filename = os.path.basename(filepath)
            
            texto_resultado = self.batch_results.get(filepath, "")
            sin_texto = not texto_resultado.strip() or "No se encontró texto" in texto_resultado
            
            text_color = "#A0A0A0" if sin_texto else self.COLOR_TEXT_SECONDARY
            display_text = f"📄 {filename}" if sin_texto else filename

            btn = ctk.CTkButton(self.file_list_frame, text=display_text, font=self.FONT_BODY, 
                                fg_color="transparent", text_color=text_color, hover_color=self.COLOR_FRAME, 
                                anchor="w")
            btn.configure(command=lambda f=filepath, b=btn: self._display_text_for_file(f, b))
            btn.pack(fill="x", padx=5, pady=2)

    def _display_text_for_file(self, filepath: str, button_widget: ctk.CTkButton):
        if self.active_file_button:
            self.active_file_button.configure(fg_color="transparent", font=self.FONT_BODY)
        
        button_widget.configure(fg_color=self.COLOR_FRAME, font=(self.FONT_BODY[0], self.FONT_BODY[1], "bold"))
        self.active_file_button = button_widget

        self._load_and_display_image(filepath)
        text = self.batch_results.get(filepath, "Error: No se encontró el texto para este archivo.")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self._set_ui_state("normal")
    
    def _set_ui_state(self, state: str):
        is_normal = state == "normal"
        for widget in [self.select_image_button, self.batch_button, self.help_button]: widget.configure(state=state)
        
        self.extract_button.configure(state="normal" if is_normal and self.image_paths_to_process else "disabled")
        
        has_text = len(self.result_textbox.get("0.0", "end-1c").strip()) > 0
        can_copy_save = is_normal and has_text
        
        if not self.copy_in_progress:
            self.copy_button.configure(state="normal" if can_copy_save else "disabled", fg_color=self.COLOR_SECONDARY if can_copy_save else self.COLOR_DISABLED)
        
        self.save_button.configure(state="normal" if can_copy_save else "disabled", fg_color=self.COLOR_PRIMARY if can_copy_save else self.COLOR_DISABLED)
        
        self.save_all_button.configure(state="normal" if is_normal and len(self.batch_results) > 1 else "disabled",
                                       fg_color=self.COLOR_PRIMARY if is_normal and len(self.batch_results) > 1 else self.COLOR_DISABLED)
        
        self.clean_text_button.configure(state="normal" if can_copy_save else "disabled",
                                         fg_color=self.COLOR_SECONDARY if can_copy_save else self.COLOR_DISABLED)

    def _copy_to_clipboard(self):
        if self.copy_in_progress: return
        text = self.result_textbox.get("0.0", "end-1c")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self._update_status("¡Texto copiado al portapapeles! 💚")
            self.copy_in_progress = True
            self.copy_button.configure(image=None, text="✓", font=(self.FONT_BODY[0], 22, "bold"), fg_color=self.COLOR_SECONDARY_HOVER)
            self.after(1500, self._reset_copy_button)

    def _reset_copy_button(self):
        self.copy_in_progress = False
        self.copy_button.configure(image=self.copy_icon, text="")
        self._set_ui_state("normal")

    def _save_to_file(self):
        text_to_save = self.result_textbox.get("0.0", "end-1c")
        if not text_to_save: return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")], title="Guardar resultado como...")
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as file: file.write(text_to_save)
                self._update_status(f"Archivo guardado en: {os.path.basename(filepath)} 💗")
            except Exception as e: self._update_status(f"Error al guardar archivo: {e}")

    def _save_all_results(self):
        folder_path = filedialog.askdirectory(title="Seleccionar carpeta para guardar los resultados")
        if not folder_path: return

        saved_count = 0
        for filepath, text in self.batch_results.items():
            if not text.strip() or "No se encontró texto" in text:
                continue

            base_name = os.path.basename(filepath)
            file_name_without_ext = os.path.splitext(base_name)[0]
            new_filepath = os.path.join(folder_path, f"{file_name_without_ext}.txt")
            
            try:
                with open(new_filepath, "w", encoding="utf-8") as file:
                    file.write(text)
                saved_count += 1
            except Exception as e:
                self._update_status(f"Error al guardar {base_name}: {e}")
                return

        self._update_status(f"Se guardaron {saved_count} archivos en la carpeta seleccionada.")

    def _clean_displayed_text(self):
        current_text = self.result_textbox.get("1.0", "end-1c")
        if not current_text: return
        
        processed_text = current_text.replace('\n\n', '___PARAGRAPH_BREAK___')
        processed_text = processed_text.replace('\n', ' ')
        final_text = processed_text.replace('___PARAGRAPH_BREAK___', '\n\n')
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", final_text)
        self._update_status("¡Formato de texto limpiado! ✨")

    def _update_status(self, message: str):
        self.status_label.configure(text=message)

    def _show_help_window(self):
        if hasattr(self, 'help_win') and self.help_win.winfo_exists():
            self.help_win.focus()
            return
        self.help_win = ctk.CTkToplevel(self)
        self.help_win.title("Guía de Uso")
        self.help_win.geometry("550x380")
        self.help_win.resizable(False, False)
        self.help_win.transient(self)
        self.help_win.grab_set()
        self.help_win.configure(fg_color=self.COLOR_FRAME)
        self.help_win.grid_columnconfigure(0, weight=1)
        self.help_win.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(self.help_win, text="Consejos para una Detección Exitosa", font=self.FONT_TITLE, text_color=self.COLOR_TEXT).grid(row=0, column=0, padx=20, pady=(20, 10))
        container = ctk.CTkFrame(self.help_win, fg_color=self.COLOR_BACKGROUND)
        container.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        help_text = ("\n💡 Para obtener los mejores resultados:\n\n   •  Iluminación uniforme y sin sombras.\n   •  •  Imagen nítida y bien enfocada.\n   •  •  Buen contraste entre texto y fondo.\n   •  •  Alta resolución para mayor precisión.\n")
        ctk.CTkLabel(container, text=help_text, font=self.FONT_BODY, justify="left", wraplength=480, text_color=self.COLOR_TEXT).pack(padx=15, pady=15, anchor="w")
        ctk.CTkButton(self.help_win, text="Entendido 💚", command=self.help_win.destroy, width=120, font=self.FONT_BUTTON, fg_color=self.COLOR_PRIMARY, hover_color=self.COLOR_PRIMARY_HOVER, text_color="white").grid(row=2, column=0, padx=20, pady=(10, 20))

    def _minimize_window(self):
        alpha = 1.0
        for _ in range(10):
            alpha -= 0.1
            if alpha < 0: alpha = 0
            self.attributes("-alpha", alpha)
            self.update()
            self.after(10)
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()
        self.attributes("-alpha", 1.0)
        self.bind("<Map>", self._on_restore)

    def _toggle_maximize(self):
        self.state('zoomed' if self.state() == 'normal' else 'normal')

    def _start_move(self, event): self.x, self.y = event.x, event.y
    def _do_move(self, event): self.geometry(f"+{self.winfo_x() + event.x - self.x}+{self.winfo_y() + event.y - self.y}")
    def _close_window(self): self.destroy()

def main():
    ocr_service = OcrService()
    app = App(ocr_service=ocr_service)
    app.mainloop()

if __name__ == "__main__":
    main()
