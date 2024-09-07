from tkinter import *
from tkinter import filedialog, messagebox
from tinyec import registry
import secrets
import pickle

# Función para reducir el tamaño de la clave pública sin perder información importante
def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

# Generación de llaves pública y privada
def generar_llaves():
    curve = registry.get_curve('brainpoolP512r1')
    PrivKey = secrets.randbelow(curve.field.n)
    PubKey = PrivKey * curve.g
    return PrivKey, PubKey    

# Calcula la llave compartida usando la llave privada del usuario
def calcular_llave(privKey, pubKeyCompartida):
    llave_calculada = privKey * pubKeyCompartida
    return compress(llave_calculada), llave_calculada

# Crea un archivo txt para compartir la llave pública y la clave calculada
def crear_Txt(pubKey, nombre):
    with open(nombre, "wb") as archivo:
        pickle.dump(pubKey, archivo)
    return f"Archivo creado: {nombre}"

# Lee el contenido de un archivo existente
def leer_Txt(nombre):
    with open(nombre, "rb") as archivo:
        contenido = pickle.load(archivo)
    return contenido

# Funciones de la GUI
def generar_y_mostrar_llaves():
    global privKey, pubKey
    privKey, pubKey = generar_llaves()
    pubCompressed = compress(pubKey)
    public_key_display.config(text=f"Tu llave pública: {pubCompressed}")
    nombre_usuario = nombre_entry.get()
    archivo_nombre = f"miPublicKey_{nombre_usuario}.pickle"
    resultado_archivo.config(text=crear_Txt(pubKey, archivo_nombre))

def cargar_llave_compartida():
    nombre_usuario = nombre_entry.get()
    filename = filedialog.askopenfilename()
    llave_compartida = leer_Txt(filename)
    segundaVuelta, llave_calculada = calcular_llave(privKey, llave_compartida)
    compartir_key_display.config(text=f"Llave compartida: {segundaVuelta}")
    archivo_nombre = f"clave_2_{nombre_usuario}.pickle"
    crear_Txt(llave_calculada, archivo_nombre)
    cargar_llave_button.config(state=NORMAL)  # Activar el botón para la tercera vuelta

def cargar_llave_final():
    nombre_usuario = nombre_entry.get()
    filename = filedialog.askopenfilename()
    llave_compartida_final = leer_Txt(filename)
    terceraVuelta, llave_final = calcular_llave(privKey, llave_compartida_final)
    final_key_display.config(text=f"Llave final compartida: {terceraVuelta}")
    archivo_nombre = f"clave_final_{nombre_usuario}.pickle"
    crear_Txt(llave_final, archivo_nombre)

# Configuración de la ventana principal
root = Tk()
root.title("Generador de Llaves")

# Campo de entrada para el nombre del usuario
nombre_label = Label(root, text="Introduce tu nombre:")
nombre_label.pack(pady=5)
nombre_entry = Entry(root)
nombre_entry.pack(pady=5)

# Etiqueta y botón para mostrar y generar llaves
public_key_display = Label(root, text="Tu llave pública aparecerá aquí")
public_key_display.pack(pady=20)
generate_button = Button(root, text="Generar y mostrar llaves", command=generar_y_mostrar_llaves)
generate_button.pack(pady=10)

# Etiqueta para mostrar resultado del archivo
resultado_archivo = Label(root, text="")
resultado_archivo.pack(pady=10)

# Botón para cargar la llave compartida y calcular la segunda vuelta
load_button = Button(root, text="Cargar llave compartida y calcular la segunda vuelta", command=cargar_llave_compartida)
load_button.pack(pady=10)

# Etiqueta para mostrar llave compartida
compartir_key_display = Label(root, text="")
compartir_key_display.pack(pady=10)

# Botón para cargar la llave final y calcular la tercera vuelta
cargar_llave_button = Button(root, text="Cargar llave final y calcular la tercera vuelta", command=cargar_llave_final, state=DISABLED)
cargar_llave_button.pack(pady=10)

# Etiqueta para mostrar la llave final
final_key_display = Label(root, text="")
final_key_display.pack(pady=10)

# Ejecutar la ventana
root.mainloop()
