# Programación Orientada a Objetos (POO)

## Información del Estudiante
* **Nombre Completo:** LILIBETH DEMERA
* **Asignatura:** Programación Orientada a Objetos (2626)
* **Semestre:** Segundo Semestre
* **Institución:** Universidad / Instituto Educativo
* **Proyectos Incluidos:** Parcial 1 y prácticas adicionales

---

## 📚 Resumen del Curso
Este repositorio contiene los trabajos, proyectos y prácticas desarrollados durante el curso de **Programación Orientada a Objetos**. El objetivo general es consolidar el entendimiento de los pilares fundamentales de la POO mediante la implementación práctica de aplicaciones modulares, seguras y escalables en Python.

### Objetivos de Aprendizaje
* Comprender y aplicar los tres pilares fundamentales de la POO: **Herencia**, **Encapsulación** y **Polimorfismo**
* Diseñar arquitecturas modulares y mantenibles utilizando paquetes y módulos en Python
* Implementar patrones de diseño para resolver problemas reales de programación
* Aplicar reglas de validación y manejo de datos mediante encapsulación
* Desarrollar soluciones escalables que faciliten el crecimiento y mantenimiento del código

---

## Descripción del Sistema Desarrollado - restaurante_app
El sistema **restaurante_app** es una aplicación modular en Python diseñada para administrar el menú de un restaurante. Permite registrar diferentes tipos de productos del restaurante, como comidas (**Platillos**) y líquidos (**Bebidas**). El sistema demuestra la aplicación práctica de los tres pilares fundamentales de la Programación Orientada a Objetos (POO): **Herencia**, **Encapsulación** y **Polimorfismo**, en una arquitectura modular limpia y mantenible.

---

## 🏗️ Estructura del Proyecto General

```
2626-POO-DEMERA-LILIBETH/
├── PARCIAL 1/
│   └── restaurante_app/        # Proyecto principal del parcial 1
│       ├── modelos/
│       │   ├── __init__.py
│       │   ├── producto.py
│       │   ├── platillo.py
│       │   └── bebida.py
│       ├── servicios/
│       │   ├── __init__.py
│       │   └── restaurante.py
│       └── main.py
├── README.md                   # Este archivo
└── [Otros ejercicios y prácticas del curso]
```

---

## 📋 Estructura del Proyecto - restaurante_app
El proyecto se organiza en paquetes y módulos según la siguiente estructura:

```
restaurante_app/
├── modelos/
│   ├── __init__.py      # Inicializa el paquete de modelos
│   ├── producto.py      # Clase padre (Producto)
│   ├── platillo.py      # Clase hija (Platillo)
│   └── bebida.py        # Clase hija (Bebida)
├── servicios/
│   ├── __init__.py      # Inicializa el paquete de servicios
│   └── restaurante.py   # Clase de servicio que administra la lista de productos
└── main.py              # Punto de arranque y ejecución de pruebas del sistema
```

### Responsabilidad de cada componente:
* **`modelos/producto.py`**: Define la clase general `Producto`, la cual posee atributos comunes (`nombre`, `__precio` y `disponible`), además de los métodos de acceso y modificación para el precio.
* **`modelos/platillo.py`**: Define la clase `Platillo`, agregando el atributo específico de calorías (`calorias` en kcal).
* **`modelos/bebida.py`**: Define la clase `Bebida`, agregando el atributo específico de volumen (`volumen` en ml).
* **`servicios/restaurante.py`**: Define la clase `Restaurante`, la cual contiene una lista privada de productos y el método de negocio para presentarlos de manera polimórfica.
* **`main.py`**: Instancia los objetos, prueba las reglas de encapsulación (intentos de precios inválidos y válidos) y ejecuta la presentación del menú.

---

## 💡 Principios de POO Implementados

### 1. Herencia
Se implementó una relación de jerarquía lógica donde `Producto` actúa como clase base (padre), y `Platillo` y `Bebida` actúan como subclases (hijas):
* **Atributos comunes en la clase padre (`Producto`):** `nombre`, `__precio`, `disponible`.
* **Atributos específicos en las clases hijas:**
  * `Platillo` añade `calorias` (medidas en kcal).
  * `Bebida` añade `volumen` (medido en ml).
* Se utiliza la función `super().__init__(nombre, precio, disponible)` en los constructores de las clases hijas para delegar la inicialización de los atributos comunes a la clase padre.
* Este enfoque permite reutilizar código y mantener una estructura lógica y coherente de las clases.

### 2. Encapsulación
El precio de los productos se protege aplicando encapsulación mediante el atributo privado `__precio` (con doble guion bajo) en la clase `Producto`:
* **Acceso:** Se lee a través del método getter `obtener_precio()`.
* **Modificación y Validación:** Se modifica mediante el método setter `cambiar_precio(nuevo_precio)`.
* **Regla de Validación:** El setter valida que el precio sea estrictamente mayor que cero (`nuevo_precio > 0`). Si se introduce un valor negativo o cero, la modificación es rechazada, se imprime un mensaje informativo del error y se mantiene el precio anterior, protegiendo la consistencia de los datos del sistema.
* Este mecanismo garantiza que los datos internos del objeto no se alteren de forma accidental o maliciosa.

### 3. Polimorfismo
El polimorfismo se demuestra mediante el método `mostrar_informacion()`:
* La clase padre `Producto` define una implementación base de `mostrar_informacion()`.
* Las clases hijas `Platillo` y `Bebida` sobrescriben (`override`) este método para incorporar sus detalles exclusivos (`calorias` y `volumen` respectivamente).
* Al recorrer la lista de productos registrados dentro de la clase `Restaurante` (`mostrar_productos()`), se llama a `producto.mostrar_informacion()` para cada elemento. Python resuelve en tiempo de ejecución cuál método ejecutar según el tipo de objeto real de la iteración.
* Esto permite que el servicio imprima correctamente la información formateada para cualquier tipo de producto sin necesidad de comprobar manualmente su tipo mediante condicionales `if/else`.
* El polimorfismo facilita la extensión del sistema para nuevos tipos de productos sin modificar el código existente.

---

## 🔍 Aplicación de Principios de POO

---

## 🎯 Reflexión sobre la POO Modular en Python
La aplicación de los principios de la Programación Orientada a Objetos en una estructura de carpetas modular resulta de vital importancia para el desarrollo de software profesional. 

### Beneficios de la Arquitectura Modular:
* **Organización y Legibilidad:** Separar el dominio de negocio en subcarpetas (`modelos` y `servicios`) permite localizar y modificar el código de forma intuitiva, reduciendo el acoplamiento y facilitando el trabajo en equipo.
* **Seguridad y Control:** La encapsulación garantiza que los datos sensibles, como los precios de los productos, no se alteren de forma accidental o maliciosa con valores ilógicos (como números negativos), centralizando la lógica de validación.
* **Mantenibilidad y Escalabilidad:** Si en el futuro el restaurante añade nuevos tipos de productos (por ejemplo, combos promocionales o souvenirs), solo se requerirá crear un nuevo archivo bajo `modelos/` que herede de `Producto`, sin necesidad de alterar las clases del servicio ni la lógica existente.
* **Reutilización de Código:** La herencia permite que los atributos y métodos comunes se definan una sola vez en la clase padre, evitando duplicación y facilitando cambios globales.
* **Testabilidad:** Una estructura modular permite crear pruebas unitarias independientes para cada componente, garantizando mayor confiabilidad.

---

## 🚀 Cómo Ejecutar el Proyecto

### Requisitos:
* Python 3.7 o superior instalado en el sistema
* Acceso a una terminal o línea de comandos

### Pasos de Ejecución:
1. Navega al directorio del proyecto:
   ```bash
   cd PARCIAL\ 1/restaurante_app
   ```

2. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```

3. El programa creará instancias de productos (Platillos y Bebidas), realizará pruebas de encapsulación y mostrará el menú completo del restaurante.

---

## 📖 Conceptos Clave Aprendidos

### Paquetes y Módulos en Python:
* Los paquetes (`modelos/`, `servicios/`) contienen archivos `__init__.py` que los declaran como paquetes importables.
* Los módulos pueden importarse de forma relativa o absoluta, permitiendo una organización clara del código.

### Métodos Especiales:
* `__init__()`: Constructor que inicializa los atributos del objeto.
* `__str__()` (implícito): Utilizado para representación legible del objeto.
* Métodos con prefijo `__` (doble guion bajo): Atributos privados protegidos de acceso directo externo.

### Validación de Datos:
* Los setters implementan reglas de validación que garantizan la integridad de los datos.
* La validación centralizada en una sola ubicación facilita el mantenimiento y reduce errores.

---

## 📝 Notas Finales
Este proyecto representa un caso de uso práctico y realista de los conceptos de POO. La arquitectura modular utilizada es similar a la empleada en proyectos profesionales de mayor envergadura. El código está diseñado para ser fácilmente extensible, permitiendo agregar nuevas funcionalidades sin comprometer la integridad del sistema existente.

---

## 📞 Contacto
* **Estudiante:** LILIBETH DEMERA
* **Asignatura:** Programación Orientada a Objetos (2626)
* **Período:** Segundo Semestre

---

## ✅ Reflexión sobre la POO Modular en Python
