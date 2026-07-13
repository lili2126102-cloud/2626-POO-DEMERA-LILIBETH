# -*- coding: utf-8 -*-
import os
import sys

# Agregamos la ruta de la aplicación al path de ejecución para resolver las importaciones
directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.append(directorio_actual)

from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante

def pausar(mensaje: str = "Presione Enter para continuar...") -> None:
    """Pausa la ejecución y espera a que el usuario presione una tecla."""
    print(f"\n--> {mensaje}", end="")
    input()

def limpiar_pantalla() -> None:
    """Limpia la consola según el sistema operativo."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main() -> None:
    """Función de arranque principal y control del menú de usuario."""
    # Instanciamos el servicio principal
    mi_restaurante = Restaurante("El Rincón Sabor y Arte")

    while True:
        limpiar_pantalla()
        
        # Despliegue del menú obligatorio
        print("========================================")
        print("        SISTEMA DE RESTAURANTE")
        print("========================================")
        print("1. Registrar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("----------------------------------------")
        print("4. Registrar cliente")
        print("5. Listar clientes")
        print("6. Buscar cliente")
        print("----------------------------------------")
        print("7. Salir")
        print("========================================")

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            limpiar_pantalla()
            print("--- REGISTRO DE NUEVO PRODUCTO ---")
            nombre = input("Ingrese el nombre del producto: ").strip()
            categoria = input("Ingrese la categoría (ej. Entrada, Plato Fuerte, Bebida): ").strip()
            precio_raw = input("Ingrese el precio (mayor a 0): ").strip()
            disponibilidad_raw = input("¿Está disponible actualmente? (S/N - Por defecto S): ").strip().upper()

            disponible = False if disponibilidad_raw == "N" else True

            try:
                # El constructor valida internamente mediante los setters
                nuevo_producto = Producto(
                    nombre=nombre,
                    categoria=categoria,
                    precio=precio_raw,  # El setter de precio convertirá a float y validará
                    disponible=disponible
                )
                mi_restaurante.registrar_producto(nuevo_producto)
            except ValueError as error:
                print(f"\n[ERROR] No se pudo registrar el producto: {error}")
            
            pausar()

        elif opcion == "2":
            limpiar_pantalla()
            mi_restaurante.listar_productos()
            pausar()

        elif opcion == "3":
            limpiar_pantalla()
            print("--- BÚSQUEDA DE PRODUCTO ---")
            termino = input("Ingrese el nombre (o parte del nombre) del producto a buscar: ").strip()
            if not termino:
                print("\n[!] El término de búsqueda no puede estar vacío.")
            else:
                resultados = mi_restaurante.buscar_producto(termino)
                if resultados:
                    print(f"\nSe encontraron {len(resultados)} coincidencia(s):")
                    for producto in resultados:
                        print("-" * 35)
                        producto.mostrar_informacion()
                    print("-" * 35)
                else:
                    print(f"\n[!] No se encontraron productos coincidentes con '{termino}'.")
            pausar()

        elif opcion == "4":
            limpiar_pantalla()
            print("--- REGISTRO DE NUEVO CLIENTE ---")
            id_cliente = input("Ingrese el identificador / ID del cliente (ej. Cédula): ").strip()
            nombre = input("Ingrese el nombre del cliente: ").strip()
            correo = input("Ingrese el correo electrónico: ").strip()

            # Validamos que los datos no estén vacíos antes de crear
            if not id_cliente:
                print("\n[ERROR] El ID del cliente es obligatorio.")
            elif not nombre:
                print("\n[ERROR] El nombre del cliente es obligatorio.")
            elif not correo:
                print("\n[ERROR] El correo del cliente es obligatorio.")
            else:
                try:
                    # Instanciamos el cliente mediante la @dataclass
                    nuevo_cliente = Cliente(
                        id_cliente=id_cliente,
                        nombre=nombre,
                        correo=correo
                    )
                    mi_restaurante.registrar_cliente(nuevo_cliente)
                except Exception as error:
                    print(f"\n[ERROR] Ocurrió un error al instanciar el cliente: {error}")
            
            pausar()

        elif opcion == "5":
            limpiar_pantalla()
            mi_restaurante.listar_clientes()
            pausar()

        elif opcion == "6":
            limpiar_pantalla()
            print("--- BÚSQUEDA DE CLIENTE ---")
            id_busqueda = input("Ingrese el ID del cliente a buscar: ").strip()
            if not id_busqueda:
                print("\n[!] Debe ingresar un ID para realizar la búsqueda.")
            else:
                cliente_encontrado = mi_restaurante.buscar_cliente(id_busqueda)
                if cliente_encontrado:
                    print("\n" + "=" * 40)
                    print("         CLIENTE ENCONTRADO")
                    print("=" * 40)
                    print(f"ID:       {cliente_encontrado.id_cliente}")
                    print(f"Nombre:   {cliente_encontrado.nombre}")
                    print(f"Correo:   {cliente_encontrado.correo}")
                    print("=" * 40)
                else:
                    print(f"\n[!] No se encontró ningún cliente registrado con el ID '{id_busqueda}'.")
            pausar()

        elif opcion == "7":
            print("\n¡Gracias por utilizar el Sistema de Restaurante! Hasta pronto.\n")
            break

        else:
            print("\n[!] Opción inválida. Ingrese un número entre 1 y 7.")
            pausar()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEjecución cancelada por el usuario.")
        sys.exit(0)
