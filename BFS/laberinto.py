import sys
from queue import Queue

class Nodo():
    def __init__(self, estado, anterior, accion):
        self.estado = estado
        self.anterior = anterior
        self.accion = accion

class ColaFrontier(Queue):
    frontier = []
    def ContieneEstado(self, estado):
        return any(nodo.estado == estado for nodo in self.frontier)

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
        inicio = Nodo(estado=self.inicio, anterior=None, accion=None)
        frontier = ColaFrontier()
        frontier.put(inicio)

        # Inicializar un set de estados explorados
        self.explorados = set()

        # Repetir hasta encontrar la solucion
        while True:

            # Si no hay nada en el frontier, no hay camino
            if frontier.empty():
                raise Exception("no hay solucion")

            # Elegir un nodo del frontier
            nodo = frontier.get()
            self.numExplorados += 1

            # Si el nodo es el final, se encontro la solucion
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

            # Marcar nodo como explorado
            self.explorados.add(nodo.estado)

            # Agregar adyacentes al frontier
            for accion, estado in self.Adyacentes(nodo.estado):
                if not frontier.ContieneEstado(estado) and estado not in self.explorados:
                    siguiente = Nodo(estado=estado, anterior=nodo, accion=accion)
                    frontier.put(siguiente)


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
    sys.exit("Uso: python laberinto.py laberinto.txt")

m = Laberinto(sys.argv[1])
print("Laberinto:")
m.Resolver()
print("Estados explorados:", m.numExplorados)
print("Solucion optima en {} pasos".format(m.estados))
print("Solucion:")
m.MostrarLab()
m.GenerarImagen("laberinto.png", mostrarExplorados=True)
