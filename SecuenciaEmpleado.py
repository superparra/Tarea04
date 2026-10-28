# Programa: SecuenciaEmpleado.py
# Objetivo: Mostrar la implementación de la "interdaz" Conjuntable, pata ilustrar la creacón de un TAD de objetos.
#           Tarea 4: el almacenamiento con arreglo de numpy (que se "hacía crecer" duplicando su
#           capacidad) se sustituyó por una lista simplemente ligada con centinela al inicio
#           (ListaCentinela.Lista), logrando una organización completamente dinámica.
# Autor: Huitzilovers2.0 (Tarea 4 - Integrante 1: Emiliano Parra Miranda)
# Fecha: 03/09/2026 (actualizado: 28/10/2026)

import Secuenciable as s
import Empleado as e
import ListaCentinela as lc
import numpy as np


class Secuencia(s.Secuenciable):
    """
    TAD Secuencia (multiconjunto) de objetos Empleado.

    Los elementos se almacenan en una lista simplemente ligada con nodo centinela
    al inicio, por lo que ya no existe una capacidad máxima: la Secuencia crece y
    decrece nodo por nodo. Todos los recorridos se hacen mediante el iterador de la lista.
    """

    def __init__(self, *params):
        """
        Constructor de la Secuencia.
        :param params: Si no recibe nada, es el constructor por omisión (Secuencia vacía).
                       Si recibe un parámetro, debe ser una Secuencia u otro iterable de
                       Empleados y funciona como constructor de copia.
        :raises TypeError: si el parámetro no es iterable, contiene objetos que no son
                           Empleado o se reciben más de un parámetro.
        """
        self.__datos = lc.Lista()
        if len(params) == 0:  # Constructor por omisión
            return
        if len(params) == 1:  # Constructor de copia
            origen = params[0]
            if isinstance(origen, (str, bytes)) or not hasattr(origen, "__iter__"):
                raise TypeError("El constructor recibe una Secuencia o un iterable de Empleados "
                                "(con listas ya no es necesario indicar una capacidad)")
            for elemento in origen:
                self.agregar(elemento)
        else:
            raise TypeError("El constructor recibe 0 o 1 parámetros")

    def __iter__(self) -> lc.IteradorLista:
        """
        Método que devuelve un iterador para recorrer la Secuencia.
        Se delega al iterador de la lista ligada; cada llamada crea un iterador
        nuevo e independiente, por lo que se permiten recorridos anidados.
        :return: Un iterador sobre los Empleados de la Secuencia
        :rtype: IteradorLista
        """
        return iter(self.__datos)

    @property
    def datos(self) -> lc.Lista:
        """
        Metodo GET para obtener la estructura de almacenamiento (lista ligada con centinela).
        La lista admite len(datos) y datos[i] (acceso O(n) recorriendo los nodos).
        :return: La lista ligada con los Empleados
        :rtype: Lista
        """
        return self.__datos

    @property
    def nd(self) -> int:
        """
        Método GET para obtener el número de datos de la Secuencia.
        :return: El número de datos insertados en la Secuencia
        :rtype: int
        """
        return self.__datos.longitud()

    def obtener(self, indice: int) -> e.Empleado:
        """
        Método que devuelve el Empleado en la posición indicada (0 .. nd-1).
        :param indice: Posición del Empleado
        :return: El Empleado en esa posición
        :raises IndexError: si el índice está fuera de rango
        """
        return self.__datos.obtener(indice)

    def agregar(self, elemento: e.Empleado, nveces: int = 1):
        """
        Agrega el elemento 'nveces' veces (por omisión, una) al final de la Secuencia.
        Cada inserción crea un nodo nuevo en O(1); ya no hay que copiar el arreglo.
        :param elemento: El Empleado a agregar
        :param nveces: El número de veces que se agrega
        :raises TypeError: si el elemento no es un Empleado
        :raises ValueError: si nveces no es un entero positivo
        """
        if not isinstance(elemento, e.Empleado):
            raise TypeError("Solo se pueden agregar objetos Empleado")
        if not isinstance(nveces, int) or isinstance(nveces, bool) or nveces < 1:
            raise ValueError("nveces debe ser un entero positivo")
        for _ in range(nveces):
            self.__datos.agregar(elemento)

    def eliminar(self, elemento: e.Empleado, nrep: int | None = None):
        """
        Sin nrep: elimina todas las repeticiones del elemento.
        Con nrep: elimina nrep repeticiones; si hay menos de nrep, no hace nada.
        Los nodos se desconectan en una sola pasada usando un apuntador al nodo
        anterior que inicia en el centinela (no hay que recorrer/compactar un arreglo).
        :param elemento: El Empleado a eliminar
        :param nrep: (Opcional) Número de repeticiones a eliminar
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
        self.__datos.eliminar(elemento, por_quitar)

    def actualizar(self, elemento: e.Empleado, nuevo: e.Empleado, nrep: int | None = None) -> int:
        """
        Actualiza (reemplaza) un Empleado de la Secuencia por otro, conservando su posición.
        Sin nrep: actualiza todas las repeticiones del elemento.
        Con nrep: actualiza nrep repeticiones; si hay menos de nrep, no hace nada
        (misma regla que eliminar).
        Se recorren los nodos de la lista y solo se cambia su dato.
        :param elemento: El Empleado que se desea actualizar
        :param nuevo: El Empleado con los datos actualizados
        :param nrep: (Opcional) Número de repeticiones a actualizar
        :return: El número de Empleados actualizados
        :rtype: int
        :raises TypeError: si elemento o nuevo no son Empleado
        :raises ValueError: si nrep no es un entero positivo
        """
        if not isinstance(elemento, e.Empleado) or not isinstance(nuevo, e.Empleado):
            raise TypeError("Solo se pueden actualizar objetos Empleado")
        if nrep is not None and (not isinstance(nrep, int) or isinstance(nrep, bool) or nrep < 1):
            raise ValueError("nrep debe ser un entero positivo")
        total = self.repeticiones(elemento)
        if total == 0 or (nrep is not None and total < nrep):
            return 0
        return self.__datos.reemplazar(elemento, nuevo, total if nrep is None else nrep)

    def contiene(self, elemento: e.Empleado) -> bool:
        """
        Indica si el elemento está en la Secuencia (recorrido con el iterador).
        :param elemento: El Empleado a buscar
        :return: True si lo encontró, False en otro caso
        :rtype: bool
        """
        for empleado in self:
            if empleado == elemento:
                return True
        return False

    def repeticiones(self, elemento: e.Empleado) -> int:
        """
        Cuenta cuántas veces aparece el elemento en la Secuencia (recorrido con el iterador).
        :param elemento: El Empleado a contar
        :return: El número de repeticiones
        :rtype: int
        """
        cuenta = 0
        for empleado in self:
            if empleado == elemento:
                cuenta += 1
        return cuenta

    # Función que verifica si nuestra secuencia es vacía
    def esta_vacia(self) -> bool:
        """
        Método que Verifica si la secuencia está vacía
        (el centinela no tiene siguiente).
        :return: True si está vacía, False en caso contrario
        :rtype: bool
        """
        return self.__datos.esta_vacia()

    # Función que devuelve la cardinalidad de la secuencia
    def cardinalidad(self) -> int:
        """
        Método que que permite conocer la cardinalidad de la secuencia
        :return: La cantidad de elementos almacenados en la Secuencia (incluyendo repeticiones)
        :rtype: int
        """
        return self.__datos.longitud()

    # Función que permite vaciar la secuencia
    def vaciar(self):
        """
        Método que permite eliminar todos los elementos de la secuencia.
        Con la lista basta con desconectar el centinela del primer nodo; ya no se
        crea un arreglo nuevo de la misma capacidad.
        """
        self.__datos.vaciar()

    # Función que crea una secuencia unica
    def secuencia_unica(self):
        """
        Método que permite crear y devolver una secuencia con elementos unicos (sin repeticiones)
        :return: Nueva secuencia sin elementos repetidos
        :rtype: Secuencia
        """
        secu_unica = Secuencia()  # Ya no se calcula una capacidad inicial
        for elemento in self:
            # Utiliza el método contiene
            if not secu_unica.contiene(elemento):
                secu_unica.agregar(elemento)
        return secu_unica

    # Función que permite ordenar una secuencia.
    def ordenar(self, comparador=None):
        """
        Método que devuelve la Secuencia de elementos de manera ordenada.
        Utiliza Quick Sort y habilita la existencia de dos comparadores.
        Como la lista no tiene acceso aleatorio, primero se vuelca (con el iterador)
        a un arreglo auxiliar de tamaño exacto y sobre él se aplica Quick Sort.
        (El Integrante 2 integra la Lista Ordenada del material para la visualización.)
        :param comparador: Función comparadora (por omisión, nombre_salario)
        :return: Arreglo con los Empleados ordenados
        :rtype: np.ndarray
        """
        if self.esta_vacia():
            return np.empty(0, dtype=e.Empleado)
        # Criterio por defecto si no se pasa ningún comparador
        if comparador is None:
            comparador = Secuencia.nombre_salario
        copia = np.empty(self.nd, dtype=e.Empleado)
        for i, empleado in enumerate(self):
            copia[i] = empleado
        return Secuencia.__quick_sort(copia, 0, self.nd - 1, comparador)

    # Método str que imprime en formato cadena los elementos de una secuencia
    def __str__(self):
        """
        Método que devuelve la representación en formato str de la secuencia
        :return: Cadena con la lista de elementos
        :rtype: str
        """
        return str(self.__datos)

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
        for elemento in self.secuencia_unica():
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
