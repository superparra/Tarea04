# Programa: MenuSecuenciaEmp.py
# Objetivo: Menú interactivo de opciones para interactuar y evaluar el TAD Secuencia
#           con objetos Empleado, incluyendo carga/guardado de datos desde archivo
#           y recorrido mediante iterador (10 puntos extra).
# Autores: Integrante 3 e Integrante 4 (Tarea 3 - Manejo de Datos, Facultad de Ciencias, UNAM)
# Fecha: Octubre 2026

import os
import csv
from datetime import datetime, date
from typing import Optional, List
import numpy as np

import Empleado as e
import SecuenciaEmpleado as se

# ==============================================================================
# FUNCIONES AUXILIARES DE ENTRADA Y FORMATEO
# ==============================================================================

def limpiar_pantalla():
    """Limpia la consola si es posible o imprime una línea separadora."""
    print("\n" + "=" * 70)


def imprimir_encabezado(titulo: str):
    """Muestra un encabezado estilizado en consola."""
    print("\n" + "=" * 70)
    print(f"  {titulo.upper()}")
    print("=" * 70)


def capturar_cadena(mensaje: str, permitir_vacio: bool = False) -> str:
    """Solicita una cadena de texto al usuario con validación."""
    while True:
        valor = input(mensaje).strip()
        if valor or permitir_vacio:
            return valor
        print("  [Error]: El texto no puede estar vacío. Intente de nuevo.")


def capturar_entero(mensaje: str, positivo: bool = False, min_val: Optional[int] = None) -> int:
    """Solicita un número entero con validaciones de rango."""
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if positivo and valor <= 0:
                print("  [Error]: El número debe ser un entero positivo (mayor que 0).")
                continue
            if min_val is not None and valor < min_val:
                print(f"  [Error]: El número debe ser mayor o igual a {min_val}.")
                continue
            return valor
        except ValueError:
            print("  [Error]: Debe ingresar un número entero válido.")


def capturar_flotante(mensaje: str, min_val: Optional[float] = None) -> float:
    """Solicita un número flotante con validaciones de rango."""
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = float(entrada)
            if min_val is not None and valor < min_val:
                print(f"  [Error]: El valor debe ser mayor o igual a {min_val}.")
                continue
            return valor
        except ValueError:
            print("  [Error]: Debe ingresar un valor numérico válido.")


def capturar_fecha(mensaje: str) -> date:
    """Solicita una fecha admitiendo formato dd/mm/aaaa o aaaa-mm-dd."""
    formatos = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
    while True:
        entrada = input(mensaje).strip()
        for formato in formatos:
            try:
                dt = datetime.strptime(entrada, formato)
                return dt.date()
            except ValueError:
                continue
        print("  [Error]: Fecha inválida. Utilice el formato dd/mm/aaaa (ejemplo: 15/04/1990).")


def capturar_empleado() -> e.Empleado:
    """
    Solicita interactivamente todos los datos necesarios para instanciar un Empleado.
    :return: Nueva instancia de Empleado
    """
    print("\n--- Captura de datos del Empleado ---")
    nombre = capturar_cadena("  Nombre: ")
    apellidos = capturar_cadena("  Apellidos: ")
    nacimiento = capturar_fecha("  Fecha de nacimiento (dd/mm/aaaa): ")
    email = capturar_cadena("  Correo electrónico: ")
    num_emp = capturar_entero("  Número de empleado: ", positivo=True)
    salario = capturar_flotante("  Salario mensual (mínimo $1,000): ", min_val=1000.0)

    empleado = e.Empleado(nombre, apellidos, nacimiento, email, num_emp, salario)
    print("  [Éxito]: Empleado creado correctamente.")
    return empleado


def seleccionar_empleado(secuencia: se.Secuencia) -> Optional[e.Empleado]:
    """
    Permite al usuario elegir entre seleccionar un empleado ya existente
    en la secuencia (por número de índice) o capturar uno nuevo manualmente.
    """
    if secuencia.nd > 0:
        print("\n¿Cómo desea especificar el Empleado?")
        print("  1. Seleccionar de los empleados actualmente en la Secuencia")
        print("  2. Capturar datos de un nuevo Empleado")
        opc = input("  Elija opción [1/2] (por omisión 1): ").strip()
        if opc != "2":
            mostrar_elementos_secuencia(secuencia)
            idx = capturar_entero(
                f"  Ingrese el índice del empleado deseado (1 a {secuencia.nd}): ",
                min_val=1
            )
            if 1 <= idx <= secuencia.nd:
                return secuencia.datos[idx - 1]
            else:
                print("  [Error]: Índice fuera de rango. Se procederá a captura manual.")

    return capturar_empleado()


def mostrar_elementos_secuencia(secuencia: se.Secuencia):
    """Muestra los elementos de la secuencia numerados."""
    if secuencia.nd == 0:
        print("  (La secuencia no contiene elementos actualmente)")
        return
    print(f"\nTotal de elementos en la Secuencia: {secuencia.nd}")
    print("-" * 70)
    for i, emp in enumerate(secuencia, start=1):  # recorrido con el iterador de la lista
        print(f"  [{i:02d}] {emp}")
    print("-" * 70)


# ==============================================================================
# CARGA Y GUARDADO DE DATOS DESDE ARCHIVO (CSV / TEXTO PLANO)
# ==============================================================================

def cargar_desde_archivo(ruta: str, secuencia: se.Secuencia) -> int:
    """
    Lee un archivo de texto o CSV con registros de empleados y los agrega a la secuencia.
    El archivo debe contener columnas:
      nombre,apellidos,fecha_nacimiento,email,num_emp,salario
    Admite delimitadores ',' o ';', y fechas en 'dd/mm/aaaa' o 'aaaa-mm-dd'.
    
    :param ruta: Ruta al archivo en disco
    :param secuencia: Instancia de Secuencia a la que se agregarán los empleados
    :return: Cantidad de empleados cargados con éxito
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: '{ruta}'")

    cargados = 0
    omitidos = 0

    with open(ruta, mode="r", encoding="utf-8-sig") as f:
        # Detectar delimitador inspeccionando la primera línea
        primera_linea = f.readline()
        if not primera_linea:
            print("  [Aviso]: El archivo está vacío.")
            return 0
        f.seek(0)
        delimitador = ";" if ";" in primera_linea and "," not in primera_linea else ","

        lector = csv.reader(f, delimiter=delimitador)
        for num_linea, fila in enumerate(lector, start=1):
            if not fila or len(fila) < 6:
                continue

            # Saltar fila si es el encabezado
            if num_linea == 1 and ("nombre" in fila[0].lower() or "salario" in fila[-1].lower()):
                continue

            try:
                nombre = fila[0].strip()
                apellidos = fila[1].strip()
                nac_str = fila[2].strip()
                email = fila[3].strip()
                num_emp = int(fila[4].strip())
                salario = float(fila[5].strip())

                # Parsear fecha
                nacimiento = None
                for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
                    try:
                        nacimiento = datetime.strptime(nac_str, fmt).date()
                        break
                    except ValueError:
                        pass

                if nacimiento is None:
                    raise ValueError(f"Formato de fecha inválido '{nac_str}'")

                emp = e.Empleado(nombre, apellidos, nacimiento, email, num_emp, salario)
                secuencia.agregar(emp)
                cargados += 1
            except Exception as err:
                omitidos += 1
                print(f"  [Aviso]: Línea {num_linea} omitida debido a error: {err}")

    print(f"\n  Resumen de carga desde '{ruta}':")
    print(f"    - Empleados cargados con éxito: {cargados}")
    if omitidos > 0:
        print(f"    - Líneas con errores u omitidas: {omitidos}")
    print(f"    - Total actual en la Secuencia: {secuencia.nd}")
    return cargados


def guardar_en_archivo(ruta: str, secuencia: se.Secuencia) -> bool:
    """
    Exporta todos los empleados de la Secuencia a un archivo CSV utilizando el iterador.
    :param ruta: Ruta de destino
    :param secuencia: Instancia de Secuencia
    :return: True si se guardó exitosamente
    """

    with open(ruta, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f, delimiter=",")
        # Escribir encabezado
        escritor.writerow(["nombre", "apellidos", "nacimiento", "email", "num_emp", "salario"])
        
        # Recorrer mediante el iterador del TAD Secuencia
        total_escritos = 0
        for emp in secuencia:
            nac_str = emp.nacimiento.strftime("%d/%m/%Y")
            escritor.writerow([emp.nombre, emp.apellidos, nac_str, emp.email, emp.num_emp, emp.salario])
            total_escritos += 1

    print(f"  [Éxito]: Se guardaron {total_escritos} empleados en '{ruta}'.")
    return True

def pedir_nombre_csv() -> str:
    """
    Solicita al usuario el nombre del archivo .csv donde se guardarán los datos.
    Si el nombre no termina en '.csv', se le agrega la extension.
    :return: El nombre del archivo con extension .csv
    :rtype: str
    """
    nombre = capturar_cadena("  Nombre del archivo .csv donde se guardarán los datos: ")
    if not nombre.lower().endswith(".csv"):
        nombre += ".csv"
    return nombre


def guardar_al_salir(secuencia: se.Secuencia, archivo_origen: Optional[str] = None) -> Optional[str]:

    """
    Guarda automaticamente el directorio al terminar la ejecucion, recorriendo
    la lista con su iterador.
    Si el programa inició desde un archivo, se sobrescribe ese mismo archivo.
    Si inicio con un directorio en blanco, se pide el nombre del nuevo .csv.
    Si ademas el directorio quedo vacio, no hay nada que guardar.
    :param secuencia: La Secuencia (directorio) con los cambios de la sesion
    :param archivo_origen: Ruta del archivo con el que se inicio, o None si se inicio en blanco
    :return: La ruta donde se guardo, o None si no se guardo
    :rtype: str | None
    """
    if archivo_origen is None and secuencia.nd == 0:
        print("  [Aviso]: El directorio esta vacio y no se cargo ningun archivo, entonces no se guardo nada.")
        return None
    try:
        if archivo_origen is None:
            archivo_origen = pedir_nombre_csv()
        guardar_en_archivo(archivo_origen, secuencia)
        return archivo_origen
    except OSError as err:
        print(f"  [Error al guardar]: {err}")
        return None


# ==============================================================================
# OPCIONES ESPECÍFICAS DEL MENÚ INTERACTIVO
# ==============================================================================

def opcion_cargar_archivo(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 1: Cargar Secuencia desde Archivo (CSV / Texto)")
    archivo_defecto = "empleados.csv"
    print(f"Archivo por omisión en el directorio: '{archivo_defecto}'")
    ruta = input(f"Ingrese la ruta del archivo [Enter para usar '{archivo_defecto}']: ").strip()
    if not ruta:
        ruta = archivo_defecto

    try:
        cargar_desde_archivo(ruta, secuencia)
    except FileNotFoundError:
        print(f"  [Error]: El archivo '{ruta}' no fue encontrado.")
    except Exception as err:
        print(f"  [Error al leer el archivo]: {err}")


def opcion_agregar_uno(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 2: Agregar un Empleado (1 vez)")
    emp = capturar_empleado()
    try:
        secuencia.agregar(emp)
        print("  [Éxito]: Empleado agregado a la Secuencia satisfactoriamente.")
        print(f"  Cardinalidad actual: {secuencia.nd}")
    except Exception as err:
        print(f"  [Error al agregar]: {err}")


def opcion_agregar_nveces(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 3: Agregar un Empleado con n Repeticiones")
    emp = seleccionar_empleado(secuencia)
    nveces = capturar_entero("  Número de veces a agregar (nveces): ", positivo=True)
    try:
        secuencia.agregar(emp, nveces)
        print(f"  [Éxito]: Se agregó el empleado {nveces} vez/veces a la Secuencia.")
        print(f"  Cardinalidad actual: {secuencia.nd}")
    except Exception as err:
        print(f"  [Error al agregar]: {err}")


def opcion_eliminar_todo(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 4: Eliminar todas las repeticiones de un Empleado")
    if secuencia.nd == 0:
        print("  [Aviso]: La secuencia está vacía.")
        return
    emp = seleccionar_empleado(secuencia)
    rep_antes = secuencia.repeticiones(emp)
    print(f"  El empleado aparece {rep_antes} vez/veces en la secuencia.")
    try:
        secuencia.eliminar(emp)
        print("  [Éxito]: Se ejecutó eliminar(elemento).")
        rep_despues = secuencia.repeticiones(emp)
        print(f"  Repeticiones restantes del empleado: {rep_despues}")
        print(f"  Cardinalidad actual: {secuencia.nd}")
    except Exception as err:
        print(f"  [Error al eliminar]: {err}")


def opcion_eliminar_nrep(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 5: Eliminar n repeticiones de un Empleado")
    if secuencia.nd == 0:
        print("  [Aviso]: La secuencia está vacía.")
        return
    emp = seleccionar_empleado(secuencia)
    rep_antes = secuencia.repeticiones(emp)
    print(f"  El empleado cuenta actualmente con {rep_antes} repetición(es).")
    nrep = capturar_entero("  Ingrese el número de repeticiones a eliminar (nrep): ", positivo=True)
    try:
        secuencia.eliminar(emp, nrep)
        rep_despues = secuencia.repeticiones(emp)
        if rep_antes < nrep:
            print(f"  [Aviso]: Había {rep_antes} repeticiones, menos que nrep ({nrep}). La secuencia no fue modificada según la especificación.")
        else:
            print(f"  [Éxito]: Se eliminaron {nrep} repeticiones.")
        print(f"  Repeticiones actuales de este empleado: {rep_despues}")
        print(f"  Cardinalidad actual: {secuencia.nd}")
    except Exception as err:
        print(f"  [Error al eliminar]: {err}")


def opcion_contiene(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 6: Verificar si la Secuencia contiene un Empleado")
    if secuencia.nd == 0:
        print("  [Aviso]: La secuencia está vacía.")
        return
    emp = seleccionar_empleado(secuencia)
    try:
        encontrado = secuencia.contiene(emp)
        if encontrado:
            print("  -> RESULTADO: True. El empleado SÍ está contenido en la Secuencia.")
        else:
            print("  -> RESULTADO: False. El empleado NO se encuentra en la Secuencia.")
    except Exception as err:
        print(f"  [Error al verificar contiene]: {err}")


def opcion_repeticiones(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 7: Consultar Repeticiones de un Empleado")
    if secuencia.nd == 0:
        print("  [Aviso]: La secuencia está vacía.")
        return
    emp = seleccionar_empleado(secuencia)
    try:
        total = secuencia.repeticiones(emp)
        print(f"  -> RESULTADO: El empleado aparece {total} vez/veces en la Secuencia.")
    except Exception as err:
        print(f"  [Error al consultar repeticiones]: {err}")


def opcion_esta_vacia(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 8: Verificar si la Secuencia está Vacía (esta_vacia)")
    if hasattr(secuencia, "esta_vacia") and callable(getattr(secuencia, "esta_vacia")):
        try:
            resultado = secuencia.esta_vacia()
            print(f"  -> RESULTADO oficial esta_vacia(): {resultado}")
            return
        except NotImplementedError:
            print("  [Aviso]: El método esta_vacia() arrojó NotImplementedError.")
    
    # Manejo en espera de que Integrante 2 fusione su implementación
    print(f"  -> Diagnóstico actual (nd={secuencia.nd}): {'Vacía (True)' if secuencia.nd == 0 else 'No vacía (False)'}")


def opcion_cardinalidad(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 9: Consultar Cardinalidad de la Secuencia")
    if hasattr(secuencia, "cardinalidad") and callable(getattr(secuencia, "cardinalidad")):
        try:
            resultado = secuencia.cardinalidad()
            print(f"  -> RESULTADO oficial cardinalidad(): {resultado}")
            return
        except NotImplementedError:
            print("  [Aviso]: El método cardinalidad() arrojó NotImplementedError.")

    # Manejo en espera de que Integrante 2 fusione su implementación
    print(f"  -> Cardinalidad según contador de elementos (nd): {secuencia.nd}")


def opcion_vaciar(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 10: Vaciar la Secuencia (vaciar)")
    if hasattr(secuencia, "vaciar") and callable(getattr(secuencia, "vaciar")):
        try:
            secuencia.vaciar()
            print("  [Éxito]: Se ejecutó vaciar() en la Secuencia.")
            print(f"  Elementos actuales: {secuencia.nd}")
            return
        except NotImplementedError:
            print("  [Aviso]: El método vaciar() arrojó NotImplementedError.")



def opcion_secuencia_unica(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 11: Obtener Secuencia Única / Sin Repetidos")
    metodo = None
    for nombre in ("secuencia_unica", "secuencia_unico"):
        if hasattr(secuencia, nombre) and callable(getattr(secuencia, nombre)):
            metodo = getattr(secuencia, nombre)
            break

    if metodo is not None:
        try:
            unica = metodo()
            print("  [Éxito]: Secuencia única obtenida con éxito.")
            if isinstance(unica, se.Secuencia):
                mostrar_elementos_secuencia(unica)
            else:
                print(f"  Resultado devuelto: {unica}")
            return
        except NotImplementedError:
            print("  [Aviso]: El método de secuencia única arrojó NotImplementedError.")


def opcion_ordenar(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 12: Ordenar la Secuencia")
    if secuencia.nd == 0:
        print("  [Aviso]: La secuencia está vacía, no hay elementos para ordenar.")
        return

    print("Seleccione el criterio de ordenamiento:")
    print("  1. Ordenar por Salario y Nombre (usando QuickSort)")
    print("  2. Ordenar por Edad (usando QuickSort)")
    opc = input("  Elija una opción [1/2]: ").strip()

    if opc == "1":
        print("\n  -> Ordenando por Salario y Nombre...")
        arreglo_ordenado = secuencia.ordenar(se.Secuencia.nombre_salario)
    elif opc == "2":
        print("\n  -> Ordenando por Edad...")
        arreglo_ordenado = secuencia.ordenar(se.Secuencia.edad)
    else:
        print("  [Error]: Criterio no válido.")
        return

    print(f"\n  Elementos ordenados (Total: {secuencia.nd}):")
    print("-" * 70)
    for i in range(secuencia.nd):
        print(f"  [{i + 1:02d}] {arreglo_ordenado[i]}")
    print("-" * 70)


def opcion_recorrer_iterador(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 13: Recorrer Colección con Iterador [10 Puntos Extra]")
    if secuencia.nd == 0:
        print("  [Aviso]: La secuencia está vacía.")
        return

    print("  Demostrando el uso de __iter__() y __next__() sobre la Secuencia...")
    print("-" * 70)
    
    contador = 0
    # Consumo directo del iterador del TAD
    iterador = iter(secuencia)
    while True:
        try:
            empleado = next(iterador)
            contador += 1
            print(f"  [Iteración {contador:02d}] {empleado}")
        except StopIteration:
            break

    print("-" * 70)
    print(f"  Iteración completada exitosamente. Total de elementos recorridos: {contador}")


def opcion_probar_str(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 14: Probar Método Mágico __str__")
    cadena = str(secuencia)
    print("  Llamando a str(secuencia):")
    print(f"  --> {cadena}")
    if "<SecuenciaEmpleado.Secuencia object" in cadena:
        print("\n  [Aviso Integrante 2]: El método __str__ personalizado aún no ha sido implementado por el Integrante 2.")
    else:
        print("\n  [Éxito]: __str__ implementado correctamente.")


def opcion_probar_eq(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 15: Probar Método Mágico __eq__")
    vacia = se.Secuencia()
    print(f"  1. secuencia == secuencia vacía      -> {secuencia == vacia}"
          f"   (esperado: {secuencia.nd == 0})")
    print(f"  2. secuencia == ella misma           -> {secuencia == secuencia}   (esperado: True)")
    print(f"  3. secuencia == 5 (no es Secuencia)  -> {secuencia == 5}   (esperado: False)")

    if secuencia.nd == 0:
        print("\n  [Aviso]: Cargue o agregue empleados para probar las comparaciones 4 y 5.")
        return

    # Copia con los mismos empleados pero en orden inverso
    copia = se.Secuencia()
    for emp in reversed([emp for emp in secuencia]):  # recorrido con el iterador
        copia.agregar(emp)
    print(f"  4. misma colección, distinto orden   -> {secuencia == copia}   (esperado: True)")

    # Se agrega una repetición extra: la cardinalidad cambia
    copia.agregar(secuencia.obtener(0))
    print(f"  5. una repetición de más             -> {secuencia == copia}   (esperado: False)")


def opcion_guardar_archivo(secuencia: se.Secuencia):
    imprimir_encabezado("Opción 16: Guardar / Exportar Secuencia a Archivo CSV")
    if secuencia.nd == 0:
        print("  [Aviso]: La secuencia no tiene elementos para exportar.")
        return

    ruta_defecto = "empleados_exportados.csv"
    ruta = input(f"Ingrese la ruta de destino [Enter para '{ruta_defecto}']: ").strip()
    if not ruta:
        ruta = ruta_defecto

    try:
        guardar_en_archivo(ruta, secuencia)
    except Exception as err:
        print(f"  [Error al guardar]: {err}")


def opcion_crear_secuencia(secuencia: se.Secuencia) -> se.Secuencia:
    imprimir_encabezado("Opción 17: Crear nueva Secuencia (__init__)")
    print("  1. Constructor por omisión (Secuencia vacía, lista dinámica)")
    print("  2. Constructor de copia (copia la Secuencia actual)")
    opc = input("  Elija una opción [1/2]: ").strip()
    try:
        if opc == "1":
            nueva = se.Secuencia()
        elif opc == "2":
            nueva = se.Secuencia(secuencia)
        else:
            print("  [Error]: Opción no válida.")
            return secuencia
        print(f"  [Éxito]: Nueva Secuencia con {nueva.nd} elementos (sin capacidad máxima).")
        print("  (La Secuencia anterior fue reemplazada.)")
        return nueva
    except Exception as err:
        print(f"  [Error al crear la Secuencia]: {err}")
        return secuencia

def opcion_probar_excepciones(secuencia: se.Secuencia):
    imprimir_encabezado("Opcion 18: Probar manejo de excepciones")
    emp = e.Empleado("Prueba", "Excepcion", date(2000, 1, 1), "prueba@empresa.com", 1, 1000.0)
    pruebas = [
        ('agregar("texto")        [no es Empleado]', lambda: secuencia.agregar("texto")),
        ("agregar(emp, 0)         [nveces invalido]", lambda: secuencia.agregar(emp, 0)),
        ("eliminar(emp, -1)       [nrep invalido]", lambda: secuencia.eliminar(emp, -1)),
        ("eliminar(5)             [no es Empleado]", lambda: secuencia.eliminar(5)),
        ("Secuencia(-5)           [no es iterable]", lambda: se.Secuencia(-5)),
        ("Secuencia([\"texto\"])    [no son Empleados]", lambda: se.Secuencia(["texto"])),
        ("Secuencia(1, 2)         [demasiados parametros]", lambda: se.Secuencia(1, 2)),
    ]
    for descripcion, accion in pruebas:
        try:
            accion()
            print(f"  {descripcion} -> NO lanzó excepción")
        except Exception as err:
            print(f"  {descripcion} -> {type(err).__name__}: {err}")


# ==============================================================================
# MENÚ PRINCIPAL
# ==============================================================================

def mostrar_menu():
    """Despliega las opciones del menú interactivo."""
    print("\n" + "=" * 70)
    print("   SISTEMA DE GESTIÓN TAD SECUENCIA (EMPLEADOS) - TAREA 3")
    print("=" * 70)
    print("  [01] Cargar empleados desde archivo (CSV / Texto)")
    print("  [02] Agregar un Empleado (agregar)")
    print("  [03] Agregar un Empleado n veces (agregar nveces)")
    print("  [04] Eliminar todas las repeticiones de un Empleado (eliminar)")
    print("  [05] Eliminar n repeticiones de un Empleado (eliminar nrep)")
    print("  [06] Verificar si contiene un Empleado (contiene)")
    print("  [07] Consultar repeticiones de un Empleado (repeticiones)")
    print("  [08] Verificar si la Secuencia está vacía (esta_vacia)")
    print("  [09] Consultar cardinalidad de la Secuencia (cardinalidad)")
    print("  [10] Vaciar la Secuencia (vaciar)")
    print("  [11] Obtener secuencia única sin repetidos (secuencia_unica)")
    print("  [12] Ordenar la Secuencia (por edad o salario/nombre)")
    print("  [13] Recorrer la Secuencia con iterador (10 puntos extra)")
    print("  [14] Probar método mágico __str__ ")
    print("  [15] Probar método mágico __eq__ ")
    print("  [16] Guardar / Exportar Secuencia a archivo CSV")
    print("  [17] Probar medoto magico __init__")
    print("  [18] Probar manejo de excepciones")
    print("  [00] Salir del programa")
    print("-" * 70)
    print("  * Métodos asignados al Integrante 2 (compatibilidad dinámica integrada)")
    print("=" * 70)


def main():
    """Función de inicio del programa del menú interactivo."""
    print("Iniciando Sistema de Gestión de Secuencia de Empleados...")
    secuencia = se.Secuencia()

    archivo_origen = None  # Archivo con el que se inició (None = directorio en blanco)

    if os.path.exists("empleados.csv") and secuencia.nd == 0:
        auto = input("Se detectó 'empleados.csv'. ¿Desea cargarlo al iniciar? [S/n]: ").strip().lower()
        if auto in ("", "s", "si", "sí", "y", "yes"):
            try:
                cargar_desde_archivo("empleados.csv", secuencia)
                archivo_origen = "empleados.csv"
            except Exception as e_err:
                print(f"Error al precargar: {e_err}")

    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  [Interrupción detectada: se guardará antes de salir]")
            break

        if opcion in ("0", "00", "salir", "exit"):
            break
        elif opcion in ("1", "01"):
            opcion_cargar_archivo(secuencia)
        elif opcion in ("2", "02"):
            opcion_agregar_uno(secuencia)
        elif opcion in ("3", "03"):
            opcion_agregar_nveces(secuencia)
        elif opcion in ("4", "04"):
            opcion_eliminar_todo(secuencia)
        elif opcion in ("5", "05"):
            opcion_eliminar_nrep(secuencia)
        elif opcion in ("6", "06"):
            opcion_contiene(secuencia)
        elif opcion in ("7", "07"):
            opcion_repeticiones(secuencia)
        elif opcion in ("8", "08"):
            opcion_esta_vacia(secuencia)
        elif opcion in ("9", "09"):
            opcion_cardinalidad(secuencia)
        elif opcion == "10":
            opcion_vaciar(secuencia)
        elif opcion == "11":
            opcion_secuencia_unica(secuencia)
        elif opcion == "12":
            opcion_ordenar(secuencia)
        elif opcion == "13":
            opcion_recorrer_iterador(secuencia)
        elif opcion == "14":
            opcion_probar_str(secuencia)
        elif opcion == "15":
            opcion_probar_eq(secuencia)
        elif opcion == "16":
            opcion_guardar_archivo(secuencia)
        elif opcion == "17":
            secuencia = opcion_crear_secuencia(secuencia)
        elif opcion == "18":
            opcion_probar_excepciones(secuencia)
        else:
            print("  [Error]: Opción no válida. Por favor elija un número del menú.")

        input("\nPresione [Enter] para continuar...")

    print("\n--- Guardado automático ---")
    guardar_al_salir(secuencia, archivo_origen)
    print("\n¡Gracias por utilizar el Sistema de TAD Secuencia! Hasta pronto.\n")


if __name__ == "__main__":
    main()
