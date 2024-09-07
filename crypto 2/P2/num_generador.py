def es_primo(numero):
    if numero <= 1:
        return False
    elif numero <= 3:
        return True
    elif numero % 2 == 0 or numero % 3 == 0:
        return False
    i = 5
    while i * i <= numero:
        if numero % i == 0 or numero % (i + 2) == 0:
            return False
        i += 6
    return True

def phi(n):
    result = n  

    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1

    if n > 1:
        result -= result // n
    return result

def cantidad_generadores(p):
    return phi(p - 1)

def num_generadores(q):
    generadores = []
    for g in range(1, q):
        is_generator = True
        for i in range(1, q - 1):
            if pow(g, i, q) == 1:
                is_generator = False
                break
        if is_generator:
            generadores.append(g)
    return generadores

def orden_elemento(generador, q):
    orden = []

    for j in generador:
        for i  in range(1, q):
            modulo = pow(j, i, q)

            if(modulo == 1):
                orden.append(i)
    return orden


def main():
    while True:
        try:
            numero = int(input("Ingrese un número primo: "))
            if es_primo(numero):
                generadores = num_generadores(numero)
                gen = orden_elemento(generadores, numero)
                print(f"g = {generadores} \nord(g) = {gen}")
                break
            else:
                print(f"{numero} no es un número primo. \nIngresa por favor un número primo.")
        except ValueError:
            print("Error: Por favor ingrese un número entero válido.")
        
        print("\n")

if __name__ == "__main__":
    main()


# def elevar_a_todas_las_potencias(generador, q):
#     potencias = set()
#     for i in range(1, q):
#         potencia = pow(generador, i, q)
#         potencias.add(potencia)
#     return potencias

# def generadores_en_campo_finito(q):
#     generadores = []
#     for g in range(1, q):
#         is_generator = True
#         potencias = elevar_a_todas_las_potencias(g, q)
#         if len(potencias) == q - 1:
#             generadores.append(g)
#     return generadores