# Programación Orientada a Objetos (POO) - Semana 9

## Información del Estudiante
* **Nombre Completo:** LILIBETH DEMERA
* **Asignatura:** Programación Orientada a Objetos (2626)
* **Semestre:** Segundo Semestre
* **Institución:** UEA - Universidad Estatal

---

## 🍽️ Descripción del Sistema: restaurante_app (Semana 9)
El proyecto **restaurante_app** es una aplicación de consola en Python diseñada para gestionar la administración de productos y usuarios de un restaurante de manera modular. En esta versión correspondiente a la **Semana 9**, el enfoque del diseño evoluciona desde el manejo de objetos individuales hacia la administración organizada de colecciones de objetos utilizando las **estructuras de datos fundamentales de Python**:
1.  **Listas (`list`)** para administración de colecciones dinámicas.
2.  **Tuplas (`tuple`)** para la representación de datos estables (menú principal).
3.  **Diccionarios (`dict`)** para el mapeo clave-valor y ruteo dinámico de funciones.
4.  **Conjuntos (`set`)** para filtrado automático de valores únicos (categorías).

El sistema mantiene una separación de responsabilidades estricta distribuyendo el diseño en **modelos**, **servicios** e **interfaz de consola (main.py)**. Adicionalmente, cuenta con soporte de colores ANSI y control robusto de excepciones y validaciones interactivas.

---

## 🏗️ Estructura del Proyecto

El proyecto se organiza de la siguiente manera dentro del espacio de la Semana 9:

```
2626-POO-DEMERA-LILIBETH/
└── PARCIAL 1/
    └── SEMANA 9/
        └── restaurante_app/
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

---

## 📋 Responsabilidad de cada Clase y Componente

*   **`modelos/producto.py` (`Producto`)**:
    Representa la información propia de cada producto (código, nombre, categoría y precio). Aplica encapsulación mediante propiedades (`@property` y `@setter`) para controlar la lectura y modificación de sus atributos con validaciones estrictas que evitan valores vacíos o numéricos menores o iguales a cero.
*   **`modelos/usuario.py` (`Usuario`)**:
    Representa la información general de una persona registrada en el sistema (identificación, nombre y correo). Permite que el restaurante evolucione posteriormente hacia diferentes tipos de usuarios sin necesidad de una jerarquía compleja por ahora.
*   **`servicios/restaurante.py` (`Restaurante`)**:
    Clase de servicio encargada de administrar las colecciones del sistema. Centraliza las búsquedas, registros, actualizaciones, eliminaciones y validaciones de unicidad (evita códigos de productos o identificaciones de usuarios duplicados).
*   **`main.py`**:
    Punto de arranque que muestra el menú, solicita datos por consola, captura excepciones de validación en bucles de reintento interactivos y utiliza el servicio mediante un ruteo dinámico basado en diccionarios.

---

## 📊 Aplicación y Justificación de Estructuras de Datos

| Estructura | Aplicación Concreta en el Sistema | Justificación Técnica |
| :--- | :--- | :--- |
| **Lista (`list`)** | Colecciones internas de productos (`self._productos`) y usuarios (`self._usuarios`) en el servicio. | Son colecciones dinámicas y mutables, ideales para registrar (`append`), eliminar (`remove`), actualizar y listar objetos cuyo volumen cambia en tiempo de ejecución. |
| **Tupla (`tuple`)** | Definición inmutable de opciones del menú principal (`MENU_OPCIONES` en `main.py`). | Colección indexable e inmutable. Protege la información del menú de modificaciones accidentales en tiempo de ejecución, garantizando estabilidad en el flujo visual del programa. |
| **Diccionario (`dict`)** | Mapeo directo de opción seleccionada a función de UI correspondiente (`acciones_menu` en `main.py`). | Estructura clave-valor ideal para ruteo directo. Elimina los extensos bloques condicionales (`if/elif/else`), facilitando la escalabilidad del menú y mejorando la legibilidad. |
| **Conjunto (`set`)** | Filtrado y presentación de categorías de productos sin elementos duplicados (`obtener_categorias_unicas`). | Colección de elementos únicos no ordenados. Elimina automáticamente la duplicidad de valores repetidos en las categorías al agregar elementos al catálogo. |

---

## 🚀 Instrucciones de Ejecución

### Requisitos:
*   Python 3.8 o superior instalado.
*   Terminal que soporte secuencias de escape ANSI (como PowerShell en Windows 10/11, terminal en Linux/macOS).

### Pasos de ejecución:
1.  Abra una terminal en el directorio raíz del proyecto.
2.  Acceda a la carpeta del restaurante para la Semana 9:
    ```bash
    cd "PARCIAL 1/SEMANA 9/restaurante_app"
    ```
3.  Ejecute el archivo principal:
    ```bash
    python main.py
    ```

El programa se cargará con datos iniciales (4 productos y 2 usuarios de prueba) para que las funciones del sistema puedan visualizarse de forma inmediata.
