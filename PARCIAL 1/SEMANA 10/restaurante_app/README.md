# 🍽️ Restaurante App - Semana 10 (Persistencia con JSON)

Este proyecto corresponde a la evolución de la aplicación de consola **restaurante_app** correspondiente a la Semana 10. En esta versión se ha incorporado la **persistencia de datos** para productos y usuarios mediante archivos JSON (`productos.json` y `usuarios.json`), garantizando la conservación de los datos registrados entre cierres e inicios de la aplicación.

Se ha diseñado un servicio especializado de manejo de archivos (`ArchivoServicio`) y se ha implementado un control estructurado y robusto de excepciones para prevenir cierres inesperados del programa ante fallos de E/S o datos corruptos.

---

## 🏗️ Estructura del Proyecto de la Semana 10

El proyecto conserva su organización modular e incorpora la carpeta `datos` y el nuevo servicio responsable del almacenamiento persistente:

```
restaurante_app/
├── datos/
│   ├── productos.json (Persistencia de productos)
│   └── usuarios.json (Persistencia de usuarios)
├── modelos/
│   ├── __init__.py
│   ├── producto.py (Modificado: serialización y reconstrucción)
│   └── usuario.py (Modificado: serialización y reconstrucción)
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py (NUEVO: lectura/escritura y excepciones)
│   └── restaurante.py (Modificado: carga de catálogos en memoria)
├── main.py (Modificado: controladores de guardado y carga inicial)
└── README.md
```

### Responsabilidad de cada archivo:
*   **`modelos/producto.py` (`Producto`)**: Representa cada producto. Proporciona el método `to_dict()` para convertir el objeto a un diccionario y el método de clase `from_dict()` para reconstruirlo con sus respectivas validaciones.
*   **`modelos/usuario.py` (`Usuario`)**: Representa cada usuario. Proporciona los métodos homólogos `to_dict()` y `from_dict()` para habilitar su serialización/deserialización JSON.
*   **`servicios/archivo_servicio.py` (`ArchivoServicio`)**: Concentra la lógica de lectura y escritura física de los archivos JSON mediante `json.load()` y `json.dump()`, implementando políticas seguras para el manejo de excepciones.
*   **`servicios/restaurante.py` (`Restaurante`)**: Administra las colecciones en memoria y expone métodos como `actualizar_catalogo_productos()` y `actualizar_catalogo_usuarios()` para sincronizar los datos leídos de los archivos.
*   **`main.py`**: Punto de arranque que gestiona el flujo del menú, carga los datos desde los archivos JSON al iniciar y solicita su guardado automático de forma segura tras realizar registros, actualizaciones o eliminaciones.

---

## 💾 Flujo de Persistencia de Datos

### Guardar Datos
Cuando se registra un nuevo usuario, o cuando un producto es registrado, actualizado o eliminado exitosamente:
1. La colección en memoria del servicio `Restaurante` se actualiza.
2. `main.py` invoca al método de guardado correspondiente del `ArchivoServicio`.
3. Los objetos de negocio se transforman en una lista de diccionarios con `to_dict()`.
4. Los datos se escriben físicamente en `datos/productos.json` o `datos/usuarios.json` usando `json.dump()` con codificación UTF-8 e indentación de 4 espacios.

### Cargar Datos
Al arrancar la aplicación en `main.py`:
1. El sistema invoca los métodos `cargar_productos()` y `cargar_usuarios()` de `ArchivoServicio`.
2. Se lee el archivo físico correspondiente usando `json.load()`.
3. Por cada diccionario recuperado, se llama al método `from_dict()` de la clase correspondiente para reconstruir los objetos de negocio, validando los tipos y reglas antes de ser agregados al catálogo.

---

## ⚠️ Manejo de Excepciones

El sistema está diseñado para que los problemas comunes relacionados con el almacenamiento externo no afecten la estabilidad de la aplicación:

1.  **`FileNotFoundError`**:
    *   *Comportamiento:* Si es la primera vez que se ejecuta la aplicación y los archivos `productos.json` o `usuarios.json` aún no existen en la carpeta `datos/`, el programa lo detecta y continúa su inicio de manera normal. El catálogo de productos comenzará vacío y los usuarios se inicializarán con registros de prueba que se guardarán automáticamente para futuras ejecuciones.
2.  **`json.JSONDecodeError`**:
    *   *Comportamiento:* Si un archivo JSON existe pero su formato no es válido (por ejemplo, tiene texto corrupto o corchetes rotos), el sistema atrapa esta excepción en el inicio, notifica amigablemente el error en consola y arranca el catálogo vacío para que el usuario pueda seguir utilizando el sistema sin cierres abruptos.
3.  **`PermissionError`**:
    *   *Comportamiento:* Si la aplicación carece de permisos del sistema operativo para leer o escribir en la carpeta `datos/` o en los archivos JSON, el servicio lanza esta excepción. El controlador en `main.py` la captura, muestra una advertencia detallada del problema de permisos y evita que el programa se rompa, permitiendo al usuario continuar.
4.  **`KeyError`**:
    *   *Comportamiento:* Si se modifica manualmente un archivo JSON y se omite una clave requerida (por ejemplo, falta la clave `"precio"` en un producto), el método `from_dict()` lanza un `KeyError`. El cargador atrapa este error individualmente por registro, muestra una advertencia en color amarillo especificando el índice del registro dañado y continúa cargando el resto de los productos o usuarios válidos.
5.  **`ValueError`**:
    *   *Comportamiento:* Si los datos recuperados del JSON violan las reglas de validación (por ejemplo, un producto con precio negativo o un usuario con correo sin `@`), los setters de los modelos lanzarán un `ValueError`. El cargador atrapa este error a nivel de registro, lo reporta en consola de forma controlada y continúa reconstruyendo los demás objetos.

---

## 🚀 Instrucciones de Ejecución

### Requisitos:
*   Python 3.8 o superior instalado.
*   Consola/Terminal compatible con colores ANSI.

### Pasos:
1.  Abra su terminal en la carpeta de la Semana 10:
    ```bash
    cd "PARCIAL 1/SEMANA 10/restaurante_app"
    ```
2.  Ejecute la aplicación:
    ```bash
    python main.py
    ```
3.  Pruebe registrar productos y usuarios. Verifique cómo se actualizan automáticamente los archivos dentro de la carpeta `datos/`.
