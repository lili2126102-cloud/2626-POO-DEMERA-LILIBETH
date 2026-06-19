# PUNTO DE ENTRADA DEL SISTEMA DE GESTIÓN DEL RESTAURANTE LYDIA
# Este archivo demuestra el funcionamiento del sistema mediante la creación
# de objetos y la ejecución de métodos del restaurante

from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


def main():
    """
    Función principal que ejecuta la demostración del sistema del restaurante.
    """

    print("\n" + "="*60)
    print("   BIENVENIDO AL SISTEMA DE GESTIÓN DEL RESTAURANTE LYDIA")
    print("="*60 + "\n")

    # Crear instancia del restaurante
    lydia = Restaurante("LYDIA", "Centro Comercial del Alimento")
    print(f"✓ {lydia}\n")

    # === CREAR Y AGREGAR PRODUCTOS ===
    print("\n" + "-"*60)
    print("AGREGANDO PRODUCTOS AL CATÁLOGO")
    print("-"*60)

    # Crear objetos de tipo Producto
    producto1 = Producto("Ceviche de camarones", "plato", 14.99)
    producto2 = Producto("Lomo a la pimienta", "plato", 18.50)
    producto3 = Producto("Ensalada César", "plato", 12.75)
    producto4 = Producto("Refresco natural", "bebida", 3.50)
    producto5 = Producto("Jugo de naranja fresco", "bebida", 4.25)
    producto6 = Producto("Tiramisú", "postre", 6.99)

    # Agregar productos al restaurante
    print(lydia.agregar_producto(producto1))
    print(lydia.agregar_producto(producto2))
    print(lydia.agregar_producto(producto3))
    print(lydia.agregar_producto(producto4))
    print(lydia.agregar_producto(producto5))
    print(lydia.agregar_producto(producto6))

    # === CREAR Y REGISTRAR CLIENTES ===
    print("\n" + "-"*60)
    print("REGISTRANDO CLIENTES EN EL SISTEMA")
    print("-"*60)

    # Crear objetos de tipo Cliente
    cliente1 = Cliente("Juan Pérez", "juan.perez@email.com", "0987654321")
    cliente2 = Cliente("María García", "maria.garcia@email.com", "0987654322")
    cliente3 = Cliente("Carlos López", "carlos.lopez@email.com", "0987654323")

    # Registrar clientes en el restaurante
    print(lydia.agregar_cliente(cliente1))
    print(lydia.agregar_cliente(cliente2))
    print(lydia.agregar_cliente(cliente3))

    # === MOSTRAR INFORMACIÓN ===
    print("\n" + "-"*60)
    print("CATÁLOGO DE PRODUCTOS")
    print("-"*60)
    print(lydia.listar_productos())

    print("\n" + "-"*60)
    print("CLIENTES REGISTRADOS")
    print("-"*60)
    print(lydia.listar_clientes())

    # === REGISTRAR PEDIDOS DE CLIENTES ===
    print("\n" + "-"*60)
    print("REGISTRANDO PEDIDOS")
    print("-"*60)

    print(f"\n{cliente1.nombre} realiza un pedido:")
    print(f"  → {cliente1.registrar_pedido()}")

    print(f"\n{cliente2.nombre} realiza dos pedidos:")
    print(f"  → {cliente2.registrar_pedido()}")
    print(f"  → {cliente2.registrar_pedido()}")

    print(f"\n{cliente3.nombre} realiza un pedido:")
    print(f"  → {cliente3.registrar_pedido()}")

    # === MOSTRAR INFORMACIÓN ACTUALIZADA ===
    print("\n" + "-"*60)
    print("INFORMACIÓN DETALLADA DE CLIENTES")
    print("-"*60)

    for cliente in lydia.clientes:
        print(f"\n{cliente.obtener_informacion()}")

    # === BUSCAR PRODUCTOS Y CLIENTES ===
    print("\n" + "-"*60)
    print("BÚSQUEDAS EN EL SISTEMA")
    print("-"*60)

    producto_buscado = lydia.buscar_producto("Ceviche de camarones")
    if producto_buscado:
        print(f"\n✓ Producto encontrado: {producto_buscado}")
        print(f"   Descripción: {producto_buscado.obtener_descripcion()}")

    cliente_buscado = lydia.buscar_cliente("María García")
    if cliente_buscado:
        print(f"\n✓ Cliente encontrado: {cliente_buscado}")

    # === CAMBIAR DISPONIBILIDAD DE PRODUCTO ===
    print("\n" + "-"*60)
    print("ACTUALIZAR DISPONIBILIDAD DE PRODUCTOS")
    print("-"*60)

    print(f"\n{producto6.nombre} está actualmente {producto6}")
    print(f"  → {producto6.cambiar_disponibilidad(False)}")
    print(f"  → Producto actualizado: {producto6}")

    # === MOSTRAR ESTADÍSTICAS ===
    print(lydia.obtener_estadisticas())

    # === RESUMEN FINAL ===
    print("\n" + "="*60)
    print("   RESUMEN FINAL DEL RESTAURANTE LYDIA")
    print("="*60)
    print(f"\n{lydia}\n")

    print("\n¡Sistema de gestión del restaurante LYDIA ejecutado exitosamente!\n")


# Punto de entrada del programa
if __name__ == "__main__":
    main()

