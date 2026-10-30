# Programa: test_menu_integrante2.py
# Objetivo: Probar MenuDirectorio.py sin depender todavía de Directorio.py
# (Integrante 1) ni de Persistencia.py (Integrante 3), usando versiones falsas.
# Cuando existan los reales, borra este archivo y corre MenuDirectorio.py.

import sys
import types
import csv
import os


# ------------------------------------------------------------------------------
# Clases falsas
# ------------------------------------------------------------------------------

class Contacto:
    """Contacto falso con los atributos que usan los comparadores."""

    def __init__(self, nombre, apellidos, telefono, email):
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"{self.nombre} {self.apellidos} | {self.telefono} | {self.email}"


class Directorio:
    """Directorio falso: guarda contactos en una lista de Python y es iterable."""

    def __init__(self):
        self._contactos = []

    def agregar(self, contacto):
        self._contactos.append(contacto)

    def __iter__(self):
        return iter(self._contactos)


def cargar_desde_csv(ruta, directorio):
    """Carga falsa: lee nombre,apellidos,telefono,email de un CSV."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(ruta)
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.reader(f):
            if len(fila) >= 4 and fila[0].lower() != "nombre":
                directorio.agregar(Contacto(*[x.strip() for x in fila[:4]]))


def guardar_en_csv(ruta, directorio):
    """Guardado falso: escribe los contactos en un CSV."""
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nombre", "apellidos", "telefono", "email"])
        for c in directorio:
            w.writerow([c.nombre, c.apellidos, c.telefono, c.email])
    print(f" [Prueba]: guardado en '{ruta}'")


# ------------------------------------------------------------------------------
# Se registran como si fueran los módulos reales y se corre el menú
# ------------------------------------------------------------------------------

mod_dir = types.ModuleType("Directorio")
mod_dir.Directorio = Directorio
mod_dir.Contacto = Contacto
mod_per = types.ModuleType("Persistencia")
mod_per.cargar_desde_csv = cargar_desde_csv
mod_per.guardar_en_csv = guardar_en_csv
sys.modules["Directorio"] = mod_dir
sys.modules["Persistencia"] = mod_per

if __name__ == "__main__":
    # Archivo de ejemplo para probar la opción "cargar desde archivo"
    if not os.path.exists("contactos_prueba.csv"):
        with open("contactos_prueba.csv", "w", encoding="utf-8") as f:
            f.write("nombre,apellidos,telefono,email\n")
            f.write("Zoe,Ramírez,5511111111,zoe@ciencias.unam.mx\n")
            f.write("Ana,Torres,5522222222,ana@ciencias.unam.mx\n")
            f.write("Luis,Gómez,5533333333,luis@ciencias.unam.mx\n")
            f.write("Beto,Alvarez,5544444444,beto@ciencias.unam.mx\n")
        print("Se creó 'contactos_prueba.csv' para probar.")

    import MenuDirectorio
    MenuDirectorio.main()
