# Tarea 04: TAD Lista y TAD Pila

Manejo de Datos, Facultad de Ciencias, UNAM. Equipo **Huitzilovers2.0**. Fecha de entrega: 30 de octubre de 2026.

Esta tarea parte de la Tarea 3 ([jcaessar/Tarea03](https://github.com/jcaessar/Tarea03)): el TAD Secuencia de Empleados.

## Problema 1: Directorio con listas

| Integrante         | Parte | Estado |
|--------------------|---|--|
| 1 (Emiliano Parra) | Migración a lista simplemente ligada con centinela + tabla comparativa | ✅ Hecho |
| 2                  | Lista Ordenada para mostrar datos ordenados + menú de inicio (directorio en blanco o desde archivo) | Pendiente |
| 3 (Yoichi Servin)  | Persistencia CSV: carga inicial y guardado automático al salir | ✅ Hecho |

## Problema 2: Pilas de libros

| Integrante | Parte | Estado |
|---|---|---|
| 4 | Clase `Libro` + 3 criterios + carga de `estante1.csv`/`estante2.csv` en Pilas | Pendiente |
| 5 | Extracción LIFO hacia Lista Ordenada + guardado en un tercer CSV | Pendiente |

## Archivos

| Archivo | Descripción |
|---|---|
| `ListaCentinela.py` | `Nodo`, `IteradorLista` y `Lista` (simplemente ligada con centinela al inicio) |
| `SecuenciaEmpleado.py` | TAD Secuencia, ahora guardada en la lista ligada |
| `TablaComparativa.md` | Tabla de métodos: arreglos vs. lista |
| `MenuSecuenciaEmp.py`, `Main.py` | Menú interactivo |
| `Empleado.py`, `Persona.py`, `Secuenciable.py` | Clases base de la Tarea 3 |
| `test_lista_integrante1.py` | Pruebas de la migración |
| `test_menu_integrante3.py` | Pruebas del menú y de la carga de CSV (Tarea 3) |

## Ejecución

```bash
pip install numpy validate_email
python Main.py                      # menú interactivo
python test_lista_integrante1.py    # pruebas de la lista
python test_menu_integrante3.py     # pruebas del menú y CSV
```

## Flujo de trabajo

Cada integrante trabaja en su propia rama (`integrante-2`, `integrante-3`, ...) y abre un Pull Request a `main`.
