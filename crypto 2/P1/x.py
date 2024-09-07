import tkinter as tk

def multiplicar_binario(binario1, binario2):
    binario1 = binario1[::-1]
    binario2 = binario2[::-1]
    resultados_intermedios = [0] * (len(binario1) + len(binario2) - 1)
    for i, bit1 in enumerate(binario1):
        for j, bit2 in enumerate(binario2):
            multiplicacion = int(bit1) * int(bit2)
            resultados_intermedios[i + j] ^= multiplicacion
    resultado_binario = ''.join(str(bit) for bit in resultados_intermedios[::-1])
    return resultado_binario

def divide_binary(dividend, divisor):
    quotient = 0
    remainder = int(dividend, 2)
    divisor = int(divisor, 2)
    divisor_length = len(bin(divisor)[2:])
    while len(bin(remainder)[2:]) >= len(bin(divisor)[2:]):
        shift = len(bin(remainder)[2:]) - divisor_length
        remainder ^= divisor << shift
    return bin(remainder)[2:]

def convert_hexa_to_binary(hexa):
    binary = bin(int(hexa, 16))
    return binary[2:]

def bits_a_polinomio(bits):
    polinomio = ""
    grado = len(bits) - 1
    for i, bit in enumerate(bits):
        if bit == "1":
            if grado - i == 0:
                polinomio += "1"
            else:
                polinomio += f"x^{grado - i}"
            if i != len(bits) - 1:
                polinomio += " + "
    return polinomio

def binary_to_hexa(binario):
    decimal = int(binario, 2)
    hexadecimal = format(decimal, 'X')
    return hexadecimal

def calculate():
    a = entry_a.get()
    b = entry_b.get()
    p = "100011011"
    bin_1 = convert_hexa_to_binary(a)
    bin_2 = convert_hexa_to_binary(b)

    mult = multiplicar_binario(bin_1, bin_2)

    if (len(mult) < len(p)):
        result_text.set(f"Resultados \nBinario: {mult}\nPolinomio: {bits_a_polinomio(mult)}\nHexadecimal: 0x{binary_to_hexa(mult)}")
    else:
        res = divide_binary(mult, p)
        result_text.set(f"Resultados \nBinario: {res}\nPolinomio: {bits_a_polinomio(res)}\nHexadecimal: 0x{binary_to_hexa(res)}")


root = tk.Tk()
root.title("Calculadora")
root.geometry("300x400")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_a = tk.Label(frame, text="A(x): 0x")
label_a.grid(row=0, column=0, sticky="e")

entry_a = tk.Entry(frame)
entry_a.grid(row=0, column=1)

label_b = tk.Label(frame, text="B(x): 0x")
label_b.grid(row=1, column=0, sticky="e")

entry_b = tk.Entry(frame)
entry_b.grid(row=1, column=1)

calculate_button = tk.Button(frame, text="Calcular", command=calculate)
calculate_button.grid(row=2, columnspan=2)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, justify="left")
result_label.grid(row=3, columnspan=2, pady=10)

root.mainloop()
