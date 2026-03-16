from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

class AESCrypto:
    def __init__(self):
        self.key = None
        self.iv = None
    
    def generar_clave_aleatoria(self, key_size=32):
        self.key = get_random_bytes(key_size)
        print(f"Clave AES generada")
        return self.key
    
    def generar_iv(self):
        self.iv = get_random_bytes(16)
        return self.iv
    
    def cifrar_datos(self, data):
        if self.key is None:
            raise ValueError("No se ha generado una clave AES")
        iv = self.generar_iv()
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        print(f"Datos cifrados: {len(ciphertext)} bytes")
        return ciphertext, iv
    
    def descifrar_datos(self, ciphertext, iv):
        if self.key is None:
            raise ValueError("No se ha proporcionado una clave AES")
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        print(f"Datos descifrados: {len(plaintext)} bytes")
        return plaintext


class CifradoHibrido:
    def __init__(self, rsa_crypto):
        self.rsa_crypto = rsa_crypto
        self.aes_crypto = AESCrypto()
    
    def cifrar_archivo_hibrido(self, filepath_entrada, filepath_salida):
        print("\n" + "="*60)
        print("INICIANDO CIFRADO HÍBRIDO (RSA + AES)")
        print("="*60)
        
        # PASO 1: Cifrar con AES
        print("\nPASO 1/3: Cifrar archivo con AES-256...")
        self.aes_crypto.generar_clave_aleatoria()
        
        with open(filepath_entrada, 'rb') as f:
            data = f.read()
        
        print(f"Tamaño original: {len(data):,} bytes")
        ciphertext, iv = self.aes_crypto.cifrar_datos(data)
        
        # PASO 2: Cifrar clave AES con RSA
        print("\nPASO 2/3: Cifrar clave AES con RSA...")
        clave_aes_cifrada = self.rsa_crypto.cifrar_con_clave_publica(self.aes_crypto.key)
        print(f"Clave AES cifrada: {len(clave_aes_cifrada)} bytes")
        
        # PASO 3: Empaquetar
        print("\nPASO 3/3: Empaquetar datos...")
        with open(filepath_salida, 'wb') as f:
            f.write(len(clave_aes_cifrada).to_bytes(4, byteorder='big'))
            f.write(len(iv).to_bytes(4, byteorder='big'))
            f.write(clave_aes_cifrada)
            f.write(iv)
            f.write(ciphertext)
        
        print(f"\nCIFRADO COMPLETADO!")
        print(f"Archivo empaquetado: {filepath_salida}")
        print("="*60 + "\n")
        
        return {'archivo_cifrado': filepath_salida}
    
    def descifrar_archivo_hibrido(self, filepath_entrada, filepath_salida):
        print("\n" + "="*60)
        print("INICIANDO DESCIFRADO HÍBRIDO (RSA + AES)")
        print("="*60)
        
        # PASO 1: Extraer componentes
        print("\nPASO 1/3: Extrayendo componentes...")
        with open(filepath_entrada, 'rb') as f:
            tamaño_clave_cifrada = int.from_bytes(f.read(4), byteorder='big')
            tamaño_iv = int.from_bytes(f.read(4), byteorder='big')
            print(f"Clave AES cifrada: {tamaño_clave_cifrada} bytes")
            print(f"IV: {tamaño_iv} bytes")
            
            clave_aes_cifrada = f.read(tamaño_clave_cifrada)
            iv = f.read(tamaño_iv)
            datos_cifrados = f.read()
            print(f"Datos cifrados: {len(datos_cifrados):,} bytes")
        
        # PASO 2: Descifrar clave AES
        print("\nPASO 2/3: Descifrar clave AES con RSA...")
        clave_aes = self.rsa_crypto.descifrar_con_clave_privada(clave_aes_cifrada)
        print(f"Clave AES recuperada")
        
        # PASO 3: Descifrar archivo
        print("\nPASO 3/3: Descifrar archivo con AES...")
        self.aes_crypto.key = clave_aes
        plaintext = self.aes_crypto.descifrar_datos(datos_cifrados, iv)
        
        with open(filepath_salida, 'wb') as f:
            f.write(plaintext)
        
        print(f"\nDESCIFRADO COMPLETADO!")
        print(f"Archivo recuperado: {filepath_salida}")
        print("="*60 + "\n")
        
        return {'archivo_descifrado': filepath_salida}
