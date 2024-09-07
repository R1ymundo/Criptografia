import os

def eliminar_caracteres(texto):
    caracteres = ["\n", " ", "!", "?", ",", "'", "(", ")", "."]
    for caracter in caracteres: 
        texto = texto.replace(caracter, "")
    return texto
    

def mayusculas(cadena_minuscula):
    texto_mayusculas = "" 
    for caracter in cadena_minuscula:
            if 'a' <= caracter <= 'z':
                valor_ascii_minuscula = ord(caracter)
                valor_ascii_mayuscula = valor_ascii_minuscula - 32
                caracter_mayuscula = chr(valor_ascii_mayuscula)
                texto_mayusculas += caracter_mayuscula
            else:
                texto_mayusculas += caracter
    print(texto_mayusculas)


def minusculas(cadena_mayuscula):
    texto_minuscula = "" 
    for caracter in cadena_mayuscula:
        if 'A' <= caracter <= 'Z':
            valor_ascii_mayuscula = ord(caracter)
            valor_ascii_minuscula = valor_ascii_mayuscula + 32
            caracter_minuscula = chr(valor_ascii_minuscula)
            texto_minuscula += caracter_minuscula
        else:
            texto_minuscula += caracter
    print(texto_minuscula)


cancion = "runaway.txt"

try:
    with open(cancion, 'r') as archivo:
        cancion = archivo.read()
        
        cancion = eliminar_caracteres(cancion)

        mayusculas(cancion)

        minusculas(cancion)


except FileNotFoundError:
    print(f"El archivo '{cancion}' no fue encontrado.")

except Exception as e:
    print(f"Ocurrió un error al abrir el archivo: {e}")
