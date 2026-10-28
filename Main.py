# Programa: Main.py
# Objetivo: Punto de entrada principal para la ejecución de la Tarea 3 (TAD Secuencia).
#           Inicia el menú interactivo de gestión de la colección de Empleados.
# Autores: Integrante 3 e Integrante 4 (Tarea 3 - Manejo de Datos, UNAM)
# Fecha: Octubre 2026

import sys
import MenuSecuenciaEmp


def main():
    """Función de inicio del programa principal."""
    MenuSecuenciaEmp.main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Programa terminado por el usuario mediante teclado]")
        sys.exit(0)
