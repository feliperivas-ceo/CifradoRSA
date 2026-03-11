#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime

from modulos.rsa_crypto import RSACrypto
from modulos.aes_crypto import CifradoHibrido
from modulos.network import NetworkManager
from modulos.gui import CifradoGUI


class SistemaCifrado:
    def __init__(self, usuario, nombre):
        self.usuario = usuario
        self.nombre = nombre
        
        self.carpeta_base = os.path.join(os.path.dirname(__file__), self.usuario)
        self.carpeta_claves = os.path.join(self.carpeta_base, "claves")
        self.carpeta_enviar = os.path.join(self.carpeta_base, "enviar")
        self.carpeta_recibidos = os.path.join(self.carpeta_base, "recibidos")
        self.carpeta_logs = os.path.join(self.carpeta_base, "logs")
        
        self._crear_estructura_carpetas()
        
        self.rsa = RSACrypto()
        self.cifrado_hibrido = None
        self.network = NetworkManager(puerto=5000)
        self.gui = None
        
        self.claves_generadas = False
        self.clave_dest_cargada = False
    
    def _crear_estructura_carpetas(self):
        carpetas = [
            self.carpeta_base,
            self.carpeta_claves,
            self.carpeta_enviar,
            self.carpeta_recibidos,
            self.carpeta_logs
        ]
        
        for carpeta in carpetas:
            os.makedirs(carpeta, exist_ok=True)
    
    def _log(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        mensaje_completo = f"[{timestamp}] {mensaje}"
        
        print(mensaje_completo)
        
        if self.gui:
            self.gui.agregar_log(mensaje_completo)
        
        log_file = os.path.join(self.carpeta_logs, "actividad.log")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(mensaje_completo + "\n")
    
    def inicializar(self):
        self._log(f"🚀 Inicializando sistema para {self.nombre}...")
        
        ruta_privada = os.path.join(self.carpeta_claves, "mi_clave_privada.pem")
        ruta_publica = os.path.join(self.carpeta_claves, "mi_clave_publica.pem")
        
        if os.path.exists(ruta_privada) and os.path.exists(ruta_publica):
            self._log("📂 Cargando claves existentes...")
            try:
                self.rsa.cargar_clave_privada(ruta_privada)
                self.claves_generadas = True
                self._log("✅ Claves cargadas exitosamente")
            except Exception as e:
                self._log(f"⚠️ Error al cargar claves: {e}")
        
        ruta_dest = os.path.join(self.carpeta_claves, "destinatario_publica.pem")
        if os.path.exists(ruta_dest):
            try:
                self.rsa.cargar_clave_publica(ruta_dest)
                self.clave_dest_cargada = True
                self._log("✅ Clave del destinatario cargada")
            except Exception as e:
                self._log(f"⚠️ Error al cargar clave del destinatario: {e}")
        
        self.cifrado_hibrido = CifradoHibrido(self.rsa)
        
        self.network.callback_log = self._log
        self.network.callback_archivo_recibido = self._on_archivo_recibido
        self.network.iniciar_servidor(self.carpeta_recibidos)
        
        ip_local = self.network.obtener_ip_local()
        self._log(f"📍 Tu IP local: {ip_local}")
        
        return ip_local
    
    def generar_claves(self):
        self._log("\n" + "="*60)
        self._log("🔑 GENERANDO CLAVES RSA")
        self._log("="*60)
        
        try:
            self.rsa.generar_claves(2048)
            
            info = self.rsa.obtener_info_clave_publica()
            self._log(f"\n📊 Información de tus claves:")
            self._log(f"   • Tamaño: {info['tamaño_bits']} bits")
            self._log(f"   • Exponente público (e): {info['exponente']}")
            self._log(f"   • Módulo (n): {str(info['modulo'])[:50]}... (truncado)")
            
            ruta_privada = os.path.join(self.carpeta_claves, "mi_clave_privada.pem")
            ruta_publica = os.path.join(self.carpeta_claves, "mi_clave_publica.pem")
            
            self.rsa.guardar_clave_privada(ruta_privada)
            self.rsa.guardar_clave_publica(ruta_publica)
            
            self._log(f"\n📂 Claves guardadas en:")
            self._log(f"   🔐 Privada: {ruta_privada}")
            self._log(f"   🔓 Pública: {ruta_publica}")
            
            self._log(f"\n💡 IMPORTANTE:")
            self._log(f"   1. NUNCA compartas tu clave privada")
            self._log(f"   2. Comparte tu clave pública con el destinatario")
            self._log(f"   3. Guarda su clave pública como 'destinatario_publica.pem'")
            
            self.claves_generadas = True
            self._log("\n✅ CLAVES GENERADAS EXITOSAMENTE!")
            self._log("="*60 + "\n")
            
            return True
            
        except Exception as e:
            self._log(f"\n❌ ERROR al generar claves: {e}")
            self._log("="*60 + "\n")
            return False
    
    def cifrar_y_enviar(self, ruta_archivo, ip_destino):
        if not self.claves_generadas:
            self._log("❌ Debes generar tus claves primero")
            if self.gui:
                self.gui.mostrar_error("Error", "Genera tus claves primero")
            return False
        
        if not self.clave_dest_cargada:
            self._log("❌ Debes cargar la clave pública del destinatario")
            if self.gui:
                self.gui.mostrar_error("Error", 
                    "Coloca la clave pública del destinatario en:\n" +
                    f"{os.path.join(self.carpeta_claves, 'destinatario_publica.pem')}")
            return False
        
        try:
            nombre_archivo = os.path.basename(ruta_archivo)
            archivo_cifrado = os.path.join(
                self.carpeta_recibidos,
                nombre_archivo + ".enc"
            )
            
            self._log(f"\n🔒 Iniciando cifrado de: {nombre_archivo}")
            self.cifrado_hibrido.cifrar_archivo_hibrido(ruta_archivo, archivo_cifrado)
            
            self._log(f"📤 Enviando archivo cifrado a {ip_destino}...")
            exito = self.network.enviar_archivo(archivo_cifrado, ip_destino)
            
            if exito:
                self._log("✅ Archivo enviado exitosamente!")
                if self.gui:
                    self.gui.mostrar_info("Éxito", "Archivo cifrado y enviado correctamente")
                    self.gui.limpiar_seleccion_archivo()
                
                os.remove(archivo_cifrado)
                return True
            else:
                self._log("❌ Error al enviar archivo")
                if self.gui:
                    self.gui.mostrar_error("Error", "No se pudo enviar el archivo")
                return False
                
        except Exception as e:
            self._log(f"❌ ERROR: {e}")
            if self.gui:
                self.gui.mostrar_error("Error", str(e))
            return False
    
    def descifrar_archivo(self, nombre_archivo):
        if not self.claves_generadas:
            self._log("❌ Debes generar tus claves primero")
            if self.gui:
                self.gui.mostrar_error("Error", "Genera tus claves primero")
            return False
        
        try:
            archivo_cifrado = os.path.join(self.carpeta_recibidos, nombre_archivo)
            
            if nombre_archivo.endswith(".enc"):
                nombre_descifrado = nombre_archivo[:-4]
            else:
                nombre_descifrado = nombre_archivo + ".decrypted"
            
            archivo_descifrado = os.path.join(self.carpeta_recibidos, nombre_descifrado)
            
            self._log(f"\nIniciando descifrado de: {nombre_archivo}")
            self.cifrado_hibrido.descifrar_archivo_hibrido(archivo_cifrado, archivo_descifrado)
            
            self._log(f"Archivo descifrado exitosamente!")
            self._log(f"Archivo guardado en: {archivo_descifrado}")
            
            if self.gui:
                self.gui.mostrar_info("Éxito", 
                    f"Archivo descifrado correctamente:\n{nombre_descifrado}")
            
            os.remove(archivo_cifrado)
            
            return True
            
        except Exception as e:
            self._log(f"ERROR al descifrar: {e}")
            if self.gui:
                self.gui.mostrar_error("Error", f"Error al descifrar: {e}")
            return False
    
    def _on_archivo_recibido(self, ruta_archivo):
        """Callback cuando se recibe un archivo"""
        nombre_archivo = os.path.basename(ruta_archivo)
        self._log(f"📥 Archivo recibido: {nombre_archivo}")
        
        # NUEVO: Detectar si es una clave pública
        if nombre_archivo == "mi_clave_publica.pem":
            self._procesar_clave_recibida(ruta_archivo)
        else:
            # Es un archivo cifrado normal
            if self.gui:
                self.gui.agregar_archivo_recibido(nombre_archivo)
    
    def _procesar_clave_recibida(self, ruta_archivo):
        """Procesa automáticamente una clave pública recibida"""
        nombre_archivo = os.path.basename(ruta_archivo)
        
        # Detectar si es una clave pública
        if nombre_archivo == "mi_clave_publica.pem":
            self._log("🔑 Clave pública recibida del destinatario")
            
            try:
                # Renombrar como destinatario_publica.pem
                ruta_destino = os.path.join(self.carpeta_claves, "destinatario_publica.pem")
                
                # Copiar el archivo
                import shutil
                shutil.copy(ruta_archivo, ruta_destino)
                
                # Cargar la clave
                self.rsa.cargar_clave_publica(ruta_destino)
                self.clave_dest_cargada = True
                
                # Actualizar GUI
                if self.gui:
                    self.gui.actualizar_estado_claves(clave_dest=True)
                    self.gui.mostrar_info("Clave Recibida", 
                        "✅ Clave pública del destinatario recibida e importada.\n\n" +
                        "¡Ya puedes enviar archivos cifrados!")
                
                self._log("✅ Clave del destinatario importada automáticamente")
                
                # Eliminar el archivo original
                os.remove(ruta_archivo)
                
            except Exception as e:
                self._log(f"❌ Error al procesar clave recibida: {e}")

    def ejecutar_gui(self):
        self.gui = CifradoGUI(self.nombre, self.carpeta_base)
        
        self.gui.callback_generar_claves = self._gui_generar_claves
        self.gui.callback_cifrar_enviar = self._gui_cifrar_enviar
        self.gui.callback_descifrar = self._gui_descifrar
        self.gui.callback_conectar = self._gui_conectar
        
        ip_local = self.inicializar()
        
        self.gui.actualizar_mi_ip(ip_local)
        self.gui.actualizar_estado_red(
            conectado=True,
            mensaje=f"Escuchando en puerto 5000"
        )
        
        if self.claves_generadas:
            self.gui.actualizar_estado_claves(mis_claves=True)
        
        if self.clave_dest_cargada:
            self.gui.actualizar_estado_claves(clave_dest=True)
        
        self._cargar_archivos_recibidos()
        
        self._log("✅ Sistema listo!")
        self.gui.ejecutar()
        
        self.network.detener_servidor()
    
    def _cargar_archivos_recibidos(self):
        try:
            archivos = [f for f in os.listdir(self.carpeta_recibidos) if f.endswith('.enc')]
            for archivo in archivos:
                self.gui.agregar_archivo_recibido(archivo)
        except:
            pass
    
    def _gui_generar_claves(self):
        if self.generar_claves():
            self.gui.actualizar_estado_claves(mis_claves=True)
            self.gui.mostrar_info("Éxito", "Claves generadas correctamente")
    
    def _gui_cifrar_enviar(self, archivo, ip):
        self.cifrar_y_enviar(archivo, ip)
    
    def _gui_descifrar(self, nombre_archivo):
        self.descifrar_archivo(nombre_archivo)
    
    def _gui_conectar(self, ip):
        """Callback GUI: Conectar y enviar clave pública automáticamente"""
        self._log(f"🔗 Conectando con: {ip}")
        
        # Verificar que tengamos nuestras claves
        if not self.claves_generadas:
            self.gui.mostrar_error("Error", "Primero debes generar tus claves")
            return
        
        # NUEVO: Enviar nuestra clave pública automáticamente
        self._log("📤 Enviando tu clave pública al destinatario...")
        
        ruta_mi_clave = os.path.join(self.carpeta_claves, "mi_clave_publica.pem")
        
        try:
            # Enviar clave pública
            exito = self.network.enviar_archivo(ruta_mi_clave, ip)
            
            if exito:
                self._log("✅ Tu clave pública fue enviada exitosamente")
                self.gui.mostrar_info("Éxito", 
                    "Tu clave pública fue enviada a:\n" + ip + 
                    "\n\nAhora espera a que te envíen su clave...")
            else:
                self.gui.mostrar_error("Error", 
                    "No se pudo enviar la clave pública.\n" +
                    "Verifica que el destinatario esté conectado.")
                return
        except Exception as e:
            self.gui.mostrar_error("Error", f"Error al enviar clave: {e}")
            return
        
        # Intentar cargar clave del destinatario si ya existe
        ruta_dest = os.path.join(self.carpeta_claves, "destinatario_publica.pem")
        if os.path.exists(ruta_dest):
            try:
                self.rsa.cargar_clave_publica(ruta_dest)
                self.clave_dest_cargada = True
                self.gui.actualizar_estado_claves(clave_dest=True)
                self._log("✅ Clave del destinatario cargada")
            except Exception as e:
                self._log(f"⚠️ Error al cargar clave del destinatario: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Sistema de Cifrado RSA para transferencia segura de archivos"
    )
    parser.add_argument(
        "--usuario",
        required=True,
        choices=["PC1_Alicia", "PC2_Bob"],
        help="Carpeta de usuario (PC1_Alicia o PC2_Bob)"
    )
    parser.add_argument(
        "--nombre",
        required=True,
        help="Nombre del usuario (Alicia, Bob, etc.)"
    )
    
    args = parser.parse_args()
    
    sistema = SistemaCifrado(args.usuario, args.nombre)
    sistema.ejecutar_gui()


if __name__ == "__main__":
    main()

