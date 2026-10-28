# Programa: test_lista_integrante1.py
# Objetivo: Pruebas automatizadas de la migración de la Secuencia a una lista
#           simplemente ligada con centinela al inicio (Tarea 4 - Integrante 1).
# Autor: Emiliano Parra Miranda
# Fecha: Octubre 2026

from datetime import date

import Empleado as e
import ListaCentinela as lc
import SecuenciaEmpleado as se
import MenuSecuenciaEmp as menu


def probar_lista():
    """Pruebas de la lista ligada con centinela y su iterador."""
    lista = lc.Lista()
    assert lista.esta_vacia() and len(lista) == 0
    for x in (1, 2, 3):
        lista.agregar(x)
    lista.agregar_inicio(0)
    assert [x for x in lista] == [0, 1, 2, 3]
    assert lista.primero() == 0 and lista.ultimo() == 3 and lista[2] == 2 and lista[-1] == 3
    # Eliminar el primero (caso que el centinela simplifica) y el último (actualiza 'ultimo')
    assert lista.eliminar(0) == 1 and lista.eliminar(3) == 1
    lista.agregar(9)
    assert [x for x in lista] == [1, 2, 9] and lista.ultimo() == 9
    # Iteradores independientes (recorridos anidados)
    pares = [(a, b) for a in lista for b in lista]
    assert len(pares) == 9
    lista.vaciar()
    assert lista.esta_vacia() and len(lista) == 0
    lista.agregar(5)
    assert lista.primero() == lista.ultimo() == 5
    print("[PASÓ] Lista con centinela + iterador")


def probar_secuencia():
    """Pruebas de la Secuencia de Empleados sobre la lista."""
    a = e.Empleado("Ana", "López", date(1995, 9, 23), "ana@empresa.com", 1, 20000)
    b = e.Empleado("Beto", "Ruiz", date(1980, 1, 10), "beto@empresa.com", 2, 15000)

    sec = se.Secuencia()
    assert sec.esta_vacia() and sec.cardinalidad() == 0
    # Sin capacidad máxima: se agregan muchos elementos sin "crecer" ningún arreglo
    sec.agregar(a, 500)
    sec.agregar(b, 3)
    assert sec.cardinalidad() == 503 and sec.repeticiones(a) == 500
    assert sec.contiene(b)

    sec.eliminar(b, 5)                      # hay menos de 5 -> no hace nada
    assert sec.repeticiones(b) == 3
    sec.eliminar(b, 2)
    assert sec.repeticiones(b) == 1
    sec.eliminar(a)                         # todas las repeticiones
    assert sec.repeticiones(a) == 0 and sec.cardinalidad() == 1
    assert sec.obtener(0) == b

    # Actualización: conserva la posición y respeta la regla de nrep
    b2 = e.Empleado("Beto", "Ruiz", date(1980, 1, 10), "beto.nuevo@empresa.com", 2, 18000)
    assert sec.actualizar(b, b2) == 1 and sec.obtener(0) == b2 and not sec.contiene(b)
    assert sec.actualizar(b2, b, 3) == 0 and sec.obtener(0) == b2   # hay menos de 3
    sec.actualizar(b2, b)

    sec.agregar(a, 2)
    unica = sec.secuencia_unica()
    assert unica.cardinalidad() == 2

    copia = se.Secuencia(sec)               # constructor de copia
    assert copia == sec and copia is not sec
    copia.agregar(a)
    assert copia != sec

    ordenados = sec.ordenar(se.Secuencia.nombre_salario)
    assert [x.salario for x in ordenados] == sorted(x.salario for x in sec)

    for invalido in (lambda: se.Secuencia(5), lambda: se.Secuencia(["x"]),
                     lambda: se.Secuencia(1, 2), lambda: sec.agregar("x"),
                     lambda: sec.eliminar(a, 0)):
        try:
            invalido()
            raise AssertionError("Se esperaba una excepción")
        except (TypeError, ValueError):
            pass

    sec.vaciar()
    assert sec.esta_vacia() and str(sec) == "[]"
    print("[PASÓ] Secuencia sobre lista con centinela")


def probar_carga_csv():
    """La carga del CSV del Integrante 3 sigue funcionando con la nueva estructura."""
    sec = se.Secuencia()
    total = menu.cargar_desde_archivo("empleados.csv", sec)
    assert total == sec.cardinalidad() > 0
    assert sum(1 for _ in sec) == total
    print("[PASÓ] Carga de empleados.csv sobre la lista")


if __name__ == "__main__":
    probar_lista()
    probar_secuencia()
    probar_carga_csv()
    print("\nTodas las pruebas del Integrante 1 pasaron.")
