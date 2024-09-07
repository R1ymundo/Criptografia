import os
import tkinter as tk
from tkinter import filedialog

from Crypto.Cipher import AES
import binascii

from secrets import token_bytes
from Crypto.PublicKey import RSA

ruta_Abosulta = ""

#Creacion archivo llave
def generate_keys (key, nombre):
    nombre_archivo = nombre
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(binascii.hexlify(key).decode())

#Creacion llaves
def creacion_llaves(tipo_cifrado):
    if tipo_cifrado == "AES":
        #Creacion llave publica AES
        publickeyAES = token_bytes(16)
        generate_keys(publickeyAES, "llave_publica_AES.key")

    elif tipo_cifrado == "RSA":
        key = RSA.generate(2048)
        #Creacion llave publica RSA
        privateKey_RSA = key.exportKey('PEM')
        generate_keys(privateKey_RSA, 'llave_publica_RSA.pem')
        #Creacion llave privada RSA
        publicKey_RSA = key.publickey().exportKey('PEM')
        generate_keys(publicKey_RSA, 'llave_privada_RSA.pem')

#Cargar llaves
def cargar_llave(archivo_Key):
    with open(archivo_Key, 'r') as archivo:
        clave_hexadecimal = archivo.read()
        clave_bytes = binascii.unhexlify(clave_hexadecimal)
        return clave_bytes

def cifrar_AES(msg, key):
    cifrar = AES.new(key, AES.MODE_EAX)
    nonce = cifrar.nonce
    generate_keys(nonce,"nonce.txt")
    cifrarTexto = cifrar.encrypt(msg.encode('ascii'))
    return cifrarTexto

def descifrar_AES(nonce, descifrarTexto, key):
    descifrar = AES.new(key, AES.MODE_EAX, nonce=nonce)
    texto = descifrar.decrypt(descifrarTexto)
    return texto

def crear_archivo_codificado(nombre_archivo, texto):
    nombre_archivo = nombre_archivo + "_c.txt"
    with open(nombre_archivo, 'wb') as archivo:
        archivo.write(texto)

def crear_archivo_decodificado(nombre_archivo, texto):
    nombre_archivo = nombre_archivo + "_d.txt"
    with open(nombre_archivo, 'wb') as archivo:
        archivo.write(texto)

def abrir_explorador():
    global ruta_Abosulta
    explorador = tk.Tk()
    explorador.withdraw()
    archivo = filedialog.askopenfilename()
    ruta = os.path.abspath(archivo)
    ruta_Abosulta = ruta
    explorador.destroy()  

def abrir_archivo_bytes(ruta):
    nombre_archivo = os.path.splitext(os.path.basename(ruta))[0]
    try:
        with open(ruta, 'rb') as archivo:
            plaintext = archivo.read()            
    except FileNotFoundError:
        print(f"El archivo '{plaintext}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error al abrir el archivo: {e}")    
    return plaintext, nombre_archivo

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


#creacion_llaves("AES")
abrir_explorador()
ruta = ruta_Abosulta
texto, nombre_archivo = abrir_archivo(ruta)


abrir_explorador()
ruta = ruta_Abosulta
llave = cargar_llave(ruta)
textoCifrado = cifrar_AES(texto, llave)
crear_archivo_codificado(nombre_archivo, textoCifrado)

abrir_explorador()
ruta1 = ruta_Abosulta
texto_1, nombre_archivo1 = abrir_archivo_bytes(ruta1)


abrir_explorador()
ruta2 = ruta_Abosulta
llave = cargar_llave(ruta2)

abrir_explorador()
ruta3 = ruta_Abosulta
nonce = cargar_llave(ruta3)

texto_2 = descifrar_AES(nonce, texto_1, llave)

crear_archivo_decodificado(nombre_archivo1, texto_2)


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