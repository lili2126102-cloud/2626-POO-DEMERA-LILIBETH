# 🍽️ Restaurante App - Semana 11 (Venta de Productos y Relaciones Persistentes)

Este proyecto corresponde a la evolución de la aplicación de consola **restaurante_app** de la Semana 10 hacia la **Semana 11**. 

En esta versión se incorporó el registro de relaciones comerciales y transaccionales entre objetos de negocio mediante la operación principal de **Venta de Productos**. Además, se amplió el sistema de persistencia para que almacene y recupere las colecciones de productos (con stock), usuarios y ventas registradas mediante archivos JSON independientes.

---

## 🏗️ Estructura del Proyecto

El proyecto está organizado de manera modular bajo la siguiente jerarquía física de directorios:

```
PARCIAL 2/SEMANA 11/restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py (Modificado: incorporado control de stock)
│   ├── usuario.py
│   └── venta.py (NUEVO: modelo de relación)
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py (Modificado: lectura/escritura de ventas.json y stock)
│   └── restaurante.py (Modificado: lógica de ventas y búsquedas cruzadas)
├── main.py (Modificado: interfaz y flujos interactivos para ventas)
└── README.md
```

### Responsabilidades por Módulo

*   **`modelos/producto.py` (`Producto`)**: Representa los productos del restaurante. Incluye la propiedad encapsulada `stock` que impide valores negativos. Cuenta con el método de negocio `vender(cantidad)` para descontar stock tras validaciones previas.
*   **`modelos/usuario.py` (`Usuario`)**: Representa a la persona registrada que puede comprar.
*   **`modelos/venta.py` (`Venta`)**: Nueva entidad encargada de representar la compra de un producto por parte de un usuario. Conserva las referencias de `usuario_id`, `producto_codigo` y `cantidad`.
*   **`servicios/restaurante.py` (`Restaurante`)**: Administra las colecciones en memoria de productos, usuarios y ventas. Ejecuta la lógica central de negocio, incluyendo la búsqueda de usuarios y la ejecución segura de la venta de un producto.
*   **`servicios/archivo_servicio.py` (`ArchivoServicio`)**: Concentra la lectura y escritura física de los archivos JSON (`productos.json`, `usuarios.json` y `ventas.json`).
*   **`main.py`**: Punto de entrada que coordina el menú interactivo, la entrada/salida de datos por consola, captura excepciones y previene la manipulación directa de colecciones internas.

---

## 🔁 Relación Comercial: Usuario + Producto ➔ Venta

El flujo de negocio principal para la transacción de una venta se compone de los siguientes pasos:

1.  **Ingreso**: El usuario selecciona la opción "Realizar venta de producto" e ingresa la identificación del comprador, el código del producto y la cantidad deseada.
2.  **Validación de Existencia**: El sistema busca que el usuario comprador y el producto existan en los registros.
3.  **Validación de Cantidad y Disponibilidad**: Se comprueba que la cantidad solicitada sea estrictamente mayor que cero y no supere el stock disponible del producto.
4.  **Generación de la Venta**: Se crea un objeto `Venta` y se añade a la colección en memoria.
5.  **Deducción de Stock**: Se disminuye la cantidad del producto mediante `producto.vender(cantidad)`.
6.  **Persistencia**: Se sobrescriben de inmediato los archivos `ventas.json` y `productos.json` para reflejar la transacción y el stock actualizado físicamente.

---

## 💾 Persistencia de Datos y Manejo de Excepciones

El sistema cuenta con un control de excepciones de bajo nivel para garantizar la robustez durante la lectura/escritura JSON:

*   **`FileNotFoundError`**: Si algún archivo JSON no existe (por ejemplo, en la primera ejecución), la aplicación arranca con el catálogo correspondiente vacío o carga registros por defecto y crea los archivos necesarios de forma transparente.
*   **`json.JSONDecodeError`**: Si la estructura física de algún archivo JSON está rota o corrupta, el cargador captura el error, informa al usuario y permite iniciar la aplicación con listas vacías en lugar de cerrarse bruscamente.
*   **`PermissionError`**: Si el sistema carece de permisos de lectura o escritura sobre la carpeta de datos, se alerta amigablemente sin corromper el hilo principal.
*   **`KeyError`**: Si se manipula el archivo JSON y falta alguna propiedad requerida (por ejemplo, el stock en productos), se descarta el registro defectuoso informando su índice y se cargan los demás registros válidos.
*   **`ValueError`**: Gestionado a nivel de setter para impedir que se instancien productos con precios negativos/cero, stock negativo o ventas con cantidades incorrectas.

---

## 🚀 Instrucciones de Ejecución

### Requisitos:
*   Python 3.8 o superior instalado.
*   Consola o terminal compatible con secuencias de escape de color ANSI.

### Pasos para Ejecutar:
1.  Abra una terminal y navegue al directorio del proyecto:
    ```bash
    cd "PARCIAL 2/SEMANA 11/restaurante_app"
    ```
2.  Inicie el programa interactivo:
    ```bash
    python main.py
    ```

---

## 🧪 Guía de Pruebas y Verificación

Siga los siguientes pasos para certificar que el sistema cumple con todos los requisitos funcionales y de persistencia:

1.  **Inicio Inicial**: Ejecute `main.py`. Verifique que se carguen los productos de ejemplo con stock inicial (por ejemplo, Bife de Chorizo tiene 15 unidades) y usuarios iniciales.
2.  **Verificación de Productos**: Ingrese al menú opción `5` (Listar productos). Observe el atributo `Stock` reflejado en cada producto del menú.
3.  **Realizar una Venta exitosa**: Ingrese a la opción `9` (Realizar venta de producto).
    *   Ingrese la identificación de un usuario (ejemplo: `1700000001`).
    *   Ingrese el código del producto a vender (ejemplo: `P100`).
    *   Ingrese la cantidad a comprar (ejemplo: `3`).
    *   Confirme que el sistema muestre un mensaje de éxito.
4.  **Confirmar Descuento de Stock**: Seleccione de nuevo la opción `5`. Observe que el stock del producto `P100` disminuyó de 15 a 12.
5.  **Confirmar Persistencia Física**: Abra los archivos en la carpeta `datos/`:
    *   `productos.json` debe reflejar la actualización de stock en el producto `P100`.
    *   `ventas.json` debe contener el registro de la venta con la estructura `{"usuario_id": "1700000001", "producto_codigo": "P100", "cantidad": 3}`.
6.  **Consultar Ventas del Usuario**: Ingrese a la opción `10` (Consultar ventas de un usuario). Ingrese la identificación `1700000001`. El sistema mostrará la lista de compras del usuario, el subtotal por compra y el total acumulado invertido.
7.  **Persistencia tras Cierre**: Salga del programa con la opción `11` (Salir). Ejecute nuevamente `python main.py`. Confirme en los mensajes de consola y listados que los productos recuperan su stock actualizado (12 unidades) y que se recuperó la venta del archivo.
8.  **Rechazo de Ventas Inválidas**: Intente comprar una cantidad mayor al stock disponible (por ejemplo, intente comprar 20 unidades del producto `P100`). Confirme que el sistema muestra un error de stock insuficiente, rechaza la operación, no añade nada al JSON y no altera el stock en memoria ni en disco.
