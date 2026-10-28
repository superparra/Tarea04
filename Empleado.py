# Programa: Empleado.py
# Objetivo: Ilustrar el uso de Herencia simple a través de la clase Persona
# Autor: Gerardo
# Fecha: 19-07-2024

import Persona as p
from datetime import date, datetime
from locale import currency, setlocale, LC_MONETARY


class Empleado(p.Persona):
    def __init__(self, nombre: str, apellidos: str, nacimiento: date, email: str, num_emp: int, salario: float):
        """
        Constructor para un Empleado, además de los datos de una Persona, recibe el número de empleado
        y el salario.
        :param nombre: El nombre del Empleado
        :param apellidos: Los apellidos del Empleado
        :param nacimiento: La fecha de nacimiento del Empleado
        :param email: EL correo electrónico del Empleado
        :param num_emp: El número de empleado
        :param salario: El salario del Empleado
        """
        super().__init__(nombre, apellidos, nacimiento, email)
        self.__num_emp = num_emp if num_emp < 0 else abs(num_emp)
        self.__salario = salario if salario >= 1000 else 1000

    # Métodos GET
    @property
    def num_emp(self) -> int:
        """
        Método para obtener el número de empleado
        :return: El número de Empleado
        :rtype: int
        """
        return self.__num_emp

    @property
    def salario(self) -> float:
        """
        Método para obtener el salario del empleado
        :return: El salario del Empleado
        :rtype: float
        """
        return self.__salario

    # Métodos SET
    @num_emp.setter
    def num_emp(self, num_emp: int):
        """
        Método para establecer el número de empleado
        :param num_emp: El número de empleado
        """
        self.__num_emp = num_emp if num_emp < 0 else abs(num_emp)

    @salario.setter
    def salario(self, salario: float):
        """
        Método para establecer el salario del empleado
        :param salario: El salario del empleado
        """
        self.__salario = salario if salario >= 1000 else 1000

    # Métodos calculadores
    def __str__(self) -> str:
        """
        Método para obtener un Empleado en formato cadena
        :return: El Empleado en formato de impresión
        :rtype: str
        """
        setlocale(LC_MONETARY, "en_US")
        return super().__str__().replace("Persona", "Empleado") + \
            " | Num_emp: {} | Salario: {}".format(self.__num_emp, currency(self.__salario, grouping=True))

    # Este método se definen cuando se desea que los objetos se guarden en un archivo
    def __iter__(self):
        """
        Método que devuelve una representación iterable de un objeto
        :return: La representación en formato iterable del Empleado
        :rtype: iterable
        """
        return iter([super().nombre, super().apellidos, super().nacimiento, super().email,
                     self.__num_emp, self.__salario])

    # Estos métodos se tienen que agregar cuando se trabajan con objetos en los Conjuntos y lograr
    # que sus objetos sean hasheables
    def __llave(self) -> tuple:
        """
        Método privado que permite definir una llave a través de los atributos del objeto
        :return: Una tupla con los atributos del objeto.
        :rtype: tuple
        """
        return super().nombre, super().apellidos, super().nacimiento, super().email, self.__num_emp, self.__salario

    def __hash__(self) -> int:
        """
        Método que internamente llama la función hash() para obtener el valor hash del objeto.
        Se utilizan generalmente para una comparación más rápida entre los dos objetos,
        ya que los valores hash se comparan directamente en lugar de comparar el valor de cada objeto.
        :return: Un valor entero que corresponde al valor hash del objeto
        :rtype: int
        """
        return hash(self.__llave())

    def __eq__(self, otro) -> bool:
        """
        Método que permite definir el criterio de igualdad para dos objetos
        :param otro: El Empleado con la que se va a realizar la comparación
        :return: True si los Empleados son iguales, False en caso contrario
        :rtype: bool
        """
        if isinstance(otro, Empleado):
            return self.__llave() == otro.__llave()

    def __gt__(self, otro) -> bool:
        """
        Este método se utiliza para dos Empleados y determinar
        el primero es "mayor" que el segundo.
        :param otra: El Empleado con la que se va a realizar la comparación
        :return: True si el empleado actual es mayor que otro, False en caso contrario
        :rtype: bool
        """
        if isinstance(otro, Empleado):
            return self.edad() > otro.edad()
            """
            if self.edad() - otro.edad() == 0:
                fullname1 = self.nombre + " " + self.apellidos
                fullname2 = otro.nombre + " " + otro.apellidos
                return fullname1 > fullname2
            else:
                return self.edad() > otro.edad()
            """


# Probar la clase Empleado
if __name__ == "__main__":
    # Utilizando el constructor por parámetros
    nombre = input("Escribe el nombre: ")
    apellidos = input("Escribe los apellidos: ")
    nacimiento = input("Escribe la fecha de nacimiento (dd/mm/aaaa): ")
    # Convertir str a date
    nacimiento = datetime.strptime(nacimiento, "%d/%m/%Y").date()
    email = input("Escribe el correo electrónico: ")
    num_emp = int(input("Escribe el número de empleado: "))
    salario = float(input("Escribe el salario del empleado: "))
    empleado = Empleado(nombre, apellidos, nacimiento, email, num_emp, salario)
    print(empleado)