
from tinyec import registry
import secrets
import pickle

#reducir el tamaño de la clave pública sin perder información importante.
def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

#Generacion de llaves publica y privada
def generar_llaves():
    PrivKey = secrets.randbelow(curve.field.n)
    PubKey = PrivKey * curve.g
    return PrivKey, PubKey    

#Calcula la llave compartida usando la llave privada del user
def calcular_llave(privKey, pubKeyCompartida):
    llave_calculada = privKey * pubKeyCompartida
    llave_com = compress(llave_calculada)
    return llave_com, llave_calculada

#Crea un archivo txt para compartir la llave publica y la clave calculada
def crear_Txt(pubKey, nombre):
    with open(nombre, "wb") as archivo:
        pickle.dump(pubKey, archivo)
        print(f"ARCHIVO CREADO {nombre}")

#Lee el contenido de un archivo existente
def leer_Txt(nombre):
    with open(nombre, "rb") as archivo:
        contenido = pickle.load(archivo)
        return contenido
    
nombre_user = input("INTRODUCE TU NOMBRE: ")

#Definición de la curva
curve = registry.get_curve('brainpoolP512r1')

#Generar las llaves pub y privadas
privKey, pubKey = generar_llaves()

#Se comprime para tener un valor Hex
pubCompressed = compress(pubKey)
print(f"COMPARTE TU LLAVE PUBLICA --> {pubCompressed}")

#Se crea el archivo
crear_Txt(pubKey, "miPublicKey"+ nombre_user +".pickle")

#Se pide el archivo de la llave que le comparten al user
nombre_archivo = input("INTRODUCE EL NOMBRE DEL ARVHIVO DE LA CLAVE RECIBIDA: ")
llave_compartida = leer_Txt(nombre_archivo)

#Se calcula de nuevo la llave
segundaVuelta, llave_calculada = calcular_llave(privKey, llave_compartida)

print(segundaVuelta)

#Se crea el archivo
crear_Txt(llave_calculada, "clave_2_"+ nombre_user +".pickle")

#Se pide el archivo de la llave que le comparten al user
nombre_archivo = input("INTRODUCE EL NOMBRE DEL ARVHIVO DE LA CLAVE RECIBIDA: ")
llave_compartida = leer_Txt(nombre_archivo)

terceraVuelta, llave_final = calcular_llave(privKey, llave_compartida)

print(terceraVuelta)