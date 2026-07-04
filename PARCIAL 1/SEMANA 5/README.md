# Sistema de Gestión de Restaurante - Semana 5

## 📋 Descripción del Proyecto

Este proyecto es una actividad de la **Semana 5** de la asignatura **Programación Orientada a Objetos (POO)**. El objetivo es aplicar correctamente los identificadores, las convenciones de nombres y los tipos de datos básicos en un proyecto Python modular.

Se desarrolló un sistema básico de gestión de restaurante que demuestra el uso de:
- **Clases y Objetos**
- **Constructores (`__init__`)**
- **Atributos y Métodos**
- **Método especial `__str__()`**
- **Importaciones entre módulos**
- **Listas como tipo de dato compuesto**
- **Anotaciones de tipo**
- **Buenas prácticas de código**

---

## 🏗️ Estructura del Proyecto

```
restaurante_app/
├── modelos/
│   ├── __init__.py           # Inicializa el paquete de modelos
│   ├── producto.py           # Clase Producto
│   └── cliente.py            # Clase Cliente
├── servicios/
│   ├── __init__.py           # Inicializa el paquete de servicios
│   └── restaurante.py        # Clase Restaurante
└── main.py                   # Punto de entrada del programa
```

---

## 📚 Descripción de Clases

### 1. Clase `Producto` (modelos/producto.py)

Representa un producto del restaurante.

**Atributos:**
- `nombre: str` - Nombre del producto
- `precio: float` - Precio en dólares
- `cantidad_disponible: int` - Cantidad en inventario
- `es_disponible: bool` - Disponibilidad actual

**Métodos principales:**
- `__init__()` - Constructor
- `__str__()` - Representación en texto
- `reducir_stock(cantidad)` - Reduce el inventario
- `aumentar_stock(cantidad)` - Aumenta el inventario
- `cambiar_disponibilidad(es_disponible)` - Cambia disponibilidad

### 2. Clase `Cliente` (modelos/cliente.py)

Representa un cliente del restaurante.

**Atributos:**
- `nombre: str` - Nombre completo
- `correo: str` - Correo electrónico
- `telefono: str` - Número de teléfono
- `es_miembro: bool` - Es cliente frecuente
- `cantidad_visitas: int` - Número de visitas

**Métodos principales:**
- `__init__()` - Constructor
- `__str__()` - Representación en texto
- `registrar_visita()` - Incrementa contador de visitas
- `convertir_a_miembro()` - Cambia estado a miembro
- `obtener_informacion_contacto()` - Retorna contacto

### 3. Clase `Restaurante` (servicios/restaurante.py)

Gestiona los productos y clientes del restaurante.

**Atributos:**
- `nombre: str` - Nombre del restaurante
- `ubicacion: str` - Dirección
- `año_fundacion: int` - Año de fundación
- `productos: List[Producto]` - Lista de productos
- `clientes: List[Cliente]` - Lista de clientes

**Métodos principales:**
- `__init__()` - Constructor
- `agregar_producto()` - Añade producto a la lista
- `agregar_cliente()` - Registra cliente
- `mostrar_productos()` - Imprime listado de productos
- `mostrar_clientes()` - Imprime listado de clientes
- `contar_productos()` - Retorna cantidad de productos
- `contar_clientes()` - Retorna cantidad de clientes
- `contar_miembros()` - Retorna cantidad de miembros
- `obtener_informacion_restaurante()` - Retorna información general

---

## 🚀 Cómo Ejecutar

### Requisitos:
- Python 3.7 o superior

### Pasos:
1. Navega a la carpeta del proyecto:
   ```bash
   cd "PARCIAL 1/SEMANA 5/restaurante_app"
   ```

2. Ejecuta el programa:
   ```bash
   python main.py
   ```

3. El programa mostrará:
   - Creación de productos y clientes
   - Información del restaurante
   - Listados de productos y clientes
   - Demostración de métodos de gestión
   - Información actualizada

---

## ✨ Características Implementadas

✅ **Estructura Modular:** Proyecto organizado en carpetas `modelos` y `servicios`

✅ **Convenciones de Nombres:** 
- `PascalCase` para clases (Producto, Cliente, Restaurante)
- `snake_case` para variables, métodos y archivos

✅ **Tipos de Datos Básicos:**
- `str` - Nombres, correos, ubicación
- `int` - Cantidad, año de fundación, visitas
- `float` - Precio de productos
- `bool` - Disponibilidad, membresía

✅ **Listas Compuestas:** `List[Producto]` y `List[Cliente]` en la clase Restaurante

✅ **Anotaciones de Tipo:** En parámetros y retornos de métodos

✅ **Método Especial `__str__()`:** En todas las clases principales

✅ **Importaciones:** Correctas entre módulos (`from modelos.producto import Producto`)

✅ **Objetos y Métodos:** Mínimo 2 objetos de cada modelo, interacción entre ellos

✅ **Comentarios:** Explicaciones breves de funcionalidad

---

## 📝 Requisitos Cumplidos

- ✅ Estructura de carpetas solicitada
- ✅ Mínimo 2 clases en modelos (Producto, Cliente)
- ✅ 1 clase en servicios (Restaurante)
- ✅ Constructor `__init__()` en todas las clases
- ✅ Identificadores descriptivos
- ✅ Convenciones PascalCase y snake_case
- ✅ Tipos de datos: str, int, float, bool
- ✅ Listas como tipo compuesto
- ✅ Anotaciones de tipo
- ✅ Métodos de gestión
- ✅ Método `__str__()` en clases principales
- ✅ Importaciones correctas
- ✅ Mínimo 2 objetos de cada modelo
- ✅ Objetos agregados a listas
- ✅ Información mostrada en consola
- ✅ Comentarios explicativos
- ✅ No copiar ejemplo de biblioteca
- ✅ No usar nombres genéricos

---

## 🎓 Conceptos Aprendidos

- Creación de clases y objetos
- Constructores y destructores
- Atributos y métodos de instancia
- Encapsulación de datos
- Métodos especiales como `__str__()`
- Importaciones entre módulos
- Uso de listas tipadas
- Anotaciones de tipo (Type Hints)
- Organización modular de proyectos
- Buenas prácticas de nomenclatura

---

## 👨‍💻 Autor

**Estudiante:** LILIBETH DEMERA  
**Asignatura:** Programación Orientada a Objetos (2626)  
**Semana:** Semana 5  
**Semestre:** Segundo Semestre
