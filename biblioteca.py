import random



def crear_matriz(filas: int, columnas: int, dato=0) -> list:
    '''
    Funcion: Nos genera una matriz bidimensional inicializada con un valor dado.

    Recibe: 
        - filas (int): Número de filas de la matriz.
        - columnas (int): Número de columnas de la matriz.
        - dato (int, opcional): Valor inicial con el que se llenará la matriz. Por defecto, 0.

    Retorna: 
        Una lista bidimensional de tamaño (filas x columnas) llena con el valor especificado.
    '''
    matriz = []
    for _ in range(filas):
        fila = [dato] * columnas
        matriz.append(fila)
    return matriz

def es_valido(matriz: list, fila: int, columna: int, num: int) -> bool:
    '''
    Funcion: Valida si un número puede colocarse en una celda de un Sudoku.

    Recibe: 
        - matriz (list): Tablero del Sudoku.
        - fila (int): Índice de la fila.
        - columna (int): Índice de la columna.
        - num (int): Número a validar.

    Retorna: 
        True si el número puede colocarse en la celda, False en caso contrario.
    '''
    valido = True

    if num in matriz[fila]:  # Revisa filas
        valido = False

    if valido:  # Revisa columnas
        for i in range(len(matriz)):
            if matriz[i][columna] == num:
                valido = False
                break

    if valido:  # Revisa bloques de 3x3
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        for i in range(inicio_fila, inicio_fila + 3):
            for j in range(inicio_columna, inicio_columna + 3):
                if matriz[i][j] == num:
                    valido = False
                    break
            if not valido:
                break

    return valido


def lista_numeros_aleatorios(cantidad: int, rango_min: int, rango_max: int) -> list:
    '''
    Funcion: Nos genera una lista de números aleatorios únicos.

    Recibe: 
        - cantidad (int): Número de elementos en la lista.
        - rango_min (int): Valor mínimo del rango.
        - rango_max (int): Valor máximo del rango.

    Retorna: 
        Una lista de números aleatorios únicos dentro del rango especificado.
    '''
    lista = []
    while len(lista) < cantidad:
        num = random.randint(rango_min, rango_max)
        if num not in lista:
            lista.append(num)
    return lista

def llenar_sudoku(matriz: list) -> bool:
    '''
    Funcion: Llena un tablero de Sudoku de forma recursiva.

    Recibe: 
        - matriz (list): Tablero del Sudoku (matriz bidimensional).

    Retorna: 
        True si logra llenar el tablero exitosamente, False si no es posible.
    '''
    exito = False

    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == 0:
                lista_num_alea = lista_numeros_aleatorios(9, 1, 9)
                for num in lista_num_alea:
                    if es_valido(matriz, fila, columna, num):
                        matriz[fila][columna] = num
                        if llenar_sudoku(matriz):
                            exito = True
                            break
                        matriz[fila][columna] = 0
                if not exito:
                    exito = False
                break
        if exito or matriz[fila][columna] == 0:
            break
    else:
        exito = True

    return exito


def generar_sudoku(filas: int, columnas: int) -> list:
    '''
    Funcion: Genera un tablero de Sudoku completo.

    Recibe: 
        - filas (int): Número de filas del tablero (9 para Sudoku estándar).
        - columnas (int): Número de columnas del tablero (9 para Sudoku estándar).

    Retorna: 
        Una matriz bidimensional representando un Sudoku completo.
    '''
    sudoku = crear_matriz(filas, columnas, dato=0)
    llenar_sudoku(sudoku)
    return sudoku

def lista_posiciones_a_ocultar(cantidad: int) -> list:
    '''
    Funcion: Nos genera una lista de posiciones aleatorias para ocultar celdas en un Sudoku.

    Recibe: 
        - cantidad (int): Cantidad de celdas a ocultar.

    Retorna: 
        Una lista de coordenadas (fila, columna) únicas.
    '''
    lista = []
    while len(lista) < cantidad:
        coordenadas = [random.randint(0, 8), random.randint(0, 8)]
        if coordenadas not in lista:
            lista.append(coordenadas)
    return lista

def ocultar_celdas(sudoku: list, celdas_a_tapar: int) -> list:
    '''
    Funcion: Oculta celdas de un Sudoku colocando ceros en posiciones aleatorias.

    Recibe: 
        - sudoku (list): Tablero del Sudoku (matriz bidimensional).
        - celdas_a_tapar (int): Cantidad de celdas a ocultar.

    Retorna: 
        El tablero del Sudoku con las celdas ocultas.
    '''
    lista_coordenadas = lista_posiciones_a_ocultar(celdas_a_tapar)
    for fila, columna in lista_coordenadas:
        sudoku[fila][columna] = 0
    return sudoku


##########################


