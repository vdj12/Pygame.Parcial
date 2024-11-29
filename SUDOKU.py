import copy
import pygame
from biblioteca import *

# Inicializar Pygame
pygame.init()

MENU = "menu"
JUEGO = "juego"
APAGADO = "apagado"


####################################################################################################################################
#                   INGRESO NOMBRE Y DIFICULTAD
####################################################################################################################################


# Función para mostrar la pantalla de ingreso de nombre
def mostrar_ingreso_nombre(ventana:pygame.Surface)->str:
    """
    Muestra una pantalla para ingresar el nombre del jugador.
    Recibe:
        ventana (pygame.Surface): Ventana donde se mostrara la interfaz.
    Retorna:
        str: el nombre del jugador
    """
    ventana.fill((255, 255, 255))  
    ventana.blit(imagen_fondo_sudoku, (0, 0))
    
    # Fuente mensaje de ingresar nombre 
    fuente = pygame.font.SysFont("Arial", 20, bold=True)  
    texto = fuente.render("INGRESE SU NOMBRE", True, COLOR_NEGRO)
    
    
    # rectangulos caja "ingrese su nombre"
    pygame.draw.rect(ventana, COLOR_GRIS_OSCURO, (202, 280, 250, 50)) # rectangulo negro borde
    pygame.draw.rect(ventana, COLOR_CELESTE, (207, 285, 240, 40)) # rectangulo celeste
    ventana.blit(texto, (233, 294))  # Centrar el texto horizontalmente
    
    # crea rectangulos caja "ingreso"
    caja_texto = pygame.Rect(207, 340, 240, 40)  
    pygame.draw.rect(ventana, (220, 210, 220), caja_texto)     # caja gris
    pygame.draw.rect(ventana, COLOR_GRIS_OSCURO, (202, 335, 250, 50), width=5)  # caja borde negra

    nombre = ""  # variable para almacenar el nombre ingresado
    ingresando = True
    while ingresando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if bandera_jugar == True:
                    if juego_completado:  # solo guardar si el juego fue completado
                        tiempo_total = pygame.time.get_ticks() - tiempo_inicial
                        puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)
                        guardar_puntaje(nombre_jugador, puntaje_final)
                    pygame.quit()
                    exit()
                else:
                    pygame.quit()
                    exit()
            elif evento.type == pygame.KEYDOWN:  # detectar teclas presionadas
                if evento.key == pygame.K_RETURN:  # confirmar con enter
                    if nombre.strip():  # asegurar que no este vacio
                        ingresando = False
                elif evento.key == pygame.K_BACKSPACE:  # borrar ultimo caracter
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 15:  # limitar longitud del nombre
                        nombre += evento.unicode  # añadir caracter ingresado

        # Actualizar pantalla con el nombre ingresado
        pygame.draw.rect(ventana, (220, 210, 220), caja_texto)
        texto_ingreso = fuente.render(nombre, True, COLOR_NEGRO) 
        
        # centrar de forma dinamica el ingreso del nombre
        texto_ancho, texto_alto = fuente.size(nombre)  # Obtiene el ancho del texto
        texto_x = caja_texto.x + (caja_texto.width - texto_ancho) // 2
        
        ventana.blit(texto_ingreso, (texto_x, caja_texto.y + 7))
        
        pygame.display.flip()  

    return nombre  # Retornar el nombre ingresado

# Función para mostrar la pantalla de selección de dificultad
def mostrar_seleccion_dificultad(ventana:pygame.Surface)->int:
    """
    Muestra una pantalla para seleccionar la dificultad con un fondo semitransparente.
        Recibe: la superficie (pygame.Surface)
        Retorna: la dificultad seleccionada (int)
    """
    # Transparentar fondo del menu para mostrar dificultades
    overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)  
    overlay.fill((0, 0, 0, 205))  #  opacidad de 205/255
    ventana.blit(overlay, (0, 0))  

    # Definir las cajas para las opciones de dificultad
    caja_facil = pygame.Rect((225, 280, 200, 50))
    caja_intermedio = pygame.Rect((225, 340, 200, 50))
    caja_dificil = pygame.Rect((225, 400, 200, 50))

    # Inicialmente, las cajas tienen el color estatico
    color_caja_facil = COLOR_NEGRO
    color_caja_intermedio = COLOR_NEGRO
    color_caja_dificil = COLOR_NEGRO
    
    seleccionada = None
    while seleccionada == None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if bandera_jugar == True:
                    tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # calcula tiempo transcurrido (en milisegundos)
                    puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # calcular puntaje 
                    guardar_puntaje(nombre_jugador, puntaje_final)  # guardar el puntaje en el archivo JSON
                    pygame.quit()
                    exit()
                else:
                    pygame.quit()
                    exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:  # seleccionar la dificultad y guardarla en la variable "seleccionada"
                if caja_facil.collidepoint(evento.pos):
                    seleccionada = 0
                if caja_intermedio.collidepoint(evento.pos):
                    seleccionada = 1
                if caja_dificil.collidepoint(evento.pos):
                    seleccionada = 2
            if evento.type == pygame.MOUSEMOTION: # cambio de color de cajas al pasar el mouse por encima
                if caja_facil.collidepoint(evento.pos):
                    color_caja_facil = COLOR_GRIS
                else: 
                    color_caja_facil = COLOR_NEGRO
                if caja_intermedio.collidepoint(evento.pos):
                    color_caja_intermedio = COLOR_GRIS
                else: 
                    color_caja_intermedio = COLOR_NEGRO
                if caja_dificil.collidepoint(evento.pos):
                    color_caja_dificil = COLOR_GRIS
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


####################################################################################################################################
#                   DERROTA Y VICTORIA
####################################################################################################################################


def mostrar_mensaje_derrota(ventana:pygame.Surface, puntaje:int)->str:
    """
    Muestra un mensaje de fin de juego indicando que el jugador perdio y su puntaje final.
        Recibe: la superficie (pygame.Surface)
                el puntaje (int)
        Retorna: la cadena para regresar al menu principal (str)
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
        texto_titulo = fuente.render("¡PERDISTE!", True, COLOR_BLANCO)

        ventana.blit(texto_titulo, (195, 197))

        fuente_puntaje = pygame.font.Font(None, 38)
        texto_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}", True, COLOR_BLANCO)
        ventana.blit(texto_puntaje, (245, 303))

        texto_instrucciones = fuente_puntaje.render("Presiona ESC para regresar al menú", True, COLOR_BLANCO)
        ventana.blit(texto_instrucciones, (107, 399))
        
        pygame.display.flip()
        reloj.tick(35)
    
def mostrar_mensaje_victoria(ventana:pygame.Surface, puntaje:int)->str:
    """
    Muestra un mensaje de fin de juego indicando que el jugador gano y su puntaje final.
        Recibe: la superficie (pygame.Surface)
                el puntaje (int)
        Retorna: la cadena para regresar al menu principal (str)
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
    
    # posiciones
    posiciones = []
    for _ in range(cantidad_numeros):
        x = random.randint(0, ANCHO_VENTANA - 20)  
        y = random.randint(ALTO_VENTANA + 10, ALTO_VENTANA + 500)  # Inicializar más abajo
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
            y -= velocidades[i]  
            if y < -20:  
                y = random.randint(ALTO_VENTANA + 10, ALTO_VENTANA + 500)  
            posiciones[i] = (x, y)  

        # Dibujar en la pantalla
        ventana.fill(COLOR_NEGRO)
        for i in range(cantidad_numeros):
            x, y = posiciones[i]
            texto_numeros = fuente_numeros.render(str(numeros[i]), True, colores[i])  
            ventana.blit(texto_numeros, (x, y))

        fuente = pygame.font.Font(None, 72)
        texto_titulo = fuente.render("¡GANASTE!", True, COLOR_BLANCO)
        ventana.blit(texto_titulo, (195, 197))

        fuente_puntaje = pygame.font.Font(None, 38)
        texto_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}", True, COLOR_BLANCO)
        ventana.blit(texto_puntaje, (245, 303))

        texto_instrucciones = fuente_puntaje.render("Presiona ESC para regresar al menú", True, COLOR_BLANCO)
        ventana.blit(texto_instrucciones, (107, 399))
        
        pygame.display.flip()
        reloj.tick(120)


####################################################################################################################################
#                   PUNTAJES
####################################################################################################################################


# Función para mostrar la pantalla de puntajes
def mostrar_puntajes(ventana: pygame.Surface)->None:
    """
    Muestra los puntajes en la pantalla y permite volver al menu.
    Recibe:
        ventana (pygame.Surface)
    Retorna:
        None
    """
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


####################################################################################################################################
#                   TABLERO
####################################################################################################################################


# Funcion para dibujar el tablero
def dibujar_tablero(ventana:pygame.Surface, sudoku:list, sudoku_inicial:list, celda_resaltada=None)->None:
    """
    Dibuja el tablero de Sudoku en la ventana principal, incluyendo celdas, números y resaltados.

    Recibe: 
        - ventana (pygame.Surface): Ventana donde se dibuja el tablero.
        - sudoku (list): Tablero actual del Sudoku (modificado por el usuario).
        - sudoku_inicial (list): Tablero inicial con celdas predeterminadas.
        - celda_resaltada (tuple, optional): Coordenadas de la celda resaltada (fila, columna). 
        Por defecto es None.

    Retorna: 
        No retorna valores. Dibuja directamente el tablero en la ventana.
"""
    for fila in range(9):
        for columna in range(9):
            x = PUNTO_DE_INICIO_TABLERO_SUDOKU_X + (columna * TAMAÑO_CELDA)
            y = PUNTO_DE_INICIO_TABLERO_SUDOKU_Y + (fila * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR)

            # Color de las celdas fijas y editables
            if sudoku_inicial[fila][columna] != 0:
                fondo_color = (208, 208, 208)  # gris claro para celdas fijas
            else:
                fondo_color = (245, 245, 245)  # blanco para celdas editables

            # Resaltar celda seleccionada
            if celda_resaltada == (fila, columna):
                pygame.draw.rect(ventana, COLOR_AMARILLO_CLARO, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)) # celdas que le pasas el mouse encima
            elif celda_seleccionada == (fila, columna):
                pygame.draw.rect(ventana, COLOR_VIOLETA_CLARO, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)) # celdas que seleccionas con un click
            else:
                pygame.draw.rect(ventana, fondo_color, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)) # celdas por defecto (sin ninguna interaccion)

            # Dibujar el contorno de las celdas
            pygame.draw.rect(ventana, COLOR_GRIS, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA), 1)

            # Dibujar los numeros
            if sudoku[fila][columna] != 0:
                if (fila, columna) in numeros_errados: # rojo para los numeros incorrectos
                    color = COLOR_ROJO
                elif sudoku_inicial[fila][columna] != 0: # azul para los numeros fijos (no editables)
                    color = COLOR_AZUL_OSCURO
                else:
                    color = COLOR_VERDE # verde para los numeros correctos  
                texto = pygame.font.Font(None, 36).render(str(sudoku[fila][columna]), True, color)
                ventana.blit(
                    texto,
                    (x + TAMAÑO_CELDA // 2 - texto.get_width() // 2, y + TAMAÑO_CELDA // 2 - texto.get_height() // 2),
                )

            # Dibujar las lineas mas gruesas para los bloques   
            for i in range(0, 10, 3):
                # Horizontales
                pygame.draw.line(
                    ventana, 
                    COLOR_NEGRO, 
                    (55, 55 + i * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR),  # inicio
                    (55 + 9 * TAMAÑO_CELDA, 55 + i * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR),  # fin
                    4  # grosor
                )
                # Verticales
                pygame.draw.line(
                    ventana, 
                    COLOR_NEGRO, 
                    (55 + i * TAMAÑO_CELDA, 55 + ALTO_BARRA_SUPERIOR),  # inicio
                    (55 + i * TAMAÑO_CELDA, 55 + 9 * TAMAÑO_CELDA + ALTO_BARRA_SUPERIOR),  # fin
                    4  # grosor
                )


############################################################################################################################################
#                        EJECUCION
############################################################################################################################################

estado = MENU

# ESTADO MENU --------------------------------------------------------------------------------------------------------------------------------

while True:
    if estado == MENU:
        # Crear rectangulos interactivos para botones del menu
                                # x    y  ( tamaño )
        rect_jugar = pygame.Rect(253, 437, 145, 35)  
        rect_puntaje = pygame.Rect(253, 475, 145, 35)  
        rect_salir = pygame.Rect(253, 513, 145, 35)  

        # CREAR LA VENTANA PRINCIPAL
        ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Sudoku Interactivo")

        nombre_jugador = ""

        # colores iniciales de los botones (hasta que se les pasa el mouse por encima)
        color_rect_jugar = COLOR_GRIS_OSCURO
        color_rect_puntaje = COLOR_GRIS_OSCURO
        color_rect_salir = COLOR_GRIS_OSCURO

        bandera_jugar = False
        
        # bucle del menu
        menu_activado = True
        while menu_activado:
            ventana.fill(COLOR_NEGRO)
            ventana.blit(imagen_fondo_sudoku, (0, 0))
            ventana.blit(imagen_menu, (56, 100))
            
# INICIO DE EVENTOS (menu) ..............................................................................................................

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Pregunta si entramos a la pantalla jugar antes de cerrar (para evitar que se ejecuten variables que no declaramos)
                    if bandera_jugar == True:
                    # Calcular puntaje antes de salir
                        tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # Calcular tiempo transcurrido en milisegundos
                        puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # Usar la función calcular_puntaje
                        guardar_puntaje(nombre_jugador, puntaje_final)  # Guardar el puntaje
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
                            dificultad = mostrar_seleccion_dificultad(ventana)
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=700)
                            # Ingreso del nombre del jugador
                            nombre_jugador = mostrar_ingreso_nombre(ventana)
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=700)
                            bandera_jugar = True
                            estado = JUEGO
                            menu_activado = False
                        if rect_puntaje.collidepoint(evento.pos):
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=500)
                            mostrar_puntajes(ventana)       
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=500)
                        if rect_salir.collidepoint(evento.pos):
                            transicion_fundido(ventana, color=(0, 0, 0), duracion=400)
                            pygame.quit()
                            exit()
                            
                # Cambio de color botones al pasar mouse por encima
                if evento.type == pygame.MOUSEMOTION: 
                    if rect_jugar.collidepoint(evento.pos):  # boton jugar
                        color_rect_jugar = COLOR_AMARILLO_FUERTE 
                    else: 
                        color_rect_jugar = COLOR_GRIS_OSCURO
                    if rect_puntaje.collidepoint(evento.pos):  # boton puntaje
                        color_rect_puntaje = COLOR_AMARILLO_FUERTE 
                    else: 
                        color_rect_puntaje = COLOR_GRIS_OSCURO
                    if rect_salir.collidepoint(evento.pos):  # boton salir
                        color_rect_salir = COLOR_AMARILLO_FUERTE
                    else: 
                        color_rect_salir = COLOR_GRIS_OSCURO
            
# CIERRE DE EVENTOS ................................................................................................................

            # dibujo de rectangulos de botones jugar, puntaje, salir...
            pygame.draw.rect(ventana, color_rect_jugar, rect_jugar, width=2)
            pygame.draw.rect(ventana, color_rect_puntaje, rect_puntaje, width=2)
            pygame.draw.rect(ventana, color_rect_salir, rect_salir, width=2)

            pygame.display.flip()


# ESTADO JUEGO --------------------------------------------------------------------------------------------------------------------------------

    elif estado == JUEGO: 
        juego_completado = False
        # Crear rectangulos interactivos para boton de la pantalla jugando
        rect_nuevo_tablero = pygame.Rect(430, 686, 170, 40)  
        rect_volver_al_menu = pygame.Rect(54, 686, 170, 40)

        # Generar Sudoku inicial y tablero inicial
        sudoku_inicial = generar_nuevo_sudoku(dificultad)
        sudoku = copy.deepcopy(sudoku_inicial)
        errores = 0
        tiempo_inicial = pygame.time.get_ticks()

        # Ciclo principal del juego
        celda_resaltada = None
        celda_seleccionada = None
        
        color_boton_nuevo_tablero = COLOR_VERDE_OSCURO
        color_borde_nuevo_tablero = COLOR_VERDE_CLARO  
        
        color_boton_volver_al_menu = COLOR_NARANJA_OSCURO
        color_borde_volver_al_menu = COLOR_NARANJA_CLARO

        numeros_errados = []

        jugando = True
        while jugando:
            
            ventana.fill(COLOR_BLANCO)
            ventana.blit(imagen_fondo_sudoku, (0, 0))
            
            dibujar_barra_superior(ventana, tiempo_inicial, errores, nombre_jugador)
            dibujar_tablero(ventana, sudoku, sudoku_inicial, celda_resaltada)
            
            # Borde blanco para el tablero sudoku
            pygame.draw.rect(ventana, COLOR_BLANCO, (51, 111, 550, 550), width=3)

            # Texto boton nuevo tablero
            fuente_boton = pygame.font.Font(None, 28)  
            texto_boton_nuevo_tablero = fuente_boton.render("Nuevo tablero", True, COLOR_BLANCO)  

            # Texto boton volver al menu
            fuente_boton = pygame.font.Font(None, 28)  
            texto_boton_volver_al_menu = fuente_boton.render("Volver al menu", True, COLOR_BLANCO)  

# EVENTOS (juego) --------------------------------------------------------------------------------------------------------------------------------

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: 
                    if estado == JUEGO:  # verifica si estas en JUEGO
                        tiempo_total = pygame.time.get_ticks() - tiempo_inicial  # Calcular tiempo transcurrido en milisegundos
                        puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  # Usar la función calcular_puntaje
                        if juego_completado:  # guardar solo si el juego fue completado
                            guardar_puntaje(nombre_jugador, puntaje_final)
                    pygame.quit()
                    exit()
                
                if evento.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = evento.pos
                    # Calcular coordenadas relativas al tablero
                    if 55 <= mouse_x < 55 + 9 * TAMAÑO_CELDA and 55 + ALTO_BARRA_SUPERIOR <= mouse_y < 55 + ALTO_BARRA_SUPERIOR + 9 * TAMAÑO_CELDA:
                        columna = (mouse_x - 55) // TAMAÑO_CELDA # columna
                        fila = (mouse_y - 55 - ALTO_BARRA_SUPERIOR) // TAMAÑO_CELDA # fila
                        if 0 <= columna < 9 and 0 <= fila < 9:
                            celda_resaltada = (fila, columna) # si estas sobre una celda se guardan las coordenadas en una variable
                        else:
                            celda_resaltada = None # de lo contrario, celda_resaltada == None
                    else:
                        celda_resaltada = None # si no estas sobre el tablero: celda_resaltada == None
                    # Iluminar botones de nuevo tablero y de volver al menu (cuando pasas por encima con el mouse)
                    if rect_nuevo_tablero.collidepoint(evento.pos): # nuevo tablero
                        color_boton_nuevo_tablero = COLOR_VERDE_CLARO
                    else:
                        color_boton_nuevo_tablero = COLOR_VERDE_OSCURO
                    if rect_volver_al_menu.collidepoint(evento.pos): # volver al menu
                        color_boton_volver_al_menu = COLOR_NARANJA_CLARO
                    else:
                        color_boton_volver_al_menu = COLOR_NARANJA_OSCURO

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if rect_nuevo_tablero.collidepoint(evento.pos):  # Nuevo tablero y se reinicia el tiempo, el sudoku y los errores
                            sudoku_inicial = generar_nuevo_sudoku(dificultad)
                            sudoku = copy.deepcopy(sudoku_inicial)
                            tiempo_inicial = pygame.time.get_ticks()
                            errores = 0
                            numeros_errados = []
                        if rect_volver_al_menu.collidepoint(evento.pos): # volver al menu
                            estado = MENU
                            jugando = False
                        if celda_resaltada and sudoku_inicial[celda_resaltada[0]][celda_resaltada[1]] == 0: 
                            celda_seleccionada = celda_resaltada  # si clickeas una celda, esta se guarda en una variable para cambiar su color
                        else:
                            celda_seleccionada = None

                if evento.type == pygame.KEYDOWN:
                    if celda_seleccionada:  # verifica que hayamos seleccionado una celda para poder ingresar un numero
                        fila, columna = celda_seleccionada  # guarda las coordenadas de la celda
                        if evento.key in [pygame.K_BACKSPACE, pygame.K_DELETE]: # borrar numero
                            sudoku[fila][columna] = 0
                            if (fila, columna) in numeros_errados:
                                numeros_errados.remove((fila, columna)) # borra el numero errado de la lista de errados
                        elif evento.unicode.isdigit() and evento.unicode != "0":
                            num = int(evento.unicode)  # ingreso de numero
                            if es_valido(sudoku, fila, columna, num):  # se valida que sea correcto el num ingresado
                                sudoku[fila][columna] = num  
                                bandera_error = False  # bandera numero correcto
                                if (fila, columna) in numeros_errados:
                                    numeros_errados.remove((fila, columna))  
                            else:                              # si el numero no es valido...
                                sudoku[fila][columna] = num
                                bandera_error = True   # bandera numero incorrecto
                                if (fila, columna) not in numeros_errados:
                                    numeros_errados.append((fila, columna))  # se agrega el nmero errado a la lista de errados
                                errores += 1  
                                if errores >= 3:  
                                    tiempo_total = pygame.time.get_ticks() - tiempo_inicial  
                                    puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)  
                                    guardar_puntaje(nombre_jugador, puntaje_final)  
                                    cambiar_musica(RUTA_MUSICA_DERROTA)
                                    resultado = mostrar_mensaje_derrota(ventana, puntaje_final)
                                    if resultado == "menu_derrota":
                                        cambiar_musica(RUTA_MUSICA_SUDOKU)
                                        estado = MENU
                                        jugando = False
                                        menu_activado = True
                                    break

        # Verificar si el tablero esta completo despues de procesar eventos
            
            # Verifica que no haya (ceros) para saber si esta completo el sudoku
            completo = True
            for i in range(len(sudoku)):
                for j in range(len(sudoku[i])):
                    if sudoku[i][j] == 0:
                        completo = False
                        break 

            if completo == True and tablero_valido(sudoku) == True:  # Tablero completo y valido
                tiempo_total = pygame.time.get_ticks() - tiempo_inicial
                puntaje_final = calcular_puntaje(dificultad, errores, tiempo_total)
                guardar_puntaje(nombre_jugador, puntaje_final)
                juego_completado = True  # Marcar como completado
                cambiar_musica(RUTA_MUSICA_VICTORIA)
                resultado = mostrar_mensaje_victoria(ventana, puntaje_final)
                if resultado == "menu_victoria":
                    cambiar_musica(RUTA_MUSICA_SUDOKU)
                    estado = MENU
                    jugando = False
                break
            
            # REVISAR (ME PARECE QUE ESTA AL PEDO PORQUE NO HAY FORMA DE Q EL TABLEO SE ARME MAL SI SE VA VALIDANDO SOLO...)
            # LO COMENTE PORQUE ME TIRABA ERROR

            # elif completo:
            #     print("El tablero no cumple las reglas")
            #     # Calcular el tiempo transcurrido
            #     tiempo_final = pygame.time.get_ticks()
            #     tiempo_transcurrido = (tiempo_final - tiempo_inicial) // 60000  # Convertir milisegundos a minutos
                
            #     # Obtener el multiplicador de dificultad
            #     multiplicador_dificultad = DIFICULTADES[dificultad]  # Basado en la dificultad seleccionada

            #     # Calcular el puntaje final
            #     puntaje_final = calcular_puntaje(
            #         PUNTOS_BASE,
            #         errores,
            #         PENALIZACION_ERROR,
            #         tiempo_transcurrido,
            #         PENALIZACION_TIEMPO,
            #         multiplicador_dificultad
            #     )
            #     # Guardar el puntaje del jugador
            #     guardar_puntaje(nombre_jugador, puntaje_final)
            #     print(f"Juego completo! Puntaje de {nombre_jugador}: {puntaje_final}")

                # Salir del bucle del juego
                # jugando = False
            
            # Boton para reinciar tablero 
            pygame.draw.rect(ventana, color_boton_nuevo_tablero, rect_nuevo_tablero, border_radius=10)  # Fondo del botón
            pygame.draw.rect(ventana, color_borde_nuevo_tablero, rect_nuevo_tablero, width=3, border_radius=10)  # Borde del botón
            ventana.blit(texto_boton_nuevo_tablero, (447, 696))

            # Boton para volver al menu
            pygame.draw.rect(ventana, color_boton_volver_al_menu, rect_volver_al_menu, border_radius=10)  # Fondo del boton
            pygame.draw.rect(ventana, color_borde_volver_al_menu, rect_volver_al_menu, width=3, border_radius=10)  # Borde del boton
            ventana.blit(texto_boton_volver_al_menu, (67, 696))
            
            pygame.display.flip()
