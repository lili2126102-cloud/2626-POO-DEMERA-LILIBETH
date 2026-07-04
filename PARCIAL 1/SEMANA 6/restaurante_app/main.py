import sys
import os

# Agregamos la ruta del directorio actual al path por si se ejecuta desde directorios externos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.platillo import Platillo
from modelos.bebida import Bebida
from servicios.restaurante import Restaurante

def mostrar_caja(titulo: str, lineas: list, tag: str = "[INFO]") -> None:
    """
    Dibuja una caja elegante en la consola con un título y contenido usando ASCII estándar
    para asegurar la compatibilidad total en consolas Windows (cp1252).
    """
    ancho = 78
    print("\n+" + "-" * (ancho - 2) + "+")
    # Formateamos el título
    titulo_formateado = f"| {tag} {titulo}"
    print(f"{titulo_formateado:<{ancho - 1}}|")
    print("+" + "-" * (ancho - 2) + "+")
    for linea in lineas:
        linea_str = f"| {linea}"
        print(f"{linea_str:<{ancho - 1}}|")
    print("+" + "-" * (ancho - 2) + "+")

def pausar(mensaje: str = "Presione Enter para continuar...") -> None:
    """
    Pausa la ejecucion y espera a que el usuario presione Enter.
    """
    print(f"\n--> {mensaje}", end="")
    input()

def demostracion_herencia() -> tuple:
    mostrar_caja(
        "CONCEPTO: HERENCIA (INHERITANCE)",
        [
            "La HERENCIA permite a una clase (hija) adquirir atributos y metodos",
            "de otra clase (padre). Esto evita la duplicacion de codigo y crea",
            "una jerarquia logica entre entidades del mundo real.",
            "",
            "En esta aplicacion:",
            "  - Clase Padre: 'Producto' (en modelos/producto.py)",
            "    Define atributos basicos comunes: nombre, disponible y __precio.",
            "  - Clases Hijas: 'Platillo' (en modelos/platillo.py) y 'Bebida'",
            "    (en modelos/bebida.py).",
            "",
            "Ambas clases hijas heredan de 'Producto' y llaman a su constructor",
            "mediante super().__init__(nombre, precio, disponible), añadiendo",
            "atributos especificos: calorias (Platillo) y volumen (Bebida).",
        ],
        "[HERENCIA]"
    )

    pausar("Presione Enter para ejecutar la demostracion de Herencia...")

    print("\n" + "-" * 78)
    print("* EJECUCION EN VIVO: Creacion de objetos usando Herencia")
    print("-" * 78)
    
    print(">>> Creando objeto Platillo (hijo de Producto):")
    print("    platillo1 = Platillo(nombre='Lasana de Carne', precio=12.50, disponible=True, calorias=680)")
    platillo1 = Platillo(nombre="Lasana de Carne", precio=12.50, disponible=True, calorias=680)
    print(f"    <- Creado exitosamente: {type(platillo1).__name__}")
    print(f"       Atributos heredados: nombre='{platillo1.nombre}', disponible={platillo1.disponible}")
    print(f"       Atributo propio de Platillo: calorias={platillo1.calorias} kcal")

    print("\n>>> Creando objeto Bebida (hijo de Producto):")
    print("    bebida1 = Bebida(nombre='Limonada Imperial', precio=2.50, disponible=True, volumen=400)")
    bebida1 = Bebida(nombre="Limonada Imperial", precio=2.50, disponible=True, volumen=400)
    print(f"    <- Creado exitosamente: {type(bebida1).__name__}")
    print(f"       Atributos heredados: nombre='{bebida1.nombre}', disponible={bebida1.disponible}")
    print(f"       Atributo propio de Bebida: volumen={bebida1.volumen} ml")
    
    print("-" * 78)
    print("¡Herencia demostrada! Platillo y Bebida reutilizan la logica de Producto.")
    print("-" * 78)
    
    return platillo1, bebida1

def demostracion_encapsulamiento(platillo1, bebida1) -> None:
    mostrar_caja(
        "CONCEPTO: ENCAPSULAMIENTO (ENCAPSULATION)",
        [
            "El ENCAPSULAMIENTO consiste en ocultar el estado interno de un objeto",
            "y restringir el acceso directo a sus atributos. Esto protege la",
            "integridad de los datos, obligando a interactuar con ellos mediante",
            "metodos publicos (interfaz controlada): Getters y Setters.",
            "",
            "En esta aplicacion:",
            "  - Atributo privado: 'self.__precio' en la clase Producto (inicia con '__')",
            "  - Getter (Lectura): 'obtener_precio()'",
            "  - Setter (Escritura con validacion): 'cambiar_precio(nuevo_precio)'",
            "    El setter no permite que el precio sea menor o igual a cero.",
        ],
        "[ENCAPSULAMIENTO]"
    )

    pausar("Presione Enter para ejecutar la demostracion de Encapsulamiento...")

    print("\n" + "-" * 78)
    print("* EJECUCION EN VIVO: Proteccion y validacion mediante Encapsulamiento")
    print("-" * 78)

    # 1. Intento de acceso directo que debe fallar
    print("1) INTENTO DE ACCESO DIRECTO NO AUTORIZADO:")
    print("   Tratamos de leer platillo1.__precio directamente en main.py...")
    try:
        # Intentamos acceder al atributo privado. Python lanzara un AttributeError
        # debido al Name Mangling (_Producto__precio)
        valor_invalido = platillo1.__precio
        print(f"   [!] Exito inesperado (no deberia ocurrir): {valor_invalido}")
    except AttributeError as e:
        print(f"   [ERROR ESPERADO] AttributeError: {e}")
        print("   <- Explicacion: Python ha ocultado el atributo '__precio'.")
        print("      No es visible desde fuera de la clase Producto.")

    # 2. Uso correcto del Getter
    print("\n2) USO CORRECTO DEL GETTER:")
    print("   Llamamos a: precio = platillo1.obtener_precio()")
    precio = platillo1.obtener_precio()
    print(f"   <- Precio obtenido de forma segura: ${precio:.2f}")

    # 3. Setter con valor invalido
    print("\n3) VALIDACION DE DATOS (SETTER CON VALOR INVALIDO):")
    print("   Intentamos cambiar el precio a un valor negativo: platillo1.cambiar_precio(-5.00)")
    exito_negativo = platillo1.cambiar_precio(-5.00)
    print(f"   <- ¿Operacion exitosa?: {exito_negativo}")
    print(f"   <- Precio del producto: ${platillo1.obtener_precio():.2f} (permanecio intacto)")

    # 4. Setter con valor valido
    print("\n4) MODIFICACION DE DATOS CORRECTA (SETTER CON VALOR VALIDO):")
    print("   Intentamos cambiar el precio a un valor valido: platillo1.cambiar_precio(14.50)")
    exito_valido = platillo1.cambiar_precio(14.50)
    print(f"   <- ¿Operacion exitosa?: {exito_valido}")
    print(f"   <- Nuevo precio actualizado: ${platillo1.obtener_precio():.2f}")

    print("-" * 78)
    print("¡Encapsulamiento demostrado! El objeto protege sus datos de valores erroneos.")
    print("-" * 78)

def demostracion_polimorfismo(platillo1, bebida1) -> None:
    mostrar_caja(
        "CONCEPTO: POLIMORFISMO (POLYMORPHISM)",
        [
            "El POLIMORFISMO es la capacidad de que diferentes clases respondan",
            "al mismo metodo de formas distintas. Permite tratar de forma uniforme",
            "a objetos de distintas clases hijas bajo la interfaz de la clase padre.",
            "",
            "En esta aplicacion:",
            "  - La clase padre 'Producto' define 'mostrar_informacion()'.",
            "  - Las clases 'Platillo' y 'Bebida' sobrescriben 'mostrar_informacion()'",
            "    para mostrar sus datos particulares (calorias y volumen).",
            "  - Al recorrer una lista de productos en el Restaurante e invocar",
            "    'mostrar_informacion()', cada objeto se comporta segun su clase real.",
        ],
        "[POLIMORFISMO]"
    )

    pausar("Presione Enter para ejecutar la demostracion de Polimorfismo...")

    print("\n" + "-" * 78)
    print("* EJECUCION EN VIVO: Llamadas dinamicas por Polimorfismo")
    print("-" * 78)

    # Creamos el restaurante y agregamos mas productos
    mi_restaurante = Restaurante("El Rincon Gourmet")
    
    print("\n>>> Registrando productos en el menu (todos entran como tipo 'Producto'):")
    # Agregamos los que ya creamos en el paso 1
    mi_restaurante.agregar_producto(platillo1)
    mi_restaurante.agregar_producto(bebida1)
    
    # Creamos un segundo platillo y segunda bebida
    platillo2 = Platillo(nombre="Tacos al Pastor (3 uds)", precio=8.00, disponible=True, calorias=450)
    bebida2 = Bebida(nombre="Cafe Espresso Double", precio=3.00, disponible=True, volumen=120)
    mi_restaurante.agregar_producto(platillo2)
    mi_restaurante.agregar_producto(bebida2)

    print("\n>>> Ejecutando mi_restaurante.mostrar_productos():")
    print("    El sistema ejecutara: ")
    print("    for producto in self.productos:")
    print("        producto.mostrar_informacion()  <-- Llamada polimorfica dinamica")
    
    mi_restaurante.mostrar_productos()

    print("-" * 78)
    print("¡Polimorfismo demostrado! El bucle llama al mismo metodo de Producto, pero")
    print("obtiene resultados especificos (calorias para Platillo y volumen para Bebida).")
    print("-" * 78)

def ejecutar_didactico() -> None:
    """
    Ejecucion paso a paso interactiva para fines educativos.
    """
    print("\n" + "=" * 78)
    print("             INICIANDO GUIA INTERACTIVA DE CONCEPTOS POO              ")
    print("=" * 78)
    
    # Paso 1: Herencia
    platillo1, bebida1 = demostracion_herencia()
    pausar("Presione Enter para ir al paso de Encapsulamiento...")
    
    # Paso 2: Encapsulamiento
    demostracion_encapsulamiento(platillo1, bebida1)
    pausar("Presione Enter para ir al paso de Polimorfismo...")
    
    # Paso 3: Polimorfismo
    demostracion_polimorfismo(platillo1, bebida1)
    
    print("\n" + "=" * 78)
    print("            ¡FIN DE LA GUIA INTERACTIVA DE CONCEPTOS POO!             ")
    print("=" * 78)
    pausar("Presione Enter para regresar al menu principal.")

def ejecutar_tradicional() -> None:
    """
    Ejecucion clasica de corrido, pero con marcas didacticas sencillas.
    """
    print("\n" + "=" * 78)
    print("                 MODO DE EJECUCION RAPIDA (DE CORRIDO)                ")
    print("=" * 80)
    
    print("\n[HERENCIA] Instanciando productos...")
    platillo1 = Platillo(nombre="Lasana de Carne", precio=12.50, disponible=True, calorias=680)
    platillo2 = Platillo(nombre="Tacos al Pastor (3 uds)", precio=8.00, disponible=True, calorias=450)
    bebida1 = Bebida(nombre="Limonada Imperial", precio=2.50, disponible=True, volumen=400)
    bebida2 = Bebida(nombre="Cafe Espresso Double", precio=3.00, disponible=True, volumen=120)
    print("-> Productos creados correctamente.")

    print("\n[ENCAPSULAMIENTO] Pruebas de acceso y modificacion:")
    print(f" - Precio actual de '{platillo1.nombre}': ${platillo1.obtener_precio():.2f}")
    print(" - Modificando precio a $14.50...")
    platillo1.cambiar_precio(14.50)
    print(f"   Nuevo precio: ${platillo1.obtener_precio():.2f}")
    
    print(" - Modificando precio a -$5.00 (Invalido)...")
    platillo1.cambiar_precio(-5.00)
    print(f"   Precio final: ${platillo1.obtener_precio():.2f} (sin cambios)")

    print("\n[POLIMORFISMO] Imprimiendo el menu desde el Restaurante:")
    mi_restaurante = Restaurante("El Rincon Gourmet")
    mi_restaurante.agregar_producto(platillo1)
    mi_restaurante.agregar_producto(platillo2)
    mi_restaurante.agregar_producto(bebida1)
    mi_restaurante.agregar_producto(bebida2)
    
    mi_restaurante.mostrar_productos()
    
    print("=" * 78 + "\n")
    pausar("Presione Enter para regresar al menu principal.")

def main() -> None:
    """
    Funcion de entrada principal que despliega el menu interactivo para el usuario.
    """
    while True:
        # Limpiar consola si es posible para mejorar la experiencia visual
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
        print("=" * 65)
        print("    SISTEMA DE ADMINISTRACION DE RESTAURANTE - APRENDIZAJE POO  ")
        print("=" * 65)
        print("  Selecciona una opcion para ejecutar el software de forma didactica:")
        print("\n  [1] Modo Guia Didactica (Interactivo Paso a Paso - RECOMENDADO)")
        print("  [2] Modo Ejecucion Rapida (Sin interrupciones)")
        print("  [3] Salir")
        print("=" * 65)
        
        opcion = input("\n> Ingrese el numero de su opcion: ").strip()
        
        if opcion == "1":
            ejecutar_didactico()
        elif opcion == "2":
            ejecutar_tradicional()
        elif opcion == "3":
            print("\n¡Gracias por aprender POO con nosotros! Hasta pronto. \n")
            break
        else:
            print("\n[!] Opcion no valida. Por favor, intente de nuevo.")
            pausar("Presione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEjecucion cancelada por el usuario. ")
        sys.exit(0)
