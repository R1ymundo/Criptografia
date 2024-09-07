from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec  
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# Genera un par de claves (privada y pública) usando la curva elíptica SECP256R1
def generar_llaves():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())  # Genera la clave privada
    public_key = private_key.public_key()  # Obtiene la clave pública correspondiente

    # Serializa la clave privada a formato PEM
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()  # Sin cifrado para la clave privada
    )
    # Serializa la clave pública a formato PEM
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem  # Devuelve las claves serializadas

# Firma un archivo usando la clave privada proporcionada
def firmar_archivo(private_pem, archivo):
    private_key = serialization.load_pem_private_key(private_pem, password=None, backend=default_backend())  # Deserializa la clave privada
    with open(archivo, 'rb') as f:
        contenido = f.read()  # Lee el contenido del archivo

    # Calcula el hash del archivo
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(contenido)
    digest = hash_mensaje.finalize()  # Obtiene el digest del hash

    # Firma el hash del archivo
    signature = private_key.sign(digest, ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(signature)  # Decodifica la firma en sus componentes r y s

    # Escribe la firma (r, s) al final del archivo
    with open(archivo, 'ab') as f:
        f.write(f"\n{r}\n{s}".encode())  # Añade la firma al archivo

    return r, s  # Devuelve los valores r y s de la firma

# Lee la firma de un archivo
def leer_firma(archivo):
    with open(archivo, 'rb') as f:
        contenido = f.read()  # Lee el contenido del archivo
    lineas = contenido.split(b'\n')  # Divide el contenido en líneas
    r = int(lineas[-2])  # Obtiene el penúltimo valor como r
    s = int(lineas[-1])  # Obtiene el último valor como s
    contenido_sin_firma = b'\n'.join(lineas[:-2])  # Obtiene el contenido sin la firma
    return r, s, contenido_sin_firma  # Devuelve r, s y el contenido sin firma

# Verifica la firma de un archivo usando la clave pública
def verificar_archivo(public_pem, archivo):
    public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())  # Deserializa la clave pública
    r, s, contenido = leer_firma(archivo)  # Lee la firma y el contenido sin firma del archivo

    # Calcula el hash del archivo
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(contenido)
    digest = hash_mensaje.finalize()  # Obtiene el digest del hash

    # Verifica la firma
    signature = encode_dss_signature(r, s)  # Codifica r y s en una firma DSS
    try:
        public_key.verify(signature, digest, ec.ECDSA(hashes.SHA256()))  # Verifica la firma con la clave pública
        return True  # La firma es válida
    except Exception as e:
        print(f"Error durante la verificación: {e}")
        return False  # La firma no es válida
    
def key_iv(key):
    with open(key, 'rb') as f:
        ecdh_key = f.read()  # Lee el contenido de la llave

    # Derivación de la clave AES y el IV a partir de la clave compartida
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32 + 16,  # 32 bytes para la clave AES, 16 bytes para el IV
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(ecdh_key)

    aes_key = derived_key[:32]
    iv = derived_key[32:]

    return aes_key, iv

def cifrarArchivo(archivo, ecdh_key):
    with open(archivo, 'rb') as f:
        contenido = f.read()  # Lee el contenido del archivo

    aes_key, iv = key_iv(ecdh_key)

    data = contenido

    # Cifrado con AES en modo CBC
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext

def descifrarArchivo(archivo, ecdh_key):
    with open(archivo, 'rb') as f:
        contenido = f.read()  # Lee el contenido del archivo

    aes_key, iv = key_iv(ecdh_key)

    # Descifrado con AES en modo CBC
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(contenido) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext

def cifrado_firma(private_pem, archivo, key):
    private_key = serialization.load_pem_private_key(private_pem, password=None, backend=default_backend())  # Deserializa la clave privada
    with open(archivo, 'rb') as f:
        contenido = f.read()  # Lee el contenido del archivo

    ciphertext = cifrarArchivo(archivo, key)

    with open(archivo, 'wb') as f:
        f.write(ciphertext)  # Sobreescribe el contenido del archivo

    # Calcula el hash del archivo
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(contenido)
    digest = hash_mensaje.finalize()  # Obtiene el digest del hash

    # Firma el hash del archivo
    signature = private_key.sign(digest, ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(signature)  # Decodifica la firma en sus componentes r y s

    # Escribe la firma (r, s) al final del archivo
    with open(archivo, 'ab') as f:
        f.write(f"\n{r}\n{s}".encode())  # Añade la firma al archivo

def descifrado_verificado(public_pem, archivo, key):
    public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())  # Deserializa la clave pública
    r, s, contenido = leer_firma(archivo)  # Lee la firma y el contenido sin firma del archivo

    with open(archivo, 'rb') as f:
        contenido = f.readlines()
    
    contenido = b''.join(contenido[:-2]).rstrip(b'\n')
    
    aes_key, iv = key_iv(key)

    # Descifrado con AES en modo CBC
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(contenido) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(archivo, 'wb') as f:
        f.write(plaintext)

    # Escribe la firma (r, s) al final del archivo
    with open(archivo, 'ab') as f:
        f.write(f"\n{r}\n{s}".encode())  # Añade la firma al archivo

    # Calcula el hash del archivo
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(plaintext)
    digest = hash_mensaje.finalize()  # Obtiene el digest del hash

    # Verifica la firma
    signature = encode_dss_signature(r, s)  # Codifica r y s en una firma DSS
    try:
        public_key.verify(signature, digest, ec.ECDSA(hashes.SHA256()))  # Verifica la firma con la clave pública
        return True  # La firma es válida
    except Exception as e:
        print(f"Error durante la verificación: {e}")
        return False  # La firma no es válida

# Función principal que proporciona una interfaz de usuario
def main():
    print("Elige una opción:")
    print("1. Generar llaves")
    print("2. Firmar un archivo")
    print("3. Verificar una firma")
    print("4. Cifrar un archivo")
    print("5. Descifrar un archivo")
    print("6. Cifrar y Firmar un archivo")
    print("7. Descifrar y Verificar una firma")
    
    opcion = int(input())  # Lee la opción del usuario

    if opcion == 1:
        private_pem, public_pem = generar_llaves()  # Genera las claves
        with open("clave_privada.pem", "wb") as f:
            f.write(private_pem)  # Guarda la clave privada en un archivo
        with open("clave_publica.pem", "wb") as f:
            f.write(public_pem)  # Guarda la clave pública en un archivo
        print("Claves generadas y guardadas en 'clave_privada.pem' y 'clave_publica.pem'")

    elif opcion == 2:
        private_pem_path = input("Introduce la ruta de la clave privada PEM: ")
        archivo = input("Introduce la ruta del archivo a firmar: ")
        with open(private_pem_path, "rb") as f:
            private_pem = f.read()  # Lee la clave privada desde un archivo
        r, s = firmar_archivo(private_pem, archivo)  # Firma el archivo
        print(f"Firma generada: (r={r}, s={s})")

    elif opcion == 3:
        public_pem_path = input("Introduce la ruta de la clave pública PEM: ")
        archivo = input("Introduce la ruta del archivo a verificar: ")
        with open(public_pem_path, "rb") as f:
            public_pem = f.read()  # Lee la clave pública desde un archivo
        es_valido = verificar_archivo(public_pem, archivo)  # Verifica la firma del archivo
        if es_valido:
            print("La firma es válida.")
        else:
            print("La firma no es válida.")

    if opcion == 4:
        archivo = input("Introduce la ruta del archivo a firmar: ")
        key_path = input("Introduce la ruta de la llave compartida: ")
        ciphertext = cifrarArchivo(archivo, key_path)
        
        with open("archivo.txt", "wb") as f:
            f.write(ciphertext)

    elif opcion == 5:
        archivo = input("Introduce la ruta del archivo a firmar: ")
        key_path = input("Introduce la ruta de la llave compartida: ")
        plaintext = descifrarArchivo(archivo, key_path)

        with open("archivo1.txt", "wb") as f:
            f.write(plaintext)

    elif opcion == 6:
        private_pem_path = input("Introduce la ruta de la clave pública PEM: ")
        archivo = input("Introduce la ruta del archivo a firmar: ")
        key_path = input("Introduce la ruta de la llave compartida: ")

        with open(private_pem_path, "rb") as f:
            private_pem = f.read()  # Lee la clave privada desde un archivo

        cifrado_firma(private_pem, archivo, key_path)

    elif opcion == 7:
        public_pem_path = input("Introduce la ruta de la clave pública PEM: ")
        archivo = input("Introduce la ruta del archivo a verificar: ")
        key_path = input("Introduce la ruta de la llave compartida: ")
        
        with open(public_pem_path, "rb") as f:
            public_pem = f.read()  # Lee la clave pública desde un archivo

        es_valido = descifrado_verificado(public_pem, archivo, key_path)
        
        if es_valido:
            print("La firma es válida.")
        else:
            print("La firma no es válida.")
        

# Ejecuta la función principal si el script es ejecutado directamente
if __name__ == "__main__":
    main()
