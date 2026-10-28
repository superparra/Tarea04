# Script de verificación automatizada: test_menu_integrante3.py
# Valida la lógica de carga de archivo, persistencia, iterador y operaciones del TAD Secuencia.

import os
from datetime import date
import Empleado as e
import SecuenciaEmpleado as se
import MenuSecuenciaEmp as menu


def run_tests():
    print("=" * 60)
    print("Iniciando pruebas automatizadas del Integrante 3...")
    print("=" * 60)

    # 1. Prueba de instanciación de Secuencia
    sec = se.Secuencia()
    assert sec.nd == 0, f"Error: nd inicial debe ser 0, se obtuvo {sec.nd}"
    print("[PASÓ] 1. Instanciación correcta de Secuencia.")

    # 2. Prueba de carga desde archivo CSV
    assert os.path.exists("empleados.csv"), "Error: empleados.csv no existe"
    total_cargados = menu.cargar_desde_archivo("empleados.csv", sec)
    assert total_cargados > 0, "Error: no se cargaron empleados desde empleados.csv"
    assert sec.nd == total_cargados, f"Error: sec.nd ({sec.nd}) != total_cargados ({total_cargados})"
    print(f"[PASÓ] 2. Carga desde empleados.csv ({total_cargados} registros cargados).")

    # 3. Prueba de iterador (10 puntos extra)
    contador_iter = 0
    for emp in sec:
        assert isinstance(emp, e.Empleado), f"Elemento no es Empleado: {type(emp)}"
        contador_iter += 1
    assert contador_iter == sec.nd, f"Error en iterador: recorrió {contador_iter} != {sec.nd}"
    print(f"[PASÓ] 3. Recorrido con iterador completado con éxito ({contador_iter} elementos).")

    # 4. Prueba de duplicados y repeticiones
    carlos = sec.datos[0] # Carlos Santana Gomez
    rep_carlos = sec.repeticiones(carlos)
    assert rep_carlos >= 2, f"Se esperaban al menos 2 repeticiones de Carlos, se obtuvieron {rep_carlos}"
    print(f"[PASÓ] 4. Consulta de repeticiones correcta ({carlos.nombre} tiene {rep_carlos} repeticiones).")

    # 5. Prueba de contiene
    assert sec.contiene(carlos) is True, "Error: contiene() reportó False para un empleado existente"
    emp_inexistente = e.Empleado("Inexistente", "Fantasma", date(2000, 1, 1), "fantasma@empresa.com", 9999, 50000.0)
    assert sec.contiene(emp_inexistente) is False, "Error: contiene() reportó True para un empleado inexistente"
    print("[PASÓ] 5. Método contiene() verificado con positivos y negativos.")

    # 6. Prueba de ordenamiento (QuickSort con comparadores)
    ordenados_salario = sec.ordenar(se.Secuencia.nombre_salario)
    assert len(ordenados_salario) == sec.nd, "Error en longitud del arreglo ordenado"
    # Verificar que el salario esté ordenado ascendentemente
    for i in range(sec.nd - 1):
        dif = se.Secuencia.nombre_salario(ordenados_salario[i], ordenados_salario[i+1])
        assert dif <= 0, f"Error de orden en salario: {ordenados_salario[i].salario} > {ordenados_salario[i+1].salario}"
    print("[PASÓ] 6.1 Ordenamiento por Salario y Nombre verificado correctamente.")

    ordenados_edad = sec.ordenar(se.Secuencia.edad)
    for i in range(sec.nd - 1):
        dif = se.Secuencia.edad(ordenados_edad[i], ordenados_edad[i+1])
        assert dif <= 0, f"Error de orden en edad: {ordenados_edad[i].edad()} > {ordenados_edad[i+1].edad()}"
    print("[PASÓ] 6.2 Ordenamiento por Edad verificado correctamente.")

    # 7. Prueba de exportación / guardado a CSV
    ruta_export = "test_export.csv"
    if os.path.exists(ruta_export):
        os.remove(ruta_export)
    exito_export = menu.guardar_en_archivo(ruta_export, sec)
    assert exito_export is True, "Error al exportar a archivo CSV"
    assert os.path.exists(ruta_export), "Error: archivo exportado no existe"

    # Verificar recarga desde el archivo exportado
    sec_recargada = se.Secuencia()
    recargados = menu.cargar_desde_archivo(ruta_export, sec_recargada)
    assert recargados == sec.nd, f"Recargados ({recargados}) != originales ({sec.nd})"
    print(f"[PASÓ] 7. Exportación y recarga de archivo CSV verificada ({recargados} registros).")
    
    # Limpieza de archivo temporal
    if os.path.exists(ruta_export):
        os.remove(ruta_export)

    # 8. Prueba de eliminación parcial
    nd_antes = sec.nd
    sec.eliminar(carlos, 1)
    assert sec.repeticiones(carlos) == rep_carlos - 1, "Error: no se redujo en 1 la repetición"
    assert sec.nd == nd_antes - 1, "Error en nd tras eliminación de 1 repetición"
    print("[PASÓ] 8. Eliminación de n repeticiones verificada.")

    print("=" * 60)
    print("¡TODAS LAS PRUEBAS AUTOMATIZADAS PASARON CON ÉXITO! (100% OK)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
