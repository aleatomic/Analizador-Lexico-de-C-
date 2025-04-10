#Analizador Lexico para archivo .cpp, con interfaz grafica realizado en Python

# Importar librerias necesarias
import sys #Nos ayuyda a ejecutar aplicaciones GUI en el sistema operativo
import re #Se usar para poder trabajar con expresiones regulares
from collections import defaultdict # Se usa para contar los tokens, crea un diccionario que almacena listas de tokens
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView #Importar librerias de PyQt6 para crear la interfaz grafica
# Documentacion de PyQt6: https://www.riverbankcomputing.com/static/Docs/PyQt6/index.html | Pagina oficial de PyQt6: https://pypi.org/project/PyQt6/

def cargar_codigo_cpp(file_path):
    #Abrimos un archivo .cpp en modo lectura y con codificacion utf-8
    with open(file_path, 'r', encoding='utf-8') as file:
        #Devolmes el contenido del archivo como una cadena de texto
        return file.read()

def contador_tokens(cpp_codigo):
    #Definimos expresiones regulraes para poder detectar los distimntos tipos de tokens
    expRegu_tokens = {
        'palabras_clave': r'\b(int|float|double|char|return|if|else|while|for|break|switch|void|bool|define|include|iostream|main|cout|cin|using|namespace|string|std|endl)\b', #Palabras Clave
        'operadores': r'#|==|!=|<=|>=|&&|\|\||\+\+|--|<<|>>|[-+*/%=!<>|&]',#Operadores matematicos y logicos
        #'identificadores': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',#Indetificadores, nombres de'a' a la 'z' y de 'A' a la 'Z', con numeros o guiones bajos
        'identificadores': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',#Indetificadores, nombres de'a' a la 'z' y de 'A' a la 'Z', con numeros o guiones bajos / asi como tambien cadenas de texto entre comillas dobles o simples para evitar confusiones con las constantes y hacer filtraciones
        'constantes': r'\b\d+\b|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',#Numeros enteros y cadenas de texto
        #'delimitadores': r'[;(),{}\[\]]',#Simbollos de finalizacion de linea y delimitadores
        'delimitadores': r'[\;\,\.]', #Punto y coma, coma, punto
        'parentesis_llaves': r'[\(\)\{\}\[\]]' #Parentesis y llaves
    }
    '''
        > El prefijo r en la cadena (r'...') indica que es una cadena sin formato (raw string), lo que significa que las barras invertidas (\) se interpretan literalmente y no como caracteres de escape. Esto es útil para las expresiones regulares, ya que a menudo contienen muchas barras invertidas.
        > \b indica un límite de palabra, lo que significa que el patrón debe coincidir con una palabra completa y no con una parte de otra palabra. Por ejemplo en printint(); de debe de detctar la palabra printint como un identificador y no como dos palabras (print, int).
    
        > En las constantes \d+ indica uno o más dígitos, y el uso de comillas dobles (") y simples (') permite detectar cadenas de texto y caracteres individuales. El uso de \\. dentro de las comillas permite escapar caracteres especiales dentro de las cadenas.
        > En los operadores, el uso de | indica una alternativa, lo que significa que el patrón puede coincidir con cualquiera de los operadores listados. Por ejemplo, el patrón puede coincidir con == o != o <=, etc.
    '''

    tokens_contador = defaultdict(list) # Diccionario para almacenar los toknes
    '''
        Ahora, sucede que los identificadores, tambien detecta palabras clave y constantes, por lo que se debe de filtrar los tokens encontrados para que no se repitan en los diferentes tipos de tokens.
    '''

    # Extraer palabras clave y constantes primero / con re.findall() se busca todas las coincidencias del patrón en el código C++ segun la expresion regular y se guardan en un conjunto (set) para evitar duplicados.
    palabras_clave = set(re.findall(expRegu_tokens['palabras_clave'], cpp_codigo))
    constantes = set(re.findall(expRegu_tokens['constantes'], cpp_codigo))

    for tipo_token, patron in expRegu_tokens.items():
        if tipo_token == 'identificadores': #Cuando estemos en identificadores
            posibles_identificadores = set(re.findall(patron, cpp_codigo))
            identificadores_filtrados = posibles_identificadores - palabras_clave  # Excluir palabras clave y constantes
            identificadores_filtrados = identificadores_filtrados - constantes  # Excluir constantes
            tokens_contador[tipo_token] = list(identificadores_filtrados)
        else:
            tokens_contador[tipo_token] = re.findall(patron, cpp_codigo)  # Guardar los demás tokens sin filtro
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    '''
    for tipo_token, patron in expRegu_tokens.items(): #Buscar y contar cada tipo de token
        matches = re.findall(patron, cpp_codigo)
        tokens_contador[tipo_token].extend(matches)
    '''
    '''
    > re.findall(patron, cpp_codigo) busca todas las coincidencias del patrón en el código C++ y devuelve una lista de ellas.
    > tokens_contador[tipo_token].extend(matches) agrega las coincidencias encontradas a la lista correspondiente en el diccionario tokens_contador.
    '''
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    return tokens_contador #Devolvemos el diccionario con los tokens encontrados

#Clase para interfaz grafica
class AnalizadorLexicoGUI(QWidget): #Clase principal de la interfaz grafica, que hereda de QWidget
    def __init__(self): #Constructor de la clase
        #Inicializamos la clase padre QWidget
        super().__init__()
        self.iniciar_interfaz()

    def iniciar_interfaz(self): #Funcion para iniciar la interfaz grafica
        #Configuracion de la ventana principal
        self.setWindowTitle("Analizador Léxico C++") #Titulo de la ventana
        self.setGeometry(100, 100, 860, 400) #Posicion y tamaño de la ventana
        
        layout = QVBoxLayout() # Diseño Vertical
        
        self.label = QLabel("Seleccione un archivo .cpp") #Etiqueta inicial
        layout.addWidget(self.label) #Agregar etiqueta al diseño
        
        self.boton = QPushButton("Abrir Archivo") # Boton para seleccionar el archivo
        self.boton.clicked.connect(self.abrir_archivo) #Conectar el boton a la funcion abrir_archivo
        layout.addWidget(self.boton) #Agregar boton al diseño
        
        self.tabla = QTableWidget()# Tabla para mostrar los resultados
        self.tabla.setColumnCount(3) #Establecer el numero de columnas en la tabla
        self.tabla.setHorizontalHeaderLabels(["Tipo de Token", "Cantidad", "Tokens Encontrados"])#Establecer los nombres de las columnas en la tabla
        #self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) #Ajustar el tamaño de las columnas al contenido automaticamente
        # Ajustar el ancho de cada columna
        self.tabla.setColumnWidth(0, 150)
        self.tabla.setColumnWidth(1, 100)
        self.tabla.setColumnWidth(2, 600)

        # Ajustar la altura de las filas
        self.tabla.verticalHeader().setDefaultSectionSize(30)

        layout.addWidget(self.tabla) #Agregar tabla al diseño
        
        self.setLayout(layout)#Establecer el diseño en la ventana

    # Funcion para abrir y analizar un archivo C++ con interfaz grafica
    def abrir_archivo(self): #Funcion para abrir un archivo .cpp
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Archivos C++ (*.cpp)") #Abrir un cuadro de dialogo para seleccionar el archivo .cpp
        if file_path: #Si se selecciona un archivo
            cpp_codigo = cargar_codigo_cpp(file_path) #Cargar el codigo del archivo .cpp
            tokens_contador = contador_tokens(cpp_codigo)#Analizar tokens
            
            self.tabla.setRowCount(len(tokens_contador))# Ajustar numero de filas en la tabla / Ajusta el numero de filas sugun la cantidad de tipos de tokens encontrados
            
            #Llenado de tabla con los resultados
            for i, (tipo_token, tokens) in enumerate(tokens_contador.items()):
                '''
                    Lo que retorna tokens_contador.items() es una lista de tuplas, donde cada tupla contiene el tipo de token y la lista de tokens encontrados.
                    Por ejemplo: [('palabras_clave', ['int', 'float']), ('identificadores', ['variable1', 'variable2']), ...]
                '''
                self.tabla.setItem(i, 0, QTableWidgetItem(tipo_token)) #Agregar tipo de token a la tabla
                self.tabla.setItem(i, 1, QTableWidgetItem(str(len(tokens)))) #Agregar cantidad de tokens a la tabla
                self.tabla.setItem(i, 2, QTableWidgetItem(", ".join(tokens))) #Agregar tokens encontrados a la tabla

            self.label.setText(f"Ruta de Archivo Analizado: {file_path}") #Actualizar etiqueta con la ruta del archivo analizado

#Codigo principal para ejecutar la aplicacion
#Nos aseguramos de que el script solo se ejecute cuando es el archivo principal / Funcion principal
if __name__ == "__main__":
    app = QApplication(sys.argv) #Crear una aplicacion de PyQt6
    ventana = AnalizadorLexicoGUI() #Crear una instancia de la clase AnalizadorLexicoGUI
    ventana.show() #Mostrar la ventana
    sys.exit(app.exec()) #Ejecutar la aplicacion y salir al cerrar la ventana
