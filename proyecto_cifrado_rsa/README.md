# Sistema de Cifrado RSA para Transferencia Segura de Archivos

## Descripción del Proyecto

Este es un sistema de cifrado híbrido que combina RSA y AES para la transferencia segura de archivos entre dos usuarios. El sistema permite generar claves criptográficas, intercambiar claves públicas de forma automática, cifrar y descifrar archivos utilizando cifrado híbrido (RSA + AES), y transferir archivos de manera segura a través de la red.

## Video Explicativo

[Ver Video Explicativo del Proyecto](https://youtu.be/5o39ALTM80Y?si=84D4Ad7q019z32tB)

## Características Principales

- **Cifrado Híbrido**: Combina la seguridad de RSA para el intercambio de claves con la eficiencia de AES para el cifrado de archivos
- **Interfaz Gráfica**: Sistema intuitivo con GUI para facilitar el uso
- **Intercambio Automático de Claves**: Las claves públicas se envían automáticamente al conectar
- **Transferencia Segura**: Todos los archivos se cifran antes de ser transferidos
- **Registro de Actividad**: Sistema de logs para monitorear todas las operaciones

## Instalación y Ejecución

### Requisitos Previos
- Python 3.7 o superior
- Las dependencias se encuentran en el archivo `requirements.txt`

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Ejecución del Sistema

El sistema requiere dos terminales para simular la comunicación entre dos usuarios (Alicia y Bob):

#### Terminal 1 (Alicia)
```bash
python sistema_cifrado.py --usuario PC1_Alicia --nombre Alicia
```

#### Terminal 2 (Bob)
```bash
python sistema_cifrado.py --usuario PC2_Bob --nombre Bob
```

### Flujo de Operación

#### Método 1: Intercambio Automático de Claves (Recomendado)
1. **Generación de Claves**: Cada usuario genera su par de claves RSA (privada y pública)
2. **Intercambio de Claves**: Los usuarios conectan entre sí para intercambiar claves públicas automáticamente
3. **Cifrado de Archivos**: Selecciona un archivo para cifrar y enviar al destinatario
4. **Transferencia Segura**: El archivo se cifra con AES y la clave AES se cifra con RSA del destinatario
5. **Descifrado**: El destinatario descifra el archivo usando su clave privada RSA

#### Método 2: Intercambio Manual de Claves (Alternativa)
1. **Ejecutar PS1_Alicia**: 
   ```bash
   python sistema_cifrado.py --usuario PC1_Alicia --nombre Alicia
   ```
   - Aparecerá una ventana emergente
   - Seleccionar la opción "Generar Mis Claves"
   - Dentro de la carpeta `PC1_Alicia/claves/` se crearán dos archivos:
     - `mi_clave_privada.pem` (NO COMPARTIR)
     - `mi_clave_publica.pem` (COMPARTIR ESTA)

2. **Copiar Clave Pública de Alicia**:
   - Abrir el archivo `PC1_Alicia/claves/mi_clave_publica.pem`
   - Copiar todo el contenido del archivo

3. **Ejecutar PC2_Bob**:
   ```bash
   python sistema_cifrado.py --usuario PC2_Bob --nombre Bob
   ```
   - Aparecerá la ventana emergente para Bob
   - Generar las claves de Bob siguiendo el mismo proceso

4. **Crear Archivo de Clave Destinatario en Bob**:
   - Dentro de la carpeta `PC2_Bob/claves/`
   - Crear un nuevo archivo llamado `destinatario_publica.pem`
   - Pegar el contenido de la clave pública de Alicia en este archivo

5. **Verificar Importación**:
   - En la interfaz de Bob, debería aparecer "Clave Destinatario: Importada"
   - Ahora Bob puede recibir archivos cifrados de Alicia

6. **Proceso Inverso (Opcional)**:
   - Para comunicación bidireccional, repetir el proceso copiando la clave pública de Bob a la carpeta de Alicia

**Nota Importante**: El método automático (conectar las IPs) realiza este proceso de forma automática y es más seguro.

### Proceso de Conexión y Transferencia de Archivos

#### Establecimiento de Conexión
1. **Obtener Direcciones IP**:
   - Cada usuario verá su IP local en la interfaz (ej: "Mi IP: 192.168.1.100")
   - Para pruebas locales: ambos usan `127.0.0.1`
   - Para red real: cada uno usa su IP respectiva

2. **Conexión Bidireccional**:
   - En la interfaz de Alicia, ingresar la IP de Bob en "IP Destinatario"
   - En la interfaz de Bob, ingresar la IP de Alicia en "IP Destinatario"
   - Ambos usuarios deben hacer clic en "Conectar" para establecer la comunicación

3. **Intercambio Automático de Claves**:
   - Al conectar, el sistema automáticamente envía la clave pública de cada usuario
   - Las claves se importan automáticamente en la carpeta `claves/` del destinatario
   - El estado mostrará "Clave Destinatario: Importada"

#### Transferencia de Archivos Cifrados
1. **Selección de Archivo**:
   - En la sección "Enviar Archivo Cifrado", hacer clic en "Seleccionar Archivo"
   - Navegar a la carpeta `enviar/` y elegir el archivo deseado
   - El sistema mostrará el nombre y tamaño del archivo seleccionado

2. **Proceso de Cifrado y Envío**:
   - Hacer clic en "CIFRAR Y ENVIAR"
   - El sistema realiza:
     - Cifrado del archivo con AES-256
     - Cifrado de la clave AES con RSA del destinatario
     - Empaquetado y envío por la red

3. **Recepción y Descifrado**:
   - El archivo recibido aparecerá en la sección "Archivos Recibidos"
   - Seleccionar el archivo recibido de la lista
   - Hacer clic en "Descifrar Archivo Seleccionado"
   - El archivo descifrado se guardará en la carpeta `recibidos/`

4. **Verificación**:
   - El archivo descifrado aparecerá con su nombre original
   - Se puede verificar que el contenido sea idéntico al archivo original

#### Comunicación Bidireccional
- **Simultánea**: Ambos usuarios pueden enviar archivos al mismo tiempo
- **Independiente**: Cada conexión funciona de manera autónoma
- **Segura**: Cada archivo se cifra con la clave pública específica del destinatario

### Configuración de Red

Para pruebas locales, utilizar:
- IP de prueba: `127.0.0.1` (ambos usuarios)
- Puerto: `5000` (configurado automáticamente)

Para red real:
- Cada usuario utiliza su propia IP local
- Ambos deben estar en la misma red o tener conectividad TCP directa

## Autores

- **Daniel Guzmán**
- **Felipe Rivas**
- **David Vergara**
- **Santiago Santacruz**

## Información Académica

- **Universidad**: ICESI
- **Materia**: Ciberseguridad
- **Proyecto**: Sistema de Cifrado RSA para Transferencia Segura de Archivos

## Video Explicativo

[Espacio reservado para video explicativo del proyecto]

*El video explicativo del proyecto será agregado aquí próximamente*