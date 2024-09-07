import tkinter as tk

def multiply_binary(a, b):
    product = 0
    for i, digit in enumerate(reversed(b)):
        if digit == '1':
            product ^= int(a, 2) << i
    return bin(product)[2:]

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

def binary_to_polynomial(binary):
    polynomial = ""
    for i in range(len(binary)):
        if binary[i] == '1':
            degree = len(binary) - 1 - i
            if degree == 0:
                polynomial += "1"
            elif degree == 1:
                polynomial += "x + "
            else:
                polynomial += "x^" + str(degree) + " + "
    if polynomial.endswith(" + "):
        polynomial = polynomial[:-3]
    return polynomial

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

    mult = multiply_binary(bin_1, bin_2)

    if (len(mult) < len(p)):
        result_text.set(f"Resultados \nBinario: {mult}\nPolinomio: {binary_to_polynomial(mult)}\nHexadecimal: 0x{binary_to_hexa(mult)}")
    else:
        res = divide_binary(mult, p)
        result_text.set(f"Resultados \nBinario: {res}\nPolinomio: {binary_to_polynomial(res)}\nHexadecimal: 0x{binary_to_hexa(res)}")


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
