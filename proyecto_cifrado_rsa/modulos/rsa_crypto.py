from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

class RSACrypto:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.recipient_public_key = None
    
    def generar_claves(self, key_size=2048):
        print(f"Generando claves RSA de {key_size} bits...")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        print("Claves RSA generadas exitosamente!")
        return self.private_key, self.public_key
    
    def guardar_clave_privada(self, filepath):
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filepath, 'wb') as f:
            f.write(pem)
        print(f"Clave privada guardada en: {filepath}")
    
    def guardar_clave_publica(self, filepath):
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(filepath, 'wb') as f:
            f.write(pem)
        print(f"Clave pública guardada en: {filepath}")
    
    def cargar_clave_privada(self, filepath):
        with open(filepath, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )
        self.public_key = self.private_key.public_key()
        print(f"Clave privada cargada")
    
    def cargar_clave_publica(self, filepath):
        with open(filepath, 'rb') as f:
            self.recipient_public_key = serialization.load_pem_public_key(
                f.read(), backend=default_backend()
            )
        print(f"Clave pública del destinatario cargada")
    
    def cifrar_con_clave_publica(self, data):
        return self.recipient_public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def descifrar_con_clave_privada(self, ciphertext):
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def obtener_info_clave_publica(self):
        if self.public_key is None:
            return None
        public_numbers = self.public_key.public_numbers()
        return {
            'exponente': public_numbers.e,
            'modulo': public_numbers.n,
            'tamaño_bits': self.public_key.key_size
        }
