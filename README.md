# Programación Orientada a Objetos (POO) - Semana 8

## Información del Estudiante
* **Nombre Completo:** LILIBETH DEMERA
* **Asignatura:** Programación Orientada a Objetos (2626)
* **Semestre:** Segundo Semestre
* **Institución:** UEA - Universidad Estatal

---

## 🍽️ Descripción del Sistema: restaurante_app (Mejorado)
El proyecto **restaurante_app** es una aplicación de consola en Python diseñada para gestionar los productos, bebidas y clientes de un restaurante de manera modular. En esta versión mejorada correspondiente a la Actividad de la Semana 8, se ha reestructurado el sistema completo aplicando tres de los principios fundamentales de diseño **SOLID**:
1. **Responsabilidad Única (SRP)**
2. **Abierto/Cerrado (OCP)**
3. **Sustitución de Liskov (LSP)**

El programa cuenta con un menú interactivo y dinámico que soporta colores ANSI para destacar estados de éxito, error y advertencia, además de incluir validaciones robustas interactivas en bucles que permiten al usuario corregir datos ingresados erróneamente sin que la aplicación se detenga o reinicie.

---

## 🏗️ Estructura del Proyecto
El proyecto se organiza de forma modular respetando la estructura de paquetes y módulos requerida:

```
2626-POO-DEMERA-LILIBETH/
├── restaurante_app/
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── bebida.py
│   │   └── cliente.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   └── restaurante.py
│   └── main.py
└── README.md
```

---

## 📋 Responsabilidad de cada Clase y Componente

* **`modelos/producto.py` (`Producto`)**:
  Representa los datos comunes de cualquier producto del restaurante (código, nombre, categoría y precio). Aplica encapsulación mediante propiedades (`@property` y `@setter`) para controlar la lectura y modificación de sus atributos con validaciones que evitan valores vacíos o numéricos menores o iguales a cero. Define el método `mostrar_informacion()`.
* **`modelos/bebida.py` (`Bebida`)**:
  Clase especializada que hereda de `Producto`. Incorpora atributos específicos (`tamano` y `tipo_envase`) con sus correspondientes getters y setters. Sobrescribe el método `mostrar_informacion()` invocando al método de la clase padre mediante `super().mostrar_informacion()` y sumando sus propios detalles.
* **`modelos/cliente.py` (`Cliente`)**:
  Clase independiente encargada únicamente de representar la información de un cliente (identificación, nombre y correo). Valida que los datos ingresados no estén vacíos y que el correo electrónico contenga un formato elemental (`@`). Define su propio método `mostrar_informacion()`.
* **`servicios/restaurante.py` (`Restaurante`)**:
  Clase de servicio encargada de administrar las colecciones en memoria de productos y clientes. Contiene los métodos para registrar y listar los objetos, validando reglas de negocio tales como evitar códigos de producto duplicados e identificaciones de clientes repetidas.
* **`main.py`**:
  Punto de entrada de la aplicación. Coordina el menú interactivo, la entrada de datos de consola mediante `input()`, la creación de objetos y las llamadas a los métodos del servicio `Restaurante`. Contiene el control de excepciones de validación en tiempo de ejecución.

---

## 💡 Relación entre Producto y Bebida (Herencia y Polimorfismo)
La clase `Bebida` hereda de `Producto` porque una bebida **es un** producto del restaurante. Al aplicar herencia, se reutilizan atributos como el código, nombre, categoría y precio.
* **Polimorfismo y LSP:** La colección de productos de la clase `Restaurante` (`self.productos`) almacena tanto objetos `Producto` como `Bebida` de manera unificada. En el método `listar_productos()`, el servicio recorre la lista y ejecuta `producto.mostrar_informacion()`. Debido al polimorfismo, cada objeto se comporta de acuerdo con su clase real en tiempo de ejecución (mostrando los detalles correspondientes), sin necesidad de que el servicio pregunte si el objeto es un `Producto` o una `Bebida`.

---

## 🎯 Principios SOLID Aplicados

### 1. S - Responsabilidad Única (Single Responsibility Principle)
Cada clase tiene un rol claro y delimitado. Los modelos se encargan de representar y validar los datos de sus correspondientes entidades; la clase de servicio `Restaurante` centraliza la gestión de las listas y la validación de unicidad; y `main.py` maneja exclusivamente el flujo de la consola y la interacción directa con el usuario.

### 2. O - Abierto/Cerrado (Open/Closed Principle)
El diseño del software permite agregar nuevas especializaciones de productos (como postres, combos, promociones) heredando de `Producto` sin modificar el código de la clase de servicio `Restaurante` ni el del listado polimórfico. El sistema está abierto a la extensión pero cerrado a la modificación.

### 3. L - Sustitución de Liskov (Liskov Substitution Principle)
Los objetos de la subclase `Bebida` pueden reemplazar a los objetos de la superclase `Producto` sin alterar la corrección ni el comportamiento esperado del sistema. `Restaurante` procesa y lista a todos bajo la interfaz común de `Producto` sin que se generen errores o inconsistencias.

---

## 🚀 Instrucciones de Ejecución

### Requisitos:
* Python 3.8 o superior instalado en el sistema.
* Terminal que soporte secuencias de escape ANSI (como PowerShell en Windows 10/11, terminal en Linux/macOS).

### Pasos de ejecución:
1. Abra una terminal en el directorio raíz del proyecto.
2. Acceda a la carpeta del restaurante:
   ```bash
   cd restaurante_app
   ```
3. Ejecute el archivo principal:
   ```bash
   python main.py
   ```

El programa se iniciará cargando datos iniciales predeterminados (Lasaña de Carne, Jugo de Mora y un Cliente de prueba) para que pueda probar la opción de listado polimórfico de manera inmediata.

---

## 🧠 Reflexión sobre la Importancia de Diseñar Proyectos Mantenibles
Diseñar proyectos de manera modular y estructurada empleando buenas prácticas de POO y principios de diseño SOLID es fundamental para el éxito de cualquier software en el mundo real. 
* **Reducción de Deuda Técnica:** Facilita la legibilidad y la escalabilidad del sistema, permitiendo que varios desarrolladores colaboren de manera simultánea en diferentes módulos (modelos, vistas o controladores) sin interferir entre sí.
* **Seguridad ante Cambios:** Si en el futuro cambian las reglas de negocio o los atributos de una bebida, los cambios se concentran en `bebida.py`, sin peligro de romper la lógica de registro o el menú de consola. Esto ahorra tiempo de depuración y disminuye drásticamente el costo de mantenimiento a lo largo del tiempo.
