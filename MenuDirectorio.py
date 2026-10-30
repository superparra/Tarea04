# Programa: MenuDirectorio.py
# Objetivo: Menú interactivo del Directorio Escolar: menú de inicio (blanco o
# desde archivo) y visualización ordenada con Lista Ordenada e iteradores.
# Integrante 2 - Tarea 4

from ListaOrdenada import ListaOrdenada
from Directorio import Directorio
from MenuSecuenciaEmp import cargar_desde_archivo as cargar_desde_csv   # Integrante 3
from MenuSecuenciaEmp import guardar_al_salir as guardar_persistente    # Integrante 3


# ==============================================================================
# COMPARADORES
# ==============================================================================

def _comparar(a, b) -> int:
    """
    Compara dos valores y devuelve -1, 0 o 1.
    :param a: Primer valor
    :param b: Segundo valor
    :return: Negativo si a va antes que b, cero si son iguales, positivo si va después
    """
    return (a > b) - (a < b)


def comparar_por_nombre(a, b) -> int:
    """
    Comparador de contactos por nombre y, en caso de empate, por apellidos
    (sin distinguir mayúsculas).
    :param a: Primer contacto
    :param b: Segundo contacto
    :return: Valor negativo, cero o positivo según el orden
    """
    r = _comparar(a.nombre.lower(), b.nombre.lower())
    return r if r != 0 else _comparar(a.apellidos.lower(), b.apellidos.lower())


def comparar_por_apellidos(a, b) -> int:
    """
    Comparador de contactos por apellidos y, en caso de empate, por nombre
    (sin distinguir mayúsculas).
    :param a: Primer contacto
    :param b: Segundo contacto
    :return: Valor negativo, cero o positivo según el orden
    """
    r = _comparar(a.apellidos.lower(), b.apellidos.lower())
    return r if r != 0 else _comparar(a.nombre.lower(), b.nombre.lower())


def comparar_por_email(a, b) -> int:
    """
    Comparador de contactos por correo electrónico (sin distinguir mayúsculas).
    :param a: Primer contacto
    :param b: Segundo contacto
    :return: Valor negativo, cero o positivo según el orden
    """
    return _comparar(a.email.lower(), b.email.lower())


# ==============================================================================
# VISUALIZACIÓN
# ==============================================================================

def imprimir_encabezado(titulo: str):
    """
    Muestra un encabezado en consola.
    :param titulo: Texto del encabezado
    """
    print("\n" + "=" * 60)
    print(f" {titulo.upper()}")
    print("=" * 60)


def mostrar_directorio(directorio: Directorio):
    """
    Muestra los contactos en el orden en que están almacenados,
    recorriendo el directorio con su iterador.
    :param directorio: Directorio a mostrar
    """
    imprimir_encabezado("Directorio (sin ordenar)")
    total = 0
    for total, contacto in enumerate(directorio, start=1):  # iterador del directorio
        print(f" [{total:02d}] {contacto}")
    if total == 0:
        print(" (El directorio no tiene contactos)")


def mostrar_ordenado(directorio: Directorio, comparador) -> int:
    """
    Muestra el directorio ordenado. Recorre el directorio con su iterador,
    inserta cada contacto en una Lista Ordenada y luego recorre esa lista,
    también con su iterador, para imprimir.
    :param directorio: Directorio a mostrar
    :param comparador: Función f(a, b) que define el criterio de orden
    :return: Cantidad de contactos mostrados
    """
    ordenada = ListaOrdenada(comparador)
    for contacto in directorio:                 # iterador del directorio
        ordenada.agregar(contacto)

    total = 0
    for total, contacto in enumerate(ordenada, start=1):  # iterador de la lista ordenada
        print(f" [{total:02d}] {contacto}")
    if total == 0:
        print(" (El directorio no tiene contactos)")
    return total


def opcion_mostrar_ordenado(directorio: Directorio):
    """
    Submenú que pide el criterio de ordenamiento y muestra el directorio ordenado.
    :param directorio: Directorio a mostrar
    """
    imprimir_encabezado("Directorio ordenado")
    print(" 1. Por nombre")
    print(" 2. Por apellidos")
    print(" 3. Por correo electrónico")
    criterios = {
        "1": comparar_por_nombre,
        "2": comparar_por_apellidos,
        "3": comparar_por_email,
    }
    opc = input(" Elija un criterio [1/2/3]: ").strip()
    if opc not in criterios:
        print(" [Error]: Criterio no válido.")
        return
    print("-" * 60)
    mostrar_ordenado(directorio, criterios[opc])


# ==============================================================================
# MENÚ DE INICIO Y MENÚ PRINCIPAL
# ==============================================================================

def menu_inicio() -> tuple:
    """
    Pregunta al usuario cómo desea comenzar: con un directorio en blanco o
    cargando los contactos desde un archivo CSV.
    :return: Tupla (directorio, ruta_origen). ruta_origen es None si se
             comenzó en blanco, o el nombre del archivo si se cargaron datos.
    """
    while True:
        imprimir_encabezado("¿Cómo desea comenzar?")
        print(" 1. Directorio en blanco (sin contactos)")
        print(" 2. Cargar datos desde un archivo CSV")
        opcion = input(" Elija una opción [1/2]: ").strip()
        if opcion == "1":
            return Directorio(), None
        if opcion == "2":
            ruta = input(" Nombre del archivo: ").strip()
            if not ruta:
                print(" [Error]: El nombre no puede estar vacío.")
                continue
            directorio = Directorio()
            try:
                cargar_desde_csv(ruta, directorio)   # Integrante 3
                return directorio, ruta
            except FileNotFoundError:
                print(f" [Error]: No se encontró '{ruta}'. Intente de nuevo.")
            except Exception as err:
                print(f" [Error al leer el archivo]: {err}")
        else:
            print(" [Error]: Opción no válida.")


def mostrar_menu():
    """Despliega las opciones del menú principal del Directorio."""
    imprimir_encabezado("Directorio Escolar")
    print(" [1] Mostrar directorio (sin ordenar)")
    print(" [2] Mostrar directorio ordenado")
    # Integrante 1: agrega aquí agregar, buscar, actualizar y eliminar contactos
    print(" [0] Salir (guarda los cambios)")
    print("-" * 60)


def guardar_al_salir(directorio: Directorio, ruta_origen):
    """
    Guarda el directorio al terminar. Si se inició desde un archivo, lo
    actualiza; si se inició en blanco, pide el nombre del nuevo .csv.
    :param directorio: Directorio a guardar
    :param ruta_origen: Archivo de origen, o None si se inició en blanco
    """
    ruta = ruta_origen
    if ruta is None:
        ruta = input(" Nombre del archivo .csv donde guardar: ").strip()
        if not ruta.lower().endswith(".csv"):
            ruta += ".csv"
    guardar_persistente(directorio, ruta)        # Integrante 3: (coleccion, ruta)


def main():
    """Función principal: menú de inicio, ciclo del menú y guardado al salir."""
    directorio, ruta_origen = menu_inicio()

    while True:
        mostrar_menu()
        opcion = input(" Seleccione una opción: ").strip()
        if opcion == "0":
            guardar_al_salir(directorio, ruta_origen)
            print("\n ¡Hasta pronto!\n")
            break
        elif opcion == "1":
            mostrar_directorio(directorio)
        elif opcion == "2":
            opcion_mostrar_ordenado(directorio)
        # Integrante 1: agrega aquí los elif de sus opciones
        else:
            print(" [Error]: Opción no válida.")
        input("\n Presione [Enter] para continuar...")


if __name__ == "__main__":
    main()
