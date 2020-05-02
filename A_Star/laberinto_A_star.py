import sys
from queue import Queue

# Frontier = Cuadrados o nodos que se evaluaran para ver si forman parte de la solucion

def Manhattan(actual,final):
    return (abs(actual[0] - final[0]) + abs(actual[1] - final[1])) 

class Nodo():
    def __init__(self, estado, anterior, accion, g, h, f):
        self.estado = estado
        self.anterior = anterior
        self.accion = accion
        self.g = g # g(n) es la distancia desde el inicio hasta el nodo actual
        self.h = h # h(n) es la heuristica (distancia desde el nodo actual hasta el final)
        self.f = f # f(n) = g(n) + h(n) - Costo total del nodo

class Frontier():
    estados = []
    def ContieneEstado(self, estado):
        for nodo in self.estados:
            if nodo.estado == estado:
                return nodo

class Laberinto():

    def __init__(self, filename):

        # Leer el archivo de texto
        with open(filename) as f:
            contenido = f.read()

        # Validar que exista un inicio y un final en el lab
        if contenido.count("A") != 1:
            raise Exception("El laberinto debe tener un inicio")
        if contenido.count("B") != 1:
            raise Exception("El laberinto debe tener un final")

        # Determinar dimensiones del lab
        contenido = contenido.splitlines() 
        self.altura = len(contenido) # Cantidad de filas
        self.anchura = max(len(linea) for linea in contenido) # Anchura va a ser = a la fila mas larga

        # Identificar las paredes del lab. Una pared es cualquier espacio que no incluya "A", "B" o un espacio en blanco.
        self.paredes = []
        for i in range(self.altura):
            fila = []
            for j in range(self.anchura):
                try:
                    if contenido[i][j] == "A":
                        self.inicio = (i, j)
                        fila.append(False)
                    elif contenido[i][j] == "B":
                        self.final = (i, j)
                        fila.append(False)
                    elif contenido[i][j] == " ":
                        fila.append(False)
                    else:
                        fila.append(True)
                except IndexError:
                    fila.append(False)
            self.paredes.append(fila)

        self.solucion = None


    def MostrarLab(self):
        solucion = self.solucion[1] if self.solucion is not None else None
        print()
        for i, fila in enumerate(self.paredes):
            for j, columna in enumerate(fila):
                if columna:
                    print("█", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.final:
                    print("B", end="")
                elif solucion is not None and (i, j) in solucion:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def Adyacentes(self, estado):
        fila, columna = estado
        candidatos = [
            ("arriba", (fila - 1, columna)),
            ("abajo", (fila + 1, columna)),
            ("izquierda", (fila, columna - 1)),
            ("derecha", (fila, columna + 1))
        ]

        resultado = []
        for accion, (fila, columna) in candidatos:
            if 0 <= fila < self.altura and 0 <= columna < self.anchura and not self.paredes[fila][columna]:
                resultado.append((accion, (fila, columna)))
        return resultado


    def Resolver(self):

        # Mantener numero de estados explorados
        self.numExplorados = 0

        # Inicializar el frontier al estado inicial
        inicio = Nodo(estado=self.inicio, anterior=None, accion=None,
                      g = 0, h = 0, f = 0)
        frontier = Frontier()
        frontier.estados.append(inicio)

        # Inicializar un set de estados explorados
        self.explorados = set()

        # Repetir hasta encontrar la solucion
        while True:

            # Si no hay nada en el frontier, no hay camino
            if len(frontier.estados) < 0:
                raise Exception("no hay solucion")

            # Seleccionar el primer cuadrado de la frontier
            nodo = frontier.estados[0]
            pos = 0

            # Buscar el cuadrado con el menor costo total F de la frontier
            for i, nnodo in enumerate(frontier.estados):
                if nnodo.f < nodo.f:
                    nodo = nnodo
                    pos = i

                    
            # Quitar el cuadrado actual de la frontier
            frontier.estados.pop(pos)
            
            self.numExplorados += 1
                        

            # Si el cuadrado es el final, se encontro la solucion
            if nodo.estado == self.final:
                acciones = []
                estados = []
                while nodo.anterior is not None:
                    acciones.append(nodo.accion)
                    estados.append(nodo.estado)
                    nodo = nodo.anterior
                acciones.reverse()
                estados.reverse()
                self.solucion = (acciones, estados)
                self.estados = len(estados)
                return

            # Marcar cuadrado como explorado
            self.explorados.add(nodo.estado)

            # Agregar adyacentes al frontier
            for accion, estado in self.Adyacentes(nodo.estado):
                #Calcular valores de g, h y f
                g = nodo.g + 1
                h = Manhattan(estado,self.final)
                f = g + h
                xnodo = frontier.ContieneEstado(estado)
                if estado not in self.explorados:
                    # Si el adyacente aun no ha sido recorrido y no esta en la frontier, se añade
                    # a la frontier como hijo del cuadrado actual con los valores g, h y f calculados.
                    if xnodo is None:
                        siguiente = Nodo(estado=estado, anterior=nodo, accion=accion,   
                                         g=g, h=h, f=f)
                        frontier.estados.append(siguiente)
                    # Si el adyacente aun no ha sido recorrido pero se encuentra en la frontier, se verifica si el camino
                    # para llegar a el es mejor, evaluando su valor g. Si este cuadrado presenta un mejor camino, se vuelve el hijo
                    # del cuadrado actual y se recalculan los valores g y f.
                    elif xnodo is not None:
                        if xnodo.g < g:
                            g = xnodo.g + 1
                            f = g + h
                            siguiente = Nodo(estado=estado, anterior=xnodo, accion=accion,
                                             g=g, h=h, f=f)
                            frontier.estados.append(siguiente)  
                     


    def GenerarImagen(self, filename, mostrarSolucion=True, mostrarExplorados=False):
        from PIL import Image, ImageDraw
        sizeCuadro = 50
        sizeBorde = 2

        # Crear un canvas en blanco
        img = Image.new(
            "RGBA",
            (self.anchura * sizeCuadro, self.altura * sizeCuadro),
            "black"
        )
        canvas = ImageDraw.Draw(img)

        solucion = self.solucion[1] if self.solucion is not None else None
        for i, fila in enumerate(self.paredes):
            for j, columna in enumerate(fila):

                # Paredes
                if columna:
                    fill = (40, 40, 40)

                # Inicio
                elif (i, j) == self.inicio:
                    fill = (255, 0, 0)

                # Final
                elif (i, j) == self.final:
                    fill = (255, 0, 0)

                # Solucion
                elif solucion is not None and mostrarSolucion and (i, j) in solucion:
                    fill = (102, 255, 102)

                # Explorados
                elif solucion is not None and mostrarExplorados and (i, j) in self.explorados:
                    fill = (255, 97, 85)

                # Cuadro vacio
                else:
                    fill = (237, 240, 252)

                # Dibujar cuadro
                canvas.rectangle(
                    ([(j * sizeCuadro + sizeBorde, i * sizeCuadro + sizeBorde),
                      ((j + 1) * sizeCuadro - sizeBorde, (i + 1) * sizeCuadro - sizeBorde)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Uso: python laberinto_A_star.py laberinto.txt")

m = Laberinto(sys.argv[1])
print("Laberinto:")
m.Resolver()
print("Estados explorados:", m.numExplorados)
print("Solucion optima en {} pasos".format(m.estados))
print("Solucion:")
m.MostrarLab()
m.GenerarImagen("laberinto_A_star.png", mostrarExplorados=True)
