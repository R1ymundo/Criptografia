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
    if opcion.get() == 2:
        cargar_llave_button.config(state=NORMAL)
        load_button.config(state=DISABLED)
    else:
        cargar_llave_button.config(state=DISABLED)
        load_button.config(state=NORMAL)

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

# Radiobuttons para seleccionar el número de entidades
def cambiar_opcion():
    generate_button.pack(pady=10)
    if opcion.get() == 2:
        load_button.pack_forget()
        compartir_key_display.pack_forget()
        cargar_llave_button.config(state=DISABLED, text="Cargar llave compartida y calcular llave final")
        cargar_llave_button.pack(pady=10)
    else:
        load_button.pack(pady=10)
        compartir_key_display.pack(pady=10)
        cargar_llave_button.config(state=DISABLED, text="Cargar llave final y calcular la tercera vuelta")
        cargar_llave_button.pack(pady=10)

opcion = IntVar()
opcion.set(3)  # Selecciona 3 entidades por defecto

radio_2_entidades = Radiobutton(root, text="2 Entidades", variable=opcion, value=2, command=cambiar_opcion)
radio_2_entidades.pack(pady=5)

radio_3_entidades = Radiobutton(root, text="3 Entidades", variable=opcion, value=3, command=cambiar_opcion)
radio_3_entidades.pack(pady=5)

# Etiqueta y botón para mostrar y generar llaves
public_key_display = Label(root, text="Tu llave pública aparecerá aquí")
public_key_display.pack(pady=20)

# Botón para generar y mostrar llaves
generate_button = Button(root, text="Generar y mostrar llaves", command=generar_y_mostrar_llaves)

# Etiqueta para mostrar resultado del archivo
resultado_archivo = Label(root, text="")
resultado_archivo.pack(pady=10)

# Botón para cargar la llave compartida y calcular la segunda vuelta
load_button = Button(root, text="Cargar llave compartida y calcular la segunda vuelta", command=cargar_llave_compartida)

# Etiqueta para mostrar llave compartida
compartir_key_display = Label(root, text="")

# Botón para cargar la llave final y calcular la tercera vuelta o la llave final
cargar_llave_button = Button(root, text="Cargar llave final y calcular la tercera vuelta", command=cargar_llave_final, state=DISABLED)

# Etiqueta para mostrar la llave final
final_key_display = Label(root, text="")
final_key_display.pack(pady=10)

# Ejecutar la ventana
root.mainloop()
