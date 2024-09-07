from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Crear una instancia de una curva elíptica (por ejemplo, la curva P-256)
curve = ec.SECP256R1()

# Generar un par de claves para Alice
private_key_alicia = ec.generate_private_key(curve, default_backend())
public_key_alicia = private_key_alicia.public_key()

# Generar un par de claves para Bob
private_key_betito = ec.generate_private_key(curve, default_backend())
public_key_betito = private_key_betito.public_key()

# Generar un par de claves para Charly
private_key_charly = ec.generate_private_key(curve, default_backend())
public_key_charly = private_key_charly.public_key()

# Calcular las claves compartidas
shared_key_alicia_betito = private_key_alicia.exchange(ec.ECDH(), public_key_betito)
shared_key_betito_charly = private_key_betito.exchange(ec.ECDH(), public_key_charly)
shared_key_charly_alicia = private_key_charly.exchange(ec.ECDH(), public_key_alicia)

derived_public_key_alicia_betito = private_key_alicia.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

decoded_public_key_alicia_betito = serialization.load_pem_public_key(
    derived_public_key_alicia_betito,
    backend=default_backend()
)

derived_public_key_betito_charly = private_key_betito.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# decoded_public_key_betito_charly = serialization.load_pem_public_key(
#     derived_public_key_betito_charly,
#     backend=default_backend()
# )

# derived_public_key_charly_alicia = private_key_charly.public_key().public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# decoded_public_key_charly_alicia = serialization.load_pem_public_key(
#     derived_public_key_charly_alicia,
#     backend=default_backend()
# )

# Imprimir las claves compartidas
print("Clave compartida de Alice:", shared_key_alicia_betito.hex())
print("Clave compartida de Betito:", shared_key_betito_charly.hex())
print("Clave compartida de Charly:", shared_key_charly_alicia.hex())

shared_key_alicia_betito_charly = private_key_alicia.exchange(ec.ECDH(), derived_public_key_alicia_betito)
shared_key_betito_charly_alicia = private_key_betito.exchange(ec.ECDH(), derived_public_key_alicia_betito)
shared_key_charly_alicia_betito = private_key_charly.exchange(ec.ECDH(), derived_public_key_alicia_betito)

print("Clave compartida de Alice:", shared_key_alicia_betito_charly.hex())
print("Clave compartida de Betito:", shared_key_betito_charly_alicia.hex())
print("Clave compartida de Charly:", shared_key_charly_alicia_betito.hex())