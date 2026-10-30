#Programa: Listaordenada.py
# Objetivo: Lista ligada con centinela que mantiene sus elementos ordenados según un comparador.
# Reutiliza Nodo e IteradorLista de ListaCentinela.py (Integrante 1).
# Huitzilovers2.0 - Integrante 2 (Enzo Olvera González)


from typing import Any, Callable
from ListaCentinela import Lista


class ListaOrdenada(Lista):
    """
    Lista simplemente ligada con centinela que mantiene sus elementos ordenados
    de acuerdo con un comparador. Hereda todo de Lista (iterador, longitud, eliminar,
    contiene, etc.); lo único que cambia es la forma de agregar.
    """

    def __init__(self, comparador: Callable[[Any, Any], float]):
        """
        Constructor de la lista ordenada.
        :param comparador: Función f(a, b) que devuelve un valor negativo si a, va antes
                           que b, cero si son equivalentes y positivo si a, va después
        """
        super().__init__()
        self.__comparador = comparador

    def agregar(self, elemento: Any):
        """
        Método que agrega un elemento en la posición que le corresponde según el
        comparador. Si ya hay elementos equivalentes, el nuevo queda después de ellos.
        Se recorre la lista con su iterador y se reconstruye con los métodos de Lista,
        colocando el nuevo elemento antes del primero que sea mayor que él.
        :param elemento: El elemento a agregar
        """
        existentes = [dato for dato in self]  # recorrido con el iterador
        self.vaciar()
        colocado = False
        for dato in existentes:
            if not colocado and self.__comparador(dato, elemento) > 0:
                super().agregar(elemento)
                colocado = True
            super().agregar(dato)
        if not colocado:
            super().agregar(elemento)
