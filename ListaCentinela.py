# Programa: ListaCentinela.py
# Objetivo: Implementación del TAD Lista simplemente ligada con nodo centinela al inicio,
#           junto con su iterador. Es la estructura de almacenamiento dinámico que sustituye
#           al arreglo redimensionable (numpy) de la Secuencia de la Tarea 3.
# Autor: Huitzilovers2.0 - Integrante 1 (Emiliano Parra Miranda)
# Fecha: Octubre 2026

from typing import Any, Callable, Iterable, Optional


class Nodo:
    """
    Nodo de una lista simplemente ligada. Guarda un dato y la referencia al
    siguiente nodo de la lista.
    """

    def __init__(self, dato: Any = None, siguiente: Optional["Nodo"] = None):
        """
        Constructor del Nodo.
        :param dato: El dato que almacena el nodo (None para el nodo centinela)
        :param siguiente: Referencia al siguiente nodo (None si es el último)
        """
        self.__dato = dato
        self.__siguiente = siguiente

    @property
    def dato(self) -> Any:
        """
        Método GET para obtener el dato almacenado en el nodo.
        :return: El dato del nodo
        """
        return self.__dato

    @dato.setter
    def dato(self, dato: Any):
        """
        Método SET para modificar el dato almacenado en el nodo.
        :param dato: El nuevo dato
        """
        self.__dato = dato

    @property
    def siguiente(self) -> Optional["Nodo"]:
        """
        Método GET para obtener la referencia al siguiente nodo.
        :return: El siguiente nodo, o None si es el último
        :rtype: Nodo | None
        """
        return self.__siguiente

    @siguiente.setter
    def siguiente(self, siguiente: Optional["Nodo"]):
        """
        Método SET para modificar la referencia al siguiente nodo.
        :param siguiente: El nuevo nodo siguiente
        """
        self.__siguiente = siguiente


class IteradorLista:
    """
    Iterador de la lista ligada con centinela. Recorre los nodos a partir del
    primer nodo con datos (el siguiente del centinela) hasta el final de la lista.
    """

    def __init__(self, centinela: Nodo):
        """
        Constructor del iterador.
        :param centinela: El nodo centinela de la lista a recorrer
        """
        self.__actual = centinela.siguiente

    def __iter__(self) -> "IteradorLista":
        """
        Método que permite usar el iterador directamente en un ciclo for.
        :return: El propio iterador
        :rtype: IteradorLista
        """
        return self

    def hay_siguiente(self) -> bool:
        """
        Método que indica si aún quedan elementos por recorrer.
        :return: True si hay un siguiente elemento, False en otro caso
        :rtype: bool
        """
        return self.__actual is not None

    def __next__(self) -> Any:
        """
        Método que devuelve el siguiente elemento de la lista y avanza el iterador.
        :return: El siguiente dato de la lista
        :raises StopIteration: cuando ya no hay más elementos
        """
        if self.__actual is None:
            raise StopIteration
        dato = self.__actual.dato
        self.__actual = self.__actual.siguiente
        return dato


class Lista:
    """
    TAD Lista simplemente ligada con nodo centinela al inicio.

    El centinela es un nodo "vacío" que siempre existe y precede al primer
    elemento real. Gracias a él, insertar o eliminar al inicio no requiere
    casos especiales: todo nodo con datos tiene siempre un nodo anterior.
    Se mantiene además una referencia al último nodo para que agregar al final
    sea O(1), y un contador de elementos para que la longitud sea O(1).
    """

    def __init__(self, elementos: Optional[Iterable] = None):
        """
        Constructor de la lista.
        :param elementos: (Opcional) Iterable cuyos elementos se agregan, en orden,
                          a la nueva lista.
        """
        self.__centinela = Nodo()
        self.__ultimo = self.__centinela
        self.__nd = 0
        if elementos is not None:
            for elemento in elementos:
                self.agregar(elemento)

    # ------------------------------------------------------------------ consulta
    def esta_vacia(self) -> bool:
        """
        Método que indica si la lista no tiene elementos.
        :return: True si está vacía, False en otro caso
        :rtype: bool
        """
        return self.__centinela.siguiente is None

    def longitud(self) -> int:
        """
        Método que devuelve el número de elementos de la lista.
        :return: La cantidad de elementos almacenados
        :rtype: int
        """
        return self.__nd

    def __len__(self) -> int:
        """
        Permite usar len(lista).
        :return: La cantidad de elementos almacenados
        :rtype: int
        """
        return self.__nd

    def primero(self) -> Any:
        """
        Método que devuelve el primer elemento de la lista.
        :return: El primer elemento
        :raises IndexError: si la lista está vacía
        """
        if self.esta_vacia():
            raise IndexError("La lista está vacía")
        return self.__centinela.siguiente.dato

    def ultimo(self) -> Any:
        """
        Método que devuelve el último elemento de la lista.
        :return: El último elemento
        :raises IndexError: si la lista está vacía
        """
        if self.esta_vacia():
            raise IndexError("La lista está vacía")
        return self.__ultimo.dato

    def obtener(self, indice: int) -> Any:
        """
        Método que devuelve el elemento en la posición indicada (0 .. n-1).
        Recorre la lista desde el centinela, por lo que es O(n).
        :param indice: La posición del elemento
        :return: El elemento en esa posición
        :raises IndexError: si el índice está fuera de rango
        """
        if not isinstance(indice, int) or isinstance(indice, bool):
            raise TypeError("El índice debe ser un entero")
        if indice < 0:
            indice += self.__nd
        if indice < 0 or indice >= self.__nd:
            raise IndexError("Índice fuera de rango")
        actual = self.__centinela.siguiente
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato

    def __getitem__(self, indice: int) -> Any:
        """
        Permite usar la notación lista[i] (equivalente a obtener(i)).
        :param indice: La posición del elemento
        :return: El elemento en esa posición
        """
        return self.obtener(indice)

    def contiene(self, elemento: Any) -> bool:
        """
        Método que indica si el elemento se encuentra en la lista.
        :param elemento: El elemento a buscar
        :return: True si lo encuentra, False en otro caso
        :rtype: bool
        """
        for dato in self:
            if dato == elemento:
                return True
        return False

    def __contains__(self, elemento: Any) -> bool:
        """
        Permite usar el operador 'in'.
        :param elemento: El elemento a buscar
        :return: True si lo encuentra, False en otro caso
        """
        return self.contiene(elemento)

    # ------------------------------------------------------------- modificación
    def agregar(self, elemento: Any):
        """
        Método que agrega un elemento al final de la lista en O(1)
        (se usa la referencia al último nodo).
        :param elemento: El elemento a agregar
        """
        nuevo = Nodo(elemento)
        self.__ultimo.siguiente = nuevo
        self.__ultimo = nuevo
        self.__nd += 1

    def agregar_inicio(self, elemento: Any):
        """
        Método que agrega un elemento al inicio de la lista (justo después del
        centinela) en O(1).
        :param elemento: El elemento a agregar
        """
        nuevo = Nodo(elemento, self.__centinela.siguiente)
        self.__centinela.siguiente = nuevo
        if self.__ultimo is self.__centinela:
            self.__ultimo = nuevo
        self.__nd += 1

    def eliminar_si(self, condicion: Callable[[Any], bool], maximo: Optional[int] = None) -> int:
        """
        Método que elimina, en una sola pasada, los elementos que cumplen la condición.
        El recorrido se hace con un apuntador al nodo anterior que inicia en el
        centinela, por lo que eliminar el primer nodo no es un caso especial.
        :param condicion: Función que recibe un dato y devuelve True si se debe eliminar
        :param maximo: (Opcional) Número máximo de elementos a eliminar. Si es None, elimina todos
        :return: El número de elementos eliminados
        :rtype: int
        """
        eliminados = 0
        anterior = self.__centinela
        while anterior.siguiente is not None and (maximo is None or eliminados < maximo):
            actual = anterior.siguiente
            if condicion(actual.dato):
                anterior.siguiente = actual.siguiente
                if actual is self.__ultimo:
                    self.__ultimo = anterior
                self.__nd -= 1
                eliminados += 1
            else:
                anterior = actual
        return eliminados

    def eliminar(self, elemento: Any, maximo: Optional[int] = 1) -> int:
        """
        Método que elimina apariciones del elemento en la lista.
        :param elemento: El elemento a eliminar
        :param maximo: Número máximo de apariciones a eliminar (1 por omisión).
                       Si es None se eliminan todas las apariciones.
        :return: El número de elementos eliminados
        :rtype: int
        """
        return self.eliminar_si(lambda dato: dato == elemento, maximo)

    def vaciar(self):
        """
        Método que elimina todos los elementos de la lista. Basta con desconectar
        el centinela del resto de los nodos (el recolector de basura libera la memoria).
        """
        self.__centinela.siguiente = None
        self.__ultimo = self.__centinela
        self.__nd = 0

    # ---------------------------------------------------------------- recorrido
    def __iter__(self) -> IteradorLista:
        """
        Método que devuelve un nuevo iterador para recorrer la lista.
        Cada llamada crea un iterador independiente, así que se pueden
        anidar recorridos sobre la misma lista.
        :return: Un iterador de la lista
        :rtype: IteradorLista
        """
        return IteradorLista(self.__centinela)

    def __str__(self) -> str:
        """
        Método que devuelve la lista en formato cadena.
        :return: La lista como [e1, e2, ..., en]
        :rtype: str
        """
        return "[" + ", ".join(str(dato) for dato in self) + "]"


# Prueba rápida de la lista
if __name__ == "__main__":
    lista = Lista()
    print("¿Vacía?", lista.esta_vacia())
    for x in (3, 1, 4, 1, 5, 9, 2, 6):
        lista.agregar(x)
    lista.agregar_inicio(0)
    print("Lista:", lista, "| longitud:", len(lista))
    print("Elemento [3]:", lista[3])
    print("Eliminados (1, todas):", lista.eliminar(1, None), "->", lista)
    print("Contiene 9:", 9 in lista, "| Contiene 7:", 7 in lista)
    lista.vaciar()
    print("Tras vaciar:", lista, "| ¿Vacía?", lista.esta_vacia())
