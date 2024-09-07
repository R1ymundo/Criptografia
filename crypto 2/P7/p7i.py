import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec  
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Funciones del código original
def generar_llaves():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

def firmar_archivo(private_pem, archivo):
    private_key = serialization.load_pem_private_key(private_pem, password=None, backend=default_backend())
    with open(archivo, 'rb') as f:
        contenido = f.read()
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(contenido)
    digest = hash_mensaje.finalize()
    signature = private_key.sign(digest, ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(signature)
    with open(archivo, 'ab') as f:
        f.write(f"\n{r}\n{s}".encode())
    return r, s

def leer_firma(archivo):
    with open(archivo, 'rb') as f:
        contenido = f.read()
    lineas = contenido.split(b'\n')
    r = int(lineas[-2])
    s = int(lineas[-1])
    contenido_sin_firma = b'\n'.join(lineas[:-2])
    return r, s, contenido_sin_firma

def verificar_archivo(public_pem, archivo):
    public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())
    r, s, contenido = leer_firma(archivo)
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(contenido)
    digest = hash_mensaje.finalize()
    signature = encode_dss_signature(r, s)
    try:
        public_key.verify(signature, digest, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception as e:
        print(f"Error durante la verificación: {e}")
        return False

def key_iv(key):
    with open(key, 'rb') as f:
        ecdh_key = f.read()
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32 + 16,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(ecdh_key)
    aes_key = derived_key[:32]
    iv = derived_key[32:]
    return aes_key, iv

def cifrarArchivo(archivo, ecdh_key):
    with open(archivo, 'rb') as f:
        contenido = f.read()
    aes_key, iv = key_iv(ecdh_key)
    data = contenido
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

def descifrarArchivo(archivo, ecdh_key):
    with open(archivo, 'rb') as f:
        contenido = f.read()
    aes_key, iv = key_iv(ecdh_key)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(contenido) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

def cifrado_firma(private_pem, archivo, key):
    private_key = serialization.load_pem_private_key(private_pem, password=None, backend=default_backend())
    with open(archivo, 'rb') as f:
        contenido = f.read()
    ciphertext = cifrarArchivo(archivo, key)
    with open(archivo, 'wb') as f:
        f.write(ciphertext)
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(contenido)
    digest = hash_mensaje.finalize()
    signature = private_key.sign(digest, ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(signature)
    with open(archivo, 'ab') as f:
        f.write(f"\n{r}\n{s}".encode())

def descifrado_verificado(public_pem, archivo, key):
    public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())
    r, s, contenido = leer_firma(archivo)
    with open(archivo, 'rb') as f:
        contenido = f.readlines()
    contenido = b''.join(contenido[:-2]).rstrip(b'\n')
    aes_key, iv = key_iv(key)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(contenido) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    with open(archivo, 'wb') as f:
        f.write(plaintext)
    with open(archivo, 'ab') as f:
        f.write(f"\n{r}\n{s}".encode())
    hash_mensaje = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash_mensaje.update(plaintext)
    digest = hash_mensaje.finalize()
    signature = encode_dss_signature(r, s)
    try:
        public_key.verify(signature, digest, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception as e:
        print(f"Error durante la verificación: {e}")
        return False

# Interfaz gráfica con Tkinter
def mostrar_opciones(opcion):
    for widget in opciones_frame.winfo_children():
        widget.destroy()

    if opcion == "Generar Llaves":
        tk.Button(opciones_frame, text="Generar Llaves", command=generar_llaves_gui).pack(fill="x")

    elif opcion == "Firmar Archivo":
        crear_seleccion_archivo(opciones_frame, "Seleccionar Clave Privada PEM", "private_pem")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Archivo a Firmar", "archivo")
        tk.Button(opciones_frame, text="Firmar Archivo", command=firmar_archivo_gui).pack(fill="x")

    elif opcion == "Verificar Firma":
        crear_seleccion_archivo(opciones_frame, "Seleccionar Clave Pública PEM", "public_pem")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Archivo a Verificar", "archivo")
        tk.Button(opciones_frame, text="Verificar Firma", command=verificar_archivo_gui).pack(fill="x")

    elif opcion == "Cifrar Archivo":
        crear_seleccion_archivo(opciones_frame, "Seleccionar Archivo a Cifrar", "archivo")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Llave Compartida", "key")
        tk.Button(opciones_frame, text="Cifrar Archivo", command=cifrar_archivo_gui).pack(fill="x")

    elif opcion == "Descifrar Archivo":
        crear_seleccion_archivo(opciones_frame, "Seleccionar Archivo a Descifrar", "archivo")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Llave Compartida", "key")
        tk.Button(opciones_frame, text="Descifrar Archivo", command=descifrar_archivo_gui).pack(fill="x")

    elif opcion == "Cifrar y Firmar Archivo":
        crear_seleccion_archivo(opciones_frame, "Seleccionar Clave Privada PEM", "private_pem")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Archivo a Cifrar y Firmar", "archivo")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Llave Compartida", "key")
        tk.Button(opciones_frame, text="Cifrar y Firmar Archivo", command=cifrar_firma_gui).pack(fill="x")

    elif opcion == "Descifrar y Verificar Firma":
        crear_seleccion_archivo(opciones_frame, "Seleccionar Clave Pública PEM", "public_pem")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Archivo a Descifrar y Verificar", "archivo")
        crear_seleccion_archivo(opciones_frame, "Seleccionar Llave Compartida", "key")
        tk.Button(opciones_frame, text="Descifrar y Verificar Firma", command=descifrar_verificar_gui).pack(fill="x")

def crear_seleccion_archivo(frame, texto_boton, tipo):
    def seleccionar_archivo():
        archivo_path = filedialog.askopenfilename()
        archivos[tipo] = archivo_path
        label.config(text=archivo_path if archivo_path else "No seleccionado")

    boton_frame = tk.Frame(frame)
    boton_frame.pack(fill="x")
    tk.Button(boton_frame, text=texto_boton, command=seleccionar_archivo).pack(side="left")
    label = tk.Label(boton_frame, text="No seleccionado")
    label.pack(side="left", padx=5)

def generar_llaves_gui():
    private_pem, public_pem = generar_llaves()
    with open("clave_privada.pem", "wb") as f:
        f.write(private_pem)
    with open("clave_publica.pem", "wb") as f:
        f.write(public_pem)
    messagebox.showinfo("Éxito", "Claves generadas y guardadas en 'clave_privada.pem' y 'clave_publica.pem'")

def firmar_archivo_gui():
    private_pem_path = archivos.get("private_pem")
    archivo = archivos.get("archivo")
    if not private_pem_path or not archivo:
        messagebox.showerror("Error", "Por favor selecciona todos los archivos necesarios.")
        return
    with open(private_pem_path, "rb") as f:
        private_pem = f.read()
    r, s = firmar_archivo(private_pem, archivo)
    messagebox.showinfo("Firma generada", f"Firma generada: (r={r}, s={s})")

def verificar_archivo_gui():
    public_pem_path = archivos.get("public_pem")
    archivo = archivos.get("archivo")
    if not public_pem_path or not archivo:
        messagebox.showerror("Error", "Por favor selecciona todos los archivos necesarios.")
        return
    with open(public_pem_path, "rb") as f:
        public_pem = f.read()
    es_valido = verificar_archivo(public_pem, archivo)
    if es_valido:
        messagebox.showinfo("Verificación", "La firma es válida.")
    else:
        messagebox.showerror("Verificación", "La firma no es válida.")

def cifrar_archivo_gui():
    archivo = archivos.get("archivo")
    key_path = archivos.get("key")
    if not archivo or not key_path:
        messagebox.showerror("Error", "Por favor selecciona todos los archivos necesarios.")
        return
    ciphertext = cifrarArchivo(archivo, key_path)
    with open("archivo_cifrado.txt", "wb") as f:
        f.write(ciphertext)
    messagebox.showinfo("Éxito", "Archivo cifrado y guardado como 'archivo_cifrado.txt'")

def descifrar_archivo_gui():
    archivo = archivos.get("archivo")
    key_path = archivos.get("key")
    if not archivo or not key_path:
        messagebox.showerror("Error", "Por favor selecciona todos los archivos necesarios.")
        return
    plaintext = descifrarArchivo(archivo, key_path)
    with open("archivo_descifrado.txt", "wb") as f:
        f.write(plaintext)
    messagebox.showinfo("Éxito", "Archivo descifrado y guardado como 'archivo_descifrado.txt'")

def cifrar_firma_gui():
    private_pem_path = archivos.get("private_pem")
    archivo = archivos.get("archivo")
    key_path = archivos.get("key")
    if not private_pem_path or not archivo or not key_path:
        messagebox.showerror("Error", "Por favor selecciona todos los archivos necesarios.")
        return
    with open(private_pem_path, "rb") as f:
        private_pem = f.read()
    cifrado_firma(private_pem, archivo, key_path)
    messagebox.showinfo("Éxito", "Archivo cifrado y firmado.")

def descifrar_verificar_gui():
    public_pem_path = archivos.get("public_pem")
    archivo = archivos.get("archivo")
    key_path = archivos.get("key")
    if not public_pem_path or not archivo or not key_path:
        messagebox.showerror("Error", "Por favor selecciona todos los archivos necesarios.")
        return
    with open(public_pem_path, "rb") as f:
        public_pem = f.read()
    es_valido = descifrado_verificado(public_pem, archivo, key_path)
    if es_valido:
        messagebox.showinfo("Verificación", "La firma es válida.")
    else:
        messagebox.showerror("Verificación", "La firma no es válida.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Criptografía con Curvas Elípticas")

frame = tk.Frame(root, padx=100, pady=100)
frame.pack(padx=10, pady=10)

tk.Button(frame, text="Generar Llaves", command=lambda: mostrar_opciones("Generar Llaves")).pack(fill="x")
tk.Button(frame, text="Firmar Archivo", command=lambda: mostrar_opciones("Firmar Archivo")).pack(fill="x")
tk.Button(frame, text="Verificar Firma", command=lambda: mostrar_opciones("Verificar Firma")).pack(fill="x")
tk.Button(frame, text="Cifrar Archivo", command=lambda: mostrar_opciones("Cifrar Archivo")).pack(fill="x")
tk.Button(frame, text="Descifrar Archivo", command=lambda: mostrar_opciones("Descifrar Archivo")).pack(fill="x")
tk.Button(frame, text="Cifrar y Firmar Archivo", command=lambda: mostrar_opciones("Cifrar y Firmar Archivo")).pack(fill="x")
tk.Button(frame, text="Descifrar y Verificar Firma", command=lambda: mostrar_opciones("Descifrar y Verificar Firma")).pack(fill="x")

opciones_frame = tk.Frame(root, padx=10, pady=10)
opciones_frame.pack(padx=10, pady=10)

archivos = {}

root.mainloop()
