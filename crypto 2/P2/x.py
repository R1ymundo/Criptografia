import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 18))

# Define the steps and positions for a flowchart
steps = [
    ("Entrada de Audio", "Captura de la señal de audio a través de un micrófono."),
    ("Preprocesamiento", "Normalización, Filtrado y Ventaneado."),
    ("STFT", "Transformada de Fourier de Corto Plazo: Conversión de la señal en el dominio del tiempo al dominio de la frecuencia."),
    ("Extracción de Características", "Cálculo de Coeficientes Cepstrales de Frecuencia Mel (MFCC)."),
    ("Definición de Gramática con JSGF", "Definición de reglas de gramática para secuencias de palabras válidas."),
    ("Modelos Acústicos", "Utilización de HMM para modelar fonemas."),
    ("Concordancia de Patrones con Gramáticas Definidas", "Búsqueda de secuencias válidas en la gramática JSGF."),
    ("Algoritmo de Viterbi Modificado", "Decodificación considerando las reglas de la gramática."),
    ("Procesamiento del Lenguaje Natural (NLP)", "Mejora del contexto y la semántica utilizando modelos de lenguaje."),
    ("Aprendizaje Automático", "Entrenamiento continuo del sistema con conjuntos de datos amplios.")
]

# Define box style
box_style = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="#66b3ff")

# Add boxes and arrows for flowchart
for i, (title, desc) in enumerate(steps):
    y = 1 - (i + 1) * 0.08
    ax
