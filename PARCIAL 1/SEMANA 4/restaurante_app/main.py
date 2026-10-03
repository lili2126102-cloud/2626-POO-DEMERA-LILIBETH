"""
Módulo principal del sistema de gestión de restaurante.
Este archivo demuestra el funcionamiento del sistema mediante la creación
de instancias y la ejecución de métodos de las clases.
"""

from servicios.restaurante import Restaurante


def main():
    """Función principal que ejecuta la demostración del sistema."""

    print("\n" + "="*60)
    print("SISTEMA DE GESTIÓN DE RESTAURANTE")
    print("="*60 + "\n")

    # ========== CREAR INSTANCIA DEL RESTAURANTE ==========
    resto = Restaurante("El Buen Sabor", "Calle Principal #123, Ciudad")

    # Demostración del método __str__() del restaurante
    print(f"[0] INFO DEL RESTAURANTE: {resto}\n")

    # ========== AGREGAR PRODUCTOS ==========
    print("\n[1] AGREGANDO PRODUCTOS AL RESTAURANTE\n")

    # Platos principales
    resto.agregar_producto(1, "Pasta Carbonara", "Pasta con salsa de huevo, jamón y queso", 12.50, "plato")
    resto.agregar_producto(2, "Bistec de Res", "Carne a la parrilla con vegetales", 18.99, "plato")
    resto.agregar_producto(3, "Pechuga de Pollo", "Pechuga rellena de queso y champiñones", 14.75, "plato")
    resto.agregar_producto(4, "Salmón a la Mantequilla", "Salmón fresco con salsa de limón", 22.50, "plato")

    # Bebidas
    resto.agregar_producto(5, "Agua Mineral", "Agua mineral con gas", 2.50, "bebida")
    resto.agregar_producto(6, "Jugo de Naranja", "Jugo natural recién exprimido", 4.00, "bebida")
    resto.agregar_producto(7, "Vino Tinto", "Vino tinto importado", 15.00, "bebida")
    resto.agregar_producto(8, "Refrescos Variados", "Gaseosa variada", 3.00, "bebida")

    # Postres
    resto.agregar_producto(9, "Flan Casero", "Flan tradicional con dulce de leche", 6.50, "postre")
    resto.agregar_producto(10, "Helado Sorpresa", "Helado variado con frutos rojos", 5.00, "postre")

    # ========== LISTAR PRODUCTOS ==========
    print("\n[2] MENÚ DISPONIBLE\n")
    resto.listar_productos()

    # ========== LISTAR POR CATEGORÍA ==========
    print("\n[3] PRODUCTOS POR CATEGORÍA\n")
    resto.listar_productos_por_categoria("plato")
    resto.listar_productos_por_categoria("bebida")

    # ========== REGISTRAR CLIENTES ==========
    print("\n[4] REGISTRANDO CLIENTES\n")
    cliente1 = resto.registrar_cliente("Juan Pérez", "juan.perez@email.com", "555-1234")
    cliente2 = resto.registrar_cliente("María García", "maria.garcia@email.com", "555-5678")
    cliente3 = resto.registrar_cliente("Carlos López", "carlos.lopez@email.com", "555-9012")

    # Demostración del método __str__() de clientes
    print("\nRepresentación de clientes usando __str__():")
    print(f"  • {cliente1}")
    print(f"  • {cliente2}")
    print(f"  • {cliente3}")

    # ========== LISTAR CLIENTES ==========
    print("\n[5] CLIENTES REGISTRADOS\n")
    resto.listar_clientes()

    # ========== CREAR PEDIDOS ==========
    print("\n[6] CREANDO PEDIDOS\n")

    # Pedido 1: Juan Pérez ordena Pasta Carbonara, Vino Tinto y Flan
    pedido1 = resto.crear_pedido(1, [1, 7, 9])

    # Pedido 2: María García ordena Bistec, Jugo y Helado
    pedido2 = resto.crear_pedido(2, [2, 6, 10])

    # Pedido 3: Carlos López ordena Salmón, Agua y Flan
    pedido3 = resto.crear_pedido(3, [4, 5, 9])

    # Pedido adicional del mismo cliente (Juan)
    pedido4 = resto.crear_pedido(1, [3, 8])

    # ========== LISTAR TODOS LOS PEDIDOS ==========
    print("\n[7] RESUMEN DE TODOS LOS PEDIDOS\n")
    resto.listar_pedidos()

    # ========== MOSTRAR INFORMACIÓN DE CLIENTES ==========
    print("\n[8] INFORMACIÓN DETALLADA DE CLIENTES\n")
    cliente1.mostrar_informacion()
    cliente2.mostrar_informacion()
    cliente3.mostrar_informacion()

    # ========== MOSTRAR INFORMACIÓN DE PRODUCTOS ==========
    print("\n[9] INFORMACIÓN DETALLADA DE PRODUCTOS SELECCIONADOS\n")

    # Demostración del método __str__() de productos
    print("Representación de productos usando __str__():")
    producto1 = resto.obtener_producto_por_id(1)
    if producto1:
        print(f"  • {producto1}")
        producto1.mostrar_informacion()

    producto7 = resto.obtener_producto_por_id(7)
    if producto7:
        print(f"  • {producto7}")
        producto7.mostrar_informacion()

    # ========== ACTUALIZAR INFORMACIÓN ==========
    print("\n[10] ACTUALIZANDO INFORMACIÓN\n")

    # Actualizar email de cliente
    cliente1.set_email("juan.perez.nuevo@email.com")
    print(f"✓ Email de {cliente1.get_nombre()} actualizado a: {cliente1.get_email()}")

    # Actualizar precio de un producto
    producto = resto.obtener_producto_por_id(5)
    producto.actualizar_precio(3.00)
    print(f"✓ Precio de {producto.get_nombre()} actualizado a: ${producto.get_precio():.2f}")

    # Cambiar disponibilidad de producto
    producto = resto.obtener_producto_por_id(7)
    producto.cambiar_disponibilidad(False)
    print(f"✓ {producto.get_nombre()} marcado como no disponible")

    # ========== RESUMEN FINAL ==========
    print("\n[11] RESUMEN FINAL DEL RESTAURANTE\n")

    # Mostrar el estado actualizado del restaurante usando __str__()
    print(f"Estado actual del restaurante: {resto}")

    resto.obtener_resumen_restaurante()

    # ========== INTENTAR CREAR PEDIDO CON PRODUCTO NO DISPONIBLE ==========
    print("\n[12] INTENTANDO CREAR PEDIDO CON PRODUCTO NO DISPONIBLE\n")
    pedido_error = resto.crear_pedido(2, [7, 1])  # El producto 7 no está disponible

    print("\n" + "="*60)
    print("FIN DE LA DEMOSTRACIÓN DEL SISTEMA")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

