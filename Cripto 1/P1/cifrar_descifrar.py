import os
import tkinter as tk
from tkinter import filedialog

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import binascii

from secrets import token_bytes
from Crypto.PublicKey import RSA

ruta_Abosulta = ""


#Archivo llave publica AES
def public_key_AES(public_key):
    nombre_archivo = "llave_publica_AES.key"
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(binascii.hexlify(public_key).decode())

#Archivo nonce
def archivo_nonce(nonce):
    nombre_archivo = "nonce.txt"
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(binascii.hexlify(nonce).decode())

#Archivo llave publica y privada RSA
def public_key_RSA(public_key):
    nombre_archivo = "llave_publica_RSA.pem"
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(binascii.hexlify(public_key).decode())

def private_key_RSA(private_key):
    nombre_archivo = "llave_privada_RSA.pem"
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(binascii.hexlify(private_key).decode())

#Creacion llaves
def creacion_llaves(tipo_cifrado):
    if tipo_cifrado == "AES":
        #Creacion llave publica AES
        publickeyAES = token_bytes(16)
        public_key_AES(publickeyAES)

    elif tipo_cifrado == "RSA":
        key = RSA.generate(2048)
        #Creacion llave publica RSA
        privateKey_RSA = key.exportKey('PEM')
        private_key_RSA(privateKey_RSA)
        #Creacion llave privada RSA
        publicKey_RSA = key.publickey().exportKey('PEM')
        public_key_RSA(publicKey_RSA)

#Cargar llave AES
def cargar_llave_AES(archivo_publicKey_AES):
    with open(archivo_publicKey_AES, 'r') as archivo:
        clave_hexadecimal = archivo.read()
        clave_bytes = binascii.unhexlify(clave_hexadecimal)
        return clave_bytes

#Cargar nonce
def cargar_noce(archivo_nonce):
    with open(archivo_nonce, 'r') as archivo:
        clave_hexadecimal = archivo.read()
        clave_bytes = binascii.unhexlify(clave_hexadecimal)
        return clave_bytes

#Cargar llave publica RSA
def cargar_keyPublic_RSA(archivo_keyPublic_RSA):
    with open(archivo_keyPublic_RSA, 'r') as archivo:
        clave_hexadecimal = archivo.read()
        clave_bytes = binascii.unhexlify(clave_hexadecimal)
        return clave_bytes

#Cargar llave privada RSA    
def cargar_keyPrivate_RSA(archivo_keyPrivate_RSA):
    with open(archivo_keyPrivate_RSA, 'r') as archivo:
        clave_hexadecimal = archivo.read()
        clave_bytes = binascii.unhexlify(clave_hexadecimal)
        return clave_bytes

def cifrar_AES(msg, key):
    cifrar = AES.new(key, AES.MODE_EAX)
    nonce = cifrar.nonce
    archivo_nonce(nonce)
    cifrarTexto = cifrar.encrypt(msg.encode('ascii'))
    return cifrarTexto

def descifrar_AES(nonce, cifrarTexto, key):
    descifrar = AES.new(key, AES.MODE_EAX, nonce=nonce)
    texto = descifrar.decrypt(cifrarTexto)
    return texto

def crear_archivo_codificado(nombre_archivo, texto):
    nombre_archivo = nombre_archivo + "_c.txt"
    with open(nombre_archivo, 'wb') as archivo:
        archivo.write(texto)

def crear_archivo_decodificado(nombre_archivo, texto):
    nombre_archivo = nombre_archivo + "_d.txt"
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(str(texto))

def abrir_explorador():
    global ruta_Abosulta
    explorador = tk.Tk()
    explorador.withdraw()
    archivo = filedialog.askopenfilename()
    ruta = os.path.abspath(archivo)
    ruta_Abosulta = ruta
    explorador.destroy()  

def abrir_archivo(ruta):
    nombre_archivo = os.path.splitext(os.path.basename(ruta))[0]
    try:
        with open(ruta, 'r') as archivo:
            plaintext = archivo.read()            
    except FileNotFoundError:
        print(f"El archivo '{plaintext}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error al abrir el archivo: {e}")    
    return plaintext, nombre_archivo

def realizar_operacion():
    global ruta_Abosulta
    ruta = ruta_Abosulta


#opcion = input()

creacion_llaves("AES")
abrir_explorador()
ruta = ruta_Abosulta
texto, nombre_archivo = abrir_archivo(ruta)



abrir_explorador()
ruta = ruta_Abosulta

llave = cargar_llave_AES(ruta)

textoCifrado = cifrar_AES(texto, llave)

crear_archivo_codificado(nombre_archivo, textoCifrado)

    




"""

def cifrar(cadena, clave):
    a
ventana = tk.Tk()
ventana.title("Cifrado y Descifrado")
ventana.geometry("400x250")

opcion = tk.StringVar()
opcion.set(" ")
radio_cifrar = tk.Radiobutton(ventana, text="Cifrar", variable=opcion, value="cifrar")
radio_descifrar = tk.Radiobutton(ventana, text="Descifrar", variable=opcion, value="descifrar")
radio_cifrar.pack(pady=5) 
radio_descifrar.pack(pady=5) 

etiqueta_numero = tk.Label(ventana, text="Ingrese un número del 1-26:")
etiqueta_numero.pack(pady=5)

numero = tk.Entry(ventana)
numero.pack(pady=5)

boton_seleccionar = tk.Button(ventana, text="Seleccionar Archivo", command=abrir_explorador)
boton_seleccionar.pack(pady=5)

boton_realizar = tk.Button(ventana, text="Realizar Operación", command=realizar_operacion)
boton_realizar.pack(pady=5)

resultado = tk.Label(ventana, text="")
resultado.pack(pady=5)

ventana.mainloop()
"""