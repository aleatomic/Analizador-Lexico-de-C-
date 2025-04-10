# Analizador-Lexico-de-C-
Pequeño Analizador Lexico del lenguaje C++ en Python

# Analizador Lexico para archivos C++ con Interfaz Gráfica en Python

Este es un analizador léxico para archivos C++ que permite extraer y clasificar distintos tipos de tokens dentro de un archivo fuente. La aplicación cuenta con una interfaz gráfica creada con PyQt6, permitiendo la selección de archivos y la visualización de los resultados en una tabla.

## Características

- Interfaz intuitiva para cargar archivos C++.

- Detección de distintos tipos de tokens mediante expresiones regulares.

- Presentación de resultados en una tabla con clasificación por tipo de token.

## Librerías utilizadas

Este proyecto utiliza las siguientes librerías de Python:

- *sys*: Para la ejecución de la aplicación y gestión de argumentos del sistema.

- *re*: Para la manipulación y detección de patrones mediante expresiones regulares.

- *collections.defaultdict*: Para almacenar y contar los distintos tipos de tokens encontrados.

- *PyQt6.QtWidgets*: Para la creación de la interfaz gráfica de usuario.

## Instalación

Para ejecutar este analizador léxico, asegúrese de tener instalada la librería PyQt6. Puede instalarla utilizando pip:

```
pip install PyQt6
```

## Uso

1.- Ejecute el script principal:
```
python nombre_del_script.py
```

2.- Haga clic en el botón "Abrir Archivo".

3.- Seleccione un archivo con extensión *.cpp*.

4.- El programa analizará el archivo y mostrará en la tabla los distintos tokens encontrados, agrupados en las siguientes categorías:

- Palabras clave: *int, float, if, else, while, etc*.

- Operadores: *+, -, *, /, ==, !=, etc*.

- Identificadores: Variables y nombres de funciones.

- Constantes: Números y cadenas de texto.

- Delimitadores: *;, ,, *.

- Paréntesis y llaves: *(), {}, []*

## Cómo funciona

1.- Carga del archivo: Se selecciona un archivo *.cpp* y se lee su contenido.

2.- Análisis de tokens: Se aplican expresiones regulares para identificar los distintos tipos de tokens.

3.- Filtrado: Se eliminan las palabras clave y constantes de la lista de identificadores para evitar repeticiones incorrectas.

4.- Visualización de resultados: Los tokens encontrados se muestran en una tabla con su respectivo tipo y cantidad de apariciones.

## Expresiones regulares utilizadas

El analizador utiliza expresiones regulares para identificar distintos elementos del código C++. Algunas de ellas incluyen:

- Identificadores: *\b[a-zA-Z_][a-zA-Z0-9_]*\b*

- Palabras clave: *\b(int|float|double|char|return|if|else|while|for|break|switch|void|bool|define|include|iostream|main|cout|cin|using|namespace|string|std|endl)\b*

- Operadores: *#|==|!=|<=|>=|&&|\|\||\+\+|--|<<|>>|[-+*/%=!<>|&]*

- Constantes: *\b\d+\b|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'*

- Delimitadores: *[;,\.]*

- Paréntesis y llaves: *[\(\)\{\}\[\]]*

## Licencia

*Este proyecto es de código abierto y puede ser utilizado libremente bajo la licencia MIT.*

