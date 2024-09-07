# import tkinter as tk

# def convert_hexa_to_binary(hexa):
#     binary = bin(int(hexa, 16))
#     return binary[2:]

# def multiplicar_binario(binario1, binario2):
#     binario1 = binario1[::-1]
#     binario2 = binario2[::-1]
#     resultados_intermedios = [0] * (len(binario1) + len(binario2) - 1)
#     for i, bit1 in enumerate(binario1):
#         for j, bit2 in enumerate(binario2):
#             multiplicacion = int(bit1) * int(bit2)
#             resultados_intermedios[i + j] ^= multiplicacion
#     resultado_binario = ''.join(str(bit) for bit in resultados_intermedios[::-1])
#     return resultado_binario

# def bits_a_polinomio(bits):
#     polinomio = ""
#     grado = len(bits) - 1
#     for i, bit in enumerate(bits):
#         if bit == "1":
#             if grado - i == 0:
#                 polinomio += "1"
#             else:
#                 polinomio += f"x^{grado - i}"
#             if i != len(bits) - 1:
#                 polinomio += " + "
#     return polinomio

# def binario_a_hexadecimal(binario):
#     decimal = int(binario, 2)
#     hexadecimal = format(decimal, 'X')
#     return hexadecimal

# def calcular():
#     num_hexa = entry1.get()
#     num_hexa_1 = entry2.get()
#     bin_1 = convert_hexa_to_binary(num_hexa)
#     bin_2 = convert_hexa_to_binary(num_hexa_1)
#     mult = multiplicar_binario(bin_1, bin_2)
#     if len(mult) <= 8:
#         resultado_label.config(text=f"Resultados \nBinario: {mult}\nPolinomio: {bits_a_polinomio(mult)}\nHexadecimal: 0x{binario_a_hexadecimal(mult)}")
#     else:
#         Q = mult
#         M = '100011011'
#         resultado = residuo_bits(int(Q), int(M))
#         resultado_label.config(text=f"Resultados \nBinario: {resultado}\nPolinomio: {bits_a_polinomio(resultado)}\nHexadecimal: 0x{binario_a_hexadecimal(resultado)}")

# def residuo_bits(Q, M):
#     A = 0
#     aux = Q
#     n = 4
#     d = 2
#     z = d ** n
#     while Q >= z:
#         n += 1
#         z = d ** n
#     for _ in range(n, 0, -1):
#         A = A << 1
#         if Q > (z / 2) - 1:
#             A = A + 1
#         if Q >= (z / 2):
#             Q = Q - int(z / 2)
#         Q = Q << 1
#         A = A + (~M + 1)
#         if A < 0:
#             A = A - (~M + 1)
#         else:
#             Q = Q + 1
#     residuo = multiplicar_binario(str(M), str(Q))
#     residuo = resta(str(aux), residuo)
#     residuo = residuo.lstrip('0')
#     return residuo

# def resta(binario1, binario2):
#     max_length = max(len(binario1), len(binario2))
#     binario1 = binario1.zfill(max_length)
#     binario2 = binario2.zfill(max_length)
#     resultado = xor(binario1, binario2)
#     return resultado

# def xor(binario1, binario2):
#     resultado = ''
#     for bit1, bit2 in zip(binario1, binario2):
#         resultado += str(int(bit1) ^ int(bit2))
#     return resultado

# # Crear la ventana principal
# root = tk.Tk()
# root.title("Calculadora")
# root.geometry("300x400")

# # Crear los elementos de la interfaz
# label1 = tk.Label(root, text="A(x): 0x")
# label1.grid(row=0, column=0, sticky="e")
# entry1 = tk.Entry(root)
# entry1.grid(row=0, column=1)

# label2 = tk.Label(root, text="B(x): 0x")
# label2.grid(row=1, column=0, sticky="e")
# entry2 = tk.Entry(root)
# entry2.grid(row=1, column=1)

# calcular_button = tk.Button(root, text="Calcular", command=calcular)
# calcular_button.grid(row=2, column=0, columnspan=2)

# resultado_label = tk.Label(root, text="")
# resultado_label.grid(row=3, column=0, columnspan=2)

# # Ejecutar el bucle de eventos
# root.mainloop()


# def binary_to_polynomial(binary):
#     polynomial = ""
#     for i in range(len(binary)):
#         if binary[i] == '1':
#             degree = len(binary) - 1 - i
#             if degree == 0:
#                 polynomial += "1"
#             elif degree == 1:
#                 polynomial += "x + "
#             else:
#                 polynomial += "x^" + str(degree) + " + "
#     if polynomial.endswith(" + "):
#         polynomial = polynomial[:-3]  # Eliminar el último " + "
#     return polynomial

# # Ejemplo de uso:
# binary_number = "1100"
# polynomial_representation = binary_to_polynomial(binary_number)
# print("El polinomio correspondiente a", binary_number, "es:", polynomial_representation)

x = 3
num = 17
print(num % x)