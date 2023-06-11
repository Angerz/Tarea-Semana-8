# Análisis de fuerzas y cálculo de esfuerzos Lewis en engranajes helicoidales, cónicos y rectos.
Este repositorio contiene un código en Python que permite realizar el análisis de fuerzas y esfuerzos en engranajes rectos, helicoidales y cónicos. El análisis se basa en los datos proporcionados en un archivo de Excel y utiliza la biblioteca pandas, numpy y sympy para el procesamiento de datos y cálculos.

Requisitos previos
Asegúrate de tener instaladas las siguientes bibliotecas de Python:

- pandas
- numpy
- sympy

Uso del código
Descarga el código y el archivo de Excel "Datos_engranajes.xlsx" en tu sistema local.
Asegúrate de tener instaladas las bibliotecas mencionadas anteriormente.
Ejecuta el código en un entorno de Python.

# Explicación del código
El código proporcionado contiene varias funciones y pasos que se deben seguir para realizar el análisis de fuerzas y esfuerzos en los engranajes. A continuación, se detallan los principales componentes del código:

Funciones para leer los datos del archivo de Excel: El código contiene una función leer_datos_excel() que lee los datos del archivo de Excel "Datos_engranajes.xlsx" y crea vectores con los nombres de las filas correspondientes a los diferentes parámetros de los engranajes.

Funciones para realizar cálculos de velocidades y fuerzas: El código incluye funciones como velocidad_salida(), diametro_paso(), velocidad_linea(), fuerza_tangencial(), entre otras, que realizan los cálculos necesarios para obtener la velocidad de salida, el diámetro de paso, la velocidad lineal y la fuerza tangencial en los engranajes.

Análisis estático y cálculo de esfuerzo Lewis: El código realiza un análisis estático para encontrar las reacciones en los cojinetes y calcula el esfuerzo Lewis en un engranaje específico. Utiliza ecuaciones y símbolos simbólicos de la biblioteca sympy para resolver las ecuaciones y obtener los valores desconocidos.


Autor: GRUPO 3
