import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string

# Documentos con info de civilizaciones antiguas
docs = {
    "doc 1": "Los egipcios construyeron las pirámides y desarrollaron una escritura jeroglífica",
    "doc 2": "La civilización romana fue una de las más influyentes en la historia occidental",
    "doc 3": "Los mayas eran expertos astrónomos y tenían un avanzado sistema de escritura",
    "doc 4": "La antigua Grecia sentó las bases de la democracia y la filosofía moderna",
    "doc 5": "Los sumerios inventaron la escritura cuneiforme y fundaron las primeras ciudades"}

# Inicializo el stemmer para español (Snowball es mejor para español)
stemmer = SnowballStemmer('spanish')

# Stopwords para quitar palabras muy comunes que no aportan info
stop_words = set(stopwords.words('spanish'))

# Función para limpiar, tokenizar y stemmizar cada documento
def procesar_texto(texto):
    texto = texto.lower()
    tokens = word_tokenize(texto)
    tokens = [t for t in tokens if t not in string.punctuation and t not in stop_words]
    tokens_stem = [stemmer.stem(t) for t in tokens]
    return tokens_stem

# Crear índice invertido
indice_invertido = {}

for doc_id, contenido in docs.items():
    palabras = procesar_texto(contenido)
    for palabra in palabras:
        if palabra not in indice_invertido:
            indice_invertido[palabra] = set()
        indice_invertido[palabra].add(doc_id)

# Función para buscar documentos según consulta booleana
def buscar(consulta):
    partes = consulta.lower().split()
    if len(partes) != 3:
        return set()  

    palabra1, operador, palabra2 = partes

    palabra1 = stemmer.stem(palabra1)
    palabra2 = stemmer.stem(palabra2)

    docs1 = indice_invertido.get(palabra1, set())
    docs2 = indice_invertido.get(palabra2, set())

    # Según el operador, hago la operación booleana
    if operador == 'and':
        return docs1 & docs2 
    elif operador == 'or':
        return docs1 | docs2  
    elif operador == 'not':
        return docs1 - docs2  
    else:
        return set()  

# Bucle principal para que el usuario ingrese consultas
print("Ingrese una consulta booleana (o 'salir' para terminar): ")

while True:
    entrada = input(">> ").strip()
    if entrada.lower() == 'salir':
        break
    resultado = buscar(entrada)
    if resultado:
        print(" Documentos encontrados:", resultado)
    else:
        print(" Documentos encontrados: Ninguno")

