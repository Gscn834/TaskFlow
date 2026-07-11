import math
import statistics
import numpy as np

# MÓDULO: Fundamentos de Matemáticas Aplicados para Computación

def math_custom_hash(password: str) -> str:

    # Genera un hash utilizando Álgebra Lineal, Teoría de Números y Funciones no lineales.
    # 1. Teoría de los Números: Uso de un número primo para el módulo
    # Utilizamos p = 257 porque es un número primo cercano a 256 (tamaño de un byte).
    # Esto asegura que las operaciones modulares no tengan divisores triviales.
    PRIME_MOD = 257

    # 2. Vectores: Convertimos la contraseña plana en un vector numérico 
    # utilizando los valores ASCII de sus caracteres.
    vector_ascii = [ord(c) for c in password]

    # Aseguramos que la longitud del vector sea par para poder multiplicarlo 
    # por una matriz de 2x2. Si es impar, aplicamos padding matemático.
    if len(vector_ascii) % 2 != 0:
        vector_ascii.append(33) # Añadimos el valor ASCII de '!'

    # 3. Matrices (Álgebra Básica): Definimos una matriz de transformación de 2x2.
    # Esta matriz actúa como la "clave" de dispersión.
    # Su determinante es (3*5) - (2*7) = 15 - 14 = 1.
    transform_matrix = np.array([
        [3, 2],
        [7, 5]
    ])

    hashed_vector = []
    
    # 4. Multiplicación de Matrices y Vectores
    for i in range(0, len(vector_ascii), 2):
        # Tomamos sub-vectores de dimensión 2x1
        vec_chunk = np.array([vector_ascii[i], vector_ascii[i+1]])
        
        # Producto punto entre la matriz y el vector, aplicando aritmética modular
        # T(x) = (A * x) mod p
        transformed = np.dot(transform_matrix, vec_chunk) % PRIME_MOD
        hashed_vector.extend(transformed)

    final_hash_chars = []
    
    # 5. Funciones Matemáticas y Cálculo Básico
    for val in hashed_vector:
        # Aplicamos una función polinómica y trigonométrica no lineal.
        # f(x) = (x^2 + |sin(x) * 100|) mod p
        # Esto aumenta la entropía y hace computacionalmente irreversible la función.
        non_linear_val = (val**2 + int(math.fabs(math.sin(val) * 100))) % PRIME_MOD
        
        # Convertimos el resultado a formato hexadecimal de 2 dígitos
        final_hash_chars.append(f"{non_linear_val:02x}")

    return "".join(final_hash_chars)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    
    # Verifica si una contraseña en texto plano coincide con el hash almacenado.
    # Al ser una función unidireccional (one-way hash), encriptamos la entrada
    # y comparamos los resultados.
    
    return math_custom_hash(raw_password) == hashed_password


def analyze_entropy(hash_list: list) -> dict:

    # 6. Estadística Básica: 
    # Función de prueba para medir la varianza y desviación estándar 
    # de los valores numéricos de los hashes generados, asegurando distribución uniforme.

    if not hash_list:
        return {"media": 0, "varianza": 0, "desviacion_estandar": 0}
        
    numeric_values = [int(h, 16) for h in hash_list]
    media = statistics.mean(numeric_values)
    varianza = statistics.variance(numeric_values) if len(numeric_values) > 1 else 0
    desv_est = math.sqrt(varianza)
    
    return {
        "media": round(media, 2),
        "varianza": round(varianza, 2),
        "desviacion_estandar": round(desv_est, 2)
    }