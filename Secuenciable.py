# Programa: Secuenciable.py
# Objetivo: Clase abstracta que permite simular la interfaz para un TAD Secuencia
# Autor: Gerardo Avilés
# Version: 12-09-2024

from abc import abstractmethod, ABCMeta
from typing import TypeVar

T = TypeVar('T')


# Le cambié el nombre porque el profe le puso conjuntable y me estaba confundiendo
class Secuenciable(metaclass=ABCMeta):
    @abstractmethod
    def agregar(self, elemento: T):
        """
        Método que permite agregar un elemento a la Secuencia, siempre
        que sea posible.
        :param elemento: El elemento que se va a agregar a la Secuencia
        """
        pass

    @abstractmethod
    def agregar(self, elemento: T, nveces: int):
        """
        Método que permite agregar un elemento a la Secuencia, el número de
        veces indicado, siempreque sea posible.
        :param elemento: El elemento que se va a agregar a la Secuencia
        :param nveces: El número de veces que el elemento se agrega a la Secuencia
        """
        pass

    @abstractmethod
    def eliminar(self, elemento: T):
        """
        Método que permite eliminar todas las repeticiones del elemento dentro
        de la Secuencia, siempre que esto sea posible.
        :param elemento: El elemento a eliminar
        """
        pass

    @abstractmethod
    def eliminar(self, elemento: T, nrep: int):
        """
        Método que permite eliminar el número de repeticiones del elemento dentro
        de la Secuencia, indicadas por nrep, siempre que esto sea posible.
        Si el elemento no aparece al menos las repeticiones indicadas por nrep,
        no hace nada.
        :param elemento: El elemento a eliminar
        """
        pass

    @abstractmethod
    def contiene(self, elemento: T) -> bool:
        """
        Método que permite saber sí un elemento se encuentra contenido
        dentro de la Secuencia.
        :param elemento: El elemento a buscar
        :return: True si lo encontró, False en otro caso
        :rtype: bool
        """
        pass

    @abstractmethod
    def repeticiones(self, elemento: T) -> int:
        """
        Método que determina el número de repeticiones que el elemento
        presenta dentro de la Secuencia.
        :param elemento: El elemento a determinar las repeticiones
        :return: El número de veces que aparece en la Secuencia
        :rtype: int
        """
        pass

    @abstractmethod
    def esta_vacia(self) -> bool:
        """
        Método que permite saber sí la Secuencia está vacía.
        :return: True sí está vacía, False en otro caso.
        :rtype: bool
        """
        pass

    @abstractmethod
    def cardinalidad(self) -> int:
        """
        Método que permite conocer la cardinalidad de la Secuencia.
        :return: La cantidad de elementos almacenados en la Secuencia
        :rtype: int
        """
        pass

    @abstractmethod
    def vaciar(self):
        """
        Método que permite vaciar la Secuencia de elementos.
        """
        pass

    @abstractmethod
    def secuencia_unica(self):
        """
        Método que permite devuelve la Secuencia de elementos únicos
        (sin repeticiones).
        :return: La Secuencia sin repetidos
        """
        pass

    @abstractmethod
    def ordenar(self):
        """
        Método que permite devuelve la Secuencia de elementos ordenada.
        Utiliza Quick Sort o Merge Sort y habilita la existencia de dos comparadores
        por ejemplo, en el caso de los Empleados, se pueden ordenar por edad, por
        salario, por edad y nombre, salario y nombre, etc.
        :return: La Secuencia ordenada
        """
        pass