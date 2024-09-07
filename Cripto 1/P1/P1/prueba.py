import tkinter as tk
from tkinter import filedialog

def generar_llaves():
    # Lógica para generar llaves
    pass

def cargar_archivo():
    archivo = filedialog.askopenfilename()
    # Lógica para cargar el archivo
    pass

def cargar_llave():
    archivo = filedialog.askopenfilename()
    # Lógica para cargar la llave
    pass

def realizar_operacion():
    # Lógica para realizar la operación (cifrar o descifrar)
    pass

# Crear la ventana principal
root = tk.Tk()
root.title("Cifrar/Descifrar")

# Funciones para activar/desactivar opciones según la selección
def mostrar_opciones_cifrar():
    ocultar_opciones_descifrar()
    subir_archivo_button_cifrar.pack()
    subir_llave_button_cifrar.pack()

def ocultar_opciones_cifrar():
    subir_archivo_button_cifrar.pack_forget()
    subir_llave_button_cifrar.pack_forget()

def mostrar_opciones_descifrar():
    ocultar_opciones_cifrar()
    subir_archivo_button_descifrar.pack()
    subir_llave_button_descifrar.pack()
    subir_llave2_button_descifrar.pack()

def ocultar_opciones_descifrar():
    subir_archivo_button_descifrar.pack_forget()
    subir_llave_button_descifrar.pack_forget()
    subir_llave2_button_descifrar.pack_forget()

# Crear radio botones para Cifrar/Descifrar
opcion_var = tk.StringVar()
opcion_var.set("cifrar")  # Por defecto, seleccionar Cifrar

cifrar_radio = tk.Radiobutton(root, text="Cifrar", variable=opcion_var, value="cifrar", command=mostrar_opciones_cifrar)
descifrar_radio = tk.Radiobutton(root, text="Descifrar", variable=opcion_var, value="descifrar", command=mostrar_opciones_descifrar)

cifrar_radio.pack()
descifrar_radio.pack()

# Botón para Generar Llaves
generar_llaves_button = tk.Button(root, text="Generar Llaves", command=generar_llaves)
generar_llaves_button.pack()

# Botones para subir archivo y llaves
subir_archivo_button_cifrar = tk.Button(root, text="Subir Archivo", command=cargar_archivo)
subir_llave_button_cifrar = tk.Button(root, text="Subir Llave", command=cargar_llave)
subir_archivo_button_descifrar = tk.Button(root, text="Subir Archivo", command=cargar_archivo)
subir_llave_button_descifrar = tk.Button(root, text="Subir Llave", command=cargar_llave)
subir_llave2_button_descifrar = tk.Button(root, text="Subir Otra Llave", command=cargar_llave)

# Botón para realizar la operación
realizar_operacion_button = tk.Button(root, text="Realizar Operación", command=realizar_operacion)
realizar_operacion_button.pack()

# Ocultar las opciones de Cifrar/Descifrar al inicio
ocultar_opciones_descifrar()

root.mainloop()
