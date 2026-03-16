import socket
import threading
import os
import json
from datetime import datetime

class NetworkManager:
    def __init__(self, puerto=5000):
        self.puerto = puerto
        self.servidor_activo = False
        self.callback_archivo_recibido = None
        self.callback_log = None
        self.socket_servidor = None
    
    def log(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        mensaje_completo = f"[{timestamp}] {mensaje}"
        print(mensaje_completo)
        if self.callback_log:
            self.callback_log(mensaje_completo)
    
    def obtener_ip_local(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            return ip_local
        except Exception:
            return "127.0.0.1"
    
    def iniciar_servidor(self, carpeta_recepcion):
        if self.servidor_activo:
            return
        
        self.carpeta_recepcion = carpeta_recepcion
        self.servidor_activo = True
        
        servidor_thread = threading.Thread(target=self._ejecutar_servidor, daemon=True)
        servidor_thread.start()
        
        ip_local = self.obtener_ip_local()
        self.log(f"Servidor iniciado en {ip_local}:{self.puerto}")
    
    def _ejecutar_servidor(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket_servidor.bind(('0.0.0.0', self.puerto))
            self.socket_servidor.listen(1)
            
            while self.servidor_activo:
                try:
                    self.socket_servidor.settimeout(1.0)
                    cliente_socket, direccion = self.socket_servidor.accept()
                    self.log(f"Conexión entrante desde {direccion[0]}")
                    
                    conexion_thread = threading.Thread(
                        target=self._manejar_conexion,
                        args=(cliente_socket,),
                        daemon=True
                    )
                    conexion_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.servidor_activo:
                        self.log(f"Error: {e}")
                    break
        except Exception as e:
            self.log(f"Error al iniciar servidor: {e}")
        finally:
            if self.socket_servidor:
                self.socket_servidor.close()
    
    def _manejar_conexion(self, cliente_socket):
        try:
            metadatos_raw = cliente_socket.recv(1024).decode('utf-8')
            metadatos = json.loads(metadatos_raw)
            
            nombre_archivo = metadatos['nombre']
            tamaño_archivo = metadatos['tamaño']
            
            self.log(f"Recibiendo: {nombre_archivo} ({tamaño_archivo:,} bytes)")
            cliente_socket.send(b'OK')
            
            ruta_destino = os.path.join(self.carpeta_recepcion, nombre_archivo)
            bytes_recibidos = 0
            
            with open(ruta_destino, 'wb') as f:
                while bytes_recibidos < tamaño_archivo:
                    bloque = cliente_socket.recv(min(4096, tamaño_archivo - bytes_recibidos))
                    if not bloque:
                        break
                    f.write(bloque)
                    bytes_recibidos += len(bloque)
            
            if bytes_recibidos == tamaño_archivo:
                self.log(f"Archivo recibido: {nombre_archivo}")
                if self.callback_archivo_recibido:
                    self.callback_archivo_recibido(ruta_destino)
        except Exception as e:
            self.log(f"Error al recibir: {e}")
        finally:
            cliente_socket.close()
    
    def enviar_archivo(self, ruta_archivo, ip_destino):
        if not os.path.exists(ruta_archivo):
            self.log(f"Archivo no encontrado")
            return False
        
        nombre_archivo = os.path.basename(ruta_archivo)
        tamaño_archivo = os.path.getsize(ruta_archivo)
        
        self.log(f"Enviando: {nombre_archivo}")
        
        try:
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.settimeout(10)
            cliente_socket.connect((ip_destino, self.puerto))
            
            metadatos = {'nombre': nombre_archivo, 'tamaño': tamaño_archivo}
            cliente_socket.send(json.dumps(metadatos).encode('utf-8'))
            
            respuesta = cliente_socket.recv(1024)
            if respuesta != b'OK':
                raise Exception("Sin confirmación")
            
            with open(ruta_archivo, 'rb') as f:
                while True:
                    bloque = f.read(4096)
                    if not bloque:
                        break
                    cliente_socket.send(bloque)
            
            self.log(f"Archivo enviado")
            cliente_socket.close()
            return True
            
        except Exception as e:
            self.log(f"Error al enviar: {e}")
            return False
    
    def detener_servidor(self):
        self.servidor_activo = False
        if self.socket_servidor:
            try:
                self.socket_servidor.close()
            except:
                pass
