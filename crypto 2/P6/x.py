from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Generar una clave y un vector de inicialización (IV)
key = get_random_bytes(32)  # Clave de 16 bytes (AES-128)
iv = get_random_bytes(16)   # IV de 16 bytes

# Datos a cifrar
data = b"Este es un mensaje secreto"

# Cifrado
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(data, AES.block_size))

print(f"Cifrado: {ciphertext.hex()}")

# Descifrado
decipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)

print(f"Descifrado: {plaintext.decode()}")
