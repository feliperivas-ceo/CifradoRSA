# Sistema de Cifrado RSA - Transferencia Segura de Archivos

## Descripción
Sistema educativo de cifrado de archivos con RSA + AES para demostración en clase.

## Instalación Rápida

1. Instalar dependencias:
```bash
pip install cryptography pycryptodome
```

2. Ejecutar en PC1 (Alicia):
```bash
python sistema_cifrado.py --usuario PC1_Alicia --nombre Alicia
```

3. Ejecutar en PC2 (Bob):
```bash
python sistema_cifrado.py --usuario PC2_Bob --nombre Bob
```

## Uso Paso a Paso

### 1. Generar Claves (Primera vez)
- Hacer clic en "Generar Mis Claves"
- Se crean archivos en carpeta `claves/`

### 2. Intercambiar Claves Públicas
- Copiar `mi_clave_publica.pem` de PC1 → PC2
- Renombrar como `destinatario_publica.pem`
- Hacer lo mismo de PC2 → PC1

### 3. Conectar y Enviar
- Ingresar IP del destinatario
- Seleccionar archivo
- Hacer clic en "CIFRAR Y ENVIAR"

### 4. Recibir y Descifrar
- Los archivos llegan automáticamente
- Seleccionar archivo recibido
- Hacer clic en "Descifrar"

## Seguridad
- RSA-2048 bits
- AES-256 bits
- Cifrado híbrido eficiente

## Proyecto Educativo
Desarrollado para demostración en clase de criptografía.
