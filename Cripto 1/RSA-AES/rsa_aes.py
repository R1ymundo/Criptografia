from flask import Flask, request, send_file
from flask_cors import CORS
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask import jsonify
from fpdf import FPDF
import binascii
import os
import base64
import fitz


def key_iv_cifrado(data):

    key = get_random_bytes(16)
    IV = get_random_bytes(16)

    key = PBKDF2(key, salt=16, dkLen=16)
    IV = PBKDF2(IV, salt=16, dkLen=16)

    cipher = AES.new(key, AES.MODE_CBC, iv = IV)
    ciphertext_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

    ciphertext_hexadecimal = binascii.hexlify(ciphertext_bytes).decode('utf-8')
    
    return key, IV, ciphertext_hexadecimal

def key_iv_descifrado(data, IV, key):
    decipher = AES.new(key, AES.MODE_CBC, iv=IV)
    deciphertext = unpad(decipher.decrypt(data), AES.block_size)

    return deciphertext.decode('utf-8')

def cifrado_RSA (clave_publica, iv, key):
    with open(clave_publica) as f:
        llave_publica = f.read()
        llave_publica = RSA.importKey(llave_publica)

        cipher = PKCS1_OAEP.new(llave_publica)

        iv_cifrado = cipher.encrypt(iv)
        key_cifrado = cipher.encrypt(key)
    
    return iv_cifrado, key_cifrado

def descifrado_RSA(clave_privada, key, iv):
    with open(clave_privada) as f:
        llave_privada = f.read()
        llave_privada = RSA.importKey(llave_privada)
        
        decipher = PKCS1_OAEP.new(llave_privada) 

        key_descifrado = decipher.decrypt(key)
        iv_descifrado = decipher.decrypt(iv)
        
    
    return iv_descifrado, key_descifrado

def firmar(message, direccion):
    message = message.replace('\n', ' ')
    with open(direccion) as f:
        key = f.read()
        rsaKey = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsaKey)

        digesto = SHA.new()
        digesto.update(message.encode())

        sign = signer.sign(digesto)
        signature = base64.b64encode(sign).decode('utf-8')
        
    return signature

def verificar_firma(mensaje, firma, clave_publica):
    with open(clave_publica) as f:
            key = f.read()
            rsaKey = RSA.importKey(key)
            verifier = Signature_pkcs1_v1_5.new(rsaKey)
            
            digesto = SHA.new()
            digesto.update(mensaje)
            is_Verify = verifier.verify(digesto, base64.b64decode(firma))

            if is_Verify:
                return "La firma es válida."
            else:
                return "La firma no es válida."
            
def generar_pdf(mensaje, firma):
    current_dir = os.path.dirname(__file__)  # Obtiene la ruta del directorio actual
    pdf_path = os.path.join(current_dir, 'documento.pdf')  # Ruta completa para guardar el PDF

    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    pdf.add_page()

    pdf.set_font('Arial', '', 12)

    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Mensaje', 0, 1)
    pdf.set_text_color(0, 0, 0)  

    pdf.multi_cell(w=0, h=5, txt=mensaje, border=0, align='J', fill=0)
    pdf.ln()

    pdf.cell(0, 10, 'Firma', 0, 1)
    pdf.multi_cell(w=0, h=5, txt=firma, border=0, align='J', fill=0)
    pdf.ln()

    pdf.output(pdf_path)

    return pdf_path

def generar_pdf_AES_RSA(mensaje, firma, key, iv):
    current_dir = os.path.dirname(__file__)  # Obtiene la ruta del directorio actual
    pdf_path = os.path.join(current_dir, 'documento.pdf')  # Ruta completa para guardar el PDF

    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    pdf.add_page()

    pdf.set_font('Arial', '', 12)

    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Mensaje', 0, 1)
    pdf.set_text_color(0, 0, 0)  

    pdf.multi_cell(w=0, h=5, txt=mensaje, border=0, align='J', fill=0)
    pdf.ln()

    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'IV', 0, 1)
    pdf.set_text_color(0, 0, 0)

    pdf.multi_cell(w=0, h=5, txt=iv, border=0, align='J', fill=0)

    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'KEY', 0, 1)
    pdf.set_text_color(0, 0, 0)  

    pdf.multi_cell(w=0, h=5, txt=key, border=0, align='J', fill=0)
    pdf.ln()

    pdf.cell(0, 10, 'Firma', 0, 1)
    pdf.multi_cell(w=0, h=5, txt=firma, border=0, align='J', fill=0)
    pdf.ln()

    pdf.output(pdf_path)

    return pdf_path

def generar_pdf_auxiliar(mensaje):
    current_dir = os.path.dirname(__file__)  # Obtiene la ruta del directorio actual
    pdf_path = os.path.join(current_dir, 'documento.pdf')  # Ruta completa para guardar el PDF

    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    pdf.add_page()

    pdf.set_font('Arial', '', 12)

    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Mensaje', 0, 1)
    pdf.set_text_color(0, 0, 0)  

    pdf.multi_cell(w=0, h=5, txt=mensaje, border=0, align='J', fill=0)
    pdf.ln()

    pdf.output(pdf_path)

    return pdf_path

def extraer_mensaje_y_firma(pdf_path):
    mensaje = ""
    firma = ""

    # Abre el archivo PDF
    pdf_documento = fitz.open(pdf_path)

    # Banderas para detectar las palabras clave "Mensaje" y "Firma"
    mensaje_encontrado = False
    firma_encontrada = False

    # Recorre cada página del PDF
    for pagina in range(pdf_documento.page_count):
        pagina_actual = pdf_documento.load_page(pagina)
        texto_pagina = pagina_actual.get_text()

        # Busca las palabras clave "Mensaje" y "Firma" seguidas de un salto de línea
        for linea in texto_pagina.split('\n'):
            if not mensaje_encontrado and linea.strip().lower() == "mensaje":
                mensaje_encontrado = True
                continue

            if mensaje_encontrado and linea.strip().lower() == "firma":
                firma_encontrada = True
                continue

            # Almacena el texto entre "Mensaje" y "Firma"
            if mensaje_encontrado and not firma_encontrada and linea.strip() != "":
                # Elimina saltos de línea en el mensaje y concatena líneas según las reglas
                if not mensaje.endswith((' ', '-', ',', ';', ':', '.', '?', '!', '"', "'", ')')):
                    mensaje += ' '

                mensaje += linea.strip()

            # Almacena todo el texto después de "Firma"
            if firma_encontrada and linea.strip() != "":
                firma += linea.strip() + ' '
    # Cierra el archivo PDF
    pdf_documento.close()

    return mensaje.strip(), firma.strip()

def extraer_datos(pdf_path):
    mensaje = ""
    firma = ""
    texto_iv = ""
    texto_key = ""
    extrayendo_iv = False
    extrayendo_key = False

    # Abre el archivo PDF
    pdf_documento = fitz.open(pdf_path)

    # Banderas para detectar las palabras clave "Mensaje", "Firma", "IV" y "key"
    mensaje_encontrado = False
    firma_encontrada = False

    # Recorre cada página del PDF
    for pagina in range(pdf_documento.page_count):
        pagina_actual = pdf_documento.load_page(pagina)
        texto_pagina = pagina_actual.get_text()

        # Busca las palabras clave "Mensaje" y "Firma" seguidas de un salto de línea
        for linea in texto_pagina.split('\n'):
            if not mensaje_encontrado and linea.strip().lower() == "mensaje":
                mensaje_encontrado = True
                continue
            
            if mensaje_encontrado and not extrayendo_iv:
                if linea.strip().lower() == "iv":
                    extrayendo_iv = True
                    mensaje_encontrado = False
                else:
                    mensaje += linea.strip()

            # Extraer contenido entre "IV" y "key", y entre "key" y "firma"
            if  extrayendo_iv and linea.strip().lower() == "iv":
                extrayendo_iv = True
                continue

            if extrayendo_iv and not extrayendo_key:
                if linea.strip().lower() == "key":
                    extrayendo_iv = False
                    extrayendo_key = True
                else:
                    texto_iv += linea.strip()
            
            if  extrayendo_key and linea.strip().lower() == "key":
                extrayendo_key = True
                continue
            
            if extrayendo_key and not firma_encontrada:
                if linea.strip().lower() == "firma":
                    firma_encontrada = True
                    extrayendo_key = False
                else:
                    texto_key += linea.strip()
            
            if  firma_encontrada and linea.strip().lower() == "firma":
                firma_encontrada = True
                continue

            if firma_encontrada and linea.strip() != "":
                firma += linea.strip()

    # Cierra el archivo PDF
    pdf_documento.close()

    return mensaje.strip(), firma.strip(), texto_iv.strip(), texto_key.strip()


# Guardar el archivo del mensaje en el servidor o realizar alguna acción
ruta_mensaje = 'C:/Users/raymu/OneDrive/Escritorio/Crypto/firma/runaway.txt'

# Guardar el archivo recibido en el servidor
ruta_llave_privada = 'C:/Users/raymu/OneDrive/Escritorio/Crypto/firma/Clave_Privada.pem'

# Guardar el archivo recibido en el servidor
ruta_llave_publica = 'C:/Users/raymu/OneDrive/Escritorio/Crypto/firma/Clave_Publica.pem'

with open(ruta_mensaje, 'r') as file:
    # Lee el contenido del archivo y lo guarda en una variable
    contenido = file.read()

key, IV, ciphertext = key_iv_cifrado(contenido)
key_1 = binascii.hexlify(key).decode('utf-8')
IV_1 = binascii.hexlify(IV).decode('utf-8')

pdf_path_auxiliar =  generar_pdf_auxiliar(contenido)
mensaje_extraido, firma_extraida = extraer_mensaje_y_firma(pdf_path_auxiliar)

# Firmar el mensaje recibido
signature = firmar(mensaje_extraido, ruta_llave_privada)

IV_cifrado, key_cifrado = cifrado_RSA(ruta_llave_publica, IV, key)

key_cifrado = binascii.hexlify(key_cifrado).decode('utf-8')
IV_cifrado = binascii.hexlify(IV_cifrado).decode('utf-8')

# Crear el PDF con el mensaje, firma, key y IV
pdf_path = generar_pdf_AES_RSA(ciphertext, signature, key_cifrado, IV_cifrado)



#-----------Descifrar--------------------#
# mensaje, firma, iv, llave = extraer_datos(pdf_path)

# key_descifrado = binascii.unhexlify(llave)
# IV_descifrado = binascii.unhexlify(iv)
# mensaje = binascii.unhexlify(mensaje.encode('utf-8'))


# IV_descifrado, key_descifrado = descifrado_RSA(ruta_llave_privada, key_descifrado, IV_descifrado)

# deciphertext = key_iv_descifrado(mensaje, IV_descifrado, key_descifrado)


# pdf_path = generar_pdf(deciphertext, firma)
# mensaje_extraido, firma_extraida = extraer_mensaje_y_firma(pdf_path)
# mensaje_extraido = mensaje_extraido.encode('utf-8')
# firma_extraida = firma_extraida.encode('utf-8')

# mensaje_verificado = verificar_firma(mensaje_extraido, firma_extraida, ruta_llave_publica)

# print(mensaje_verificado)
