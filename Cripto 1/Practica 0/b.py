import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

ruta_Abosulta = ""
#8043 82 32
def abrir_explorador():
    global ruta_Abosulta
    explorador = tk.Tk()
    explorador.withdraw()
    archivo = filedialog.askopenfilename()
    ruta = os.path.abspath(archivo)
    ruta_Abosulta = ruta
    explorador.destroy() 

def modulo(r, g, b):
    r_mod, g_mod, b_mod = r, g, b 

    if r_mod > 255:
        r_mod = r_mod % 256
    if g_mod > 255:
        g_mod = g_mod % 256
    if b_mod > 255:
        b_mod = b_mod % 256

    return r_mod, g_mod, b_mod

def absoluto(r, g, b):
    if r < 0:
        r = 256 + r
    if g < 0:
        g = 256 + g
    if b < 0:
        b = 256 + b
    return r, g, b

def mostrar_imagen(imagen_path):
    imagen = Image.open(imagen_path)
    imagen.thumbnail((300, 300))
    foto = ImageTk.PhotoImage(imagen)
    imagen_label.config(image=foto)
    imagen_label.image = foto

def realizar_operacion():
    global ruta_Abosulta

    ruta = ruta_Abosulta
    nombre = os.path.splitext(os.path.basename(ruta))[0]

    r_input = int(numero_r.get())
    g_input = int(numero_g.get())
    b_input = int(numero_b.get())

    r_input, g_input, b_input = modulo(r_input, g_input, b_input)

    imagen = Image.open(ruta)
    ancho, alto = imagen.size

    for x in range(ancho):
        for y in range(alto):
            r, g, b = imagen.getpixel((x, y))
            
            if opcion.get() == "cifrar":
                r_actualizado, g_actualizado, b_actualizado = r - r_input, g - g_input, b - b_input
                r_act, g_act, b_act = absoluto(r_actualizado, g_actualizado, b_actualizado)
            elif opcion.get() == "descifrar":
                r_actualizado, g_actualizado, b_actualizado = r + r_input, g + g_input, b + b_input
                r_act, g_act, b_act = modulo(r_actualizado, g_actualizado, b_actualizado)

            imagen.putpixel((x, y), (r_act, g_act, b_act))

    imagen_resultante_path = f"{nombre}_c.bmp" if opcion.get() == "cifrar" else f"{nombre}_d.bmp"
    imagen.save(imagen_resultante_path)
    imagen.close()

    mostrar_imagen(imagen_resultante_path)


ventana = tk.Tk()
ventana.title("Cifrado y Descifrado")
ventana.geometry("500x600")

opcion = tk.StringVar()
opcion.set(" ")
radio_cifrar = tk.Radiobutton(ventana, text="Cifrar", variable=opcion, value="cifrar")
radio_descifrar = tk.Radiobutton(ventana, text="Descifrar", variable=opcion, value="descifrar")
radio_cifrar.pack(pady=5) 
radio_descifrar.pack(pady=5) 

etiqueta_r = tk.Label(ventana, text="Ingrese un número del 0-255:")
etiqueta_r.pack(pady=5)

numero_r = tk.Entry(ventana)
numero_r.pack(pady=5)

etiqueta_g = tk.Label(ventana, text="Ingrese un número del 0-255:")
etiqueta_g.pack(pady=5)

numero_g = tk.Entry(ventana)
numero_g.pack(pady=5)

etiqueta_b = tk.Label(ventana, text="Ingrese un número del 0-255:")
etiqueta_b.pack(pady=5)

numero_b = tk.Entry(ventana)
numero_b.pack(pady=5)

boton_seleccionar = tk.Button(ventana, text="Seleccionar Archivo", command=abrir_explorador)
boton_seleccionar.pack(pady=5)

boton_realizar = tk.Button(ventana, text="Realizar Operación", command=realizar_operacion)
boton_realizar.pack(pady=5)

imagen_label = tk.Label(ventana)
imagen_label.pack(pady=10)

ventana.mainloop()
