# Tabla comparativa de métodos: arreglos → lista con centinela

**Tarea 4, Problema 1, Integrante 1** (Emiliano Parra Miranda)

En la versión de la Tarea 3, `Secuencia` (el "directorio" de empleados) guardaba los datos en un
arreglo de numpy de tamaño fijo (`np.empty(20)`), y lo "hacía crecer" con `__crecer()`. Ese método
pedía un arreglo nuevo del doble de tamaño y copiaba todos los elementos.
En esta versión el almacenamiento es una **lista simplemente ligada con nodo centinela al inicio**
([ListaCentinela.py](ListaCentinela.py)). Los recorridos se hacen con su **iterador** (`IteradorLista`).

## Estructura de almacenamiento

| Aspecto | Solución con arreglos (Tarea 3) | Solución con lista (Tarea 4) |
|---|---|---|
| Atributos | `__datos: NDArray[Empleado]`, `__nd: int` | `__datos: Lista` (centinela, último nodo y contador) |
| Capacidad | Fija al construir; se duplica copiando todo | Sin límite: un nodo por elemento |
| Memoria desperdiciada | Posiciones vacías (`None`) del arreglo | Ninguna |
| Recorrido | `for i in range(self.__nd): self.__datos[i]` | `for emp in self:` (iterador de la lista) |

## Métodos

| Método (arreglos) | ¿Se mantiene? | ¿Cambia? | Cambio realizado en la programación |
|---|---|---|---|
| `__init__(*params)` | Sí | **Sí** | Antes: `Secuencia()` creaba un arreglo de 20 y `Secuencia(n)` uno de `n`. Ahora: `Secuencia()` crea una `Lista` vacía con su centinela. `Secuencia(iterable)` es un constructor de copia. Ya no se recibe una capacidad. |
| `__iter__()` | Sí | **Sí** | Antes regresaba `self` y guardaba la posición en `self.pos`, así que no se podían anidar recorridos. Ahora regresa un `IteradorLista` nuevo que avanza por los nodos (`actual = actual.siguiente`). |
| `__next__()` | **No** | — | Se eliminó de `Secuencia`. Ahora vive en `IteradorLista`. |
| `datos` (GET) | Sí | **Sí** | Antes regresaba el `NDArray`. Ahora regresa la `Lista`. Se conserva `datos[i]` y `len(datos)` con `__getitem__`/`__len__` de la lista (acceso O(n)). |
| `nd` (GET) | Sí | **Sí** | Antes leía el atributo `__nd`. Ahora regresa `self.__datos.longitud()` (contador O(1) de la lista). |
| `__crecer(minimo)` | **No** | — | Se eliminó: la lista no tiene capacidad que crecer. |
| `agregar(elemento, nveces=1)` | Sí | **Sí** | Antes llamaba a `__crecer()` y escribía en `__datos[__nd]`. Ahora llama a `lista.agregar()`, que crea un nodo y lo enlaza después del último en O(1). Las validaciones (`TypeError`, `ValueError`) no cambian. |
| `eliminar(elemento, nrep=None)` | Sí | **Sí** | Antes compactaba el arreglo moviendo elementos y ponía `None` en las posiciones sobrantes. Ahora `lista.eliminar(elemento, por_quitar)` desconecta los nodos en una sola pasada. Usa un apuntador `anterior` que empieza en el **centinela**, así que borrar el primer nodo no es un caso especial. La regla "si hay menos de `nrep`, no hace nada" y las validaciones se conservan. |
| `contiene(elemento)` | Sí | **Sí** (solo el recorrido) | La lógica es la misma (búsqueda lineal). Ahora recorre con el iterador (`for emp in self`) en lugar de usar índices. |
| `repeticiones(elemento)` | Sí | **Sí** (solo el recorrido) | Igual que `contiene`: se cambió el ciclo por índices por el iterador. |
| `esta_vacia()` | Sí | **Sí** | Antes: `__nd == 0`. Ahora: `lista.esta_vacia()`, que revisa `centinela.siguiente is None`. |
| `cardinalidad()` | Sí | **Sí** (mínimo) | Antes regresaba `__nd`. Ahora regresa `lista.longitud()`. |
| `vaciar()` | Sí | **Sí** | Antes creaba otro arreglo de la misma capacidad. Ahora `lista.vaciar()` hace `centinela.siguiente = None` en O(1). |
| `secuencia_unica()` | Sí | **Sí** | Ya no calcula una capacidad inicial (`Secuencia(capacidad)`). Crea una `Secuencia()` vacía y recorre con el iterador. |
| `ordenar(comparador=None)` | Sí | **Sí** | La lista no tiene acceso aleatorio. Ahora se vuelca con el iterador a un arreglo auxiliar de tamaño exacto (`nd`) y ahí se aplica el mismo Quick Sort. Antes se copiaba `__datos[:__nd]`. *(El Integrante 2 integra la Lista Ordenada del material para mostrar los datos ordenados.)* |
| `__str__()` | Sí | **Sí** | Delega a `Lista.__str__`, que recorre los nodos con el iterador. |
| `__eq__(otro)` | Sí | **Sí** (solo el recorrido) | La lógica de multiconjunto (misma cardinalidad y mismas repeticiones) no cambia. Ahora recorre `secuencia_unica()` con el iterador en vez de usar `unicos.datos[i]`. |
| `__compare_strings(a, b)` | Sí | No | Sin cambios: compara cadenas y no depende de la estructura. |
| `nombre_salario(a, b)` | Sí | No | Sin cambios (comparador). |
| `edad(a, b)` | Sí | No | Sin cambios (comparador). |
| `__particion(...)` | Sí | No | Sin cambios: trabaja sobre el arreglo auxiliar que crea `ordenar`. |
| `__quick_sort(...)` | Sí | No | Sin cambios: trabaja sobre el arreglo auxiliar que crea `ordenar`. |
| — | **Nuevo** | — | `obtener(indice)`: regresa el empleado en una posición recorriendo la lista. Lo usa el menú para elegir empleados por número. |
| — | **Nuevo** | — | `actualizar(elemento, nuevo, nrep=None)`: reemplaza un empleado por otro en su misma posición. Solo cambia el dato del nodo, no se re-enlaza nada. Sigue la misma regla de `nrep` que `eliminar`. La versión con arreglos no tenía método de actualización. |

## Métodos de la nueva estructura `Lista` (ListaCentinela.py)

| Método | Complejidad | Descripción |
|---|---|---|
| `agregar(e)` | O(1) | Inserta al final (usa la referencia al último nodo). |
| `agregar_inicio(e)` | O(1) | Inserta después del centinela. |
| `eliminar(e, maximo=1)` / `eliminar_si(cond, maximo)` | O(n) | Elimina en una pasada, empezando en el centinela. |
| `reemplazar(e, nuevo, maximo)` | O(n) | Actualiza el dato de los nodos que coinciden. |
| `contiene(e)`, `obtener(i)` / `[i]` | O(n) | Recorren los nodos. |
| `esta_vacia()`, `longitud()` / `len()` | O(1) | Revisan el centinela o el contador. |
| `vaciar()` | O(1) | Desconecta el centinela. |
| `__iter__()` | O(1) | Regresa un `IteradorLista` independiente. |

## Cambios en otros módulos

| Archivo | Cambio |
|---|---|
| `MenuSecuenciaEmp.py` | Las opciones 15, 17 y 18 usaban `Secuencia(n)` con capacidad. Ahora usan `Secuencia()` o el constructor de copia `Secuencia(secuencia)`. En la opción 15, la copia invertida se arma recorriendo con el iterador. `mostrar_elementos_secuencia` ahora recorre con el iterador en lugar de `datos[i]`, que con la lista sería O(n²). |
| `Empleado.py`, `Persona.py`, `Secuenciable.py` | Sin cambios: la interfaz del TAD se conserva. |
