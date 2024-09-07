import tkinter as tk

def crear_matriz():
    n = int(entry_n.get())
    matriz_frame = tk.Frame(root)
    matriz_frame.pack()
    for i in range(n):
        for j in range(n):
            entry = tk.Entry(matriz_frame, width=5)
            entry.grid(row=i, column=j)

root = tk.Tk()
root.title("Matriz NxN")

label_n = tk.Label(root, text="Ingrese el tamaño de la matriz (n):")
label_n.pack()

entry_n = tk.Entry(root)
entry_n.pack()

crear_button = tk.Button(root, text="Crear Matriz", command=crear_matriz)
crear_button.pack()

root.mainloop()
