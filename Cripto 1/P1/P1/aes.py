from Crypto.Cipher import AES
from secrets import token_bytes

key = token_bytes(16)

def cifrar(msg):
    cifrar = AES.new(key, AES.MODE_EAX)
    nonce = cifrar.nonce
    cifrarTexto = cifrar.encrypt(msg.encode('ascii'))
    return nonce, cifrarTexto

def descifrar(nonce, cifrarTexto):
    descifrar = AES.new(key, AES.MODE_EAX, nonce=nonce)
    texto = descifrar.decrypt(cifrarTexto)

    return texto

nonce, cifrarTexto = cifrar("Hola mundo")
texto = descifrar(nonce, cifrarTexto)

print(f"Texto cifrado: {cifrarTexto}" )

if not texto:
    print('que pex')
else:
    print(texto)