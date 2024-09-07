import tkinter as tk

# Función de exponenciación rápida
def exp_rapida(base, exponente, modulo):
    x = 1
    y = base % modulo
    b = exponente
    while b > 0:
        if b % 2 == 0:  # Si b es par...
            y = (y * y) % modulo
            b = b // 2  # Usar división entera para obtener un entero en Python 3
        else:  # Si b es impar...
            x = (x * y) % modulo
            b = b - 1
    return x

# Función para el algoritmo de Diffie-Hellman
def diffie_hellman():
    def calculate():
        p = int(entry_p.get())
        g = int(entry_g.get())
        a = int(entry_a.get())

        A = exp_rapida(g, a, p)
        label_result_a.config(text=f"La clave pública generada es: {A}")
        
        k = int(entry_k.get())
        B = exp_rapida(k, a, p)
        label_result_a_1.config(text=f"La clave pública generada es: {B}")
        k_1 = int(entry_k_2.get())
        K = exp_rapida(k_1, a, p)
        label_result_k.config(text=f"La clave común generada es: {K}")

    window = tk.Tk()
    window.title("Diffie-Hellman")

    label_p = tk.Label(window, text="Ingrese el valor de p (número primo):")
    label_p.pack()
    entry_p = tk.Entry(window)
    entry_p.pack()

    label_g = tk.Label(window, text="Ingrese el valor de g (generador):")
    label_g.pack()
    entry_g = tk.Entry(window)
    entry_g.pack()

    label_a = tk.Label(window, text="Ingrese el valor de a (clave privada para este usuario):")
    label_a.pack()
    entry_a = tk.Entry(window)
    entry_a.pack()

    button_calculate = tk.Button(window, text="Calcular", command=calculate)
    button_calculate.pack()

    label_result_a = tk.Label(window, text="")
    label_result_a.pack()

    label_k = tk.Label(window, text="Ingrese la clave pública del otro usuario (K):")
    label_k.pack()

    entry_k = tk.Entry(window)
    entry_k.pack()

    button_calculate_k = tk.Button(window, text="Calcular K", command=calculate)
    button_calculate_k.pack()

    label_result_a_1 = tk.Label(window, text="")
    label_result_a_1.pack()

    label_k_2 = tk.Label(window, text="Ingrese la clave pública del otro usuario (K) nuevamente:")
    label_k_2.pack()

    entry_k_2 = tk.Entry(window)
    entry_k_2.pack()

    button_calculate_k_2 = tk.Button(window, text="Calcular K", command=calculate)
    button_calculate_k_2.pack()

    label_result_k = tk.Label(window, text="")
    label_result_k.pack()

    window.mainloop()

# Ejecutar el algoritmo de Diffie-Hellman
diffie_hellman()
