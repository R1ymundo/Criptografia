import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import AES
import os

ruta_Abosulta = ""

def abrir_explorador():
    global ruta_Abosulta
    explorador = tk.Tk()
    explorador.withdraw()
    archivo = filedialog.askopenfilename()
    ruta = os.path.abspath(archivo)
    ruta_Abosulta = ruta
    ruta_archivo_var.set(ruta_Abosulta)
    explorador.destroy() 

#Funciones Ek

def EK_AES_ECBMode(input_file, key):
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)

    with open(input_file, "rb") as f:
        clear = f.read()
        
    a = len(clear) % 16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.encrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_file = input_file.replace('.bmp', '_eECB.bmp')
        
    with open(output_file, "wb") as f:
        f.write(ciphertext)

def EK_AES_CBCMode(input_file, key, iv):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
  
    with open(input_file, "rb") as f:
        clear = f.read()

    a = len(clear)%16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.encrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_file = input_file.replace('.bmp', '_eCBC .bmp')

    with open(output_file, "wb") as f:
      f.write(ciphertext)

def EK_AES_CFBMode(input_file, key, iv):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CFB, iv)
    
    with open(input_file, "rb") as f:
        clear = f.read()

    a = len(clear)%16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.encrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_file = input_file.replace('.bmp', '_eCFB .bmp')

    with open(output_file, "wb") as f:
        f.write(ciphertext)

def EK_AES_OFBMode(input_file, key, iv):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    cipher = AES.new(key, AES.MODE_OFB, iv)

    with open(input_file, "rb") as f:
        clear = f.read()

    a = len(clear)%16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.encrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_file = input_file.replace('.bmp', '_eOFB .bmp')

    with open(output_file, "wb") as f:
        f.write(ciphertext)

#Funciones Dk

def DK_AES_ECBMode(input_file, key):
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)

    with open(input_file, "rb") as f:
        clear = f.read()

    a = len(clear) % 16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.decrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_path = input_file.replace('.bmp', '_dECB.bmp')

    with open(output_path, "wb") as f:
        f.write(ciphertext)

def DK_AES_CBCMode(input_file, key, iv):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
  
    with open(input_file, "rb") as f:
        clear = f.read()

    a = len(clear)%16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.decrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_path = input_file.replace('.bmp', '_dCBC.bmp')

    with open(output_path, "wb") as f:
        f.write(ciphertext)

def DK_AES_CFBMode(input_file, key, iv):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CFB, iv)

    with open(input_file, "rb") as f:
        clear = f.read()

    a = len(clear)%16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.decrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_path = input_file.replace('.bmp', '_dCFB.bmp')

    with open(output_path, "wb") as f:
      f.write(ciphertext)

def DK_AES_OFBMode(input_file, key, iv):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    cipher = AES.new(key, AES.MODE_OFB, iv)
  
    with open(input_file, "rb") as f:
        clear = f.read()

    a = len(clear)%16
    clear_trimmed = clear[64:-a]
    ciphertext = cipher.decrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-a:]

    output_path = input_file.replace('.bmp', '_dOFB.bmp')

    with open(output_path, "wb") as f:
        f.write(ciphertext)

def procesar():
    name_file = ruta_Abosulta
    modo_seleccionado = modo_operacion.get()
    operacion_seleccionada = operacion_actual.get()
    key = clave_var.get()
    iv = iv_var.get()
    
    modo = modo_operacion.get()
    opcion = operacion_actual.get()

    if opcion == "Cifrar":

        if modo == "ECB":
            EK_AES_ECBMode(name_file, key)
        elif modo == "CBC":
            EK_AES_CBCMode(name_file, key, iv)
        elif modo == "CFB":
            EK_AES_CFBMode(name_file, key, iv)
        elif modo == "OFB":
            EK_AES_OFBMode(name_file, key, iv)

    elif "Descifrar":

        if modo == "ECB":
            DK_AES_ECBMode(name_file, key)
        elif modo == "CBC":
            DK_AES_CBCMode(name_file, key, iv)
        elif modo == "CFB":
            DK_AES_CFBMode(name_file, key, iv)
        elif modo == "OFB":
            DK_AES_OFBMode(name_file, key, iv)

    resultado.config(text=f"Modo: {modo_seleccionado}, Operación: {operacion_seleccionada}")


    
def mostrar_campos_clave_iv(*args):
    modo = modo_operacion.get()
    if modo == "ECB":
        iv_label.pack_forget()
        iv_entry.pack_forget()
        clave_label.pack()
        clave_entry.pack()
    else:
        clave_label.pack()
        clave_entry.pack()
        iv_label.pack()
        iv_entry.pack()

root = tk.Tk()
root.title("Cifrado y Descifrado AES - Modo de Operación")
root.geometry("500x400")

operacion_actual = tk.StringVar(value=" ")
cifrado_descifrado_label = tk.Label(root, text="Seleccione una opcion:")
cifrado_descifrado_label.pack()

cifrar_radio = tk.Radiobutton(root, text="Cifrar", variable=operacion_actual, value="Cifrar")
cifrar_radio.pack()

descifrar_radio = tk.Radiobutton(root, text="Descifrar", variable=operacion_actual, value="Descifrar")
descifrar_radio.pack()

modo_operacion = tk.StringVar()
modo_operacion.set("Seleccione una opcion")  # Establecer el valor predeterminado en ECB

modo_operacion_label = tk.Label(root, text="Seleccione el Modo de Operación:")
modo_operacion_label.pack()

modo_operacion_lista = tk.OptionMenu(root, modo_operacion, "Seleccione una opcion", "ECB", "CBC", "CFB", "OFB")
modo_operacion_lista.pack()

archivo_label = tk.Label(root, text="Seleccionar un archivo:")
archivo_label.pack()

seleccionar_archivo_button = tk.Button(root, text="Seleccionar", command=abrir_explorador)
seleccionar_archivo_button.pack()

ruta_archivo_var = tk.StringVar()
ruta_archivo_entry = tk.Label(root, textvariable=ruta_archivo_var)
ruta_archivo_entry.pack()

clave_label = tk.Label(root, text="Ingresa la clave:")
clave_var = tk.StringVar()
clave_entry = tk.Entry(root, textvariable=clave_var)

iv_label = tk.Label(root, text="Ingresa el Vector de Inicialización (Co):")
iv_var = tk.StringVar()
iv_entry = tk.Entry(root, textvariable=iv_var)

procesar_button = tk.Button(root, text="Procesar", command=procesar)
procesar_button.pack()


modo_operacion.trace("w", mostrar_campos_clave_iv)

resultado = tk.Label(root, text="")
resultado.pack()

root.mainloop()
