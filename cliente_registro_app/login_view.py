"""
Vista de Login del Sistema
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import Colors, Fonts

class LoginView:
    """Vista de inicio de sesión"""
    
    def __init__(self, parent, on_success_callback, db_controller):
        self.parent = parent
        self.on_success = on_success_callback
        self.db = db_controller
        
        # Configurar el fondo
        self.parent.configure(bg=Colors.BACKGROUND)
        
        # Crear el contenedor principal
        self.main_frame = tk.Frame(parent, bg=Colors.BACKGROUND)
        self.main_frame.pack(expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets de la vista de login"""
        
        # Contenedor de login
        login_container = tk.Frame(
            self.main_frame, 
            bg=Colors.SURFACE, 
            relief=tk.RAISED, 
            bd=1
        )
        login_container.pack(padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(login_container, bg=Colors.SURFACE)
        title_frame.pack(fill=tk.X, padx=40, pady=(30, 20))
        
        title = tk.Label(
            title_frame,
            text="Login",
            font=Fonts.TITLE,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        title.pack()
        
        # Separador
        separator = ttk.Separator(login_container, orient='horizontal')
        separator.pack(fill=tk.X, padx=40, pady=(0, 30))
        
        # Ícono de escudo con usuario
        icon_frame = tk.Frame(login_container, bg=Colors.SURFACE)
        icon_frame.pack(pady=20)
        
        # Crear un canvas para dibujar el ícono
        canvas = tk.Canvas(
            icon_frame, 
            width=100, 
            height=100, 
            bg=Colors.SURFACE,
            highlightthickness=0
        )
        canvas.pack()
        
        # Dibujar escudo
        canvas.create_polygon(
            50, 10, 85, 25, 85, 60, 50, 85, 15, 60, 15, 25,
            fill="#1e293b", outline="#1e293b"
        )
        
        # Dibujar ícono de usuario
        canvas.create_oval(40, 35, 60, 55, fill=Colors.SURFACE, outline=Colors.SURFACE)
        canvas.create_oval(35, 60, 65, 75, fill=Colors.SURFACE, outline=Colors.SURFACE)
        
        # Campo de Usuario
        user_frame = tk.Frame(login_container, bg=Colors.SURFACE)
        user_frame.pack(padx=40, pady=(20, 15), fill=tk.X)
        
        user_label = tk.Label(
            user_frame,
            text="Usuario",
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        user_label.pack(anchor=tk.W)
        
        self.user_entry = tk.Entry(
            user_frame,
            font=Fonts.BODY,
            relief=tk.SOLID,
            bd=1,
            width=35
        )
        self.user_entry.pack(pady=(5, 0))
        self.user_entry.insert(0, "Usuario")
        self.user_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "sin dejar espacio"))
        
        # Campo de Password
        pass_frame = tk.Frame(login_container, bg=Colors.SURFACE)
        pass_frame.pack(padx=40, pady=(0, 30), fill=tk.X)
        
        pass_label = tk.Label(
            pass_frame,
            text="Password",
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        pass_label.pack(anchor=tk.W)
        
        self.pass_entry = tk.Entry(
            pass_frame,
            font=Fonts.BODY,
            relief=tk.SOLID,
            bd=1,
            show="*",
            width=35
        )
        self.pass_entry.pack(pady=(5, 0))
        
        # Botón de Ingresar
        button_frame = tk.Frame(login_container, bg=Colors.SURFACE)
        button_frame.pack(pady=(0, 30))
        
        self.login_button = tk.Button(
            button_frame,
            text="INGRESAR",
            font=Fonts.BUTTON,
            bg=Colors.BACKGROUND,
            fg=Colors.TEXT,
            relief=tk.RAISED,
            bd=1,
            padx=40,
            pady=10,
            cursor="hand2",
            command=self.handle_login
        )
        self.login_button.pack()
        
        # Bind Enter key
        self.parent.bind('<Return>', lambda e: self.handle_login())
    
    def clear_placeholder(self, event, placeholder):
        """Limpiar el placeholder cuando se hace focus"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
    
    def handle_login(self):
        """Manejar el evento de login"""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        
        # Validación simple
        if not username or username == "sin dejar espacio":
            messagebox.showerror("Error", "Por favor ingrese un usuario válido")
            return
        
        if not password:
            messagebox.showerror("Error", "Por favor ingrese su contraseña")
            return
        
        try:
            row = self.db.validate_admin(username, password)
            if row:
                # row includes DNI and Usuario
                admin_dni = row.get("dni") or row.get("DNI")
                messagebox.showinfo("Bienvenido", f"Bienvenido {username}")
                # callback: pass username and optional admin_dni
                self.on_success(username, admin_dni)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error BD", str(e))