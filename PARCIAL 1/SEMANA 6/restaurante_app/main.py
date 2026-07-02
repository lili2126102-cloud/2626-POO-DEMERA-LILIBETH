import sys
import os

# Agregamos la ruta del directorio actual al path por si se ejecuta desde directorios externos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.platillo import Platillo
from modelos.bebida import Bebida
from servicios.restaurante import Restaurante

def ejecutar_sistema():
    """
    Función principal que arranca el sistema restaurante_app.
    Crea objetos, interactúa con el servicio y demuestra encapsulación y polimorfismo.
    """
    print("\n" + "=" * 55)
    print("      SISTEMA DE ADMINISTRACIÓN DE RESTAURANTE - POO      ")
    print("=" * 55 + "\n")

    # 1. Instanciamos el servicio principal (Restaurante)
    mi_restaurante = Restaurante("El Rincón Gourmet")

    # 2. Creación de objetos de tipo Platillo (Herencia de Producto)
    print("--- REGISTRO DE PRODUCTOS ---")
    platillo1 = Platillo(nombre="Lasaña de Carne", precio=12.50, disponible=True, calorias=680)
    platillo2 = Platillo(nombre="Tacos al Pastor (3 uds)", precio=8.00, disponible=True, calorias=450)

    # 3. Creación de objetos de tipo Bebida (Herencia de Producto)
    bebida1 = Bebida(nombre="Limonada Imperial", precio=2.50, disponible=True, volumen=400)
    bebida2 = Bebida(nombre="Café Espresso Double", precio=3.00, disponible=True, volumen=120)

    # 4. Registrar los objetos en el servicio Restaurante
    mi_restaurante.agregar_producto(platillo1)
    mi_restaurante.agregar_producto(platillo2)
    mi_restaurante.agregar_producto(bebida1)
    mi_restaurante.agregar_producto(bebida2)

    print("\n--- PRUEBA DE ENCAPSULACIÓN Y VALIDACIÓN ---")
    # Intentar obtener el precio usando el método Getter
    print(f"Precio actual de '{platillo1.nombre}': ${platillo1.obtener_precio():.2f}")

    # Intentar modificar el precio con un valor VÁLIDO (Setter)
    print(f"Modificando precio de '{platillo1.nombre}' a $14.50...")
    if platillo1.cambiar_precio(14.50):
        print(f"-> Nuevo precio actualizado: ${platillo1.obtener_precio():.2f}")
    
    # Intentar modificar el precio con un valor NEGATIVO (Validación)
    print(f"Modificando precio de '{platillo1.nombre}' a -$5.00...")
    platillo1.cambiar_precio(-5.00)  # Esto debe mostrar un mensaje de error y mantener el precio
    print(f"-> Precio de '{platillo1.nombre}' tras intento negativo: ${platillo1.obtener_precio():.2f}")

    # Intentar modificar el precio con un valor CERO (Validación)
    print(f"Modificando precio de '{bebida1.nombre}' a $0.00...")
    bebida1.cambiar_precio(0.00)  # Esto debe mostrar un mensaje de error y mantener el precio
    print(f"-> Precio de '{bebida1.nombre}' tras intento cero: ${bebida1.obtener_precio():.2f}")

    # 5. Mostrar la información completa del menú registrado (Polimorfismo)
    # Al recorrer la lista de productos, cada objeto invocará su correspondiente mostrar_informacion().
    mi_restaurante.mostrar_productos()

if __name__ == "__main__":
    ejecutar_sistema()
