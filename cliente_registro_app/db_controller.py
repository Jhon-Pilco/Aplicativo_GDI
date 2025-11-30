import psycopg2
from psycopg2.extras import RealDictCursor

class DBController:
    def __init__(self,
                 host="localhost",
                 database="registro_clientes",
                 user="postgres",
                 password="jhon",
                 port="5432"):
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            # Use RealDictCursor when fetching rows for convenience
        except Exception as e:
            # Note: don't import tkinter here; let callers handle UI messages.
            raise

    def close(self):
        if self.conn:
            self.conn.close()

    # Generic execute (no fetch)
    def execute(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            try:
                self.conn.commit()
            except Exception:
                self.conn.rollback()
                raise

    # Generic fetchall returning list of dicts
    def fetchall(self, query, params=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    def fetchone(self, query, params=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            row = cur.fetchone()
            return dict(row) if row else None

    # ---------- App specific helpers ----------

    def validate_admin(self, usuario, contrasena):
        q = "SELECT DNI, Usuario FROM Administrador WHERE Usuario = %s AND Contrasena = %s"
        row = self.fetchone(q, (usuario, contrasena))
        return row

    def insert_administrator(self, dni, nombre, usuario, contrasena, telefono, correo):
        q = """
        INSERT INTO Administrador (DNI, Nombre_Apellido, Usuario, Contrasena, Telefono, Correo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.execute(q, (dni, nombre, usuario, contrasena, telefono, correo))

    def get_all_clients(self):
        
        results = []

        # Minorista
        q1 = "SELECT DNI AS codigo, Nombre_Apellido AS nombre, Telefono AS telefono, Correo AS correo FROM ClienteMinorista"
        try:
            rows = self.fetchall(q1)
            for r in rows:
                r['tipo'] = 'Minorista'
                results.append(r)
        except Exception:
            # table may be empty or missing; ignore
            pass

        # Mayorista (join with DatosClienteMayorista for phone/email)
        q2 = """
        SELECT  cm.RUC AS codigo, 
                cm.Razon_Social AS nombre, 
                dcm.Telefono AS telefono,
                dcm.Correo AS correo
        FROM ClienteMayorista cm
        LEFT JOIN DatosClienteMayorista dcm ON dcm.RUC_Mayorista = cm.RUC
        """
        try:
            rows = self.fetchall(q2)
            for r in rows:
                r['tipo'] = 'Mayorista'
                results.append(r)
        except Exception:
            pass

        # Corporativo (join DatosClienteCorporativo)
        q3 = """
        SELECT cc.RUC AS codigo, cc.Razon_Social AS nombre, dcc.Telefono AS telefono, cc.Correo AS correo
        FROM ClienteCorporativo cc
        LEFT JOIN DatosClienteCorporativo dcc ON dcc.RUC_Corporativo = cc.RUC
        """
        try:
            rows = self.fetchall(q3)
            for r in rows:
                r['tipo'] = 'Corporativo'
                results.append(r)
        except Exception:
            pass

        return results
    
    def get_client_by_code(self, code):
        # ---------- Cliente Minorista ----------
        if len(code) == 8:  # DNI
            q = """
            SELECT 
                DNI AS codigo,
                Nombre_Apellido AS nombre,
                Direccion,
                Telefono,
                Correo,
                Preferencias,
                DNI_administrador,
                'minorista' AS tipo
            FROM ClienteMinorista
            WHERE DNI = %s
            """
            return self.fetchone(q, (code,))

    # ---------- Cliente Mayorista ----------
        elif len(code) == 11:  # RUC
        # Intentar mayorista primero
            q1 = """
            SELECT 
                cm.RUC AS codigo,
                cm.Razon_Social AS nombre,
                cm.Direccion_Fiscal,
                cm.DNI_administrador,
                dcm.Telefono,
                dcm.Correo,
                'mayorista' AS tipo
            FROM ClienteMayorista cm
            LEFT JOIN DatosClienteMayorista dcm ON dcm.RUC_Mayorista = cm.RUC
            WHERE cm.RUC = %s
            """
            result = self.fetchone(q1, (code,))
            if result:
                return result

        # ---------- Cliente Corporativo ----------
            q2 = """
            SELECT 
                cc.RUC AS codigo,
                cc.Razon_Social AS nombre,
                cc.Correo,
                cc.DNI_contacto,
                cc.DNI_administrador,
                dcc.Telefono,
                dcc.Direccion_Fiscal,
                c.Descripcion,
                c.Fecha_inicio,
                c.Fecha_vencimiento,
                c.Estado,
                'corporativo' AS tipo
            FROM ClienteCorporativo cc
            LEFT JOIN DatosClienteCorporativo dcc ON dcc.RUC_Corporativo = cc.RUC
            LEFT JOIN Contrato c ON c.RUC_Corporativo = cc.RUC
            WHERE cc.RUC = %s
            """
            return self.fetchone(q2, (code,))
        else:
            return None


    def delete_client_by_code(self, code):
        try:
            if len(code) == 8:
                # Cliente Minorista
                exists = self.fetchone(
                    "SELECT 1 FROM ClienteMinorista WHERE DNI = %s",
                    (code,)
                )
                if exists:
                    self.execute("DELETE FROM ClienteMinorista WHERE DNI = %s", (code,))
                    return True, "Cliente minorista eliminado correctamente."
                else:
                    return False, "El DNI no pertenece a un cliente minorista."
            
            elif len(code) == 11:
                # Verificar si es Mayorista
                mayorista = self.fetchone(
                    "SELECT 1 FROM ClienteMayorista WHERE RUC = %s",
                    (code,)
                )
                # Verificar si es Corporativo
                corporativo = self.fetchone(
                    "SELECT 1 FROM ClienteCorporativo WHERE RUC = %s",
                    (code,)
                )
                
                if mayorista:
                    self.execute("DELETE FROM ClienteMayorista WHERE RUC = %s", (code,))
                    return True, "Cliente mayorista eliminado correctamente."
                
                elif corporativo:
                    self.execute("DELETE FROM ClienteCorporativo WHERE RUC = %s", (code,))
                    return True, "Cliente corporativo eliminado correctamente."
                
                else:
                    return False, "El RUC no pertenece a ningún cliente registrado."
            
            else:
                return False, "El código debe tener 8 (DNI) o 11 (RUC) caracteres."
        
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"


    # Minimal insert helpers (may raise FK errors if admin/contact missing)
    def insert_minorista(self, dni, nombre, direccion, telefono, correo, preferencias, dni_admin):
        q = """
        INSERT INTO ClienteMinorista (DNI, Nombre_Apellido, Direccion, Telefono, Correo, Preferencias, DNI_administrador)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        self.execute(q, (dni, nombre, direccion, telefono, correo, preferencias, dni_admin))

    def insert_mayorista(self, ruc, razon_social, direccion_fiscal, dni_admin, telefono=None, correo=None):
        q1 = "INSERT INTO ClienteMayorista (RUC, Razon_Social, Direccion_Fiscal, DNI_administrador) VALUES (%s,%s,%s,%s)"
        self.execute(q1, (ruc, razon_social, direccion_fiscal, dni_admin))
        if telefono or correo:
            q2 = "INSERT INTO DatosClienteMayorista (RUC_Mayorista, Telefono, Correo) VALUES (%s,%s,%s)"
            self.execute(q2, (ruc, telefono, correo))

    def insert_corporativo(self, ruc, razon_social, correo, dni_contacto, dni_admin,
                           telefono=None, direccion_fiscal=None, descripcion=None, fecha_inicio=None, fecha_venc=None, estado=None):
        q1 = "INSERT INTO ClienteCorporativo (RUC, Razon_Social, Correo, DNI_contacto, DNI_administrador) VALUES (%s,%s,%s,%s,%s)"
        self.execute(q1, (ruc, razon_social, correo, dni_contacto, dni_admin))
        if telefono or direccion_fiscal:
            q2 = "INSERT INTO DatosClienteCorporativo (RUC_Corporativo, Telefono, Direccion_Fiscal) VALUES (%s,%s,%s)"
            self.execute(q2, (ruc, telefono, direccion_fiscal))
        if descripcion or fecha_inicio or fecha_venc or estado:
            q3 = "INSERT INTO Contrato (Descripcion, Fecha_inicio, Fecha_vencimiento, Estado, RUC_Corporativo) VALUES (%s,%s,%s,%s,%s)"
            self.execute(q3, (descripcion, fecha_inicio, fecha_venc, estado, ruc))

    # ---------- Update helpers ----------
    def update_minorista(self, dni, nombre=None, direccion=None, telefono=None, correo=None, preferencias=None, dni_admin=None):
        fields = []
        params = []
        if nombre is not None:
            fields.append("Nombre_Apellido=%s")
            params.append(nombre)
        if direccion is not None:
            fields.append("Direccion=%s")
            params.append(direccion)
        if telefono is not None:
            fields.append("Telefono=%s")
            params.append(telefono)
        if correo is not None:
            fields.append("Correo=%s")
            params.append(correo)
        if preferencias is not None:
            fields.append("Preferencias=%s")
            params.append(preferencias)
        if dni_admin is not None:
            fields.append("DNI_administrador=%s")
            params.append(dni_admin)
        
        if not fields:
            return  # nada que actualizar
        q = f"UPDATE ClienteMinorista SET {', '.join(fields)} WHERE DNI=%s"
        params.append(dni)
        self.execute(q, tuple(params))

    def update_mayorista(self, ruc, razon_social=None, direccion_fiscal=None, telefono=None, correo=None, dni_admin=None):
        fields = []
        params = []
        if razon_social is not None:
            fields.append("Razon_Social=%s")
            params.append(razon_social)
        if direccion_fiscal is not None:
            fields.append("Direccion_Fiscal=%s")
            params.append(direccion_fiscal)
        if dni_admin is not None:
            fields.append("DNI_administrador=%s")
            params.append(dni_admin)
        
        if fields:
            q = f"UPDATE ClienteMayorista SET {', '.join(fields)} WHERE RUC=%s"
            params.append(ruc)
            self.execute(q, tuple(params))
        
        contact_fields = []
        contact_params = []
        
        if telefono is not None:
            contact_fields.append("Telefono=%s")
            contact_params.append(telefono)
        if correo is not None:
            contact_fields.append("Correo=%s")
            contact_params.append(correo)
        if contact_fields:
            q2 = f"UPDATE DatosClienteMayorista SET {', '.join(contact_fields)} WHERE RUC_Mayorista=%s"
            contact_params.append(ruc)
            self.execute(q2, tuple(contact_params))
    
    def update_corporativo(self, ruc, razon_social=None, correo=None, dni_contacto=None, dni_admin=None,
                       telefono=None, direccion_fiscal=None, descripcion=None,
                       fecha_inicio=None, fecha_venc=None, estado=None):
        fields = []
        params = []
        
        if razon_social is not None:
            fields.append("Razon_Social=%s")
            params.append(razon_social)
        if correo is not None:
            fields.append("Correo=%s")
            params.append(correo)
        if dni_contacto is not None:
            fields.append("DNI_contacto=%s")
            params.append(dni_contacto)
        if dni_admin is not None:
            fields.append("DNI_administrador=%s")
            params.append(dni_admin)
        
        if fields:
            q = f"UPDATE ClienteCorporativo SET {', '.join(fields)} WHERE RUC=%s"
            params.append(ruc)
            self.execute(q, tuple(params))
        
        contact_fields = []
        contact_params = []
        
        if telefono is not None:
            contact_fields.append("Telefono=%s")
            contact_params.append(telefono)
        if direccion_fiscal is not None:
            contact_fields.append("Direccion_Fiscal=%s")
            contact_params.append(direccion_fiscal)
        
        if contact_fields:
            q2 = f"UPDATE DatosClienteCorporativo SET {', '.join(contact_fields)} WHERE RUC_Corporativo=%s"
            contact_params.append(ruc)
            self.execute(q2, tuple(contact_params))
        
        if any([descripcion, fecha_inicio, fecha_venc, estado]):
            fields_contract = []
            params_contract = []
            
            if descripcion is not None:
                fields_contract.append("Descripcion=%s")
                params_contract.append(descripcion)
            if fecha_inicio is not None:
                fields_contract.append("Fecha_inicio=%s")
                params_contract.append(fecha_inicio)
            if fecha_venc is not None:
                fields_contract.append("Fecha_vencimiento=%s")
                params_contract.append(fecha_venc)
            if estado is not None:
                fields_contract.append("Estado=%s")
                params_contract.append(estado)
            
            if fields_contract:
                q3 = f"UPDATE Contrato SET {', '.join(fields_contract)} WHERE RUC_Corporativo=%s"
                params_contract.append(ruc)
                self.execute(q3, tuple(params_contract))
