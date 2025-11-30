"""
Vista del Módulo de Configuración
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import Colors, Fonts

class ConfigView:
    """Vista del módulo de configuración"""
    
    def __init__(self, parent, db_controller):
        self.parent = parent
        self.db = db_controller
        # Frame principal
        self.main_frame = tk.Frame(parent, bg=Colors.SURFACE)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets de la vista de configuración"""
        
        # Header con botón INICIO
        header_frame = tk.Frame(self.main_frame, bg=Colors.SURFACE)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        inicio_btn = tk.Button(
            header_frame,
            text="INICIO",
            font=Fonts.BODY,
            bg=Colors.BACKGROUND,
            fg=Colors.TEXT,
            relief=tk.RAISED,
            bd=1,
            padx=20,
            pady=5,
            cursor="hand2"
        )
        inicio_btn.pack(side=tk.LEFT)
        
        # Título
        title = tk.Label(
            self.main_frame,
            text="Configuracion",
            font=Fonts.SUBTITLE,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        title.pack(pady=(0, 20))
        
        # Contenedor principal con dos columnas
        content_frame = tk.Frame(self.main_frame, bg=Colors.SURFACE)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Menú de configuración
        left_panel = tk.Frame(content_frame, bg=Colors.BACKGROUND, relief=tk.SOLID, bd=1, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Opciones del menú
        menu_options = [
            ("Administradores settings  ▶", self.show_admin_settings),
            ("Statistics", self.show_statistics),
            ("Notifications", self.show_notifications),
            ("Payments", self.show_payments)
        ]
        
        for text, command in menu_options:
            btn = tk.Button(
                left_panel,
                text=text,
                font=Fonts.BODY,
                bg=Colors.BACKGROUND,
                fg=Colors.TEXT,
                bd=0,
                anchor=tk.W,
                padx=20,
                pady=15,
                cursor="hand2",
                command=command
            )
            btn.pack(fill=tk.X)
        
        # Separador
        separator = ttk.Separator(left_panel, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        # Botón Sign out
        signout_btn = tk.Button(
            left_panel,
            text="Sign out",
            font=Fonts.BODY,
            bg=Colors.BACKGROUND,
            fg=Colors.DANGER,
            bd=0,
            anchor=tk.W,
            padx=20,
            pady=15,
            cursor="hand2",
            command=self.sign_out
        )
        signout_btn.pack(fill=tk.X)
        
        # Panel derecho - Formulario
        self.right_panel = tk.Frame(content_frame, bg=Colors.SURFACE)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Mostrar configuración de administradores por defecto
        self.show_admin_settings()
    
    def clear_right_panel(self):
        """Limpiar el panel derecho"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()
    
    def show_admin_settings(self):
        """Mostrar configuración de administradores"""
        self.clear_right_panel()
        
        # Título del formulario
        form_title = tk.Label(
            self.right_panel,
            text="Nuevo Administrador",
            font=Fonts.HEADING,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        form_title.pack(pady=(0, 30))
        
        # Formulario
        form_frame = tk.Frame(self.right_panel, bg=Colors.SURFACE)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50)
        
        # DNI
        self.dni_entry = self.create_config_field(form_frame, "DNI", "8 digitos")
        self.nombre_entry = self.create_config_field(form_frame, "Nombre", "")
        self.usuario_entry = self.create_config_field(form_frame, "Usuario", "sin dejar espacio")
        self.contrasena_entry = self.create_config_field(form_frame, "Contraseña", "minimo 8 caracteres", show="*")
        self.telefono_entry = self.create_config_field(form_frame, "Telefono", "9 digitos")
        self.correo_entry = self.create_config_field(form_frame, "Correo", "@dominio.com")
        
        # Botón Registrar
        button_frame = tk.Frame(form_frame, bg=Colors.SURFACE)
        button_frame.pack(pady=30)
        
        register_btn = tk.Button(
            button_frame,
            text="Registrar",
            font=Fonts.BUTTON,
            bg=Colors.BACKGROUND,
            fg=Colors.TEXT,
            relief=tk.RAISED,
            bd=1,
            padx=40,
            pady=10,
            cursor="hand2",
            command=self.register_admin
        )
        register_btn.pack()
    
    def create_config_field(self, parent, label, placeholder, show=None):
        """Crear un campo del formulario de configuración"""
        frame = tk.Frame(parent, bg=Colors.SURFACE)
        frame.pack(fill=tk.X, pady=10)
        
        label_widget = tk.Label(
            frame,
            text=label,
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT,
            width=12,
            anchor=tk.W
        )
        label_widget.grid(row=0, column=0, padx=(0, 20))
        
        entry = tk.Entry(
            frame,
            font=Fonts.BODY,
            relief=tk.SOLID,
            bd=1,
            width=35,
            show=show if show else ""
        )
        entry.grid(row=0, column=1)
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, placeholder))
        
        return entry
    
    def clear_placeholder(self, event, placeholder):
        """Limpiar el placeholder cuando se hace focus"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
    
    def show_statistics(self):
        """Mostrar estadísticas"""
        self.clear_right_panel()
        
        title = tk.Label(
            self.right_panel,
            text="Estadísticas",
            font=Fonts.HEADING,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        title.pack(pady=20)
        
        info = tk.Label(
            self.right_panel,
            text="Módulo de estadísticas en desarrollo",
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_SECONDARY
        )
        info.pack(pady=50)
    
    def show_notifications(self):
        """Mostrar notificaciones"""
        self.clear_right_panel()
        
        title = tk.Label(
            self.right_panel,
            text="Notificaciones",
            font=Fonts.HEADING,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        title.pack(pady=20)
        
        info = tk.Label(
            self.right_panel,
            text="Configuración de notificaciones en desarrollo",
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_SECONDARY
        )
        info.pack(pady=50)
    
    def show_payments(self):
        """Mostrar pagos"""
        self.clear_right_panel()
        
        title = tk.Label(
            self.right_panel,
            text="Pagos",
            font=Fonts.HEADING,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        title.pack(pady=20)
        
        info = tk.Label(
            self.right_panel,
            text="Módulo de pagos en desarrollo",
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_SECONDARY
        )
        info.pack(pady=50)
    
    def register_admin(self):
        """Registrar nuevo administrador"""
        dni = self.dni_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        correo = self.correo_entry.get().strip()

        if not (dni and nombre and usuario and contrasena and telefono and correo):
            messagebox.showwarning("Validación", "Complete todos los campos")
            return

        try:
            self.db.insert_administrator(dni, nombre, usuario, contrasena, telefono, correo)
            messagebox.showinfo("Éxito", "Administrador registrado correctamente")
            # limpiar campos
            for e in [self.dni_entry, self.nombre_entry, self.usuario_entry, self.contrasena_entry, self.telefono_entry, self.correo_entry]:
                e.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error BD", str(e))
    
    def sign_out(self):
        """Cerrar sesión"""
        response = messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?")
        if response:
            messagebox.showinfo("Sesión", "Sesión cerrada")