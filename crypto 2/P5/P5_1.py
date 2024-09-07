
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def two():
    
    return True

def three():
    #CREAMOS LLAVES
    private_key, public_key = generar_par_de_claves()
    #SE COMPARTE LA LLAVE PUBLICA
    pk_bits = llave_publica_bits(public_key)
    print(pk_bits)
    print("COMPARTE TU LLAVE PUBLICA")
    
    #RECIBE LA LLAVE PUBLICA Y CALCULA LA PRIMERA
    key_recibida = input(f"Ingresa la clave recibida: ")
    #SE CARGA EN FORMATO PARA PODER OPERARLA 
    key_recibida_cargada= cargar_clave_recibida(key_recibida)
    res = calcular_clave_compartida(private_key, key_recibida_cargada)
    res_bits = llave_publica_bits(res)
    
    print(f"Resultado: {res}")
    
    return True 

#Se solicita el valor privado del usuario
def SolicitarNum ():
    num = int(input("Introduce tu parametro privado: "))
    return num

def generar_par_de_claves():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    vals=public_key.public_numbers()
    print(f"Private key: {public_key}")
    return private_key, public_key

def llave_publica_bits(public_key):
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pem

def cargar_clave_recibida(pem):
    pk = serialization.load_pem_public_key(pem.encode(), backend=default_backend())
    return pk

def calcular_clave_compartida(private_key, pk):
    compartida = private_key.exchange(ec.ECDH, pk)
    return compartida

three()
#private_key, public_key = generar_par_de_claves()
#print(private_key)
#print(public_key)

#pk_bits = llave_publica_bits(public_key)
#print(pk_bits)

#shared = cargar_clave_recibida(pk_bits)
#print(shared)
#pk2 = llave_publica_bits(shared)
#print(f"COMPARAR: {pk2}")

