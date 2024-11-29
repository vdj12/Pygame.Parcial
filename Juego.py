import pygame
from biblioteca import * 
import time
import json


# Configuraciones generales
ANCHO_VENTANA = 650  # Ancho de la ventana principal
ALTO_VENTANA = 750  # Alto de la ventana principal
ALTO_BARRA_SUPERIOR = 60  # Alto de la barra superior donde se muestra el tiempo, errores y nombre del jugador

COLOR_BLANCO = (255, 255, 255)  
COLOR_NEGRO = (0, 0, 0)
COLOR_GRIS_OSCURO = (65, 65, 65)
COLOR_AMARILLENTO = (215, 215, 155)
COLOR_AMARILLO_FUERTE = (255, 255, 120)
COLOR_GRIS = (130, 130, 130)  
COLOR_CELESTE = (135, 206, 250)
COLOR_CELESTE_CLARO = (182, 224, 250)
COLOR_AZUL_OSCURO = (0, 0, 128)  
COLOR_VERDE = (34, 139, 34) 
COLOR_ROJO_OSCURO = (255, 99, 71)
COLOR_AMARILLO_CLARO = (255, 239, 213) 
COLOR_VERDE_CLARO = (50, 200, 50)
COLOR_VERDE_OSCURO = (10, 74, 10)
COLOR_ROJO = (255, 0, 0)
COLOR_NARANJA_OSCURO = (158, 71, 36)
COLOR_NARANJA_CLARO = (255, 151, 31)
COLOR_VIOLETA_CLARO = (190, 190, 255)
TAMAÑO_CELDA = 540 // 9  
PUNTOS_BASE = 1000  # Puntos base para calcular el puntaje
PENALIZACION_ERROR = 50  # Puntos restados por cada error
PENALIZACION_TIEMPO = 10  # Penalización por tiempo transcurrido
DIFICULTADES = [1.0, 1.5, 2.0]  # Factores multiplicadores según la dificultad: fácil, intermedia, difícil
PUNTO_DE_INICIO_TABLERO_SUDOKU_X = 55
PUNTO_DE_INICIO_TABLERO_SUDOKU_Y = 55

# Archivo para guardar los puntajes
ARCHIVO_PUNTAJES = "puntajes.json"

# Inicializar Pygame --------------------------------------------------------------------------------------------------------------------
# Inicializar Pygame y configurar la música de fondo
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("C:/Users/MATI/Desktop/Prog/FUNCIONES/Game/Music_Sudoku.mp3")
pygame.mixer.music.play(-1)  # Reproduce la música en bucle

# Tiempo inicial para calcular duración de la partida
tiempo_inicio = time.time()

# Cargar las imágenes de fondo del menú y puntajes
imagen_menu = pygame.image.load("C:/Users/MATI/Desktop/Prog/FUNCIONES/Game/Imagen de WhatsApp 2024-11-22 a las 18.13.31_72800ea1.jpg")
imagen_menu = pygame.transform.scale(imagen_menu, (540, 600 - ALTO_BARRA_SUPERIOR))  # Escalar imagen al tamaño de la ventana
imagen_puntajes = pygame.image.load("C:/Users/MATI/Desktop/Prog/FUNCIONES/Game/SUDOKU GAME puntaje.jpg")
imagen_puntajes = pygame.transform.scale(imagen_puntajes, (540, 600))
imagen_nombres = pygame.image.load("C:/Users/MATI/Desktop/Prog/FUNCIONES/Game/Diseño sin título.jpg")
imagen_nombres = pygame.transform.scale(imagen_nombres, (540, 600))
imagen_fondo_sudoku = pygame.image.load("C:/Users/MATI/Desktop/Prog/FUNCIONES/Game/Diseño sin título.jpg")
imagen_fondo_sudoku = pygame.transform.scale(imagen_fondo_sudoku, (ANCHO_VENTANA, ALTO_VENTANA))

# Función para guardar puntajes en un archivo JSON
def guardar_puntaje(nombre: str, puntaje: int):
    """
    Guarda el puntaje en un archivo JSON. Si el jugador ya existe, conserva el puntaje más alto.
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
def leer_puntajes():
    '''
    Función: Lee los puntajes desde un archivo JSON y los devuelve ordenados en orden descendente.

    Retorna: 
        dict: Diccionario de puntajes ordenados en orden descendente.
    '''
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
def calcular_puntaje(dificultad, errores, tiempo_ms):
    """
    Calcula el puntaje basado en la dificultad, los errores y el tiempo transcurrido.
    """
    puntos_base = 1000
    penalizacion_error = 50 * DIFICULTADES[dificultad]  # Penalización ajustada por dificultad
    penalizacion_tiempo = 10 * DIFICULTADES[dificultad]  # Penalización ajustada por dificultad

    # Dividir el tiempo en periodos de 20 segundos (20,000 ms)
    periodos_20_seg = tiempo_ms // 20000  # Cantidad de periodos de 20 segundos

    # Penalización total
    penalizacion_total = (errores * penalizacion_error) + (periodos_20_seg * penalizacion_tiempo)

    # Aplicar penalizaciones al puntaje base
    puntaje = puntos_base - penalizacion_total

    # Asegurar que el puntaje no sea negativo
    if puntaje < 0:
        puntaje = 0

    # Imprimir valores intermedios para depuración
    print(f"Dificultad: {dificultad} (Multiplicador: {DIFICULTADES[dificultad]})")
    print(f"Errores: {errores}, Penalización por errores: {errores * penalizacion_error}")
    print(f"Tiempo (20 seg períodos): {periodos_20_seg}, Penalización por tiempo: {periodos_20_seg * penalizacion_tiempo}")
    print(f"Puntos base: {puntos_base}, Penalización total: {penalizacion_total}")
    print(f"Puntaje final antes del ajuste: {puntaje}")

    return puntaje



def transicion_fundido(ventana:pygame.Surface, color:tuple=(0, 0, 0), duracion:int=500):
    '''
        Función: Muestra la pantalla para ingresar el nombre del jugador.

        Recibe: 
            - ventana (pygame.Surface): Ventana donde se mostrará la interfaz.

        Retorna: 
            str: Nombre ingresado por el jugador.
'''
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

# Función para mostrar la pantalla de ingreso de nombre
def mostrar_ingreso_nombre(ventana:pygame.Surface):
    '''
Función: Muestra una pantalla para seleccionar la dificultad del juego.

Recibe: 
    - ventana (pygame.Surface): Ventana donde se mostrará la interfaz.

Retorna: 
    int: Nivel de dificultad seleccionado (0=Fácil, 1=Intermedio, 2=Difícil).
'''
    ventana.fill((255, 255, 255))  
    ventana.blit(imagen_fondo_sudoku, (0, 0))
    fuente = pygame.font.SysFont("Arial", 22)  
    texto = fuente.render("INGRESE SU NOMBRE:", True, COLOR_NEGRO)
    ventana.blit(imagen_nombres, (56, 100))
    
    # rectangulos caja "ingrese su nombre"
    pygame.draw.rect(ventana, (0, 0, 0), (202, 280, 250, 50)) # rectangulo negro borde
    pygame.draw.rect(ventana, COLOR_CELESTE, (207, 285, 240, 40)) # rectangulo celeste
    ventana.blit(texto, (219, 293))  # Centrar el texto horizontalmente
    
    # crectangulos caja "ingreso"
    caja_texto = pygame.Rect(207, 340, 240, 40)  
    pygame.draw.rect(ventana, (220, 210, 220), caja_texto)     # caja gris
    pygame.draw.rect(ventana, (0, 0, 0), (202, 335, 250, 50), width=5) # caja borde negra

    pygame.display.flip()  # Actualizar la ventana para mostrar los cambios

    nombre = ""  # Variable para almacenar el nombre ingresado
    ingresando = True
    while ingresando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if bandera_jugar == True:
                    if juego_completado:  # Solo guardar si el juego fue completado
                        tiempo_total = pygame.time.get_ticks() - tiempo_inicial
                        puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)
                        guardar_puntaje(nombre_jugador, puntaje_final)
                        print(f"Partida finalizada. Puntaje de {nombre_jugador}: {puntaje_final}")
                    else:
                        print("Partida no completada. No se guardará el puntaje.")
                    pygame.quit()
                    exit()
                else:
                    pygame.quit()
                    exit()


            elif evento.type == pygame.KEYDOWN:  # Detectar teclas presionadas
                if evento.key == pygame.K_RETURN:  # Confirmar con Enter
                    if nombre.strip():  # Asegurar que no esté vacío
                        ingresando = False
                elif evento.key == pygame.K_BACKSPACE:  # Borrar último carácter
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 15:  # Limitar longitud del nombre
                        nombre += evento.unicode  # Añadir carácter ingresado

        # Actualizar pantalla con el nombre ingresado
        pygame.draw.rect(ventana, (220, 210, 220), caja_texto)
        texto_ingreso = fuente.render(nombre, True, COLOR_NEGRO)  # Renderizar el texto ingresado
        ventana.blit(texto_ingreso, (caja_texto.x + 10, caja_texto.y + 7))  # Posicionar texto en la caja
        pygame.display.flip()  # Actualizar la pantalla

    return nombre  # Retornar el nombre ingresado

# Función para mostrar la pantalla de selección de dificultad
def mostrar_seleccion_dificultad(ventana:pygame.Surface):
    """
    Muestra una pantalla para seleccionar la dificultad con un fondo semitransparente.
    """
    overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)  # Superficie transparente
    overlay.fill((0, 0, 0, 180))  # Fondo negro con opacidad de 180/255
    ventana.blit(overlay, (0, 0))  # Colocar la superficie en la ventana

    # Definir las cajas para las opciones de dificultad
    caja_facil = pygame.Rect((225, 280, 200, 50))
    caja_intermedio = pygame.Rect((225, 340, 200, 50))
    caja_dificil = pygame.Rect((225, 400, 200, 50))

    # Inicialmente, las cajas tienen el color estático
    color_caja_facil = COLOR_NEGRO
    color_caja_intermedio = COLOR_NEGRO
    color_caja_dificil = COLOR_NEGRO
    
    seleccionada = None
    while seleccionada == None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if bandera_jugar == True:
                    tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # Calcular tiempo transcurrido en milisegundos
                    puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # Calcular puntaje basado en dificultad, errores y tiempo
                    guardar_puntaje(nombre_jugador, puntaje_final)  # Guardar el puntaje en el archivo JSON
                    print(f"Partida finalizada. Puntaje de {nombre_jugador}: {puntaje_final}")
                    pygame.quit()
                    exit()
                else:
                    pygame.quit()
                    exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:  # detectar clic del mouse
                if caja_facil.collidepoint(evento.pos):
                    seleccionada = 0
                elif caja_intermedio.collidepoint(evento.pos):
                    seleccionada = 1
                elif caja_dificil.collidepoint(evento.pos):
                    seleccionada = 2
            if evento.type == pygame.MOUSEMOTION: # cambio de color de cajas al pasar el mouse por encima
                if caja_facil.collidepoint(evento.pos):
                    color_caja_facil = COLOR_GRIS_OSCURO
                else: 
                    color_caja_facil = COLOR_NEGRO
                if caja_intermedio.collidepoint(evento.pos):
                    color_caja_intermedio = COLOR_GRIS_OSCURO
                else: 
                    color_caja_intermedio = COLOR_NEGRO
                if caja_dificil.collidepoint(evento.pos):
                    color_caja_dificil = COLOR_GRIS_OSCURO
                else: 
                    color_caja_dificil = COLOR_NEGRO

        # dibujar cajas
        pygame.draw.rect(ventana, color_caja_facil, caja_facil)
        pygame.draw.rect(ventana, color_caja_intermedio, caja_intermedio)
        pygame.draw.rect(ventana, color_caja_dificil, caja_dificil)

        # dibujar bordes de las cajas
        pygame.draw.rect(ventana, (255, 255, 255), caja_facil, width=5)
        pygame.draw.rect(ventana, (255, 255, 255), caja_intermedio, width=5)
        pygame.draw.rect(ventana, (255, 255, 255), caja_dificil, width=5)

        # fuente y texto
        fuente = pygame.font.Font(None, 36)
        render_facil = fuente.render("Facil", True, (255, 255, 255))
        render_intermedio = fuente.render("Intermedio", True, (255, 255, 255))
        render_dificil = fuente.render("Dificil", True, (255, 255, 255))

        # dibujar el texto de las cajas
        ventana.blit(render_facil, (297, 294))
        ventana.blit(render_intermedio, (262, 353))
        ventana.blit(render_dificil, (290, 413))

        pygame.display.flip() 

    return seleccionada

def mostrar_mensaje_derrota(ventana:pygame.Surface, puntaje:int):
    """
    Muestra un mensaje de fin de juego indicando que el jugador perdió y su puntaje final.
    """
    ventana.fill(COLOR_NEGRO)
    fuente_numeros = pygame.font.SysFont("arial", 20)
    corriendo = True
    reloj = pygame.time.Clock()
    
    
    cantidad_numeros = 100 
    # lista numeros
    numeros = []
    for _ in range(cantidad_numeros):
        numeros.append(random.randint(1, 9)) 

    # lista posiciones
    posiciones = []
    for _ in range(cantidad_numeros):
        x = random.randint(0, ANCHO_VENTANA - 20)  # Coordenada x aleatoria
        y = random.randint(-500, -10)             # Coordenada y aleatoria fuera de pantalla
        posiciones.append((x, y))

    # lista velocidades
    velocidades = []
    for _ in range(cantidad_numeros):
        velocidades.append(random.randint(1, 2))  # Velocidades aleatorias

    # lista colores al azar
    colores = []
    for _ in range(cantidad_numeros):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Color RGB aleatorio
        colores.append(color)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # Calcular tiempo transcurrido en milisegundos
                puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # Calcular puntaje basado en dificultad, errores y tiempo
                guardar_puntaje(nombre_jugador, puntaje_final)  # Guardar el puntaje en el archivo JSON
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu_derrota"

        # actualizar posiciones
        for i in range(cantidad_numeros):
            x, y = posiciones[i]
            y += velocidades[i]  
            if y > ALTO_VENTANA:  
                y = -20    
            posiciones[i] = (x, y)  
        # dibujar numeros
        ventana.fill(COLOR_NEGRO)
        for i in range(cantidad_numeros):
            x, y = posiciones[i]
            texto_numeros = fuente_numeros.render(str(numeros[i]), True, colores[i])
            ventana.blit(texto_numeros, (x, y))

        fuente = pygame.font.Font(None, 72)
        texto_titulo = fuente.render("PERDISTE!", True, COLOR_BLANCO)

        ventana.blit(texto_titulo, (209, 197))

        fuente_puntaje = pygame.font.Font(None, 38)
        texto_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}", True, COLOR_BLANCO)
        ventana.blit(texto_puntaje, (240, 303))

        texto_instrucciones = fuente_puntaje.render("Presiona ESC para regresar al menú", True, COLOR_BLANCO)
        ventana.blit(texto_instrucciones, (107, 399))
        
        pygame.display.flip()
        reloj.tick(35)

def mostrar_mensaje_victoria(ventana:pygame.Surface, puntaje:int):
    """
    Muestra un mensaje de fin de juego indicando que el jugador perdió y su puntaje final.
    """
    ventana.fill(COLOR_NEGRO)
    fuente_numeros = pygame.font.SysFont("arial", 20)
    corriendo = True
    reloj = pygame.time.Clock()
    
    
    cantidad_numeros = 100 
    
    # lista numeros
    numeros = []
    for _ in range(cantidad_numeros):
        numeros.append(random.randint(1, 9)) 
    
    #posiciones
    posiciones = []
    for _ in range(cantidad_numeros):
        x = random.randint(0, ANCHO_VENTANA - 20)  
        y = random.randint(-500, -10)             
        posiciones.append((x, y))
    
    # velocidades
    velocidades = []
    for _ in range(cantidad_numeros):
        velocidades.append(random.randint(2, 3))  

    # colores aleatorios
    colores = []
    for _ in range(cantidad_numeros):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  
        colores.append(color)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                tiempo_total = pygame.time.get_ticks() - tiempo_inicial  
                puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  
                guardar_puntaje(nombre_jugador, puntaje_final) 
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu_victoria"

        # Actualizar posiciones
        for i in range(cantidad_numeros):
            x, y = posiciones[i]
            y += velocidades[i]  
            if y > ALTO_VENTANA:  
                y = random.randint(-100, -10)
            posiciones[i] = (x, y)  

        # Dibujar en la pantalla
        ventana.fill(COLOR_NEGRO)
        for i in range(cantidad_numeros):
            x, y = posiciones[i]
            texto_numeros = fuente_numeros.render(str(numeros[i]), True, colores[i])  
            ventana.blit(texto_numeros, (x, y))

        fuente = pygame.font.Font(None, 72)
        texto_titulo = fuente.render("Ganaste!", True, COLOR_BLANCO)

        ventana.blit(texto_titulo, (209, 197))

        fuente_puntaje = pygame.font.Font(None, 38)
        texto_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}", True, COLOR_BLANCO)
        ventana.blit(texto_puntaje, (240, 303))

        texto_instrucciones = fuente_puntaje.render("Presiona ESC para regresar al menú", True, COLOR_BLANCO)
        ventana.blit(texto_instrucciones, (107, 399))
        
        pygame.display.flip()
        reloj.tick(120)
       
def es_valido(sudoku:list, fila:int, columna:int, num:int):
    '''
    Función: Muestra un mensaje de fin de juego con la opción de regresar al menú principal.

    Recibe: 
        - ventana (pygame.Surface): Ventana del juego.

    Retorna: 
        str: "menu" si se debe regresar al menú principal.
'''
    valido = True

    # Verificar la fila
    if num in sudoku[fila]:
        valido = False

    # Verificar la columna
    if valido and num in [sudoku[i][columna] for i in range(9)]:
        valido = False

    # Verificar el subcuadro 3x3
    if valido:
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        for i in range(inicio_fila, inicio_fila + 3):
            for j in range(inicio_columna, inicio_columna + 3):
                if sudoku[i][j] == num:
                    valido = False
                    break
            if not valido:
                break

    return valido

def tablero_valido(sudoku:list):
    '''
        Función: Muestra la pantalla de puntajes guardados con una imagen de fondo.

        Recibe: 
            - ventana (pygame.Surface): Ventana donde se mostrará la interfaz.

        Retorna: 
            No retorna valores. Actualiza la ventana para mostrar los puntajes.
'''
    es_valido = True

    # Verificar filas
    for fila in sudoku:
        if sorted(fila) != list(range(1, 10)):
            es_valido = False
            break

    # Verificar columnas
    if es_valido:
        for columna in range(9):
            if sorted([sudoku[fila][columna] for fila in range(9)]) != list(range(1, 10)):
                es_valido = False
                break

    # Verificar subcuadros 3x3
    if es_valido:
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subcuadro = [
                    sudoku[x][y]
                    for x in range(i, i + 3)
                    for y in range(j, j + 3)
                ]
                if sorted(subcuadro) != list(range(1, 10)):
                    es_valido = False
                    break
            if not es_valido:
                break

    return es_valido

# Función para mostrar la pantalla de puntajes
def mostrar_puntajes(ventana: pygame.Surface):
    '''
    Función: Muestra los puntajes en la pantalla y permite volver al menú.

    Recibe:
        - ventana (pygame.Surface): Ventana donde se dibujan los elementos.

    Retorna:
        No retorna valores. Dibuja directamente en la ventana.
    '''
    en_pantalla_puntajes = True
    puntajes = leer_puntajes()  # Leer los puntajes desde el archivo JSON

    # Ordenar los puntajes de mayor a menor
    puntajes_ordenados = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    mejores_puntajes = puntajes_ordenados[:5]  

    # Configurar boton para volver al menu
    color_variable = COLOR_CELESTE
    boton_menu = pygame.Rect(223, 650, 200, 50)  # Rect del botón "Volver al menú"
    
    # Fuente
    fuente = pygame.font.Font(None, 36)

    while en_pantalla_puntajes:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if bandera_jugar == True:
                    tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # Calcular tiempo transcurrido en milisegundos
                    puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # Calcular puntaje basado en dificultad, errores y tiempo
                    guardar_puntaje(nombre_jugador, puntaje_final)  # Guardar el puntaje en el archivo JSON
                    print(f"Partida finalizada. Puntaje de {nombre_jugador}: {puntaje_final}")
                    pygame.quit()
                    exit()
                else:
                    pygame.quit()
                    exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                en_pantalla_puntajes = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_menu.collidepoint(evento.pos):
                    en_pantalla_puntajes = False  # Salir de la pantalla de puntajes
            if evento.type == pygame.MOUSEMOTION:
                if boton_menu.collidepoint(evento.pos):
                    color_variable = COLOR_CELESTE_CLARO
                else:
                    color_variable = COLOR_CELESTE

        # Dibujar fondo
        ventana.fill((0, 0, 0))  # Fondo negro
        ventana.blit(imagen_puntajes, (55, 65))  # Imagen de fondo

        # Mostrar los puntajes
        y_pos = 280  # Posición inicial para mostrar puntajes
        for entrada in mejores_puntajes:
            nombre, puntaje = entrada
            texto_puntaje = fuente.render(f"{nombre}: {puntaje}", True, COLOR_BLANCO)
            ventana.blit(texto_puntaje, (ANCHO_VENTANA // 2 - texto_puntaje.get_width() // 2, y_pos))
            y_pos += 40  # Separación entre lineas

        # Dibujar el botón
        pygame.draw.rect(ventana, color_variable, boton_menu)
        texto_boton_menu = fuente.render("Volver al Menú", True, COLOR_NEGRO)
        ventana.blit(texto_boton_menu, (235, 663))

        pygame.display.flip()

# Función para dibujar la barra superior
def dibujar_barra_superior(ventana: pygame.Surface, tiempo_inicial: int, errores, nombre):
    """
    Dibuja la barra superior con información, usando colores más suaves y diseño refinado.
    """
    tiempo_actual = pygame.time.get_ticks() - tiempo_inicial
    segundos = (tiempo_actual // 1000) % 60
    minutos = (tiempo_actual // 60000) % 60
    tiempo_formateado = f"{minutos:02}:{segundos:02}"
    
    # Fuentes
    fuente = pygame.font.SysFont("Arial", 26, bold=True)
    fuente_pequeña = pygame.font.SysFont("Arial", 20, bold=True)

    # Ajustar posición de la barra y textos
    posicion_y = 15  # Barra más abajo
    altura_barra = 70  # Más alto para dar espacio a las letras
    pygame.draw.rect(ventana, (20, 20, 20), (0, posicion_y, ventana.get_width(), altura_barra))  # Fondo negro suave

    # Dibujar tiempo con un estilo elegante
    texto_tiempo_sombra = fuente.render(f"{tiempo_formateado}", True, (50, 50, 50))  # Sombra gris oscuro
    texto_tiempo = fuente.render(f"{tiempo_formateado}", True, (200, 200, 0))        # Amarillo dorado
    ventana.blit(texto_tiempo_sombra, (72, posicion_y + 20))  # Subido 10px
    ventana.blit(texto_tiempo, (70, posicion_y + 18))         # Texto principal más arriba

    # Dibujar los errores con menor tamaño y colores combinados
    texto_errores_sombra = fuente_pequeña.render(f"ERRORES: {errores}/3", True, (50, 50, 50))  # Sombra gris oscuro
    texto_errores = fuente_pequeña.render(f"ERRORES: {errores}/3", True, (230, 90, 90))        # Rojo suave
    ventana.blit(texto_errores_sombra, (202, posicion_y + 22))  # Subido 10px
    ventana.blit(texto_errores, (200, posicion_y + 20))         # Texto principal más arriba

    # Dibujar nombre del jugador con colores suaves y elegantes
    texto_jugador_sombra = fuente_pequeña.render("JUGADOR:", True, (50, 50, 50))  # Sombra gris oscuro
    texto_jugador = fuente_pequeña.render("JUGADOR:", True, (220, 220, 220))      # Blanco apagado
    ventana.blit(texto_jugador_sombra, (430, posicion_y + 12))  # Subido 10px
    ventana.blit(texto_jugador, (428, posicion_y + 10))         # Texto principal más arriba

    texto_nombre_sombra = fuente_pequeña.render(nombre, True, (50, 50, 50))  # Sombra gris oscuro
    texto_nombre = fuente_pequeña.render(nombre, True, (135, 206, 235))      # Azul claro elegante
    ventana.blit(texto_nombre_sombra, (430, posicion_y + 42))  # Subido 10px
    ventana.blit(texto_nombre, (428, posicion_y + 40))         # Texto principal más arriba

# Función para generar un nuevo Sudoku según la dificultad
def generar_nuevo_sudoku(dificultad:int):
    '''
    Función: Dibuja el tablero de Sudoku en la ventana del juego.

    Recibe: 
        - ventana (pygame.Surface): Ventana donde se dibuja el tablero.
        - sudoku (list): Tablero actual del Sudoku (modificado por el usuario).
        - sudoku_inicial (list): Tablero inicial con celdas predeterminadas.
        - celda_resaltada (tuple, optional): Coordenadas de la celda resaltada. Defaults to None.

    Retorna: 
        No retorna valores. Dibuja directamente en la ventana.
'''
    sudoku = generar_sudoku(9, 9)  # Genera un tablero completo

    # Determinar la cantidad de celdas a ocultar según la dificultad
    if dificultad == 0:
        celdas_a_ocultar = 17
    elif dificultad == 1:
        celdas_a_ocultar = 33
    elif dificultad == 2:
        celdas_a_ocultar = 48            
    
    # Ocultar las celdas y retornar el resultado
    return ocultar_celdas(sudoku, celdas_a_ocultar)

# Función para dibujar el tablero
def dibujar_tablero(ventana:pygame.Surface, sudoku:list, sudoku_inicial:list, celda_resaltada=None):
    '''
    Función: Dibuja el tablero de Sudoku en la ventana principal, incluyendo celdas, números y resaltados.

    Recibe: 
        - ventana (pygame.Surface): Ventana donde se dibuja el tablero.
        - sudoku (list): Tablero actual del Sudoku (modificado por el usuario).
        - sudoku_inicial (list): Tablero inicial con celdas predeterminadas.
        - celda_resaltada (tuple, optional): Coordenadas de la celda resaltada (fila, columna). 
        Por defecto es None.

    Retorna: 
        No retorna valores. Dibuja directamente el tablero en la ventana.
'''
    # ventana.blit(imagen_fondo_sudoku, (0, 0))
    for fila in range(9):
        for columna in range(9):
            x = PUNTO_DE_INICIO_TABLERO_SUDOKU_X + (columna * TAMAÑO_CELDA)
            y = PUNTO_DE_INICIO_TABLERO_SUDOKU_Y + (fila * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR)

            # Cambiar color de fondo según si es predeterminado o editable
            if sudoku_inicial[fila][columna] != 0:
                fondo_color = (208, 208, 208)  # Color gris claro para números predeterminados
            else:
                fondo_color = (245, 245, 245)  # Blanco para celdas editables

            # Resaltar celda seleccionada
            if celda_resaltada == (fila, columna):
                pygame.draw.rect(ventana, COLOR_AMARILLO_CLARO, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA))
            elif celda_seleccionada == (fila, columna):
                pygame.draw.rect(ventana, COLOR_VIOLETA_CLARO, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA))
            else:
                pygame.draw.rect(ventana, fondo_color, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA))

            # Dibujar el contorno de las celdas
            pygame.draw.rect(ventana, COLOR_GRIS, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA), 1)

            # Dibujar los números

            if sudoku[fila][columna] != 0:
                if (fila, columna) in numeros_errados:  
                    color = COLOR_ROJO
                elif sudoku_inicial[fila][columna] != 0:  
                    color = COLOR_AZUL_OSCURO
                else:
                    color = COLOR_VERDE  
                texto = pygame.font.Font(None, 36).render(str(sudoku[fila][columna]), True, color)
                ventana.blit(
                    texto,
                    (x + TAMAÑO_CELDA // 2 - texto.get_width() // 2, y + TAMAÑO_CELDA // 2 - texto.get_height() // 2),
                )

            # Dibujar las líneas más gruesas para las subcuadrículas 3x3    
            for i in range(0, 10, 3):
                # Líneas horizontales
                pygame.draw.line(
                    ventana, 
                    COLOR_NEGRO, 
                    (55, 55 + i * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR),  # Inicio considerando el desplazamiento
                    (55 + 9 * TAMAÑO_CELDA, 55 + i * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR),  # Fin considerando el desplazamiento
                    4  # Grosor de la línea
                )
                # Líneas verticales
                pygame.draw.line(
                    ventana, 
                    COLOR_NEGRO, 
                    (55 + i * TAMAÑO_CELDA, 55 + ALTO_BARRA_SUPERIOR),  # Inicio considerando el desplazamiento
                    (55 + i * TAMAÑO_CELDA, 55 + 9 * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR),  # Fin considerando el desplazamiento
                    4  # Grosor de la línea
                )



############################################################################################################################################
#
#                        E J E C U C I O N  
#
############################################################################################################################################


MENU = "menu"
JUEGO = "juego"
APAGADO = "apagado"

estado = MENU

while True:

    # ESTADO MENU --------------------------------------------------------------------------------------------------------------------------

    if estado == MENU:
        # Crear rectángulos interactivos para botones del menu
        rect_jugar = pygame.Rect(253, 437, 145, 35)  # Botón "Jugar"
        rect_puntaje = pygame.Rect(253, 475, 145, 35)  # Botón "Puntajes"
        rect_salir = pygame.Rect(253, 513, 145, 35)  # Botón "Salir"

        # CREAR LA VENTANA PRINCIPAL
        ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Sudoku Interactivo")

        # Ciclo principal del menú
        nombre_jugador = ""
        color_rect_jugar = COLOR_GRIS_OSCURO
        color_rect_puntaje = COLOR_GRIS_OSCURO
        color_rect_salir = COLOR_GRIS_OSCURO

        bandera_jugar = False
        menu_activado = True
        while menu_activado:
            ventana.fill(COLOR_NEGRO)
            ventana.blit(imagen_fondo_sudoku, (0, 0))
            ventana.blit(imagen_menu, (56, 100))
            
            # EVENTOS ----------------------------------------------------------------
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Calcular puntaje antes de salir
                    if bandera_jugar == True:
                        tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # Calcular tiempo transcurrido en milisegundos
                        puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # Usar la función calcular_puntaje
                        guardar_puntaje(nombre_jugador, puntaje_final)  # Guardar el puntaje
                        print(f"Partida finalizada. Puntaje de {nombre_jugador}: {puntaje_final}")
                        transicion_fundido(ventana, color=(0, 0, 0), duracion=500)
                        pygame.quit()
                        exit()
                    else:
                        transicion_fundido(ventana, color=(0, 0, 0), duracion=500)
                        pygame.quit()
                        exit() 
                    
                    # Mostrar transición y salir

                
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if rect_jugar.collidepoint(evento.pos):
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=700)
                            # Primero seleccionamos el nivel de dificultad
                            dificultad = mostrar_seleccion_dificultad(ventana)
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=700)
                            # Luego ingresamos el nombre del jugador
                            nombre_jugador = mostrar_ingreso_nombre(ventana)
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=700)
                            bandera_jugar = True
                            estado = JUEGO
                            menu_activado = False
                        elif rect_puntaje.collidepoint(evento.pos):
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=500)
                            mostrar_puntajes(ventana)
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=500)
                        elif rect_salir.collidepoint(evento.pos):
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=500)
                            pygame.quit()
                            exit()
                            
                # Cambio de color botones al pasar mouse por encima
                if evento.type == pygame.MOUSEMOTION: 
                    if rect_jugar.collidepoint(evento.pos):
                        color_rect_jugar = COLOR_AMARILLO_FUERTE
                    else: 
                        color_rect_jugar = COLOR_GRIS_OSCURO
                    if rect_puntaje.collidepoint(evento.pos):
                        color_rect_puntaje = COLOR_AMARILLO_FUERTE
                    else: 
                        color_rect_puntaje = COLOR_GRIS_OSCURO
                    if rect_salir.collidepoint(evento.pos):
                        color_rect_salir = COLOR_AMARILLO_FUERTE
                    else: 
                        color_rect_salir = COLOR_GRIS_OSCURO
            
            # dibujo de rectangulos de botones jugar, puntaje, salir...
            pygame.draw.rect(ventana, color_rect_jugar, rect_jugar, width=2)
            pygame.draw.rect(ventana, color_rect_puntaje, rect_puntaje, width=2)
            pygame.draw.rect(ventana, color_rect_salir, rect_salir, width=2)

            pygame.display.flip()


    # ESTADO JUEGO -------------------------------------------------------------------------------------------------------------------------

    elif estado == JUEGO: 
        juego_completado = False
        # Crear rectangulos interactivos para boton de la pantalla jugando
        rect_nuevo_tablero = pygame.Rect(430, 686, 170, 40)  
        rect_volver_al_menu = pygame.Rect(54, 686, 170, 40)

        # Generar Sudoku inicial y tablero inicial
        sudoku_inicial = generar_nuevo_sudoku(dificultad)
        sudoku = [fila[:] for fila in sudoku_inicial]  # Copia del tablero para modificaciones
        errores = 0
        tiempo_inicial = pygame.time.get_ticks()

        # Ciclo principal del juego
        celda_resaltada = None
        celda_seleccionada = None
        
        color_boton_nuevo_tablero = COLOR_VERDE_OSCURO
        color_borde_nuevo_tablero = COLOR_VERDE_CLARO  
        
        color_boton_volver_al_menu = COLOR_NARANJA_OSCURO
        color_borde_volver_al_menu = COLOR_NARANJA_CLARO

        jugando = True
        
        numeros_errados = []
        while jugando:
            
            ventana.fill(COLOR_BLANCO)
            ventana.blit(imagen_fondo_sudoku, (0, 0))
            
            # Superficie de fondo un poco transparente...
            overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)  # Superficie transparente
            overlay.fill((0, 0, 0, 80))  # Fondo negro con opacidad de 180/255
            ventana.blit(overlay, (0, 0))  # Colocar la superficie en la ventana
            
            dibujar_barra_superior(ventana, tiempo_inicial, errores, nombre_jugador)
            dibujar_tablero(ventana, sudoku, sudoku_inicial, celda_resaltada)
            
            # Borde blanco para el tablero sudoku
            pygame.draw.rect(ventana, COLOR_BLANCO, (51, 111, 550, 550), width=3)

            # Texto boton nuevo tablero
            fuente_boton = pygame.font.Font(None, 28)  # Fuente más pequeña para el texto del botón
            texto_boton_nuevo_tablero = fuente_boton.render("Nuevo Tablero", True, COLOR_BLANCO)  # Texto blanco

            # Texto boton volver al menu
            fuente_boton = pygame.font.Font(None, 28)  # Fuente más pequeña para el texto del botón
            texto_boton_volver_al_menu = fuente_boton.render("Volver al menu", True, COLOR_BLANCO)  # Texto blanco

            # EVENTOS ----------------------------------------------------------------------------------------------
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:  # Evento de cerrar ventana
                    if estado == JUEGO and 'tiempo_inicial' in locals():  # Verifica que estás en JUEGO y tiempo_inicial está definido
                        tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # Calcular tiempo transcurrido en milisegundos
                        puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # Usar la función calcular_puntaje
                        if juego_completado:  # Guardar solo si el juego fue completado
                            guardar_puntaje(nombre_jugador, puntaje_final)
                            print(f"Partida finalizada. Puntaje de {nombre_jugador}: {puntaje_final}")
                    pygame.quit()
                    exit()

                
                if evento.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = evento.pos
                    # Calcular coordenadas relativas al tablero
                    if 55 <= mouse_x < 55 + 9 * TAMAÑO_CELDA and 55 + ALTO_BARRA_SUPERIOR <= mouse_y < 55 + ALTO_BARRA_SUPERIOR + 9 * TAMAÑO_CELDA:
                        columna = (mouse_x - 55) // TAMAÑO_CELDA
                        fila = (mouse_y - 55 - ALTO_BARRA_SUPERIOR) // TAMAÑO_CELDA
                        if 0 <= columna < 9 and 0 <= fila < 9:
                            celda_resaltada = (fila, columna)
                        else:
                            celda_resaltada = None
                    else:
                        celda_resaltada = None
                    if rect_nuevo_tablero.collidepoint(evento.pos):
                        color_boton_nuevo_tablero = COLOR_VERDE_CLARO
                    else:
                        color_boton_nuevo_tablero = COLOR_VERDE_OSCURO
                    if rect_volver_al_menu.collidepoint(evento.pos):
                        color_boton_volver_al_menu = COLOR_NARANJA_CLARO
                    else:
                        color_boton_volver_al_menu = COLOR_NARANJA_OSCURO

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if rect_nuevo_tablero.collidepoint(evento.pos):  # Nuevo tablero
                            sudoku_inicial = generar_nuevo_sudoku(dificultad)
                            sudoku = [fila[:] for fila in sudoku_inicial]
                            tiempo_inicial = pygame.time.get_ticks()
                            errores = 0
                            numeros_errados = []
                        elif celda_resaltada and sudoku_inicial[celda_resaltada[0]][celda_resaltada[1]] == 0:
                            celda_seleccionada = celda_resaltada
                        else:
                            celda_seleccionada = None
                        if rect_volver_al_menu.collidepoint(evento.pos):
                            if not juego_completado:
                                print("Partida no completada. No se guardará el puntaje.")
                            estado = MENU
                            jugando = False

                if evento.type == pygame.KEYDOWN:
                    if celda_seleccionada:
                        fila, columna = celda_seleccionada
                        if evento.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                            sudoku[fila][columna] = 0
                            if (fila, columna) in numeros_errados:
                                numeros_errados.remove((fila, columna))  
                        elif evento.unicode.isdigit() and evento.unicode != "0":
                            num = int(evento.unicode)
                            if es_valido(sudoku, fila, columna, num):
                                sudoku[fila][columna] = num  
                                bandera_error = False
                                if (fila, columna) in numeros_errados:
                                    numeros_errados.remove((fila, columna))  
                            else:
                                sudoku[fila][columna] = num
                                bandera_error = True
                                if (fila, columna) not in numeros_errados:
                                    numeros_errados.append((fila, columna)) 
                                errores += 1  
                                if errores >= 3:  
                                    tiempo_total = pygame.time.get_ticks() - tiempo_inicial  
                                    puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  
                                    guardar_puntaje(nombre_jugador, puntaje_final)  
                                    print(f"Has alcanzado el límite de errores. Puntaje final: {puntaje_final}")
                                    resultado = mostrar_mensaje_derrota(ventana, puntaje_final)
                                    if resultado == "menu_derrota":
                                        estado = MENU
                                        jugando = False
                                        menu_activado = True
                                    break


        # Verificar si el tablero está completo después de procesar eventos
            completo = all(0 not in fila for fila in sudoku)
            if completo and tablero_valido(sudoku):  # Tablero completo y válido
                tiempo_total = pygame.time.get_ticks() - tiempo_inicial
                puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)
                guardar_puntaje(nombre_jugador, puntaje_final)
                print(f"Juego completo! Puntaje de {nombre_jugador}: {puntaje_final}")
                juego_completado = True  # Marcar como completado
                resultado = mostrar_mensaje_victoria(ventana, puntaje_final)
                if resultado == "menu_victoria":
                    estado = MENU
                    jugando = False
                break

                
            elif completo:
                print("El tablero no cumple las reglas")
                # Calcular el tiempo transcurrido
                tiempo_final = pygame.time.get_ticks()
                tiempo_transcurrido = (tiempo_final - tiempo_inicial) // 60000  # Convertir milisegundos a minutos

                # Obtener el multiplicador de dificultad
                multiplicador_dificultad = DIFICULTADES[dificultad]  # Basado en la dificultad seleccionada

                # Calcular el puntaje final
                puntaje_final = calcular_puntaje(
                    PUNTOS_BASE,
                    errores,
                    PENALIZACION_ERROR,
                    tiempo_transcurrido,
                    PENALIZACION_TIEMPO,
                    multiplicador_dificultad
                )

                # Guardar el puntaje del jugador
                guardar_puntaje(nombre_jugador, puntaje_final)
                print(f"Juego completo! Puntaje de {nombre_jugador}: {puntaje_final}")

                # Salir del bucle del juego
                jugando = False
            
            # Boton para reinciar tablero 
            pygame.draw.rect(ventana, color_boton_nuevo_tablero, rect_nuevo_tablero, border_radius=10)  # Fondo del botón
            pygame.draw.rect(ventana, color_borde_nuevo_tablero, rect_nuevo_tablero, width=3, border_radius=10)  # Borde del botón
            ventana.blit(texto_boton_nuevo_tablero, (447, 696))

            # Boton para volver al menu
            pygame.draw.rect(ventana, color_boton_volver_al_menu, rect_volver_al_menu, border_radius=10)  # Fondo del boton
            pygame.draw.rect(ventana, color_borde_volver_al_menu, rect_volver_al_menu, width=3, border_radius=10)  # Borde del boton
            ventana.blit(texto_boton_volver_al_menu, (67, 696))
            
            pygame.display.flip()

    elif estado == APAGADO:
        if not juego_completado:
            print("El jugador salió sin completar la partida. No se guardarán los puntos.")
        break