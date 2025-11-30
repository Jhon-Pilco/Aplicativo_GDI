"""
Vista Principal (Home) del Sistema
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import Colors, Fonts

class HomeView:
    def __init__(self, parent, username, logout_callback, app_instance, db_controller):
        self.parent = parent
        self.username = username
        self.logout_callback = logout_callback
        self.app = app_instance
        self.db = db_controller
        self.current_view = None
        
        self.parent.configure(bg=Colors.BACKGROUND)
        self.create_widgets()
        self.show_inicio()
    
    def create_widgets(self):
        """Crear los widgets de la vista principal"""
        
        # Header
        header = tk.Frame(self.parent, bg=Colors.SURFACE, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Contenedor del header
        header_content = tk.Frame(header, bg=Colors.SURFACE)
        header_content.pack(expand=True, fill=tk.BOTH, padx=20)
        
        # Sección izquierda del header (logo/brand)
        left_header = tk.Frame(header_content, bg=Colors.SURFACE)
        left_header.pack(side=tk.LEFT, fill=tk.Y)
        
        # Placeholder para logo
        logo_canvas = tk.Canvas(
            left_header,
            width=50,
            height=50,
            bg=Colors.BACKGROUND,
            highlightthickness=0
        )
        logo_canvas.pack(side=tk.LEFT, pady=15)
        
        # Dibujar ícono de usuarios
        logo_canvas.create_oval(15, 10, 35, 30, fill=Colors.TEXT_SECONDARY)
        logo_canvas.create_oval(10, 25, 40, 45, fill=Colors.TEXT_SECONDARY)
        
        # Información de la empresa
        company_info = tk.Frame(left_header, bg=Colors.SURFACE)
        company_info.pack(side=tk.LEFT, padx=(10, 0), pady=15)
        
        company_lines = tk.Label(
            company_info,
            text="━━━━━━━━\n━━━━━━━━━━━━\n━━━━━━━━━━━━━━━━━",
            font=("Courier", 8),
            bg=Colors.SURFACE,
            fg=Colors.TEXT_SECONDARY
        )
        company_lines.pack(anchor=tk.W)
        
        # Navegación principal
        nav_frame = tk.Frame(header_content, bg=Colors.SURFACE)
        nav_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=50)
        
        # Botones de navegación
        nav_buttons = [
            ("Inicio", self.show_inicio),
            ("Clientes", self.show_clients),
            ("Reportes", self.show_reports),
            ("Ayuda", self.show_help),
            ("Configuracion", self.show_config)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=Fonts.BODY,
                bg=Colors.SURFACE,
                fg=Colors.TEXT,
                bd=0,
                padx=15,
                pady=25,
                cursor="hand2",
                activebackground=Colors.BACKGROUND,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Sección derecha del header (usuario)
        right_header = tk.Frame(header_content, bg=Colors.SURFACE)
        right_header.pack(side=tk.RIGHT, fill=tk.Y)
        
        user_info = tk.Frame(right_header, bg=Colors.SURFACE)
        user_info.pack(pady=20)
        
        user_label = tk.Label(
            user_info,
            text=self.username,  # Usando nombre fijo como en el diseño
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        user_label.pack(side=tk.LEFT)
        
        # Ícono de usuario
        user_canvas = tk.Canvas(
            user_info,
            width=40,
            height=40,
            bg=Colors.TEXT,
            highlightthickness=0
        )
        user_canvas.pack(side=tk.LEFT, padx=(10, 0))
        user_canvas.create_oval(12, 8, 28, 24, fill=Colors.SURFACE)
        user_canvas.create_oval(8, 20, 32, 36, fill=Colors.SURFACE)
        
        # Área de contenido principal
        self.content_area = tk.Frame(self.parent, bg=Colors.BACKGROUND)
        self.content_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def clear_content(self):
        """Limpiar el área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_inicio(self):
        """Mostrar la vista de inicio"""
        self.clear_content()
        
        # Contenedor principal
        container = tk.Frame(self.content_area, bg=Colors.SURFACE)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Área de contenido con imagen placeholder
        content_frame = tk.Frame(container, bg=Colors.BACKGROUND, height=300)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Canvas para imagen placeholder
        canvas = tk.Canvas(
            content_frame,
            bg=Colors.BACKGROUND,
            highlightthickness=0
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Dibujar placeholder de imagen
        def draw_placeholder(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            if w > 1 and h > 1:
                canvas.create_rectangle(
                    50, 50, w - 50, h - 50,
                    fill=Colors.TEXT_SECONDARY,
                    outline=""
                )
                # Ícono de imagen
                center_x = w // 2
                center_y = h // 2
                canvas.create_oval(
                    center_x - 25, center_y - 25,
                    center_x + 25, center_y + 25,
                    fill=Colors.SURFACE
                )
                canvas.create_polygon(
                    center_x - 50, center_y + 30,
                    center_x + 50, center_y + 30,
                    center_x, center_y - 70,
                    fill=Colors.SURFACE
                )
        
        canvas.bind('<Configure>', draw_placeholder)
        self.parent.after(100, draw_placeholder)
        
        # Botón Salir
        button_frame = tk.Frame(container, bg=Colors.SURFACE)
        button_frame.pack(pady=20)
        
        logout_btn = tk.Button(
            button_frame,
            text="Salir",
            font=Fonts.BUTTON,
            bg=Colors.BACKGROUND,
            fg=Colors.TEXT,
            relief=tk.RAISED,
            bd=1,
            padx=30,
            pady=8,
            cursor="hand2",
            command=self.handle_logout
        )
        logout_btn.pack()
    
    def show_clients(self):
        self.clear_content()
        from client_view import ClientView
        self.current_view = ClientView(self.content_area, self.db, admin_dni=self.app.current_admin_dni)

    def show_reports(self):
        self.clear_content()
        from reports_view import ReportsView
        self.current_view = ReportsView(self.content_area, self.db, back_callback=self.show_inicio)

    def show_config(self):
        self.clear_content()
        from config_view import ConfigView
        self.current_view = ConfigView(self.content_area, self.db)

    def show_help(self):
        self.clear_content()
        from help_view import HelpView
        self.current_view = HelpView(self.content_area)
    
    def handle_logout(self):
        response = messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?")
        if response:
            self.clear_content()
            self.logout_callback()