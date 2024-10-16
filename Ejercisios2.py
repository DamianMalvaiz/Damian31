a, b = 100, 200
su = a + b

print(f"El resultado es: {su}")


##################################
#Concatenacion de cadenas
cad1, cad2 = "Open ", "AI"
print(cad1 + cad2)

##################################
#Area del rectangulo
base, altura = 15, 2
mult = base * altura
print(f"El area del rectangulo es: {mult}")

##################################
#Comprobar si un número es par o impar
num = 100

par_imp = "par" if num % 2 == 0 else "impar"

##################################
#Calcular el factorial de un número 

###################################
#Número mas grande de una lista
lista = [-10, -5, -3, -1, 0]

print(max(lista))

##################################
#Convertir grados Celsius a Fahrenheit 
celsius = -10
conv_fanh = (-10*9/5)+32
print(f"Grados Fahrenheit: {conv_fanh}")

##################################
#Verificar si un numero es primo
numprimo = 13

#################################
cadena = "mississippi"
aracter = "s"
print()

##################################

#################################
#Sumar todos los números de una lista
lista1 = [5, -5, 10, -10]
print(sum(lista1))

#################################
inicio = 5
fin = 15
#for i in range(inicio, fin):
    #print([f"Impar: {i}",f"Par: {i}"][i%2==0])
    #if i % 2 == 0:
     #   lista = list.i
     #   print(i)
    #else:
     #   print("No hay numeros pares")

####################################
#Promedio de una lista
lista2 = [100, 200, 300, 400]
print(sum(lista2) / 4)

####################################
#Invertir cadena
cadena = "OpenAI"
print(cadena[::-1])

####################################
#Encontrar el número más pequeño de una lista   
lista3 = [100, 200, 50, 300]

print(min(lista3))

#####################################
#Verificar si una palabra es un palíndromo
palabra = "ana"


#####################################
#Contar palabras en una oración
oracion = "Me gusta programar en Python" ############
print(len(oracion))

#####################################
#potencia  de un número
base = 10
exponente = 0

print(base ** exponente)

#####################################
#Convertir km a Millas
kilometros = 42.195
convertir = kilometros * 0.62137119
print(convertir)

#####################################
#Crear una lista de números al cuadrado
lista4 = [10, 20, 30] 
cuadrado = []
for numero in lista4:
    cuadrado.append(numero ** 2)
print(cuadrado)

#####################################
#Ejercicio 21: Contar los elementos de una lista

lista7 = [100]
con_ele = len(lista7)
print(con_ele)



#####################################

#Ejercicio22: Suma de los digitos de un número

numero = 9999
suma_digitos = sum(int(digito) for digito in str(numero))
print(suma_digitos)

#####################################

#Ejercicio 23: Convertir una cadena a mayúsculas

cadena = "OpenAI"
print(cadena.upper())

######################################

#24: eliminar elemnetos duplicados 
lista = [5, 5, 5, 5, 5]
lista_sindp = list(set(lista))
print(lista_sindp)

######################################

#25: Calcular el numero de vocales en una cadena 
def contar_vocales(cadena):
    vocales = "aeiouAEIOU"
    contador = sum(1 for letra in cadena if letra in vocales)
    return contador

cadena = "examen"
resultado = contar_vocales(cadena)
print(resultado)


#Ejercicio 26: Generar los primeros n números de la serie Fibonacci

def fibonacci(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

n = 10
resultado = fibonacci(n)
print(resultado)

####################################

#Ejercicio 27: Eliminar los espacios en blanco de una cadena
cadena = " Open AI "
cadena_sin = cadena.replace(" ", "")
print(cadena_sin)

#####################################
#Ejercicio 28: Calcular la cantidad de números impares en un rango
def contar_impares(inicio, fin):
    cantidad_impares = 0
    for numero in range(inicio, fin + 1):
        if numero % 2 != 0:
            cantidad_impares += 1
    return cantidad_impares


inicio = 10
fin = 30
resultado = contar_impares(inicio, fin)
print(resultado)

######################################

#Ejercicio 29: Crear un diccionario con claves y valores invertidos
diccionario = {"uno": 1, "dos": 2}
diccionario_invertido = {valor: clave for clave, valor in diccionario.items()}
print(diccionario_invertido)

####################################

#Calcular longitud de una lista
lista5 = []
print(len(lista5))

#####################################

#Ejercicio 31: Sumar las claves de un diccionario
diccionario = {100: "uno", 200: "dos"}
sumakeys = sum(diccionario.keys())
print(sumakeys)

##################################

#Convertir una lista de cadenas a mayúsculas
lista6 = ["examen", "python"]
mayuss = []
for numero in lista6:
    mayuss.append(numero.upper())
print(mayuss)
####################################