# Sistema de Gestión de Restaurante

## Descripción
Sistema básico de gestión de restaurante desarrollado en Python utilizando Programación Orientada a Objetos (POO). El objetivo es demostrar la organización de un proyecto en módulos, la separación de responsabilidades y la comunicación entre archivos mediante importaciones.

## Estructura del Proyecto

```
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py      # Clase que representa un producto del restaurante
│   └── cliente.py       # Clase que representa un cliente del restaurante
├── servicios/
│   ├── __init__.py
│   └── restaurante.py   # Clase que gestiona las operaciones principales
└── main.py              # Punto de entrada del programa
```

## Clases Principales

### 1. **Producto** (`modelos/producto.py`)
Representa un producto (plato, bebida o postre) disponible en el restaurante.

**Atributos:**
- `id`: Identificador único del producto
- `nombre`: Nombre del producto
- `descripcion`: Descripción del producto
- `precio`: Precio del producto
- `categoria`: Categoría (plato, bebida, postre)
- `disponible`: Estado de disponibilidad

**Métodos principales:**
- `get_id()`, `get_nombre()`, `get_precio()`, etc.: Getters
- `actualizar_precio()`: Actualiza el precio del producto
- `cambiar_disponibilidad()`: Cambia el estado de disponibilidad
- `mostrar_informacion()`: Muestra la información del producto

### 2. **Cliente** (`modelos/cliente.py`)
Representa a un cliente del restaurante.

**Atributos:**
- `id`: Identificador único (auto-generado)
- `nombre`: Nombre completo del cliente
- `email`: Correo electrónico
- `telefono`: Número de teléfono
- `pedidos_realizados`: Lista de pedidos del cliente

**Métodos principales:**
- `get_id()`, `get_nombre()`, `get_email()`, etc.: Getters
- `set_email()`, `set_telefono()`: Setters
- `agregar_pedido()`: Registra un nuevo pedido
- `contar_pedidos()`: Retorna la cantidad de pedidos
- `mostrar_informacion()`: Muestra la información del cliente

### 3. **Restaurante** (`servicios/restaurante.py`)
Gestiona las operaciones principales del restaurante: productos, clientes y pedidos.

**Atributos:**
- `nombre`: Nombre del restaurante
- `direccion`: Dirección del restaurante
- `productos`: Lista de productos disponibles
- `clientes`: Lista de clientes registrados
- `pedidos`: Lista de pedidos realizados

**Métodos principales:**

**Gestión de Productos:**
- `agregar_producto()`: Agrega un nuevo producto
- `obtener_producto_por_id()`: Busca un producto por ID
- `listar_productos()`: Muestra el menú completo
- `listar_productos_por_categoria()`: Filtra productos por categoría

**Gestión de Clientes:**
- `registrar_cliente()`: Registra un nuevo cliente
- `obtener_cliente_por_id()`: Busca un cliente por ID
- `listar_clientes()`: Muestra todos los clientes

**Gestión de Pedidos:**
- `crear_pedido()`: Crea un nuevo pedido para un cliente
- `listar_pedidos()`: Muestra todos los pedidos realizados
- `obtener_resumen_restaurante()`: Muestra estadísticas generales

## Cómo Ejecutar

### Requisitos
- Python 3.6 o superior
- No requiere librerías externas

### Ejecución
```bash
cd restaurante_app
python main.py
```

## Funcionalidades Demostrables en main.py

1. **Creación de instancia del restaurante**
2. **Agregación de productos** (platos, bebidas, postres)
3. **Listado de productos** (menú completo y por categoría)
4. **Registro de clientes**
5. **Listado de clientes registrados**
6. **Creación de pedidos**
7. **Listado de pedidos realizados**
8. **Visualización de información detallada**
9. **Actualización de datos** (precios, emails, disponibilidad)
10. **Resumen financiero** del restaurante
11. **Manejo de errores** (intentos de crear pedidos con productos no disponibles)

## Conceptos POO Demostrados

- **Encapsulación**: Atributos privados con getters y setters
- **Abstracción**: Métodos que ocultan la complejidad interna
- **Modularización**: Separación de responsabilidades en diferentes módulos
- **Reutilización de código**: Importaciones entre módulos
- **Variables de clase**: Contador automático de IDs en la clase Cliente
- **Validación de datos**: Verificación de disponibilidad y existencia
- **Manejo de errores**: Mensajes de error apropiados

## Autor
Sistema desarrollado como ejercicio de Programación Orientada a Objetos

## Fecha
Junio, 2026

