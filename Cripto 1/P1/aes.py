from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad  # Importa el módulo de relleno

# Genera una clave AES aleatoria de 16 bytes
key = get_random_bytes(16)

def cifrar(msg):
    cifrar = AES.new(key, AES.MODE_CBC)
    # Agrega relleno PKCS7 al mensaje
    mensaje_rellenado = pad(msg.encode('utf-8'), AES.block_size)
    cifrarTexto = cifrar.encrypt(mensaje_rellenado)
    return cifrarTexto

def descifrar(cifrarTexto):
    descifrar = AES.new(key, AES.MODE_CBC)
    mensaje_rellenado = descifrar.decrypt(cifrarTexto)
    # Elimina el relleno PKCS7 para obtener el mensaje original
    mensaje_original = unpad(mensaje_rellenado, AES.block_size)
    return mensaje_original.decode('utf-8')

mensaje = "Hola mundo"
cifrarTexto = cifrar(mensaje)
texto = descifrar(cifrarTexto)

print(f"Mensaje cifrado: {cifrarTexto}")
print(f"Mensaje descifrado: {texto}")
