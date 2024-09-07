def inverse_modulo(number, modulus):
    """Encuentra el inverso multiplicativo de 'number' módulo 'modulus'."""
    for i in range(1, modulus):
        if (number * i) % modulus == 1:
            return i
    return None

def point_doubling(x1, y1, a, p):
    """Realiza la operación de duplicación de puntos en la curva elíptica y^2 = x^3 + ax + b (mod p)."""
    if y1 == 0:
        return None, None  # Punto en el infinito

    im = inverse_modulo(2 * y1, p)
    if im is not None:
        l = (3 * x1**2 + a) * im % p
        x3 = (l**2 - 2 * x1) % p
        y3 = (l * (x1 - x3) - y1) % p
        return x3, y3
    else:
        return None, None

def point_addition(x1, y1, x2, y2, p):
    """Realiza la operación de suma de puntos en la curva elíptica y^2 = x^3 + ax + b (mod p)."""
    if x1 == x2 and y1 == (-y2 % p):
        return None, None  # Punto en el infinito

    im = inverse_modulo(x2 - x1, p)
    if im is not None:
        l = (y2 - y1) * im % p
        x3 = (l**2 - x1 - x2) % p
        y3 = (l * (x1 - x3) - y1) % p
        return x3, y3
    else:
        return None, None

def is_prime(number):
    """Verifica si un número es primo."""
    if number <= 1:
        return False
    elif number <= 3:
        return True
    elif number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True

def find_curve_points(a, b, p):
    """Encuentra todos los puntos (x, y) que satisfacen y^2 = x^3 + ax + b (mod p)."""
    points = []
    for x in range(p):
        y_squared = (x**3 + a * x + b) % p
        if is_square(y_squared, p):
            y = modular_sqrt(y_squared, p)
            points.append((x, y))
            if y != 0:  # También considerar el punto simétrico
                points.append((x, p - y))
    return points

def is_square(n, p):
    """Verifica si n es un cuadrado perfecto módulo p."""
    return pow(n, (p - 1) // 2, p) == 1

def modular_sqrt(a, p):
    """Calcula la raíz cuadrada modular de a módulo p usando el criterio de Euler."""
    return pow(a, (p + 1) // 4, p) if pow(a, (p - 1) // 2, p) == 1 else None

def calculate_generators(points, a, p):
    """Calcula los puntos generadores en la curva elíptica y^2 = x^3 + ax + b (mod p)."""
    generators = []
    for i in range(1, len(points)):
        for j in range(i + 1, len(points) + 1):
            if (i + j) <= len(points):
                x1, y1 = points[i - 1]
                x2, y2 = points[j - 1]
                x1, y1, x2, y2 = x1 % p, y1 % p, x2 % p, y2 % p

                if x1 == x2 and y1 == (-y2 % p):  # Puntos iguales pero en signos opuestos
                    continue

                x3, y3 = point_addition(x1, y1, x2, y2, p)
                if x3 is not None and y3 is not None:
                    generators.append((x3, y3))

                x3, y3 = point_doubling(x1, y1, a, p)
                if x3 is not None and y3 is not None:
                    generators.append((x3, y3))

    return generators

# Entrada de parámetros
a = int(input("Introduce el valor de a: "))
b = int(input("Introduce el valor de b: "))
p = int(input("Introduce el valor de p (un número primo): "))

# Encontrar todos los puntos en la curva elíptica
curve_points = find_curve_points(a, b, p)

print(f"\n|E| = {len(curve_points)}\n")

# Verificar si todos los puntos son generadores
all_points_are_generators = is_prime(len(curve_points))

if all_points_are_generators:
    print("Todos los puntos son generadores.")
else:
    # Calcular puntos generadores
    generators = calculate_generators(curve_points, a, p)
    print("Coordenadas de los puntos generadores:")
    for point in generators:
        print(point)
