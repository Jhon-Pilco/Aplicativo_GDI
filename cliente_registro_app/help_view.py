"""
Vista del Módulo de Ayuda
"""

import tkinter as tk
from tkinter import ttk
from styles import Colors, Fonts

class HelpView:
    """Vista del módulo de ayuda con navegación dinámica."""

    def __init__(self, parent):
        self.parent = parent

        # Crear frame principal
        self.main_frame = tk.Frame(parent, bg=Colors.SURFACE)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Diccionario de textos de ayuda
        self.help_texts = {
            "Inicio Rápido":
            """
El módulo “Inicio Rápido” le permitirá familiarizarse con el funcionamiento general del sistema.

1. Inicie sesión con un usuario administrador válido.
2. Navegue usando el menú lateral:
   • Registro de Clientes
   • Reportes
   • Configuración
   • Ayuda
3. El sistema es intuitivo y cada vista muestra solo las opciones necesarias.
4. Antes de registrar clientes, asegúrese de que la base de datos esté correctamente configurada.
5. Desde cualquier parte del sistema puede volver al módulo de ayuda.

El objetivo es que cualquier administrador pueda usar el sistema sin capacitación adicional.
            """,

            "Gestión de Clientes":
            """
El módulo de Gestión de Clientes permite registrar y administrar clientes corporativos y mayoristas.

FUNCIONES PRINCIPALES:

1. Registrar cliente
   - Complete los campos obligatorios.
   - Valida DNI, RUC y evita duplicados.
   - Pulse “Guardar” para registrar.

2. Editar cliente
   - Seleccione un cliente.
   - Pulse “Editar”.
   - Modifique los datos y guarde.

3. Eliminar cliente
   - Seleccione un cliente.
   - Pulse “Eliminar”.
   - Confirme la operación.

4. Búsqueda y filtrado
   - Busque por nombre, empresa o tipo.
   - La tabla se actualiza automáticamente.

5. Validaciones
   - No permite datos incompletos o en formato incorrecto.

Este módulo mantiene la base de datos ordenada y confiable.
            """,

            "Generación de Reportes":
            """
El módulo de Reportes permite consultar y analizar la información de clientes y contratos.

1. Selección de reporte
   - Elija entre consultas como:
     • Clientes nuevos por fechas festivas
     • Contratos activos por mes
     • Cobertura geográfica
     • Clientes con información incompleta

2. Visualización
   - Los resultados se muestran en tabla.
   - Puede desplazarse para ver más información.

3. Gráficos
   - Algunos reportes generan gráficos automáticos (barras o pastel).

4. Exportación
   - Puede guardar los reportes en:
     • CSV
     • PDF

5. Actualización automática
   - Cada reporte se recarga al seleccionarlo.

Diseñado para análisis rápido y presentaciones.
            """,

            "Configuración":
            """
El módulo de Configuración gestiona ajustes internos del sistema.

1. Gestión de administradores
   - Crear usuarios admin
   - Cambiar contraseñas
   - Eliminar usuarios

2. Personalización
   - Ajustes visuales (si están habilitados)
   - Texto de pie de página para PDF

3. Seguridad
   - Contraseñas encriptadas
   - Acceso limitado solo a administradores

4. Parámetros generales
   - Rutas de exportación
   - Conexión a base de datos

Use esta sección solo si tiene permisos administrativos.
            """,

            "Preguntas Frecuentes":
            """
PREGUNTAS FRECUENTES:

1. No puedo iniciar sesión
   - Verifique usuario y contraseña.
   - Pida reseteo al administrador.

2. No puedo guardar un cliente
   - Revise campos obligatorios.
   - DNI o RUC podría estar registrado.

3. El reporte no muestra gráfico
   - Algunos reportes no tienen datos estadísticos.

4. ¿Cómo exporto reportes?
   - Seleccione el reporte y pulse Exportar CSV o PDF.

5. ¿Puedo agregar un logo al sistema?
   - Sí, desde Configuración (si está habilitado).

Si necesita más ayuda, revise la sección de soporte.
            """,

            "Soporte Técnico":
            """
Si necesita asistencia técnica, puede contactar al equipo encargado:

• Correo: soporte@sistema.com
• Teléfono: (01) 234-5678
• Horario: Lunes a Viernes — 9:00 a 18:00

Incluya en su reporte:
- Captura de pantalla del error
- Pasos realizados
- Fecha y hora del incidente
- Usuario administrador

Esto permitirá una atención más rápida y precisa.
            """
        }

        self.create_main_menu()

    # ----------------------------------------------------------------------
    # 1. Vista principal con opciones
    # ----------------------------------------------------------------------
    def create_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.main_frame, text="Centro de Ayuda",
            font=Fonts.TITLE, bg=Colors.SURFACE, fg=Colors.TEXT
        )
        title.pack(pady=20)

        menu_frame = tk.Frame(self.main_frame, bg=Colors.SURFACE)
        menu_frame.pack(pady=10)

        for section in self.help_texts.keys():
            btn = tk.Button(
                menu_frame,
                text=section,
                font=Fonts.BUTTON,
                bg=Colors.BACKGROUND,
                fg=Colors.TEXT,
                relief=tk.RAISED,
                padx=20, pady=5,
                command=lambda s=section: self.show_section(s)
            )
            btn.pack(fill=tk.X, pady=8)

    # ----------------------------------------------------------------------
    # 2. Vista de texto + scroll
    # ----------------------------------------------------------------------
    def show_section(self, section_name):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Botón Volver
        back_btn = tk.Button(
            self.main_frame, text="← Volver",
            font=Fonts.BUTTON,
            bg=Colors.BACKGROUND,
            fg=Colors.TEXT,
            command=self.create_main_menu,
            padx=10, pady=5
        )
        back_btn.pack(anchor=tk.W, pady=10, padx=10)

        # Título
        title = tk.Label(
            self.main_frame,
            text=section_name,
            font=Fonts.SUBTITLE,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        title.pack(pady=(0, 10))

        # Frame con scroll
        content_frame = tk.Frame(self.main_frame, bg=Colors.SURFACE)
        content_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_frame, bg=Colors.SURFACE)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=Colors.SURFACE)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Texto
        label = tk.Label(
            scroll_frame,
            text=self.help_texts[section_name],
            font=Fonts.BODY,
            bg=Colors.SURFACE,
            fg=Colors.TEXT,
            justify=tk.LEFT,
            wraplength=750
        )
        label.pack(anchor=tk.W, padx=20, pady=10)

