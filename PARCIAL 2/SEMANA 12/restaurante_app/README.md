# Sistema de Restaurante Gourmet - Semana 12
## Optimización de Búsquedas, Consultas y Validaciones con Colecciones en Python

**Asignatura:** Programación Orientada a Objetos  
**Carrera:** Ingeniería en Tecnologías de la Información  
**Estudiante:** Lilibeth Demera  
**Docente:** Msc. Edison Zambrano  
**Período Académico:** Segundo Semestre  

---

## 1. Introducción y Propósito

El presente proyecto corresponde a la **Semana 12** de la asignatura. Tomando como base la arquitectura modular desarrollada en la Semana 11, esta versión se enfoca en la optimización de las operaciones de búsqueda, validación y consulta mediante la aplicación estratégica de **colecciones en memoria** (`dict`, `set`, `list` y `tuple`).

El principio fundamental aplicado es: **optimizar no significa descartar las listas**, sino complementarlas con estructuras auxiliares basadas en hashing cuando existe una clave de búsqueda conocida (como el código de un producto o la identificación de un usuario).

---

## 2. Colecciones Utilizadas en el Proyecto

En la solución implementada se utilizan cuatro tipos de colecciones nativas de Python, cada una asignada al rol donde maximiza su eficiencia y claridad conceptual:

| Colección | Rol en el Sistema | Justificación de Uso |
| :--- | :--- | :--- |
| **`list` (Listas)** | `_productos`, `_usuarios`, `_ventas` | Almacenamiento principal y secuencial. Preservan el orden de registro, facilitan el recorrido para reportes y listados completos, y sirven como base para la serialización y persistencia en formato JSON (listas de diccionarios). |
| **`dict` (Diccionarios)** | `_productos_por_codigo`, `_usuarios_por_identificacion`, `_ventas_por_usuario`, `acciones_menu` | Tablas de dispersión (hash maps) que permiten búsquedas, validaciones de unicidad y agrupaciones en tiempo constante $O(1)$, evitando escaneos lineales costosos. En `main.py` actúa además como despachador dinámico de opciones. |
| **`set` (Conjuntos)** | `obtener_categorias_unicas()` | Colección no ordenada de elementos únicos. Garantiza la deduplicación matemática inmediata de categorías de platos sin requerir validaciones condicionales repetitivas. |
| **`tuple` (Tuplas)** | `MENU_OPCIONES` | Colección inmutable empleada en la interfaz de consola para garantizar que las opciones del menú permanezcan íntegras e inalterables durante toda la ejecución. |

---

## 3. Justificación de Diseño: `list` vs. `dict` y `set`

### ¿Por qué se mantuvieron las Listas (`list`)?
1. **Preservación del orden:** Al listar productos o usuarios en consola, el orden de inserción proporciona previsibilidad y coherencia visual para el usuario final.
2. **Compatibilidad con persistencia JSON:** El formato estándar de almacenamiento en disco requiere listas serializables (`[{...}, {...}]`). Mantener listas como colecciones maestras asegura que no se altere el esquema JSON original.
3. **Recorridos completos inevitables:** Operaciones como listar todo el catálogo o presentar todas las cuentas registradas requieren visitar cada elemento; en estos casos, una lista es óptima y no añade sobrecarga de índices.

### ¿Por qué se introdujeron Diccionarios (`dict`) y Conjuntos (`set`)?
1. **Búsquedas directas en tiempo constante $O(1)$:** En la Semana 11, buscar un producto por su código o un usuario por su cédula requería un bucle `for` que recorría la lista elemento a elemento ($O(N)$). Con diccionarios auxiliares indexados por clave normalizada (`codigo.lower().strip()`), el acceso es instantáneo mediante tablas hash.
2. **Validación de unicidad en $O(1)$:** Antes de insertar un nuevo producto o usuario, verificar si el código ya existía exigía otro escaneo lineal $O(N)$. Con `dict`, la consulta `clave in self._productos_por_codigo` toma tiempo constante $O(1)$.
3. **Agrupamiento indexado de ventas:** Consultar las ventas de un cliente particular implicaba recorrer todo el historial global de transacciones ($O(V)$). Con `_ventas_por_usuario`, las compras se recuperan directamente en $O(1)$ para la búsqueda del usuario y $O(k)$ para la lectura de sus $k$ transacciones.
4. **Deduplicación automática de categorías:** Con `set`, las categorías únicas se obtienen mediante comprensión de conjuntos en una sola pasada $O(N)$, eliminando duplicados a nivel de hashing sin comprobaciones manuales `if cat not in lista`.

---

## 4. Tabla Comparativa de Operaciones Optimizadas

| Operación | Semana 11 (Listas puras) | Complejidad S11 | Semana 12 (Colecciones Optimizadas) | Complejidad S12 | Beneficio Obtenido |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **Búsqueda de producto por código** | Recorrido lineal `for p in self._productos` | $O(N)$ | Acceso directo `self._productos_por_codigo.get(clave)` | $O(1)$ | Tiempo de respuesta inmediato e independiente del tamaño del catálogo. |
| **Validación de código duplicado al registrar** | Bucle `for p in self._productos:` con comparación | $O(N)$ | Verificación en tabla hash `clave in self._productos_por_codigo` | $O(1)$ | Validación instantánea antes de instanciar o almacenar. |
| **Búsqueda de usuario por identificación** | Recorrido secuencial `for u in self._usuarios` | $O(N)$ | Acceso directo `self._usuarios_por_identificacion.get(clave)` | $O(1)$ | Verificación inmediata durante ventas y consultas. |
| **Validación de identificación de usuario** | Bucle `for u in self._usuarios:` | $O(N)$ | Verificación en tabla hash `clave in self._usuarios_por_identificacion` | $O(1)$ | Prevención de duplicados en tiempo constante. |
| **Consulta de ventas de un usuario** | Bucle `for venta in self._ventas:` recorriendo todo el histórico | $O(V)$ *(donde $V$ es el total de ventas)* | Acceso al bucket agrupado `self._ventas_por_usuario.get(clave, [])` | $O(1)$ lookup + $O(k)$ lectura *(donde $k \ll V$)* | Aislamiento total de las transacciones del cliente sin revisar ventas ajenas. |
| **Obtención de categorías únicas** | Bucle `for` con agregación condicional a conjunto | $O(N)$ | Comprensión de conjuntos `{p.categoria for p in self._productos}` | $O(N)$ nativo | Código limpio, declarativo y optimizado en CPython. |
| **Despacho del menú principal** | Diccionario de llamadas (`dict`) con tupla de opciones | $O(1)$ | Diccionario de llamadas (`dict`) con tupla de opciones | $O(1)$ | Estabilidad inmutable del menú y navegación fluida. |

---

## 5. Sincronización entre Colecciones Principales y Auxiliares

Para evitar inconsistencias en memoria, toda operación que mute los datos (creación, edición, borrado o venta) actualiza **en el mismo instante** tanto la lista principal como las estructuras auxiliares:

### A. Registro (Alta de Producto / Usuario)
```python
# Validación en O(1)
clave = producto.codigo.strip().lower()
if clave in self._productos_por_codigo:
    raise ValueError(f"Ya existe un producto registrado con el código '{producto.codigo}'.")

# Sincronización atómica en memoria
self._productos.append(producto)              # Colección principal (list)
self._productos_por_codigo[clave] = producto  # Índice auxiliar (dict)
```

### B. Modificación (Actualización de Producto)
```python
# Búsqueda en O(1) a través del índice
producto = self.buscar_producto(codigo)
if producto:
    # Al modificar las propiedades del objeto referenciado,
    # el cambio se refleja automáticamente en la lista y en el diccionario
    # ya que ambas estructuras apuntan a la misma instancia en memoria heap.
    producto.nombre = nuevo_nombre
    producto.categoria = nueva_categoria
    producto.precio = nuevo_precio
    producto.stock = nuevo_stock
    return True
return False
```

### C. Eliminación (Baja de Producto)
```python
clave = codigo.strip().lower()
if clave in self._productos_por_codigo:
    # Se extrae del diccionario auxiliar y se remueve de la lista principal
    producto = self._productos_por_codigo.pop(clave)
    self._productos.remove(producto)
    return True
return False
```

### D. Transacción de Venta (Registro y Agrupamiento)
```python
# Inserción en la lista global de auditoría
self._ventas.append(nueva_venta)

# Inserción en el índice auxiliar agrupado por usuario
clave_u = usuario.identificacion.strip().lower()
if clave_u not in self._ventas_por_usuario:
    self._ventas_por_usuario[clave_u] = []
self._ventas_por_usuario[clave_u].append(nueva_venta)
```

### E. Reconstrucción de Índices tras Persistencia
Al arrancar la aplicación o cargar los archivos JSON, los métodos del servicio reconstruyen íntegramente las estructuras auxiliares a partir de los datos leídos:
```python
def actualizar_catalogo_productos(self, productos: List[Producto]) -> None:
    self._productos = list(productos)
    self._productos_por_codigo = {p.codigo.strip().lower(): p for p in self._productos}
```

---

## 6. Estructura del Proyecto

```
PARCIAL 2/SEMANA 12/restaurante_app/
├── datos/
│   ├── productos.json       # Persistencia de productos en lista de diccionarios
│   ├── usuarios.json        # Persistencia de usuarios en lista de diccionarios
│   └── ventas.json          # Persistencia de ventas en lista de diccionarios
├── modelos/
│   ├── __init__.py          # Inicializador del paquete de modelos
│   ├── producto.py          # Clase Producto con getters, setters y control de stock
│   ├── usuario.py           # Clase Usuario con validación de identidad y correo
│   └── venta.py             # Clase Venta que relaciona usuario, producto y cantidad
├── servicios/
│   ├── __init__.py          # Inicializador del paquete de servicios
│   ├── archivo_servicio.py  # Manejador de persistencia JSON con manejo robusto de excepciones
│   └── restaurante.py       # Lógica del negocio, colecciones principales e índices auxiliares O(1)
├── main.py                  # Interfaz de consola interactiva y ciclo de ejecución del menú
└── README.md                # Documentación técnica completa del proyecto
```

---

## 7. Instrucciones de Ejecución

### Requisitos Previos
- Python 3.8 o superior instalado en el sistema.
- Consola de comandos (PowerShell, CMD, o Terminal).

### Pasos para Ejecutar
1. Abra una terminal en la raíz del proyecto o navegue directamente a la carpeta de la Semana 12:
   ```powershell
   cd "c:\Users\LILIBETH DEMERA\OneDrive\Desktop\Segundo semestre\PROGRAMACIÓN ORIENTADA A OBJETOS\UEA\2626-POO-DEMERA-LILIBETH\PARCIAL 2\SEMANA 12\restaurante_app"
   ```
2. Ejecute el módulo principal con el intérprete de Python:
   ```powershell
   python main.py
   ```
3. El sistema verificará los archivos de persistencia en la carpeta `datos/`, cargará los registros predeterminados si es la primera ejecución y desplegará el menú interactivo en consola con colores ANSI.
