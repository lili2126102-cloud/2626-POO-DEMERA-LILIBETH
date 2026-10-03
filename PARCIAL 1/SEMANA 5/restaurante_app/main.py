# Archivo principal - Punto de entrada del sistema de gestión de restaurante

from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


def main():
    """Función principal que ejecuta el programa."""
    
    # Crear instancia del restaurante
    mi_restaurante = Restaurante(
        nombre="La Delizia",
        ubicacion="Calle Principal 123, Centro",
        año_fundacion=2010
    )
    
    # Crear productos y agregarlos al restaurante
    print("=" * 60)
    print("CREANDO PRODUCTOS...")
    print("=" * 60)
    
    producto1 = Producto(
        nombre="Pasta Carbonara",
        precio=12.50,
        cantidad_disponible=15,
        es_disponible=True
    )
    print(f"✓ Producto creado: {producto1.nombre}")
    
    producto2 = Producto(
        nombre="Ensalada César",
        precio=8.75,
        cantidad_disponible=20,
        es_disponible=True
    )
    print(f"✓ Producto creado: {producto2.nombre}")
    
    producto3 = Producto(
        nombre="Pizza Margherita",
        precio=10.00,
        cantidad_disponible=10,
        es_disponible=False
    )
    print(f"✓ Producto creado: {producto3.nombre}")
    
    # Agregar productos al restaurante
    mi_restaurante.agregar_producto(producto1)
    mi_restaurante.agregar_producto(producto2)
    mi_restaurante.agregar_producto(producto3)
    
    # Crear clientes y agregarlos al restaurante
    print("\n" + "=" * 60)
    print("CREANDO CLIENTES...")
    print("=" * 60)
    
    cliente1 = Cliente(
        nombre="Juan García",
        correo="juan.garcia@email.com",
        telefono="555-1234",
        es_miembro=True,
        cantidad_visitas=5
    )
    print(f"✓ Cliente creado: {cliente1.nombre}")
    
    cliente2 = Cliente(
        nombre="María López",
        correo="maria.lopez@email.com",
        telefono="555-5678",
        es_miembro=False,
        cantidad_visitas=1
    )
    print(f"✓ Cliente creado: {cliente2.nombre}")
    
    cliente3 = Cliente(
        nombre="Carlos Rodríguez",
        correo="carlos.rodriguez@email.com",
        telefono="555-9999",
        es_miembro=True,
        cantidad_visitas=8
    )
    print(f"✓ Cliente creado: {cliente3.nombre}")
    
    # Agregar clientes al restaurante
    mi_restaurante.agregar_cliente(cliente1)
    mi_restaurante.agregar_cliente(cliente2)
    mi_restaurante.agregar_cliente(cliente3)
    
    # Mostrar información del restaurante
    print("\n" + "=" * 60)
    print("INFORMACIÓN DEL RESTAURANTE")
    print("=" * 60)
    print(mi_restaurante.obtener_informacion_restaurante())
    
    # Mostrar listado de productos
    mi_restaurante.mostrar_productos()
    
    # Mostrar listado de clientes
    mi_restaurante.mostrar_clientes()
    
    # Realizar acciones adicionales
    print("\n" + "=" * 60)
    print("DEMOSTRANDO MÉTODOS DE GESTIÓN...")
    print("=" * 60)
    
    # Registrar una visita
    cliente2.registrar_visita()
    print(f"✓ Registrada visita para {cliente2.nombre}")
    print(f"  Nuevas visitas: {cliente2.cantidad_visitas}")
    
    # Convertir cliente a miembro
    cliente2.convertir_a_miembro()
    print(f"✓ {cliente2.nombre} convertido a miembro frecuente")
    
    # Reducir stock de un producto
    if producto1.reducir_stock(3):
        print(f"✓ Se vendieron 3 unidades de {producto1.nombre}")
        print(f"  Stock restante: {producto1.cantidad_disponible}")
    
    # Aumentar stock de un producto
    producto3.aumentar_stock(5)
    print(f"✓ Se agregaron 5 unidades de {producto3.nombre}")
    print(f"  Nuevo stock: {producto3.cantidad_disponible}")
    
    # Cambiar disponibilidad de un producto
    producto3.cambiar_disponibilidad(True)
    print(f"✓ {producto3.nombre} ahora está disponible")
    
    # Mostrar información actualizada
    print("\n" + "=" * 60)
    print("INFORMACIÓN ACTUALIZADA DEL RESTAURANTE")
    print("=" * 60)
    print(mi_restaurante.obtener_informacion_restaurante())
    
    # Mostrar listas actualizadas
    mi_restaurante.mostrar_productos()
    mi_restaurante.mostrar_clientes()
    
    print("\n" + "=" * 60)
    print("¡PROGRAMA FINALIZADO EXITOSAMENTE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
