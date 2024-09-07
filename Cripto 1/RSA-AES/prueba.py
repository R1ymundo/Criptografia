from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import binascii

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import binascii

def cifrar(data):
    key = get_random_bytes(16)
    IV = get_random_bytes(16)

    key = PBKDF2(key, salt=16, dkLen=16)
    IV = PBKDF2(IV, salt=16, dkLen=16)

    cipher = AES.new(key, AES.MODE_CBC, iv=IV)
    ciphertext_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

    ciphertext_hexadecimal = binascii.hexlify(ciphertext_bytes).decode('utf-8')
    return IV, key, ciphertext_hexadecimal

def descifrar(ciphertext_hexadecimal, key, IV):
    ciphertext_bytes = binascii.unhexlify(ciphertext_hexadecimal.encode('utf-8'))
    cipher = AES.new(key, AES.MODE_CBC, iv=IV)
    deciphertext = cipher.decrypt(ciphertext_bytes)
    return deciphertext.decode('utf-8')

# Para probarlo
data = 'Hello World!'
IV, key, ciphertext_hexadecimal = cifrar(data)
print("Texto cifrado en hexadecimal:", ciphertext_hexadecimal)

# Luego puedes utilizar la función descifrar() pasándole el texto cifrado en hexadecimal
deciphertext = descifrar(ciphertext_hexadecimal, key, IV)
print("Texto descifrado:", deciphertext)



# key = get_random_bytes(16)
# IV = get_random_bytes(16)
# data = 'Hello World!'

# key = PBKDF2(key, salt=16, dkLen=16)
# IV = PBKDF2(IV, salt=16, dkLen=16)

# cipher = AES.new(key, AES.MODE_CBC, iv = IV)
# ciphertext_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

# ciphertext_hexadecimal = binascii.hexlify(ciphertext_bytes).decode('utf-8')
# print(ciphertext_bytes)

# cipher = AES.new(key, AES.MODE_CBC, iv = IV)

# deciphertext = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)
# print(deciphertext.decode('utf-8'))

#binascii.unhexlify(ciphertext_hexadecimal)

# import json
# from base64 import b64decode, b64encode
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad, pad
# from Crypto.Random import get_random_bytes

# data = b"secret"
# key = get_random_bytes(16)
# cipher = AES.new(key, AES.MODE_CBC)
# ct_bytes = cipher.encrypt(pad(data, AES.block_size))
# iv = b64encode(cipher.iv).decode('utf-8')
# ct = b64encode(ct_bytes).decode('utf-8')
# result = json.dumps({'iv':iv, 'ciphertext':ct})
# print(result)

# # We assume that the key was securely shared beforehand
# try:
#     b64 = json.loads(result)
#     iv = b64decode(b64['iv'])
#     ct = b64decode(b64['ciphertext'])
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     pt = unpad(cipher.decrypt(ct), AES.block_size)
#     print("The message was: ", pt)
# except (ValueError, KeyError):
#     print("Incorrect decryption")