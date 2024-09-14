import time
import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Clase para representar el grafo de nodos
class Nodo:
    def __init__(self, x, y, costo=float('inf'), padre=None):
        self.x = x  # Posición X
        self.y = y  # Posición Y
        self.costo = costo  # Costo acumulado hasta este nodo
        self.padre = padre  # Nodo padre (para reconstruir el camino)

    def __lt__(self, otro):
        return self.costo < otro.costo

# Función heurística (usamos la distancia Manhattan como ejemplo)
def heuristica(nodo, objetivo):
    return abs(nodo.x - objetivo.x) + abs(nodo.y - objetivo.y)

def d_star(mapa, inicio, objetivo):
    # Inicializar lista de prioridad (open list)
    open_list = []
    heapq.heappush(open_list, (0, inicio))  # Añadir el nodo de inicio a la open list

    # Mantener una lista cerrada (closed list) para nodos ya explorados
    closed_list = set()

    # Mientras haya nodos por explorar
    while open_list:
        _, nodo_actual = heapq.heappop(open_list)

        # Si llegamos al objetivo, reconstruimos el camino
        if nodo_actual.x == objetivo.x and nodo_actual.y == objetivo.y:
            return reconstruir_camino(nodo_actual)

        # Añadir el nodo actual a la closed list
        closed_list.add((nodo_actual.x, nodo_actual.y))

        # Explorar vecinos del nodo actual
        for vecino in obtener_vecinos(nodo_actual, mapa):
            if (vecino.x, vecino.y) in closed_list:
                continue  # Saltar nodos ya explorados

            # Calcular el nuevo costo para el vecino
            nuevo_costo = nodo_actual.costo + costo_movimiento(nodo_actual, vecino)

            if nuevo_costo < vecino.costo:  # Si encontramos un camino mejor
                vecino.costo = nuevo_costo
                vecino.padre = nodo_actual  # Actualizamos el nodo padre
                prioridad = nuevo_costo + heuristica(vecino, objetivo)
                heapq.heappush(open_list, (prioridad, vecino))  # Añadir a la lista abierta

    # Si no hay camino, devolvemos None
    return None

# Función para obtener los vecinos de un nodo
def obtener_vecinos(nodo, mapa):
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimiento en 4 direcciones
    for mov in movimientos:
        nx, ny = nodo.x + mov[0], nodo.y + mov[1]
        if 0 <= nx < len(mapa) and 0 <= ny < len(mapa[0]) and mapa[nx][ny] == 0:  # Espacio libre
            vecinos.append(Nodo(nx, ny))
    return vecinos

# Función para calcular el costo de movimiento entre nodos
def costo_movimiento(nodo1, nodo2):
    return 1  # Asumimos costo uniforme por cada movimiento

# Función para reconstruir el camino desde el nodo objetivo
def reconstruir_camino(nodo):
    camino = []
    while nodo:
        camino.append((nodo.x, nodo.y))
        nodo = nodo.padre
    camino.reverse()  # Invertir para obtener el camino en orden
    return camino

# Definir el mapa (0 = libre, 1 = obstáculo)
mapa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

# Crear nodos de inicio y objetivo
inicio = Nodo(0, 0, costo=0)
objetivo = Nodo(4, 10)

# Medir el tiempo antes de ejecutar el algoritmo
start_time = time.time()

# Ejecutar el algoritmo D*
camino = d_star(mapa, inicio, objetivo)

# Medir el tiempo después de ejecutar el algoritmo
end_time = time.time()

# Mostrar el resultado
if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró camino.")

# Mostrar el tiempo de ejecución
print("Tiempo de ejecución: {:.6f} segundos".format(end_time - start_time))


# Función para dibujar el mapa y la animación del camino
def dibujar_mapa_con_animacion(mapa, camino):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Dibujar el mapa
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == 1:
                ax.plot(j, i, 'ks')  # Obstáculos como cuadrados negros

    # Marcar inicio y objetivo
    ax.plot(inicio.y, inicio.x, 'go', markersize=10, label='Inicio')  # Nodo de inicio en verde
    ax.plot(objetivo.y, objetivo.x, 'ro', markersize=10, label='Objetivo')  # Nodo objetivo en rojo

    # Configurar la cuadrícula
    ax.set_xlim(-1, len(mapa[0]))
    ax.set_ylim(-1, len(mapa))
    ax.invert_yaxis()
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xticks(range(len(mapa[0])))
    ax.set_yticks(range(len(mapa)))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Función para actualizar cada frame de la animación
    def actualizar_frame(frame):
        ax.plot(camino[frame][1], camino[frame][0], 'bo-', linewidth=2, markersize=6)  # Camino en azul

    # Crear la animación
    ani = animation.FuncAnimation(fig, actualizar_frame, frames=len(camino), interval=500, repeat=False)
    
    # Añadir leyenda
    ax.legend(loc='upper left')
    plt.show()
    
# Crear y mostrar la animación del camino
dibujar_mapa_con_animacion(mapa, camino)