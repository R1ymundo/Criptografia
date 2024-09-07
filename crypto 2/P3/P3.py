def inverso_multiplicativo(numero, modulo):
    for i in range(1, modulo):
        if (numero * i) % modulo == 1:
            return i
    return None

def doblado_puntos(x1, x2, y1, y2, a, p):
    im = inverso_multiplicativo(2 * y1, p)
    if im is not None:
        l = ((3 * pow(x1, 2)) + (a)) * (im) % p
        x3 = (pow(l, 2) - x1 - x2) % p
        y3 = ((l * (x1 - x3)) - y1) % p
    elif im is None:
        x3, y3 = -1, -1

    return x3, y3

def suma_puntos(x1, x2, y1, y2, p):
    im = inverso_multiplicativo(x2 - x1, p)
    if im is not None:
        l = ((y2 - y1) * (im)) % p
        x3 = (pow(l, 2) - x1 - x2) % p
        y3 = ((l * (x1 - x3)) - y1) % p
    elif im is None:
        x3, y3 = -1, -1
    
    return x3, y3

def delta(a, b, p):
    valor = (4 * pow(a,3) + 27 * pow(b,2)) % p
    if(valor != 0):
        return True
    else:
        return False

def puntos(a, b, p):
    puntos_list = []
    for i in range(p):
        res_ec = (pow(i,3) + a * i + b) % p
        puntos_list.append((i, res_ec))
        print(f"y^2 = {i}^3 + {a}({i}) + {b} mod {p} = {res_ec}")

    return puntos_list

def coordenadas(p, lista):
    lista_coordenadas = []
    for k, j in lista:
        for i in range(p):
            point = pow(i, 2) % p
            if (j ==  point):
                lista_coordenadas.append(f"({k},{i})")
    
    lista_coordenadas.append("φ")

    print(f"\nE: {lista_coordenadas}")
    return lista_coordenadas

def modulo(x1,y1,x2,y2,p):
    x1 %= p
    y1 %= p
    x2 %= p
    y2 %= p

    return x1,y1,x2,y2

def lista_coordenadas(punto):
    if isinstance(punto, str):
        if punto == 'φ':
            return None, None
        else:
            valores = punto.strip('()').split(',')
            x1 = int(valores[0])
            y1 = int(valores[1])
            return x1, y1

def descomponer(num):
    n1 = (num + 1) // 2
    n2 = num - n1

    return n1, n2

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

def calcular_puntos_generadores(coo, a, p):
    puntos_generadores = []
    coordenadas_generadores = []

    for puntos in coo:
        puntos_generadores.clear()
        
        if puntos == "φ":
            puntos_generadores.append(f"{puntos}")
        else:
            puntos_generadores.append(f"{puntos}")

        for i in range(2, len(coo) + 1):
            n1, n2 = descomponer(i)
            x1, y1 = lista_coordenadas(puntos_generadores[n1 - 1]) 
            x2, y2 = lista_coordenadas(puntos_generadores[n2 - 1]) 

            if x1 is None or x2 is None or y1 is None or y2 is None:
                puntos_generadores.append("φ")
                break
            else:
                x1, y1, x2, y2 = modulo(x1, y1, x2, y2, p)
                if i % 2 == 0:
                    x3, y3 = doblado_puntos(x1, x2, y1, y2, a, p)
                else:
                    x3, y3 = suma_puntos(x1, x2, y1, y2, p)

                if x3 != -1:
                    puntos_generadores.append(f"({x3},{y3})")
                else:
                    puntos_generadores.append("φ")
                    break

        if sorted(coo) == sorted(puntos_generadores):
            coordenadas_generadores.append(puntos)
            
    
    return coordenadas_generadores


a=int(input("Introduce el valor de a: "))
b=int(input("Introduce el valor de b: "))
p=int(input("Introduce el valor de p: "))
print("\n")


lista_puntos = puntos(a, b, p)
coo = coordenadas(p, lista_puntos)

print(f"\n|E| = {len(coo)}\n")

# primo = es_primo(len(coo))
primo = False
coordenadas_generadores = []

if primo == True:
    print("Todos los puntos son generadores")
else:
    coordenadas_generadores = calcular_puntos_generadores(coo, a, p)
    print(coordenadas_generadores)

