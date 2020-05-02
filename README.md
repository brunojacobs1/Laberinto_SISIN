# SISIN T1

Examen T1 del curso Sistemas Inteligentes.

## Integrantes

* Jacobs Schulz, Bruno - N00095845

### Enunciado

La cuadricula que se muestra en el grafico 1 es una cuadricula de 30 x 30, en la cual se muestra un laberinto y donde se debe considerar:

* Existen 4 caminos por donde el carro puede llegar a la meta.
* El recorrido o la iteración del carro es de cuadro por cuadro.
* El carro puede moverse a cualquiera de las 4 direcciones (izquierda, derecha, arriba y abajo).
* Se inicia en la posición (1,1) y se llega a la meta en la posición (30, 30).
* Se debe preguntar si en la siguiente iteración propuesta esta bloqueada o libre (negro bloqueado y blanco libre) y decidir si se avanza o no.

Se pide:

* Representar el espacio de problemas.
* Desarrollar un programa de software que encuentre las posibles soluciones y determine cual es la ruta más optima. La ruta mas optima es la que use menos cuadriculas para legar a la meta.
* El programa debe ser desarrollado basado en lógica y no código en duro
* Debe existir una representación gráfica de las soluciones (espacio de problemas). Esta representación no tiene que ser necesariamente con un icono de un carrito, si es en consola se puede representar el movimiento con una X, o un color tipo serpiente.

### Laberinto

![alt text](https://user-images.githubusercontent.com/29410332/80855055-43e39400-8c03-11ea-8d8e-1cde496cbc9c.png "Laberinto")

### Solución

Para la presente solución se procedió a utilizar dos tipos de algoritmos: De búsqueda desinformada (Breadth First Search) y de búsqueda informada (A*). Breadth First Search permite realizar una búsqueda desinformada de un punto final dado un punto incial. Este algoritmo genera un grafo de los nodos que recorrió, donde cada nodo es un cuadrado del laberinto. Dado a que recorre todos los posibles caminos (en profundidad) al mismo tiempo, cuando se llegue a la solución se tiene asegurado que el camino tomado es el más corto. A* por su parte, es un algoritmo de búsqueda informada, lo que quiere decir que es formulado como un grafo con costos. Su objetivo es buscar el camino más corto, y a su vez explorar la menor cantidad de caminos. Para lograr esto utiliza la siguiente fórmula:

###  f<sub>(n)</sub> = g<sub>(n)</sub> + h<sub>(n)</sub>

donde n es el siguiente nodo del camino, g<sub>(n)</sub> es el costo desde el primer nodo hasta n, y h<sub>(n)</sub> es una función heurística que estima el costo del mejor camino desde n hasta el objetivo. Esto quiere decir que en lugar de recorrer todos los posibles caminos, solo recorre aquel camino en el que el nodo actual tiene el menor costo total. Si dicha heurística es __admisible__, es decir, que nunca sobrevalora el verdadero costo para llegar a la solución o que para cada nodo se cumple que el costo total de ese nodo es menor que el valor heurístico + el costo para llegar al nodo anterior, se garantiza que A* encontrará el camino óptimo.

Para este problema, dado que cada movimiento solo puede ser en 4 direcciones, se seleccionó como heurística admisible la distancia de Manhattan. La función que representa a esta heurística es:

### d(x,y) = &sum; |x<sub>i</sub> - y<sub>i</sub>|

en otras palabras, el valor absoluto de la sumatoria de la distancia vertical y horizontal desde un nodo hasta el objetivo.

### Estados

## Bread-First Search

Cabe recalcar que nuestro script de python utiliza un archivo de texto con la distribución del laberinto como input, y genera una imagen del laberinto solucionado, donde el mejor camino es resaltado de color verde, y el resto de caminos que recorre pero que no forman parte de la solución son resaltados de color rojo. 

### Estado Inicial

### Estado Final

## A*

### Estado Inicial

### Estado Final

Como se puede observar, Bread-First Search recorre 214 estados o cuadrados en su desarollo para llegar a la solución, mientras que A* solo recorre 96 estados.
