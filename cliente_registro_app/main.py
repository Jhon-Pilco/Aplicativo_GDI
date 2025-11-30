#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Registro de Clientes
Aplicación principal con arquitectura MVC
"""

import tkinter as tk
from tkinter import ttk, messagebox
from login_view import LoginView
from home_view import HomeView
from styles import Colors, Fonts
from db_controller import DBController

class ClientRegistrationApp:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Registro de Clientes")
        self.client_type = tk.StringVar(value="minorista")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Conexión BD
        try:
            self.db = DBController()
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo conectar a la BD: {e}")
            raise
        
        # Configurar estilo
        self.setup_styles()
        
        # Variable para el usuario actual
        self.current_user = None
        self.current_admin_dni = None  # opcional: guardar DNI del admin logueado
        
        # Centrar la ventana
        self.center_window()
        
        # Iniciar con la vista de login (pasamos db)
        self.show_login()
    
    def setup_styles(self):
        """Configurar estilos ttk globales"""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('Title.TLabel', font=Fonts.TITLE)
        style.configure('Subtitle.TLabel', font=Fonts.SUBTITLE)
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width() or 1200
        height = self.root.winfo_height() or 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_login(self):
        """Mostrar la vista de login"""
        self.clear_window()
        # Pass db and a callback that receives admin_dni (optional)
        LoginView(self.root, self.on_login_success, self.db)
    
    def show_home(self):
        """Mostrar la vista principal"""
        self.clear_window()
        HomeView(self.root, self.current_user, self.on_logout, self, self.db)
    
    def clear_window(self):
        """Limpiar todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def on_login_success(self, username, admin_dni=None):
        """Callback cuando el login es exitoso"""
        self.current_user = username
        self.current_admin_dni = admin_dni
        self.show_home()
    
    def on_logout(self):
        """Callback para cerrar sesión"""
        self.current_user = None
        self.current_admin_dni = None
        self.show_login()
    
    def run(self):
        """Iniciar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ClientRegistrationApp()
    app.run()   
