import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from db_controller import DBController
from styles import Colors, Fonts

# Normalizamos los tipos que usará la UI/DB
CLIENT_TYPES = {
    "MINORISTA": "minorista",
    "MAYORISTA": "mayorista",
    "CORPORATIVO": "corporativo",
    "TODOS": "Todos"
}


class ClientView:
    def __init__(self, parent, db: DBController, admin_dni=None):
        self.parent = parent
        self.db = db
        self.admin_dni = admin_dni
        self.client_type = tk.StringVar(value="")   # valores: 'minorista','mayorista','corporativo'
        self.selected_filter = "Todos"
        self.search_term = tk.StringVar()
        self.client_vars = {}  # Para almacenar variables de formulario (StringVar / Text)

        # Frame principal
        self.main_frame = tk.Frame(self.parent, bg=Colors.BACKGROUND)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear widgets de la UI
        self.create_widgets()

        # Cargar datos iniciales
        self.load_data_from_db()

    # ------------------- CREATE_WIDGETS -------------------
    def create_widgets(self):
        """Crear los widgets de la vista de clientes con soporte CRUD"""
        # Header
        header_frame = tk.Frame(self.main_frame, bg=Colors.SURFACE)
        header_frame.pack(fill=tk.X, padx=20, pady=20)

        title = tk.Label(
            header_frame,
            text="Clientes",
            font=Fonts.SUBTITLE,
            bg=Colors.SURFACE,
            fg=Colors.TEXT
        )
        title.pack(side=tk.LEFT)

        controls_frame = tk.Frame(header_frame, bg=Colors.SURFACE)
        controls_frame.pack(side=tk.RIGHT)

        # Búsqueda
        search_frame = tk.Frame(controls_frame, bg=Colors.SURFACE)
        search_frame.pack(side=tk.LEFT, padx=5)

        search_icon = tk.Label(
            search_frame,
            text="🔍",
            font=Fonts.BODY,
            bg=Colors.SURFACE
        )
        search_icon.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_term,
            font=Fonts.BODY,
            relief=tk.SOLID,
            bd=1,
            width=20
        )
        self.search_entry.pack(side=tk.LEFT, padx=(5, 0))
        # placeholder simple
        self.search_entry.insert(0, "Búsqueda R")
        self.search_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Búsqueda R"))
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_data_from_db())

        # Botón Nuevo
        new_btn = tk.Button(
            controls_frame,
            text="+ Nuevo",
            font=Fonts.BUTTON,
            bg=Colors.SUCCESS,
            fg="white",
            relief=tk.RAISED,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.show_new_client_form
        )
        new_btn.pack(side=tk.LEFT, padx=5)

        # Botón Actualizar (para editar el cliente seleccionado)
        update_btn = tk.Button(
            controls_frame,
            text="Actualizar",
            font=Fonts.BUTTON,
            bg=Colors.PRIMARY,
            fg="white",
            relief=tk.RAISED,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.edit_selected_client
        )
        update_btn.pack(side=tk.LEFT, padx=5)

        # Botón Eliminar
        delete_btn = tk.Button(
            controls_frame,
            text="Eliminar",
            font=Fonts.BUTTON,
            bg=Colors.DANGER,
            fg="white",
            relief=tk.RAISED,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.delete_selected_clients
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        # Panel izquierdo para filtro de tipo
        content_frame = tk.Frame(self.main_frame, bg=Colors.SURFACE)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_panel = tk.Frame(content_frame, bg=Colors.BACKGROUND, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        self.filter_button = tk.Button(
            left_panel,
            text="Tipo Cliente    ▶",
            font=Fonts.BODY,
            bg=Colors.BACKGROUND,
            fg=Colors.TEXT,
            bd=0,
            anchor=tk.W,
            padx=10,
            pady=10,
            cursor="hand2",
            command=self.toggle_filter_menu
        )
        self.filter_button.pack(fill=tk.X)

        self.filter_frame = tk.Frame(left_panel, bg=Colors.BACKGROUND)

        filter_options = [
            ("Todos", lambda: self.select_filter("Todos")),
            ("Cliente Minorista", lambda: self.select_filter("Minorista")),
            ("Cliente Mayorista", lambda: self.select_filter("Mayorista")),
            ("Cliente Corporativo", lambda: self.select_filter("Corporativo"))
        ]
        for text, cmd in filter_options:
            btn = tk.Button(
                self.filter_frame,
                text=f"  {text}",
                font=Fonts.BODY,
                bg=Colors.BACKGROUND,
                fg=Colors.TEXT,
                bd=0,
                anchor=tk.W,
                padx=20,
                pady=8,
                cursor="hand2",
                command=cmd
            )
            btn.pack(fill=tk.X, pady=1)

        # Panel derecho: la tabla
        right_panel = tk.Frame(content_frame, bg=Colors.SURFACE)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        table_frame = tk.Frame(right_panel, bg=Colors.SURFACE)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('codigo', 'nombre', 'tipo', 'telefono', 'correo')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        self.tree.heading('codigo', text='Código')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('tipo', text='Tipo')
        self.tree.heading('telefono', text='Teléfono')
        self.tree.heading('correo', text='Correo')

        self.tree.column('codigo', width=100)
        self.tree.column('nombre', width=200)
        self.tree.column('tipo', width=120)
        self.tree.column('telefono', width=120)
        self.tree.column('correo', width=200)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Bind del doble clic con manejo seguro
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ------------------- METODOS AUXILIARES -------------------
    def clear_placeholder(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)

    def toggle_filter_menu(self):
        if self.filter_frame.winfo_ismapped():
            self.filter_frame.pack_forget()
        else:
            self.filter_frame.pack(fill=tk.X)

    def select_filter(self, filter_name):
        self.selected_filter = filter_name
        self.filter_button.config(text=f"Tipo Cliente    ▶ {filter_name}")
        self.load_data_from_db()

    # ------------------- CRUD -------------------
    def load_data_from_db(self):
        """Carga clientes desde BD y muestra en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            clients = self.db.get_all_clients()
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo obtener clientes: {e}")
            return

        term = self.search_term.get().strip().lower()

        for c in clients:
            tipo = c.get('tipo', '')
            codigo = str(c.get('codigo', '') or '')
            nombre = c.get('nombre', '')
            correo = c.get('correo', '') or ''
            telefono = c.get('telefono', '') or ''

            # filtro por tipo si se seleccionó algo distinto de "Todos"
            if self.selected_filter != "Todos" and tipo.lower() != self.selected_filter.lower():
                continue

            if term:
                if term not in codigo.lower() and term not in (nombre or '').lower():
                    continue

            self.tree.insert("", "end", values=(codigo, nombre, tipo.capitalize(), telefono, correo))

    def on_tree_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = sel[0]
        data = self.tree.item(item, "values")
        if not data:
            return
        client_code = data[0]
        try:
            client_data = self.db.get_client_by_code(client_code)
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo obtener el cliente: {e}")
            return
        if client_data:
            self.show_edit_client_form(client_data)

    # ------------------- FORMULARIOS -------------------
    def show_new_client_form(self):
        self.client_vars = {}
        self.choose_client_type()

    def choose_client_type(self):
        type_window = tk.Toplevel(self.parent)
        type_window.title("Seleccionar tipo de cliente")
        type_window.geometry("300x220")
        type_window.transient(self.parent)
        type_window.grab_set()

        label = tk.Label(type_window, text="Seleccione el tipo de cliente", font=Fonts.SUBTITLE)
        label.pack(pady=15)

        def select_type(tipo):
            # esperamos recibir la forma normalizada en minúscula
            self.client_type.set(tipo)
            type_window.destroy()
            self._show_form_window("Nuevo Cliente")

        tk.Button(type_window, text="Cliente Minorista", width=24,
                  command=lambda: select_type(CLIENT_TYPES["MINORISTA"])).pack(pady=5)
        tk.Button(type_window, text="Cliente Mayorista", width=24,
                  command=lambda: select_type(CLIENT_TYPES["MAYORISTA"])).pack(pady=5)
        tk.Button(type_window, text="Cliente Corporativo", width=24,
                  command=lambda: select_type(CLIENT_TYPES["CORPORATIVO"])).pack(pady=5)

    def show_edit_client_form(self, client_data):
        tipo = client_data.get("tipo", "minorista").lower()
        self.client_type.set(tipo)
        self.client_vars = {}
        self._show_form_window("Editar Cliente", client_data)

    def _show_form_window(self, title, client_data=None):
        form_window = tk.Toplevel(self.parent)
        form_window.title(title)
        form_window.geometry("800x700")
        form_window.resizable(False, False)
        form_window.transient(self.parent)
        form_window.grab_set()

        self.editing_client = bool(client_data)
        # original_code se usa para update (DNI o RUC original)
        self.editing_code = client_data.get("codigo") if (isinstance(client_data, dict) and "codigo" in client_data) else None

        main_container = tk.Frame(form_window, bg=Colors.SURFACE)
        main_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_container, bg=Colors.SURFACE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)

        self.fields_container = tk.Frame(canvas, bg=Colors.SURFACE)
        self.fields_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.fields_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ---------------- MOUSEWHEEL ----------------
        def _on_mousewheel(event):
            if not canvas.winfo_exists():
                return
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        form_window.bind_all("<MouseWheel>", _on_mousewheel)

        # Actualizar formulario (crea widgets según tipo)
        self.update_form_fields(form_window, canvas)

        # ---------------- CARGA DE DATOS SI ES EDICIÓN ----------------
        if client_data:
            # client_data proviene de DBController y tiene nombres de columnas
            # Mapeamos a las keys que usamos en client_vars (las etiquetas del formulario)
            # Simple approach: probamos varias claves posibles
            for key, widget in self.client_vars.items():
                # widget puede ser StringVar o tk.Text
                # Buscamos en client_data por posibles nombres:
                possible_names = [
                    key,  # etiqueta tal como la usamos ("DNI", "Nombre_Apellido", "Razon Social", etc.)
                    key.replace(" ", "_"),  # "Razon Social" -> "Razon_Social"
                    key.replace(" ", "_").replace("-", "_"),
                    key.lower(),
                    key.upper(),
                ]
                # además tratamos de consultar nombres esperados por la BD:
                # map de etiquetas -> columna
                col = self._label_to_column(key)
                val = None
                if col and col in client_data:
                    val = client_data.get(col)
                else:
                    # fallback: buscar por cualquiera de possible_names en client_data
                    for nm in possible_names:
                        if nm in client_data:
                            val = client_data.get(nm)
                            break
                if val is None:
                    # intentamos por nombres tradicionales en DBController
                    for nm in ["codigo", "nombre", "Direccion", "Direccion_Fiscal", "Telefono", "Correo",
                               "Preferencias", "Descripcion", "Fecha_inicio", "Fecha_vencimiento", "Estado",
                               "DNI_contacto", "DNI_administrador"]:
                        if nm in client_data:
                            # si coincide el label con el sufijo del nombre, intentar
                            if nm.lower().startswith(key.replace(" ", "_").lower()[:3]):
                                val = client_data.get(nm)
                                break

                if isinstance(widget, tk.StringVar):
                    widget.set("" if val is None else str(val))
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    if val is not None:
                        widget.insert("1.0", str(val))

        # ---------------- BOTÓN GUARDAR ----------------
        # Reasignar comando al botón guardar creado en create_form_buttons (si existe)
        for child in self.fields_container.winfo_children():
            for widget in child.winfo_children():
                if isinstance(widget, tk.Button) and widget.cget("text") in ["Guardar", "Crear"]:
                    widget.config(command=lambda w=form_window: self.save_client(
                        w,
                        is_update=getattr(self, 'editing_client', False),
                        original_code=getattr(self, 'editing_code', None)
                    ))

    # ---------------- MAPEOS ----------------
    def _label_to_column(self, label):
        """
        Mapea las etiquetas/labels del formulario a nombres de columna en la BD.
        Ej: "Razon Social" -> "Razon_Social", "DNI Contacto" -> "DNI_contacto"
        """
        mapping = {
            "DNI": "DNI",
            "RUC": "RUC",
            "Nombre_Apellido": "Nombre_Apellido",
            "Nombre": "Nombre_Apellido",
            "Razon Social": "Razon_Social",
            "Direccion": "Direccion",
            "Direccion Fiscal": "Direccion_Fiscal",
            "Correo": "Correo",
            "Telefono": "Telefono",
            "Preferencias": "Preferencias",
            "Descripcion": "Descripcion",
            "Fecha Inicio": "Fecha_inicio",
            "Fecha Vencimiento": "Fecha_vencimiento",
            "Estado": "Estado",
            "DNI Contacto": "DNI_contacto",
            "Telefono Contacto": "Telefono",  # en DatosClienteCorporativo la columna es Telefono
        }
        return mapping.get(label, label.replace(" ", "_"))

    # ------------------- FORMULARIOS POR TIPO -------------------
    def create_minorista_form(self):
        # Campos tal como serán las etiquetas
        fields = [
            ("DNI", "8 digitos"),
            ("Nombre_Apellido", "Nombre completo"),
            ("Direccion", ""),
            ("Correo", "@dominio.com"),
            ("Telefono", "9 digitos")
        ]
        for label, placeholder in fields:
            self.create_form_field(label, placeholder)

        self.create_form_field("Preferencias", "max 200 palabras", text_widget=True)
        self.create_form_buttons()

    def create_mayorista_form(self):
        fields = [
            ("RUC", "11 digitos"),
            ("Razon Social", "Nombre empresa"),
            ("Direccion Fiscal", ""),
            ("Correo", "@gmail.com"),
            ("Telefono", "9 digitos")
        ]
        for label, placeholder in fields:
            self.create_form_field(label, placeholder)

        self.create_form_buttons()

    def create_corporativo_form(self):
        # IMPORTANTE: pedimos DNI del contacto (FK), no nombre
        fields = [
            ("RUC", "11 digitos"),
            ("Razon Social", "Nombre empresa"),
            ("Direccion Fiscal", ""),
            ("Correo", "@gmail.com"),
            ("Telefono", "9 digitos"),
            ("DNI Contacto", "8 digitos"),      # debe existir en tabla Contacto
            ("Telefono Contacto", "9 digitos"), # irá a DatosClienteCorporativo (Telefono)
            ("Descripcion", "Max 200"),
            ("Fecha Inicio", datetime.now().strftime("%Y-%m-%d")),
            ("Fecha Vencimiento", datetime.now().strftime("%Y-%m-%d"))
        ]

        for label, placeholder in fields:
            self.create_form_field(label, placeholder)

        # Estado del contrato / cliente
        self.client_vars["Estado"] = tk.StringVar(value="Activo")
        frame_state = tk.Frame(self.fields_container, bg=Colors.SURFACE)
        frame_state.pack(fill=tk.X, pady=10)

        tk.Radiobutton(frame_state, text="Activo", variable=self.client_vars["Estado"],
                       value="Activo", bg=Colors.SURFACE, fg=Colors.TEXT).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_state, text="Inactivo", variable=self.client_vars["Estado"],
                       value="Inactivo", bg=Colors.SURFACE, fg=Colors.TEXT).pack(side=tk.LEFT, padx=5)

        self.create_form_buttons()

    # ------------------- FORM FIELD Y BOTONES -------------------
    def create_form_field(self, label, placeholder="", text_widget=False):
        frame = tk.Frame(self.fields_container, bg=Colors.SURFACE)
        frame.pack(fill=tk.X, pady=5)
        lbl = tk.Label(frame, text=label.replace("_", " "), font=Fonts.BODY,
                       bg=Colors.SURFACE, fg=Colors.TEXT, width=15, anchor=tk.W)
        lbl.pack(side=tk.LEFT, padx=(50, 10))

        if text_widget:
            txt = tk.Text(frame, font=Fonts.BODY, relief=tk.SOLID, bd=1, width=40, height=3)
            txt.pack(side=tk.LEFT)
            if placeholder:
                txt.insert("1.0", placeholder)
            self.client_vars[label] = txt
            return txt
        else:
            var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=var, font=Fonts.BODY, relief=tk.SOLID, bd=1, width=40)
            entry.pack(side=tk.LEFT)
            if placeholder:
                entry.insert(0, placeholder)
                # simple placeholder removal on focus
                entry.bind('<FocusIn>', lambda e, ph=placeholder: self._clear_entry_placeholder(e, ph))
            self.client_vars[label] = var
            return var

    def _clear_entry_placeholder(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)

    def create_form_buttons(self):
        frame = tk.Frame(self.fields_container, bg=Colors.SURFACE)
        frame.pack(pady=20)

        save_btn = tk.Button(
            frame, text="Guardar", font=Fonts.BUTTON, bg=Colors.SUCCESS, fg="white",
            relief=tk.RAISED, bd=0, padx=15, pady=5, cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(
            frame, text="Cancelar", font=Fonts.BUTTON, bg=Colors.DANGER, fg="white",
            relief=tk.RAISED, bd=0, padx=15, pady=5,
            command=lambda f=frame: f.master.master.destroy()
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

        # El comando del save se reasigna por _show_form_window para pasar window y flags correctos

    # ------------------- GUARDAR CLIENTE -------------------
    def edit_selected_client(self):
        """Editar el cliente seleccionado en la tabla"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Actualizar", "No ha seleccionado ningún cliente")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        codigo = values[0]

        try:
            client_data = self.db.get_client_by_code(codigo)
            if not client_data:
                messagebox.showerror("Error", "No se pudo obtener la información del cliente")
                return
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudo obtener cliente: {e}")
            return

        self.show_edit_client_form(client_data)

    def delete_selected_clients(self):
        """Eliminar cliente(s) seleccionados"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Eliminar", "No ha seleccionado ningún cliente")
            return

        confirm = messagebox.askyesno("Eliminar", "¿Está seguro que desea eliminar los clientes seleccionados?")
        if not confirm:
            return

        for item in selected:
            values = self.tree.item(item, "values")
            codigo = values[0]  # asumimos que el primer valor es el código
            try:
                result, msg = self.db.delete_client_by_code(codigo)
                if result == 1:
                    self.tree.delete(item)
                else:
                    messagebox.showerror("Error BD", msg)
            except Exception as e:
                messagebox.showerror("Error BD", f"No se pudo eliminar cliente: {e}")

    def save_client(self, window, is_update=False, original_code=None):
        try:
            data = {}
            # Obtener valores de StringVar / IntVar
            for key, var in self.client_vars.items():
                if isinstance(var, tk.StringVar):
                    data[key] = var.get().strip()
                elif isinstance(var, tk.IntVar):
                    data[key] = var.get()
                elif isinstance(var, tk.Text):
                    # Text widgets los tomamos más abajo en el recorrido de widgets,
                    # pero por si acaso incluimos esto
                    data[key] = var.get("1.0", tk.END).strip()

            # Obtener datos de widgets Text y entradas visibles en fields_container
            for child in self.fields_container.winfo_children():
                widgets = child.winfo_children()
                if len(widgets) < 2:
                    continue
                label_widget = widgets[0]
                input_widget = widgets[1]

                label_name = label_widget.cget("text").strip()
                # Texto en campo text
                if isinstance(input_widget, tk.Text):
                    data[label_name] = input_widget.get("1.0", tk.END).strip()
                elif isinstance(input_widget, tk.Entry):
                    data[label_name] = input_widget.get().strip()

            tipo = self.client_type.get()

            # Validaciones según tipo
            if tipo == CLIENT_TYPES["MINORISTA"]:
                dni = data.get("DNI", "").strip()
                if len(dni) != 8 or not dni.isdigit():
                    messagebox.showwarning("Validación", "El DNI debe tener 8 dígitos numéricos")
                    return
            elif tipo in [CLIENT_TYPES["MAYORISTA"], CLIENT_TYPES["CORPORATIVO"]]:
                ruc = data.get("RUC", "").strip()
                if len(ruc) != 11 or not ruc.isdigit():
                    messagebox.showwarning("Validación", "El RUC debe tener 11 dígitos numéricos")
                    return
            if tipo == CLIENT_TYPES["CORPORATIVO"]:
                dni_contacto = data.get("DNI Contacto", "").strip()
                if dni_contacto and (len(dni_contacto) != 8 or not dni_contacto.isdigit()):
                    messagebox.showwarning("Validación", "El DNI del contacto debe tener 8 dígitos")
                    return

            # DNI administrador (si no se pasó al constructor)
            dni_admin = self.admin_dni
            if not dni_admin:
                dni_admin = simpledialog.askstring("Administrador", "Ingrese DNI del administrador (8 dígitos):", parent=window)
            if not dni_admin:
                messagebox.showwarning("Validación", "Debe proporcionar DNI del administrador")
                return
            if len(dni_admin.strip()) != 8 or not dni_admin.strip().isdigit():
                messagebox.showwarning("Validación", "DNI administrador inválido (8 dígitos)")
                return

            # ------------------------------------------------
            # Ahora dependiente del tipo, llamamos a DBController
            # ------------------------------------------------
            if tipo == CLIENT_TYPES["MINORISTA"]:
                dni = data.get("DNI").strip()
                nombre = data.get("Nombre_Apellido") or data.get("Nombre")
                direccion = data.get("Direccion", "")
                telefono = data.get("Telefono", "")
                correo = data.get("Correo", "")
                preferencias = data.get("Preferencias", "")

                if is_update:
                    # original_code suele ser el DNI anterior
                    self.db.update_minorista(
                        dni=original_code,
                        nombre=nombre,
                        direccion=direccion,
                        telefono=telefono,
                        correo=correo,
                        preferencias=preferencias,
                        dni_admin=dni_admin
                    )
                else:
                    self.db.insert_minorista(
                        dni, nombre, direccion, telefono, correo, preferencias, dni_admin
                    )

            elif tipo == CLIENT_TYPES["MAYORISTA"]:
                ruc = data.get("RUC")
                razon = data.get("Razon Social")
                direccion_f = data.get("Direccion Fiscal", "")
                telefono = data.get("Telefono", "")
                correo = data.get("Correo", "")

                if is_update:
                    self.db.update_mayorista(
                        ruc=original_code,
                        razon_social=razon,
                        direccion_fiscal=direccion_f,
                        telefono=telefono,
                        correo=correo,
                        dni_admin=dni_admin
                    )
                else:
                    self.db.insert_mayorista(
                        ruc, razon, direccion_f, dni_admin, telefono, correo
                    )

            elif tipo == CLIENT_TYPES["CORPORATIVO"]:
                ruc = data.get("RUC", "").strip()
                razon = data.get("Razon Social")
                correo = data.get("Correo")
                telefono = data.get("Telefono", "")
                direccion_f = data.get("Direccion Fiscal", "")
                descripcion = data.get("Descripcion", "")
                fecha_inicio = data.get("Fecha Inicio", "") or None
                fecha_venc = data.get("Fecha Vencimiento", "") or None
                estado = data.get("Estado", "Activo")
                dni_contacto = data.get("DNI Contacto", "").strip()

                if is_update:
                    self.db.update_corporativo(
                        ruc=original_code,
                        razon_social=razon,
                        correo=correo,
                        dni_contacto=dni_contacto if dni_contacto else None,
                        dni_admin=dni_admin,
                        telefono=telefono,
                        direccion_fiscal=direccion_f,
                        descripcion=descripcion,
                        fecha_inicio=fecha_inicio,
                        fecha_venc=fecha_venc,
                        estado=estado
                    )
                else:
                    # Nota: DBController.insert_corporativo espera dni_contacto (FK) y no inserta Contacto por sí mismo.
                    # Asegúrate de haber creado el contacto en la tabla Contacto previamente (o puedes extender DBController).
                    self.db.insert_corporativo(
                        ruc, razon, correo, dni_contacto, dni_admin,
                        telefono, direccion_f, descripcion, fecha_inicio, fecha_venc, estado
                    )

            else:
                # tipo desconocido
                messagebox.showwarning("Tipo", "Tipo de cliente no reconocido")
                return

        except Exception as e:
            messagebox.showerror("Error BD", f"Error guardando cliente: {e}")
            return

        messagebox.showinfo("Éxito", "Cliente guardado correctamente")
        try:
            window.destroy()
        except Exception:
            pass
        self.load_data_from_db()

    # ------------------- UPDATE FORM FIELDS -------------------
    def update_form_fields(self, window, canvas=None):
        # Limpiar contenedor
        for widget in getattr(self, "fields_container", tk.Frame()).winfo_children():
            widget.destroy()

        client_type = self.client_type.get()
        # Header del formulario
        type_label = tk.Label(self.fields_container, text=f"Cliente {client_type.capitalize()}",
                              font=Fonts.HEADING, bg=Colors.SURFACE, fg=Colors.TEXT)
        type_label.pack(pady=(0, 5))
        ttk.Separator(self.fields_container, orient='horizontal').pack(fill=tk.X, pady=(0, 20))

        # Crear campos según tipo
        if client_type == CLIENT_TYPES["MINORISTA"]:
            self.create_minorista_form()
        elif client_type == CLIENT_TYPES["MAYORISTA"]:
            self.create_mayorista_form()
        elif client_type == CLIENT_TYPES["CORPORATIVO"]:
            self.create_corporativo_form()
        else:
            # por defecto mostramos las opciones
            tk.Label(self.fields_container, text="Seleccione un tipo de cliente", bg=Colors.SURFACE,
                     fg=Colors.TEXT).pack(pady=10)

        if canvas:
            self.fields_container.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
