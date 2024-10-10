#Angel Damian Malvaiz González
def contar(palabras):
    ocurrencias = {}
    for palabra in palabras:
        if palabra in ocurrencias:
            ocurrencias[palabra] += 1
        else:
            ocurrencias[palabra] = 1
    return ocurrencias

palabras = ["python", "java", "python", "c++"]
print(contar(palabras)) 

###################################

def combinar_diccionarios(dic1, dic2):
    combinado = dic1.copy()
    for clave, valor in dic2.items():
        if clave in combinado:
            combinado[clave] += valor
        else:
            combinado[clave] = valor
    return combinado

dic1 = {'a': 1, 'b': 2}
dic2 = {'b': 3, 'c': 4}
print(combinar_diccionarios(dic1, dic2)) 
#####################################

def frecuencia_numeros(numeros):
    frecuencia = {}
    for numero in numeros:
        if numero in frecuencia:
            frecuencia[numero] += 1
        else:
            frecuencia[numero] = 1
    return frecuencia

numeros = [1, 1, 2, 3, 3, 3]
print(frecuencia_numeros(numeros)) 

####################################

def filtro(pal, longitud):
    return [palabra for palabra in pal if len(palabra) > longitud]

palabras = ["hola", "mundo", "python", "programación"]
longitud = 5
resultado = filtro(palabras, longitud)
print(resultado)


######################################

def invertir_tuplas(tuplas):
    return [(y, x) for (x, y) in tuplas]

tuplas = [(1, 2), (3, 4), (5, 6)]
print(invertir_tuplas(tuplas)) 

#####################################

def valor_mas_frecuente(numeros):
    frecuencia = frecuencia_numeros(numeros)
    return max(frecuencia, key=frecuencia.get)

numeros = [1, 2, 3, 1, 2, 1]
print(valor_mas_frecuente(numeros))

#####################################

def es_subconjunto(conjunto1, conjunto2):
    return conjunto1.issubset(conjunto2)

conjunto1 = {1, 2, 3}
conjunto2 = {1, 2, 3, 4, 5}
print(es_subconjunto(conjunto1, conjunto2)) 

###################################

def agrupar_por_edad(personas):
    agrupado = {}
    for persona in personas:
        edad = persona["edad"]
        nombre = persona["nombre"]
        if edad in agrupado:
            agrupado[edad].append(nombre)
        else:
            agrupado[edad] = [nombre]
    return agrupado

personas = [{"nombre": "Ana", "edad": 25}, {"nombre": "Luis", "edad": 25}, {"nombre": "Carlos", "edad": 30}]
print(agrupar_por_edad(personas))
######################################

def merge_sort(numeros):
    if len(numeros) > 1:
        medio = len(numeros) // 2
        izquierda = numeros[:medio]
        derecha = numeros[medio:]

        merge_sort(izquierda)
        merge_sort(derecha)

        i = j = k = 0
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] < derecha[j]:
                numeros[k] = izquierda[i]
                i += 1
            else:
                numeros[k] = derecha[j]
                j += 1
            k += 1

        while i < len(izquierda):
            numeros[k] = izquierda[i]
            i += 1
            k += 1

        while j < len(derecha):
            numeros[k] = derecha[j]
            j += 1
            k += 1

    return numeros

numeros = [5, 3, 8, 6, 2]
print(merge_sort(numeros)) 
####################################

def eliminar_menores(lista, limite):
    return [x for x in lista if x >= limite]

numeros = [1, 2, 3, 4, 5]
limite = 3
print(eliminar_menores(numeros, limite)) 
###################################

def aplanar_lista(lista_de_listas):
    return [item for sublista in lista_de_listas for item in sublista]

lista_de_listas = [[1, 2], [3, 4], [5]]
print(aplanar_lista(lista_de_listas)) 

##################################

def calcular_mediana(numeros):
    numeros_ordenados = sorted(numeros)
    n = len(numeros_ordenados)
    medio = n // 2

    if n % 2 == 0:
        return (numeros_ordenados[medio - 1] + numeros_ordenados[medio]) / 2.0
    else:
        return numeros_ordenados[medio]

numeros = [1, 3, 2, 4, 5]
print(calcular_mediana(numeros)) 

######################################

def duplicar_elementos(lista):
    return [elemento for item in lista for elemento in [item, item]]

numeros = [1, 2, 3]
print(duplicar_elementos(numeros)) 

####################################

def contar_palabras(frases):
    return {i: len(frase.split()) for i, frase in enumerate(frases)}

frases = ["Hola mundo", "Python es genial", "Me gusta programar"]
print(contar_palabras(frases)) 
###################################

def clave_max_valor(diccionario):
    return max(diccionario, key=diccionario.get)

diccionario = {'a': 10, 'b': 20, 'c': 5}
print(clave_max_valor(diccionario)) 

##################################

def encontrar_palindromos(palabras):
    return [palabra for palabra in palabras if palabra == palabra[::-1]]

palabras = ["ana", "oso", "hola", "level"]
print(encontrar_palindromos(palabras)) 




