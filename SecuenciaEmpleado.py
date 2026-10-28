# Programa: SecuenciaEmpleado.py
# Objetivo: Mostrar la implementación de la "interdaz" Conjuntable, pata ilustrar la creacón de un TAD de objetos.
# Autor: Huitzilovers2.0
# Fecha: 03/09/2026

import Secuenciable as s
import Empleado as e
import numpy as np
from numpy.typing import NDArray

class Secuencia(s.Secuenciable):
    def __init__(self,*params):
        """
        Constructor de la secuencia
        :param params: Si no recib nada el
        :return: Si no recibe nada es el constructor por omisión.
                 Sí recibe un parámetro, es el constructor por parámetros.
        """
        if len(params) == 0: #constructor por omisión
            self.__datos=np.empty(20,dtype=e.Empleado)
            self.__nd = 0
            print("Se creo una Secuencia para 20 elemntos!")

        elif len(params) == 1:
            if not isinstance(params[0], int) or isinstance(params[0], bool) or params[0] < 1:
                raise ValueError("El tamaño del arreglo debe ser un entero positivo")
            self.__datos = np.empty(params[0], dtype=e.Empleado)
            self.__nd = 0

        else:
            raise TypeError("El constructor recibe 0 o 1 parámetros")

    def __iter__(self):
        """
        Método que permite inicializar el iterador de Secuencias
        :return: Un objeto iterable
        """
        self.pos = 0
        return self

    def __next__(self)-> e.Empleado:
        """
        Método que permite obtener el siguiete elmento de la Secuencia
        :return: El siguiente elemento de la Secuencia
        :rtype: int
        """
        if self.pos < self.nd:
            a = self.datos[self.pos]
            self.pos += 1
            return a
        else:
            raise StopIteration

    @property
    def datos(self) -> NDArray[e.Empleado]:
        """
        Metodo GET para obtener el arreglo de datos
        :return: Empleado[]
        """
        return self.__datos
    @property
    def nd(self)-> int :
        """
        Método GET para obtener el número de datos del conjunto
        :return: El número de datos insertados en el Conjunto
        :retype: int
        """
        return self.__nd

    def __crecer(self, minimo: int):
        """
        Duplica la capacidad del arreglo hasta que quepan 'minimo' elementos.
        :param minimo: Cantidad mínima de elementos que debe poder almacenar
        """
        cap = len(self.__datos)
        if minimo <= cap:
            return
        cap = max(cap, 1)
        while cap < minimo:
            cap *= 2
        nuevo = np.empty(cap, dtype=e.Empleado)
        for i in range(self.__nd):
            nuevo[i] = self.__datos[i]
        self.__datos = nuevo

    def agregar(self, elemento: e.Empleado, nveces: int = 1):
        """
        Agrega el elemento 'nveces' veces (por omisión, una).
        :raises TypeError: si el elemento no es un Empleado
        :raises ValueError: si nveces no es un entero positivo
        """
        if not isinstance(elemento, e.Empleado):
            raise TypeError("Solo se pueden agregar objetos Empleado")
        if not isinstance(nveces, int) or isinstance(nveces, bool) or nveces < 1:
            raise ValueError("nveces debe ser un entero positivo")
        self.__crecer(self.__nd + nveces)
        for _ in range(nveces):
            self.__datos[self.__nd] = elemento
            self.__nd += 1


    def eliminar(self, elemento: e.Empleado, nrep: int | None = None):
        """
        Sin nrep: elimina todas las repeticiones del elemento.
        Con nrep: elimina nrep repeticiones; si hay menos de nrep, no hace nada.
        :raises TypeError: si el elemento no es un Empleado
        :raises ValueError: si nrep no es un entero positivo
        """
        if not isinstance(elemento, e.Empleado):
            raise TypeError("Solo se pueden eliminar objetos Empleado")
        if nrep is not None and (not isinstance(nrep, int) or isinstance(nrep, bool) or nrep < 1):
            raise ValueError("nrep debe ser un entero positivo")
        total = self.repeticiones(elemento)
        if total == 0 or (nrep is not None and total < nrep):
            return
        por_quitar = total if nrep is None else nrep
        j = 0
        quitados = 0
        for i in range(self.__nd):  # Compacta el arreglo en una sola pasada
            if quitados < por_quitar and self.__datos[i] == elemento:
                quitados += 1
            else:
                self.__datos[j] = self.__datos[i]
                j += 1
        for k in range(j, self.__nd):  # Libera las posiciones sobrantes
            self.__datos[k] = None
        self.__nd = j

    def contiene(self, elemento: e.Empleado) -> bool:
        """
        Indica si el elemento está en la Secuencia.
        :return: True si lo encontró, False en otro caso
        :rtype: bool

        """
        for i in range(self.__nd):
            if self.__datos[i] == elemento:
                return True
        return False

    def repeticiones(self, elemento: e.Empleado) -> int:
        """
        Cuenta cuántas veces aparece el elemento en la Secuencia.
        :return: El número de repeticiones
        :rtype: int
        """
        cuenta = 0
        for i in range(self.__nd):
            if self.__datos[i] == elemento:
                cuenta += 1
        return cuenta

    # Función que verifica si nuestra secuencia es vacía
    def esta_vacia(self) -> bool:
        """
        Método que Verifica si la secuencia está vacía
        :return: True si está vacía, False en caso contrario
        :rtype: bool
        """
        return self.__nd == 0

    # Función que devuelve la cardinalidad de la secuencia
    def cardinalidad(self) -> int:
        """
        Método que que permite conocer la cardinalidad de la secuencia
        :return: La cantidad de elementos almacenados en la Secuencia (incluyendo repeticiones)
        :rtype: int
        """
        return self.__nd

    # Función que permite vaciar la secuencia
    def vaciar(self):
        """
        Método que permite eliminar todos los elementos de la secuencia, reiniciando el arreglo
        :return: Una secuencia vacía
        """
        capacidad_actual = len(self.__datos)
        self.__datos = np.empty(capacidad_actual, dtype=e.Empleado)
        self.__nd = 0

    # Función que crea una secuencia unica
    def secuencia_unica(self):
        """
        Método que permite crear y devolver una secuencia con elementos unicos (sin repeticiones)
        :return: Nueva secuencia sin elementos repetidos
        """
        # Se crea con la capacidad del número de elementos actuales o 20 por omisión
        capacidad_inicial = self.__nd if self.__nd > 0 else 20
        secu_unica = Secuencia(capacidad_inicial)
        for i in range(self.__nd):
            elemento = self.__datos[i]
            # Utiliza el método contiene
            if not secu_unica.contiene(elemento):
                secu_unica.agregar(elemento)
        return secu_unica

    # Función que permite ordenar una secuencia.
    def ordenar(self, comparador=None):
        """
        Método que devuelve la Secuencia de elementos de manera ordenada.
        Utiliza Quick Sort o Merge Sort y habilita la existencia de dos comparadores
        :return: La secuencia ordenada
        :rtype: np.ndarray
        """
        if self.esta_vacia():
            return np.empty(0, dtype=e.Empleado)
        # Criterio por defecto si no se pasa ningún comparador
        if comparador is None:
            comparador = Secuencia.nombre_salario
        # Tomamos unicamente a los elementos activos, es decir del self.__nd, para no evitar comparar con posiciones vacias
        copia = self.__datos[:self.__nd].copy()
        return Secuencia.__quick_sort(copia, 0, self.__nd - 1, comparador)

    # Método str que imprime en formato cadena los elementos de una secuencia
    def __str__(self):
        """
        Método que devuelve la representación en formato str de la secuencia
        :return: Cadena con la lista de elementos activos
        :rtype: str
        """
        if self.esta_vacia():
            return "[]"
        elementos_str = [str(self.__datos[i]) for i in range(self.__nd)]
        return "[" + ", ".join(elementos_str) + "]"

    # Método eq que compara una secuencia con otra
    def __eq__(self, otro) -> bool:
        """
        Método que compara si dos secuencias son iguales.
        Al ser un multiconjunto, dos secuencias son iguales si tienen la misma cardinalidad y las mismas repeticiones.
        :param otro: Objeto con el cual se va a comparar
        :return: True si son equivalentes, False en caso contrario
        :rtype: bool
        """
        if not isinstance(otro, s.Secuenciable):
            return False
        if self.cardinalidad() != otro.cardinalidad():
            return False
        unicos = self.secuencia_unica()
        for i in range(unicos.nd):
            elemento = unicos.datos[i]
            if self.repeticiones(elemento) != otro.repeticiones(elemento):
                return False
        return True

    # Comparadores para el ordenamiento
    @staticmethod
    def __compare_strings(str1: str, str2: str) -> int:
        """
        Método privado para comparar dos cadena y devolver su relación de orden en términos de un int
        :param str1: Primera cadena a comparar
        :param str2: Segunda cadena a comparar
        :return: -1 si str1 lexicográficamente es menor que str2, 0 si son iguales, 1 en otro caso
        """
        if str1 < str2:
            return -1
        elif str1 > str2:
            return 1
        else:
            return 0

    @staticmethod
    def nombre_salario(a,b):
        """
        Método para determinar la relacion de objetos con respecto al salario y nombre
        :param a: El primer objeto a comparar
        :param b: El segundo objeto a comparar
        :return: Valor positivo si el salario de a es mayor que b, negativo si el salario de
             b es mayo que a. Si es el mismo salario, regresa la relación de orden de los
             Empleados con respecto al orden natura de las cadenas.
        """
        dif_sueldo= a.salario- b.salario
        if dif_sueldo ==0:
            fullname1 = a.nombre + " " + a.apellidos
            fullname2 = b.nombre + " " + b.apellidos
            return Secuencia.__compare_strings(fullname1,fullname2)
        else:
            return dif_sueldo

    @staticmethod
    def edad(a, b):
        """
        Metodo para determinar la relacion de objetos con respecto a la edad
        :param a: El primer objeto a comparar
        :param b: El segundo objeto a comparar
        :return:Valor positivo si la edad de a es menor que b, cero si son iguales,
             negativo en otro caso
        """
        return a.edad() - b.edad()

    @staticmethod
    def __particion(arreglo, inicio: int, fin: int, comparador) -> int:
        """
        Este metodo organizata los contactos del arreglo de manera que todos los elementos
        menores o iguales al pivote estén a la izquierda y todos los elementos mayores estén
        a la derecha.El pivote se coloca en su posición correcta.
        :param inicio: La posición inicial
        :param fin: La posición final
        :param comparador: El comparador con el que se desea hacer el ordenamiento
        :retype: int
        """
        pivote = arreglo[inicio]
        left = inicio + 1
        right = fin
        while True:
            while left <= right and comparador(arreglo[left], pivote) <= 0:
                left += 1
            while comparador(arreglo[right], pivote) > 0 and right >= left:
                right -= 1
            if right < left:
                break
            else:
                arreglo[left], arreglo[right] = arreglo[right], arreglo[left]

        arreglo[inicio], arreglo[right] = arreglo[right], arreglo[inicio]
        return right

    @staticmethod
    def __quick_sort(arreglo, inicio: int, fin: int, comparador) -> np.ndarray:
        """
        Este metodo aplica recursivamente el algoritmo quick sort a los subarreglos definidos por el pivote
        :param inicio: La posicion inicial
        :param fin: La posicion final
        :param comparador:El comparador con el que se desea hacer el ordenamiento
        :return: Arreglo ordenado
        :rtype NDArray[]
        """
        if inicio < fin:
            posicion_part = Secuencia.__particion(arreglo, inicio, fin, comparador)
            Secuencia.__quick_sort(arreglo, inicio, posicion_part - 1, comparador)
            Secuencia.__quick_sort(arreglo, posicion_part + 1, fin, comparador)
        return arreglo

    # Posibles cambios aun tengo duda
    #def ordenar(self,comparador)-> np.ndarray:
    #    copia = self.datos.copy()
    #    return Secuencia.__quick_sort(copia,0,self.nd-1,comparador)
