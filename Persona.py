# Programa: Persona.py
# Objetivo: Clase que modela una Persona, se incluyen funciones para fechas
# Autor: Ger
# Fecha: 13-07-2024

from datetime import date, datetime
from validate_email import validate_email


class Persona:
    def __init__(self, *params):
        """
        Constructor que permite crear diferentes objetos Persona
        :param params: Lista variable de parámetros (0, n)
        """
        if len(params) == 0:  # Constructor por omisión
            self.__nombre = "Juan"
            self.__apellidos = "Martínez Sánchez"
            self.__nacimiento = date(1990, 7, 23)
            self.__email = "jmartinez@gmail.com"
        elif len(params) == 4:  # Constructor por parámetros
            self.__nombre = params[0]
            self.__apellidos = params[1]
            self.__nacimiento = params[2]
            self.__email = params[3] \
                if validate_email(params[3]) else "usuario@domino.com"

    # Agregar métodos GET
    @property
    def nombre(self):
        """
        Método para obtener el nombre de la Persona
        :return: El nombre de la Persona
        :rtype: str
        """
        return self.__nombre

    @property
    def apellidos(self):
        """
        Método para obtener los apellidos de la Persona
        :return: Los apellidos de la Persona
        :rtype: str
        """
        return self.__apellidos

    @property
    def nacimiento(self):
        """
        Método para obtener la fecha de nacimiento de la Persona
        :return: La fecha de nacimiento de la Persona
        :rtype: str
        """
        return self.__nacimiento

    @property
    def email(self):
        """
        Método para obtener el correo de la Persona
        :return: El correo de la Persona
        :rtype: str
        """
        return self.__email

    # Métodos SET
    @nombre.setter
    def nombre(self, nombre: str):
        """
        Método para modificar el nombre de la Persona
        :param nombre: El nombre de la Persona
        """
        self.__nombre = nombre

    @apellidos.setter
    def apellidos(self, apellidos: str):
        """
        Método para modificar los apellidos de la Persona
        :param apellidos: Los apellidos de la Persona
        """
        self.__apellidos = apellidos

    @nacimiento.setter
    def nacimiento(self, nacimiento: str):
        """
        Método para modificar la fecha de nacimiento de la Persona
        :param nacimiento: La fecha de nacimiento de la Persona
        """
        self.__nacimiento = nacimiento

    @email.setter
    def email(self, email: str):
        """
        Método para modificar el correo de la Persona
        :param email: El correo de la Persona
        """
        if validate_email(email):  # Si devuelve True, el correo es válido
            self.__email = email
        else:  # El correo no es válido y se define un correo genérico
            print("El correo no es válido!\n"
                  "Se definió el correo: usuario@dominio.com")
            self.__email = "usuario@dominio.com"

    # Métodos calculadores

    def edad(self):
        """
        Método para calcular la edad de una Persona
        :return: La edad de la Persona en años
        :rtype: int
        """
        hoy = date.today()  # Fecha actual
        diferencia_dias = hoy - self.__nacimiento
        edad = diferencia_dias.days // 365.25
        return int(edad)

    def __str__(self):
        """
        Método que permite definir una persona en formato cadena
        :return: La Persona en formato str
        :rtype: str
        """
        return ("Persona:: {} {} | Nacimiento: {} | "
                "Email: {} | Edad: {}").format(self.__nombre,
                                               self.__apellidos,
                                               self.__nacimiento.strftime("%d/%m/%Y"),
                                               self.__email,
                                               self.edad()
                                               )

    # Este método se definen cuando se desea que los objetos se guarden en un archivo
    def __iter__(self):
        """
        Método que devuelve una representación iterable de un objeto
        :return: La representación en formato Lista de las Personas
        :rtype: iterable
        """
        return iter([self.__nombre, self.__apellidos, self.__nacimiento, self.__email])

    # Estos métodos se tienen que agregar cuando se trabajan con objetos en los Conjuntos y lograr
    # que sus objetos sean hasheables
    def __llave(self) -> tuple:
        """
        Método privado que permite definir una llave a través de los atributos del objeto
        :return: Una tupla con los atributos del objeto.
        :rtype: tuple
        """
        return self.__nombre, self.__apellidos, self.__nacimiento, self.__email

    def __hash__(self) -> int:
        """
        Método que internamente llama la función hash() para obtener el valor hash del objeto.
        Se utilizan generalmente para una comparación más rápida entre los dos objetos,
        ya que los valores hash se comparan directamente en lugar de comparar el valor de cada objeto.
        :return: Un valor entero que corresponde al valor hash del objeto
        :rtype: int
        """
        return hash(self.__llave())

    def __eq__(self, otra) -> bool:
        """
        Método que permite definir el criterio de igualdad para dos objetos
        :param otra: La Persona con la que se va a realizar la comparación
        :return: True si las Personas son iguales, False en caso contrario
        :rtype: bool
        """
        if isinstance(otra, Persona):
            return self.__llave() == otra.__llave()


# Probar la clase Persona
if __name__ == "__main__":
    per1 = Persona()  # Creamos la Persona por omisión
    print(per1)  # La mostramos
    per2 = Persona()
    print(per2)
    # Utilizando el constructor por parámetros
    nombre = input("Escribe el nombre: ")
    apellidos = input("Escribe los apellidos: ")
    nacimiento = input("Escribe la fecha de nacimiento (dd/mm/aaaa): ")
    # Convertir str a date
    nacimiento = datetime.strptime(nacimiento, "%d/%m/%Y").date()
    email = input("Escribe el correo electrónico: ")
    per3 = Persona(nombre, apellidos, nacimiento, email)
    print(per3)
    per3.email = input("Escribe el correo electrónico: ")
    print(per3)


