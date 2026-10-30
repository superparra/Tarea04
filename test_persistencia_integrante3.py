# Programa: test_persistencia_integrante3.py
# Objetivo: Pruebas del guardado automático al salir (Tarea 4 - Integrante 3).

import os
from datetime import date
import Empleado as e
import SecuenciaEmpleado as se
import MenuSecuenciaEmp as menu


def run_tests():
    ruta = "test_persistencia.csv"
    ana = e.Empleado("Ana", "López", date(1995, 9, 23), "ana@empresa.com", 1, 20000)
    beto = e.Empleado("Beto", "Ruiz", date(1980, 1, 10), "beto@empresa.com", 2, 15000)

    # 1. Guardar y recargar
    sec = se.Secuencia()
    sec.agregar(ana, 2)
    sec.agregar(beto)
    assert menu.guardar_al_salir(sec, ruta) == ruta
    recargada = se.Secuencia()
    assert menu.cargar_desde_archivo(ruta, recargada) == 3
    assert recargada == sec
    print("[PASÓ] 1. Guardar y recargar")

    # 2. Sobrescribir el mismo archivo tras eliminar
    sec.eliminar(ana)
    menu.guardar_al_salir(sec, ruta)
    r2 = se.Secuencia()
    assert menu.cargar_desde_archivo(ruta, r2) == 1
    print("[PASÓ] 2. Sobrescritura del archivo de origen")

    # 3. Directorio vacío: el archivo queda sin datos (no conserva los viejos)
    sec.vaciar()
    menu.guardar_al_salir(sec, ruta)
    r3 = se.Secuencia()
    assert menu.cargar_desde_archivo(ruta, r3) == 0
    print("[PASÓ] 3. Directorio vacío actualiza el archivo")

    # 4. Inicio en blanco y vacío: no guarda nada
    assert menu.guardar_al_salir(se.Secuencia(), None) is None
    print("[PASÓ] 4. Inicio en blanco sin datos no guarda")

    os.remove(ruta)
    print("\nTodas las pruebas del Integrante 3 pasaron.")


if __name__ == "__main__":
    run_tests()