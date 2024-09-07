alpha = [1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23,25,26]
beta = []

for num in alpha:
    for num1 in alpha:
        c = (num * num1) % 27 
        if (c == 1):
            beta.append(num1) 

#print(beta)

def maximo_comun_divisor_recursivo(a, b):
    if b == 0:
        return a
    return maximo_comun_divisor_recursivo(b, a % b)


print(maximo_comun_divisor_recursivo(482,1180))