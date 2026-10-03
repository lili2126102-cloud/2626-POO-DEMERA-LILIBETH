# Sistema Restaurante Gourmet — Semana 16

Aplicación de escritorio desarrollada con Python y Tkinter para gestionar los productos, usuarios y ventas de un restaurante. Esta entrega continúa la aplicación de Semana 15 y conserva el inicio de sesión, la navegación, el catálogo de productos y el registro de ventas. La ampliación se concentra en el CRUD de usuarios y en el uso de eventos `bind()`.

## Requisitos y ejecución

- Python 3.10 o posterior.
- Tkinter, incluido normalmente en las distribuciones de Python para Windows.
- No se requieren paquetes externos.

Esta es una interfaz de escritorio Tkinter, no una página web. Abre en VS Code la carpeta raíz del repositorio del curso, presiona **F5** y selecciona **Ejecutar Semana 16 - Restaurante App**. La configuración establece esta carpeta como directorio de trabajo.

También puedes iniciar desde una terminal abierta en esta carpeta:

```powershell
py -3 main.py
```

## Cuentas de demostración

| Rol | Usuario / correo | Clave |
|---|---|---|
| Administrador | `lilibeth.d@gourmet.com` | `1234` |
| Empleado | `juan.perez@gourmet.com` | `admin123` |
| Cliente | `maria.lopez@gourmet.com` | `gourmet2026` |

Solo la sesión Administrador muestra la pestaña **Gestión de Usuarios**. Los perfiles Empleado y Cliente conservan sus pestañas de Productos y Ventas, pero no tienen acceso a esa gestión.

## Estructura

```text
restaurante_app/
├── assets/                  # Logotipos e íconos usados en la aplicación
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py           # Usuario incluye rol: Administrador, Empleado o Cliente
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py  # Lectura/escritura JSON
│   └── restaurante_servicio.py
├── ui/
│   ├── login_view.py
│   └── main_view.py
└── main.py
```

## Gestión de usuarios y eventos

El administrador puede registrar, consultar, actualizar y eliminar cuentas Empleado o Cliente. El Treeview presenta identificación, nombre, correo/usuario y rol; no muestra claves. Al seleccionar una fila, `<<TreeviewSelect>>` obtiene su identificador y consulta el objeto mediante `RestauranteServicio.buscar_usuario()`. La clave queda vacía al cargar un registro; al actualizar, dejarla vacía conserva la existente.

| Interacción | Mecanismo | Respuesta |
|---|---|---|
| Seleccionar una fila de usuarios | `Treeview.bind("<<TreeviewSelect>>", callback)` | Consulta por identificador y carga los datos en el formulario |
| Elegir un rol | `Combobox.bind("<<ComboboxSelected>>", callback)` | Actualiza el mensaje de estado |
| Presionar Enter en el formulario | `bind("<Return>", callback)` | Reutiliza `_registrar_usuario()` |
| Presionar Escape en el formulario o tabla | `bind("<Escape>", callback)` | Limpia campos y cancela la selección |
| Pulsar Registrar, Actualizar, Eliminar o Limpiar | `command=callback` | Ejecuta la operación correspondiente |

El recorrido mantiene la separación de capas:

```text
interacción → evento → bind() → callback → RestauranteServicio
            → ArchivoServicio → usuarios.json → respuesta en pantalla
```

Las reglas de unicidad de identificación/correo, la validación del rol, la protección de cuentas Administrador y la persistencia están en el servicio/modelo; la interfaz coordina los callbacks y presenta el resultado. La eliminación pide confirmación y rechaza borrar la cuenta administrativa autenticada.

Los datos de usuarios, incluidos sus roles, persisten en `datos/usuarios.json`. Los registros previos que no tengan el campo `rol` se interpretan como Cliente al cargarse.

## Comprobaciones manuales

1. Iniciar sesión como Administrador y comprobar la pestaña Gestión de Usuarios.
2. Registrar un Empleado o Cliente; confirmar que aparece en la tabla.
3. Seleccionar el registro y modificar nombre, correo o rol; una clave vacía debe conservarse.
4. Intentar eliminar el usuario seleccionado y confirmar el diálogo.
5. Probar Enter para registrar y Escape para limpiar formulario/selección.
6. Elegir un rol en el Combobox y verificar el mensaje de estado.
7. Iniciar sesión con las cuentas Empleado y Cliente y confirmar que no se ofrece la gestión administrativa.
8. Cerrar y reabrir la aplicación para comprobar la persistencia.
9. Verificar que Productos y Ventas sigan disponibles.
