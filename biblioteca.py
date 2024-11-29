import random
import pygame
import json
from setting import *


####################################################################################################################################
#                   EFECTOS
####################################################################################################################################

def cambiar_musica(ruta:str)->None:
    '''
    Funcion para detener la musica actual y reproducir la siguiente.
        Recibe:
                La ruta de la musica
        Retorna: None
    '''
    pygame.mixer.music.stop()
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.play(-1)  # Reproduce una vez (puedes añadir "-1" para bucle)

def transicion_fundido(ventana:pygame.Surface, color:tuple=(0, 0, 0), duracion:int=500)->None:
    """
    Funcion para hacer transiciones entre pantallas.
        Recibe: ventana (pygame.Surface)
                color (tupla)
                duracion (int)
        Retorna: None
    """
    overlay = pygame.Surface(ventana.get_size())  # Crear una superficie del tamaño de la ventana
    overlay.fill(color)  # Rellenar la superficie con el color deseado
    
    reloj = pygame.time.Clock()
    for alpha in range(0, 255, 15):  # Fade-in
        overlay.set_alpha(alpha)  # Establecer opacidad progresiva
        ventana.blit(overlay, (0, 0))  # Dibujar la capa transparente
        pygame.display.flip()
        reloj.tick(duracion // 15)

    for alpha in range(255, 0, -15):  # Fade-out
        overlay.set_alpha(alpha)  # Reducir opacidad progresiva
        ventana.blit(overlay, (0, 0))  # Dibujar la capa transparente
        pygame.display.flip()
        reloj.tick(duracion // 15)


def es_valido(matriz: list, fila: int, columna: int, num: int) -> bool:
    """
    Valida si un numero puede colocarse en una celda de un Sudoku.
    Recibe:
        matriz (list): Tablero del Sudoku.
        fila (int): indice de la fila.
        columna (int): indice de la columna.
        num (int): Numero a validar.
    Retorna: 
        True si el numero puede colocarse en la celda, False en caso contrario.
    """
    if num in matriz[fila]:  # Revisa filas
        return False
    for i in range(len(matriz)):  # Revisa columnas
        if matriz[i][columna] == num:
            return False
        
    # Revisa bloques de 3x3
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_columna, inicio_columna + 3):
            if matriz[i][j] == num:
                return False
    return True

# Función para dibujar la barra superior
def dibujar_barra_superior(ventana: pygame.Surface, tiempo_inicial: int, errores:int, nombre:str)->None:
    """
    Dibuja la barra superior paar mostrar el reloj, los errores y el jugador
        Recibe: La superficie (pygame.Surface) 
                El tiempo inicial (int)
                Los errores (int)
                Nombre (str)
        Retorna: None
    """
    tiempo_actual = pygame.time.get_ticks() - tiempo_inicial
    segundos = (tiempo_actual // 1000) % 60
    minutos = (tiempo_actual // 60000) % 60
    tiempo_formateado = f"{minutos:02}:{segundos:02}"
    
    # Fuentes
    fuente = pygame.font.SysFont("Arial", 26, bold=True)
    fuente_pequeña = pygame.font.SysFont("Arial", 20, bold=True)

    # Ajustar posicion de la barra y textos
    posicion_x = 0 
    posicion_y = 15  # barra desplazada un poco hacia abajo
    altura_barra = 70  # mas alta para dar espacio a las letras
    pygame.draw.rect(ventana, (20, 20, 20), (posicion_x, posicion_y, ventana.get_width(), altura_barra))  # fondo negro suave

    # Dibujar tiempo con sombras
    texto_tiempo_sombra = fuente.render(f"{tiempo_formateado}", True, (50, 50, 50))  # sombra gris oscuro
    texto_tiempo = fuente.render(f"{tiempo_formateado}", True, (200, 200, 0))        # amarillo dorado
    ventana.blit(texto_tiempo_sombra, (72, posicion_y + 20))  # subido 10px
    ventana.blit(texto_tiempo, (70, posicion_y + 18))         # texto principal mas arriba

    # Dibujar los errores con menor tamaño y colores combinados
    texto_errores_sombra = fuente_pequeña.render(f"ERRORES: {errores}/3", True, (50, 50, 50))  # sombra gris oscuro
    texto_errores = fuente_pequeña.render(f"ERRORES: {errores}/3", True, (230, 90, 90))        # rojo suave
    ventana.blit(texto_errores_sombra, (202, posicion_y + 22))  # subido 10px
    ventana.blit(texto_errores, (200, posicion_y + 20))         # texto principal mas arriba

    # Dibujar nombre del jugador con sombras
    texto_jugador_sombra = fuente_pequeña.render("JUGADOR:", True, (50, 50, 50))  # sombra gris oscuro
    texto_jugador = fuente_pequeña.render("JUGADOR:", True, (220, 220, 220))      # blanco apagado
    ventana.blit(texto_jugador_sombra, (430, posicion_y + 12))  # subido 10px
    ventana.blit(texto_jugador, (428, posicion_y + 10))         # texto principal mas arriba

    texto_nombre_sombra = fuente_pequeña.render(nombre, True, (50, 50, 50))  # sombra gris oscuro
    texto_nombre = fuente_pequeña.render(nombre, True, (135, 206, 235))      # azul claro elegante
    ventana.blit(texto_nombre_sombra, (430, posicion_y + 42))  # subido 10px
    ventana.blit(texto_nombre, (428, posicion_y + 40))         # texto principal mas arriba


####################################################################################################################################
#                  LOGICA TABLERO 
####################################################################################################################################


def crear_matriz(filas: int, columnas: int, dato=0) -> list:
    """
    Nos genera una matriz bidimensional inicializada con un valor dado.
    Recibe:
            filas (int): Numero de filas de la matriz.
            columnas (int): Numero de columnas de la matriz.
            dato (int, opcional): Valor inicial con el que se llenara la matriz. Por defecto, 0.
    Retorna: 
            Una lista bidimensional de tamaño (filas x columnas) llena con el valor especificado.
    """
    matriz = []
    for _ in range(filas):
        fila = [dato] * columnas
        matriz.append(fila)
    return matriz


def generar_sudoku(filas: int, columnas: int) -> list:
    """
    Genera un tablero de Sudoku completo.
    Recibe: 
            filas (int): Numero de filas del tablero (9 para Sudoku estandar).
            columnas (int): Numero de columnas del tablero (9 para Sudoku estandar).
    Retorna: 
            Una matriz bidimensional representando un Sudoku completo.
    """
    sudoku = crear_matriz(filas, columnas, dato=0)
    llenar_sudoku(sudoku)
    return sudoku


def llenar_sudoku(matriz: list) -> bool:
    """
    Llena un tablero de Sudoku de forma recursiva.
    Recibe: 
            matriz (list): Tablero del Sudoku (matriz bidimensional).
    Retorna: 
            True si logra llenar el tablero exitosamente, False si no es posible.
    """
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == 0:
                lista_num_alea = lista_numeros_aleatorios(9, 1, 9)
                for num in lista_num_alea:
                    if es_valido(matriz, fila, columna, num):
                        matriz[fila][columna] = num
                        if llenar_sudoku(matriz):
                            return True
                        matriz[fila][columna] = 0
                return False
    return True


def lista_numeros_aleatorios(cantidad: int, rango_min: int, rango_max: int) -> list:
    """
    Nos genera una lista de numeros aleatorios unicos.
    Recibe: 
            cantidad (int): Numero de elementos en la lista.
            rango_min (int): Valor minimo del rango.
            rango_max (int): Valor maximo del rango.
    Retorna: 
            Una lista de numeros aleatorios unicos dentro del rango especificado.
    """
    lista = []
    while len(lista) < cantidad:
        num = random.randint(rango_min, rango_max)
        if num not in lista:
            lista.append(num)
    return lista


def lista_posiciones_a_ocultar(cantidad: int) -> list:
    """
    Nos genera una lista de posiciones aleatorias para ocultar celdas en un Sudoku.
    Recibe: 
            cantidad (int): Cantidad de celdas a ocultar.
    Retorna: 
            Una lista de coordenadas (fila, columna) unicas.
    """
    lista = []
    while len(lista) < cantidad:
        coordenadas = [random.randint(0, 8), random.randint(0, 8)]
        if coordenadas not in lista:
            lista.append(coordenadas)
    return lista


def ocultar_celdas(sudoku: list, celdas_a_tapar: int) -> list:
    """
    Oculta celdas de un Sudoku colocando ceros en posiciones aleatorias.
    Recibe: 
        sudoku (list): Tablero del Sudoku (matriz bidimensional).
        celdas_a_tapar (int): Cantidad de celdas a ocultar.
    Retorna: 
        El tablero del Sudoku con las celdas ocultas.
    """
    lista_coordenadas = lista_posiciones_a_ocultar(celdas_a_tapar)
    for fila, columna in lista_coordenadas:
        sudoku[fila][columna] = 0
    return sudoku


# Función para generar un nuevo Sudoku según la dificultad
def generar_nuevo_sudoku(dificultad:int)->list:
    """
    Genera un nuevo sudoku con la cantidad de celdas ocultas segun la dificultad seleccionada.
        Recibe: 
                dificultad (int)
        Retorna:
                el sudoku con las celdas ocultas (list)
    """
    sudoku = generar_sudoku(9, 9)  # Genera un tablero completo

    # Determinar la cantidad de celdas a ocultar según la dificultad
    if dificultad == 0:
        celdas_a_ocultar = 17 
    elif dificultad == 1:
        celdas_a_ocultar = 33 
    elif dificultad == 2:
        celdas_a_ocultar = 48      
    
    sudoku_con_celdas_ocultas = ocultar_celdas(sudoku, celdas_a_ocultar)
    
    return sudoku_con_celdas_ocultas


def tablero_valido(sudoku:list)->bool:
    """
    Funcion para validar tablero sudoku
    Recibe: 
        el sudoku a validar (list)
    Retorna: 
        bool (si el tablero esta validado y cumple las reglas del sudoku)
    """
    es_valido = True

    # busca q todos los numeros de la fila sean distintos del 1 al 9
    for fila in sudoku:
        if sorted(fila) != list(range(1, 10)):
            es_valido = False
            break
    
    # busca q todos los numeros de la fila sean distintos del 1 al 9
    for columna in range(9):
        columna_valores = []
        for fila in range(9):
            columna_valores.append(sudoku[fila][columna])
        columna_ordenada = sorted(columna_valores)
        if columna_ordenada != list(range(1, 10)):
            es_valido = False  
            break 
 
    # busca que todos los numeros de los bloques de 3 sean distintos del
    for i in range(0, 9, 3):  
        for j in range(0, 9, 3):  
            bloque = []
            for k in range(i, i + 3):  #
                for l in range(j, j + 3):  
                    bloque.append(sudoku[k][l])  

            bloque_ordenado = sorted(bloque)

            if bloque_ordenado != list(range(1, 10)):
                es_valido = False  
                break
        if es_valido == False:  
            break

    return es_valido


####################################################################################################################################
#                   PUNTAJES
####################################################################################################################################


# Funcion para guardar puntajes en un archivo JSON
def guardar_puntaje(nombre: str, puntaje: int) -> None:
    """
    Guarda el puntaje en un archivo JSON. Si el jugador ya existe, conserva el puntaje mas alto.
        Recibe: 
                nombre (str)
                puntaje (int)
        Retorna: 
                None
    """
    try:
        with open(ARCHIVO_PUNTAJES, "r") as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = {}

    nombre = nombre.lower()

    if nombre in puntajes:
        if puntaje > puntajes[nombre]:
            puntajes[nombre] = puntaje
    else:
        puntajes[nombre] = puntaje

    with open(ARCHIVO_PUNTAJES, "w") as archivo:
        json.dump(puntajes, archivo, indent=4)


# Función para leer los puntajes desde un archivo JSON
def leer_puntajes()->dict:
    """
    Lee los puntajes desde un archivo JSON y los devuelve ordenados en orden descendente.
    Retorna: 
        - dict: Diccionario de puntajes ordenados en orden descendente.
    """
    try:
        with open(ARCHIVO_PUNTAJES, "r") as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = {}

    # Convertir el diccionario en una lista de claves y ordenarla
    nombres_ordenados = list(puntajes.keys())
    for i in range(len(nombres_ordenados)):
        for j in range(i + 1, len(nombres_ordenados)):
            if puntajes[nombres_ordenados[j]] > puntajes[nombres_ordenados[i]]:
                nombres_ordenados[i], nombres_ordenados[j] = nombres_ordenados[j], nombres_ordenados[i]

    # Reconstruir el diccionario con el orden adecuado
    puntajes_ordenados = {}
    for nombre in nombres_ordenados:
        puntajes_ordenados[nombre] = puntajes[nombre]

    return puntajes_ordenados


# Función para calcular el puntaje final del jugador
def calcular_puntaje(dificultad:float, errores:int, tiempo_ms:int)->float:
    """
    Calcula el puntaje basado en la dificultad, los errores y el tiempo transcurrido.
        Recibe: dificultad (float)
                errores (int)
                tiempo_ms (int)
        Retorna: el puntaje (float)
    """
    puntos_base = 1000
    penalizacion_error = PENALIZACION_ERROR * DIFICULTADES[dificultad]  # Penalización ajustada por dificultad
    penalizacion_tiempo = PENALIZACION_TIEMPO * DIFICULTADES[dificultad]  # Penalización ajustada por dificultad

    # Dividir el tiempo en periodos de 20 segundos (20,000 ms)
    periodos_20_seg = tiempo_ms // 20000  # Cantidad de periodos de 20 segundos

    # Penalización total
    penalizacion_total = (errores * penalizacion_error) + (periodos_20_seg * penalizacion_tiempo)

    # Aplicar penalizaciones al puntaje base
    puntaje = puntos_base - penalizacion_total

    # Asegurar que el puntaje no sea negativo
    if puntaje < 0:
        puntaje = 0

    return puntaje