import fitz  # PyMuPDF

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

# Ejemplo de uso:
ruta_pdf = 'documento.pdf'  # Cambia 'tu_archivo.pdf' por la ruta de tu PDF
mensaje_extraido, firma_extraida = extraer_mensaje_y_firma(ruta_pdf)
print("Mensaje extraído:")
print(mensaje_extraido)
print("\nFirma extraída:")
print(firma_extraida)
