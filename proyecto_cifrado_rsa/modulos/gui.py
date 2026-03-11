import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os

class CifradoGUI:
    def __init__(self, nombre_usuario, carpeta_base):
        self.nombre_usuario = nombre_usuario
        self.carpeta_base = carpeta_base
        
        self.callback_generar_claves = None
        self.callback_cifrar_enviar = None
        self.callback_descifrar = None
        self.callback_conectar = None
        
        self.root = tk.Tk()
        self.root.title(f"🔐 Sistema de Cifrado RSA - {nombre_usuario}")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        self.ip_destino = tk.StringVar()
        self.archivo_seleccionado = None
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        # TÍTULO
        frame_titulo = tk.Frame(self.root, bg="#2c3e50", height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        titulo = tk.Label(
            frame_titulo,
            text=f"🔐 SISTEMA DE CIFRADO RSA",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        titulo.pack(pady=15)
        
        usuario_label = tk.Label(
            frame_titulo,
            text=f"Usuario: {self.nombre_usuario}",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        usuario_label.place(x=10, y=10)
        
        # FRAME PRINCIPAL
        frame_principal = tk.Frame(self.root, bg="#ecf0f1")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # SECCIÓN: ESTADO DE CLAVES
        frame_claves = tk.LabelFrame(
            frame_principal,
            text="🔑 Estado de las Claves",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_claves.pack(fill=tk.X, pady=(0, 10))
        
        self.label_mis_claves = tk.Label(
            frame_claves,
            text="🔐 Mis Claves: ❌ No generadas",
            font=("Arial", 10),
            bg="#ecf0f1",
            anchor="w"
        )
        self.label_mis_claves.pack(fill=tk.X, pady=2)
        
        self.label_clave_dest = tk.Label(
            frame_claves,
            text="🔓 Clave Destinatario: ❌ No importada",
            font=("Arial", 10),
            bg="#ecf0f1",
            anchor="w"
        )
        self.label_clave_dest.pack(fill=tk.X, pady=2)
        
        btn_generar = tk.Button(
            frame_claves,
            text="🔑 Generar Mis Claves",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self._on_generar_claves
        )
        btn_generar.pack(pady=(10, 0))
        
        # SECCIÓN: CONEXIÓN DE RED
        frame_red = tk.LabelFrame(
            frame_principal,
            text="🌐 Conexión de Red",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_red.pack(fill=tk.X, pady=(0, 10))
        
        self.label_mi_ip = tk.Label(
            frame_red,
            text="📍 Mi IP: Obteniendo...",
            font=("Arial", 10),
            bg="#ecf0f1",
            anchor="w"
        )
        self.label_mi_ip.pack(fill=tk.X, pady=2)
        
        self.label_estado_red = tk.Label(
            frame_red,
            text="● Servidor: Iniciando...",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#e67e22",
            anchor="w"
        )
        self.label_estado_red.pack(fill=tk.X, pady=2)
        
        frame_ip = tk.Frame(frame_red, bg="#ecf0f1")
        frame_ip.pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(
            frame_ip,
            text="IP Destinatario:",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        entry_ip = tk.Entry(
            frame_ip,
            textvariable=self.ip_destino,
            font=("Arial", 10),
            width=20
        )
        entry_ip.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_conectar = tk.Button(
            frame_ip,
            text="🔗 Conectar",
            font=("Arial", 9),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self._on_conectar
        )
        btn_conectar.pack(side=tk.LEFT)
        
        # SECCIÓN: ENVIAR ARCHIVO
        frame_enviar = tk.LabelFrame(
            frame_principal,
            text="📤 Enviar Archivo Cifrado",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_enviar.pack(fill=tk.X, pady=(0, 10))
        
        frame_seleccionar = tk.Frame(frame_enviar, bg="#ecf0f1")
        frame_seleccionar.pack(fill=tk.X, pady=5)
        
        self.label_archivo = tk.Label(
            frame_seleccionar,
            text="📁 Ningún archivo seleccionado",
            font=("Arial", 9),
            bg="#ecf0f1",
            anchor="w"
        )
        self.label_archivo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_seleccionar = tk.Button(
            frame_seleccionar,
            text="📂 Seleccionar Archivo",
            font=("Arial", 9),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self._seleccionar_archivo
        )
        
        btn_seleccionar.pack(side=tk.RIGHT)
        
        self.btn_cifrar_enviar = tk.Button(
            frame_enviar,
            text="🔒 CIFRAR Y ENVIAR",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            state=tk.DISABLED,
            command=self._on_cifrar_enviar
        )
        self.btn_cifrar_enviar.pack(pady=(10, 0), ipadx=20, ipady=5)
        self.btn_ver_cifrados = tk.Button(
            frame_enviar,
            text="📂 Ver Archivos Cifrados",
            font=("Arial", 9),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self._on_ver_cifrados
        )
        self.btn_ver_cifrados.pack(pady=(5, 0))
        btn_seleccionar.pack(side=tk.RIGHT)
        # SECCIÓN: ARCHIVOS RECIBIDOS
        frame_recibidos = tk.LabelFrame(
            frame_principal,
            text="📥 Archivos Recibidos",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_recibidos.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        frame_listbox = tk.Frame(frame_recibidos, bg="#ecf0f1")
        frame_listbox.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_recibidos = tk.Listbox(
            frame_listbox,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set,
            height=6
        )
        self.listbox_recibidos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_recibidos.yview)
        
        self.btn_descifrar = tk.Button(
            frame_recibidos,
            text="🔓 Descifrar Archivo Seleccionado",
            font=("Arial", 10, "bold"),
            bg="#16a085",
            fg="white",
            cursor="hand2",
            state=tk.DISABLED,
            command=self._on_descifrar
        )
        self.btn_descifrar.pack(pady=(10, 0))
        
        # SECCIÓN: LOG
        frame_log = tk.LabelFrame(
            frame_principal,
            text="📋 Registro de Actividad",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_log.pack(fill=tk.BOTH, expand=True)
        
        self.text_log = scrolledtext.ScrolledText(
            frame_log,
            font=("Courier", 8),
            height=8,
            state=tk.DISABLED,
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.text_log.pack(fill=tk.BOTH, expand=True)
        
        self.listbox_recibidos.bind('<<ListboxSelect>>', self._on_seleccionar_recibido)
    
    def _seleccionar_archivo(self):
        carpeta_enviar = os.path.join(self.carpeta_base, "enviar")
        
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo para enviar",
            initialdir=carpeta_enviar,
            filetypes=[("Todos los archivos", "*.*")]
        )
        
        if archivo:
            self.archivo_seleccionado = archivo
            nombre = os.path.basename(archivo)
            tamaño = os.path.getsize(archivo)
            self.label_archivo.config(
                text=f"📁 {nombre} ({tamaño:,} bytes)"
            )
            
            if self.ip_destino.get():
                self.btn_cifrar_enviar.config(state=tk.NORMAL)
    
    def _on_seleccionar_recibido(self, event):
        if self.listbox_recibidos.curselection():
            self.btn_descifrar.config(state=tk.NORMAL)
        else:
            self.btn_descifrar.config(state=tk.DISABLED)
    
    def _on_generar_claves(self):
        if self.callback_generar_claves:
            self.callback_generar_claves()
    
    def _on_cifrar_enviar(self):
        if not self.archivo_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
            return
        
        if not self.ip_destino.get():
            messagebox.showwarning("Advertencia", "Ingresa la IP del destinatario")
            return
        
        if self.callback_cifrar_enviar:
            self.callback_cifrar_enviar(self.archivo_seleccionado, self.ip_destino.get())
    
    def _on_descifrar(self):
        seleccion = self.listbox_recibidos.curselection()
        if not seleccion:
            return
        
        archivo = self.listbox_recibidos.get(seleccion[0])
        if self.callback_descifrar:
            self.callback_descifrar(archivo)
    
    def _on_conectar(self):
        if not self.ip_destino.get():
            messagebox.showwarning("Advertencia", "Ingresa la IP del destinatario")
            return
        
        if self.callback_conectar:
            self.callback_conectar(self.ip_destino.get())
    def _on_ver_cifrados(self):
        """Abre la carpeta de archivos cifrados para descargar"""
        import subprocess
        import platform
        
        carpeta_cifrados = os.path.join(self.carpeta_base, "recibidos")
        
        # Abrir carpeta según el sistema operativo
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer "{carpeta_cifrados}"')
        elif platform.system() == "Darwin":  # Mac
            subprocess.Popen(["open", carpeta_cifrados])
        else:  # Linux
            subprocess.Popen(["xdg-open", carpeta_cifrados])
        
        self.agregar_log(f"📂 Abriendo carpeta: {carpeta_cifrados}")
    
    def actualizar_estado_claves(self, mis_claves=False, clave_dest=False):
        if mis_claves:
            self.label_mis_claves.config(
                text="🔐 Mis Claves: ✅ Generadas",
                fg="#27ae60"
            )
        
        if clave_dest:
            self.label_clave_dest.config(
                text="🔓 Clave Destinatario: ✅ Importada",
                fg="#27ae60"
            )
    
    def actualizar_mi_ip(self, ip):
        self.label_mi_ip.config(text=f"📍 Mi IP: {ip}")
    
    def actualizar_estado_red(self, conectado=False, mensaje=""):
        if conectado:
            self.label_estado_red.config(
                text=f"● Servidor: ✅ Activo - {mensaje}",
                fg="#27ae60"
            )
        else:
            self.label_estado_red.config(
                text=f"● Servidor: ⚠️ {mensaje}",
                fg="#e67e22"
            )
    
    def agregar_archivo_recibido(self, nombre_archivo):
        self.listbox_recibidos.insert(tk.END, nombre_archivo)
        self.agregar_log(f"📥 Nuevo archivo recibido: {nombre_archivo}")
    
    def agregar_log(self, mensaje):
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, mensaje + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)
    
    def limpiar_seleccion_archivo(self):
        self.archivo_seleccionado = None
        self.label_archivo.config(text="📁 Ningún archivo seleccionado")
        self.btn_cifrar_enviar.config(state=tk.DISABLED)
    
    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)
    
    def mostrar_info(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)
    
    def ejecutar(self):
        self.root.mainloop()
    
    def cerrar(self):
        self.root.quit()