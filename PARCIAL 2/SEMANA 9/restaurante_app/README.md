# 🍽️ Restaurante App - Semana 9 (Estructuras de Datos)

Este proyecto corresponde a la evolución de la aplicación de consola **restaurante_app** correspondiente a la Semana 9. En esta versión se han incorporado las principales estructuras de datos de Python (`list`, `tuple`, `dict` y `set`) de manera justificada y funcional para administrar los datos del sistema, manteniendo una estricta separación de responsabilidades entre modelos, servicios y la interfaz de consola.

---

## 🏗️ Estructura del Proyecto de la Semana 9

El proyecto conserva una organización modular y limpia:

```
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   └── restaurante.py
├── main.py
└── README.md
```

### Responsabilidad de cada archivo:
*   **`modelos/producto.py` (`Producto`)**: Clase que representa los atributos de un producto (código, nombre, categoría y precio). Cuenta con encapsulación y setters con validación de tipo y valores.
*   **`modelos/usuario.py` (`Usuario`)**: Clase que representa a las personas registradas en el sistema (identificación, nombre, correo). Reemplaza a la clase `Cliente` de semanas anteriores con un enfoque más generalizable.
*   **`servicios/restaurante.py` (`Restaurante`)**: Servicio encargado de administrar las colecciones en memoria, validar la unicidad (evitar códigos de producto o identificaciones de usuario duplicadas), y proveer operaciones CRUD.
*   **`main.py`**: Punto de inicio de la aplicación que coordina el menú y la interacción de la consola, validando las entradas del usuario e invocando los servicios.
*   **`README.md`**: Este archivo de documentación técnica.

---

## 📊 Justificación y Aplicación de las Estructuras de Datos

Las cuatro estructuras de datos principales de Python se han integrado para resolver necesidades de negocio específicas:

### 1. Lista (`list`)
*   **Uso en el sistema:** Colección dinámica de productos (`self._productos`) y usuarios (`self._usuarios`).
*   **Justificación:** Las listas en Python son colecciones ordenadas y mutables perfectas para gestionar catálogos que crecen dinámicamente. Permiten registrar (`append`), buscar (recorriendo la lista), actualizar y eliminar (`remove`) objetos en tiempo de ejecución.
*   **Buenas prácticas:** Para cumplir con el principio de encapsulación y evitar que `main.py` manipule directamente los datos, los getters `Restaurante.productos` y `Restaurante.usuarios` devuelven copias de las listas (`list(self._productos)`).

### 2. Tupla (`tuple`)
*   **Uso en el sistema:** Las opciones estables del menú principal (`MENU_OPCIONES` en `main.py`).
*   **Justificación:** Las tuplas son inmutables. Es una excelente práctica almacenar textos de menús u otras constantes del sistema en tuplas para garantizar que no se alteren accidentalmente en tiempo de ejecución.

### 3. Diccionario (`dict`)
*   **Uso en el sistema:** Ruteo dinámico de opciones del menú a funciones controladoras (`acciones_menu` en `main.py`).
*   **Justificación:** Un diccionario permite mapear de forma directa una clave única (la opción seleccionada por el usuario como `"1"`, `"2"`, etc.) con un valor (la función controladora como `registrar_producto_ui`, `buscar_producto_ui`, etc.). Esto elimina la necesidad de escribir largas estructuras condicionales `if/elif/else`, haciendo que el código del menú sea más legible, limpio y mantenible.

### 4. Conjunto (`set`)
*   **Uso en el sistema:** Obtención de categorías únicas de productos registrados (`obtener_categorias_unicas` en `Restaurante`).
*   **Justificación:** Los conjuntos no permiten elementos duplicados. Al recorrer los productos del menú, se agregan sus categorías a un conjunto. La propiedad matemática del `set` filtra de manera automática y eficiente los duplicados, permitiendo mostrar al usuario únicamente las categorías que existen en el catálogo (por ejemplo, mostrar "Carnes", "Bebidas" y "Postres" una sola vez, sin importar cuántos productos pertenezcan a ellas).

---

## 🚀 Instrucciones de Ejecución

### Requisitos:
*   Python 3.8 o superior instalado.
*   Consola/Terminal compatible con colores ANSI (PowerShell, Terminal de Windows, Bash, etc.).

### Pasos:
1.  Abra su terminal en la carpeta de la Semana 9:
    ```bash
    cd "PARCIAL 1/SEMANA 9/restaurante_app"
    ```
2.  Ejecute la aplicación:
    ```bash
    python main.py
    ```

El sistema cargará automáticamente un catálogo inicial con 4 productos y 2 usuarios de prueba para que pueda experimentar inmediatamente con búsquedas, listados y categorías.
