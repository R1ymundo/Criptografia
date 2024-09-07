import tkinter as tk

def gcd(a, b):
    while a % b != 0:
        a, b = b, a % b
    return b

def modulo (a, b):
    residuo = a % b 
    return residuo

def extendido_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extendido_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def complemento (a, b):
    complement =  a + b
    return complement

def funcion_cifrado(a, b, c):
    residuo = gcd(a,b)
    
    if residuo != 1:
        resultado = "Ingrese un alpha valido"
    else:
        if c > a:
            c = modulo(c, a)
            resultado = f"C = {b}p + {c} mod {a}"
        else:
            resultado = f"C = {b}p + {c} mod {a}"
    return b, c, a, resultado

def funcion_descifrado(a, b, c):
    mcd, x, y = extendido_gcd(a, c)
    b = complemento(a, b)

    if mcd == 1:
        if y < 0:
            y = complemento(a, y)
            b = modulo(y * b, a)
            resultado = f"p = {y}C + {b} mod {a}"
        else:
            b = modulo(c * b, a)
            resultado = f"p = {c}C + {b} mod {a}"
    else:
        resultado = f"El valor de {c} no tiene inverso multiplicativo, por lo tanto no se puede generar Dk"
    
    return resultado

def validar_entrada(input_text):
    return input_text.isdigit()

def calcular_resultados():
    n_text = entry_n.get()
    alpha_text = entry_alpha.get()
    beta_text = entry_beta.get()

    if not validar_entrada(n_text) or not validar_entrada(alpha_text) or not validar_entrada(beta_text):
        resultado_cifrado_label.config(text="Ingrese solo números válidos.")
        resultado_descifrado_label.config(text="")
        modulo_beta_label.config(text="")
    else:
        n = int(n_text)
        alpha = int(alpha_text)
        beta = int(beta_text)

        p, b, num, resultado_cifrado = funcion_cifrado(n, alpha, beta)
        resultado_descifrado = funcion_descifrado(num, -b, p)
        mensaje = "Ingrese un alpha valido"
        if resultado_cifrado != mensaje:
            modulo_beta_label.config(text="")
            if beta > n:
                beta_1 = beta
                beta =  modulo(beta, n)
                modulo_beta_label.config(text=f"Valor de beta a sido actualizado \n Valor anterior de beta: {beta_1} \n Nuevo valor de beta: {beta}")
        
            resultado_cifrado_label.config(text=f"Ek: {resultado_cifrado}")
            resultado_descifrado_label.config(text=f"Dk: {resultado_descifrado}")
        else:
            resultado_cifrado_label.config(text=resultado_cifrado)
            resultado_descifrado_label.config(text="")
            modulo_beta_label.config(text="")

ventana = tk.Tk()
ventana.title("Cifrado y Descifrado")
ventana.geometry("500x400")

etiqueta_n = tk.Label(ventana, text="Valor de n:")
entry_n = tk.Entry(ventana)
etiqueta_alpha = tk.Label(ventana, text="Valor de alpha:")
entry_alpha = tk.Entry(ventana)
etiqueta_beta = tk.Label(ventana, text="Valor de beta:")
entry_beta = tk.Entry(ventana)

boton_calcular = tk.Button(ventana, text="Calcular", command=calcular_resultados)

modulo_beta_label = tk.Label(ventana, text=" ")
resultado_cifrado_label = tk.Label(ventana, text=" ")
resultado_descifrado_label = tk.Label(ventana, text=" ")

etiqueta_n.pack()
entry_n.pack()
etiqueta_alpha.pack()
entry_alpha.pack()
etiqueta_beta.pack()
entry_beta.pack()
boton_calcular.pack(pady=10)
modulo_beta_label.pack(pady=5)
resultado_cifrado_label.pack(pady=5)
resultado_descifrado_label.pack(pady=5)

ventana.mainloop()