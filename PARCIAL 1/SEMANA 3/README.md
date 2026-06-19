# Soluciones: Programación Tradicional vs. Programación Orientada a Objetos

**Estudiante:** Lilibeth Yadira Demera Leyton

---

## 📋 Descripción General

Este proyecto contiene dos soluciones equivalentes para gestionar información de mascotas:
una usando **programación tradicional** (funciones y variables) y otra usando **programación orientada a objetos** (clases y objetos).

El objetivo es demostrar las diferencias fundamentales entre ambos paradigmas de programación y cómo la POO proporciona una estructura más robusta y reutilizable.

---

## 📁 Estructura del Repositorio

```
proyecto/
├── programacion_tradicional/
│   └── tradicional.py          # Solución usando funciones y diccionarios
├── programacion_poo/
│   ├── main.py                 # Programa principal que crea objetos
│   └── mascota.py              # Clase Mascota con atributos y métodos
└── README.md                   # Este archivo
```

### Descripción de Archivos

#### `programacion_tradicional/tradicional.py`
- **Enfoque:** Procedural/Funcional
- **Características:**
  - Utiliza funciones para solicitar datos y mostrar información
  - Almacena datos en diccionarios (no estructurados)
  - Flujo lineal del programa
  - Validación manual de datos
  - Interacción por consola (entrada/salida)

#### `programacion_poo/mascota.py`
- **Enfoque:** Orientado a Objetos
- **Características:**
  - Define la clase `Mascota` con atributos (`nombre`, `especie`, `edad`)
  - Implementa métodos (`__init__`, `mostrar_informacion()`, `hacer_sonido()`)
  - Encapsulamiento de datos y comportamiento
  - Reutilización de código mediante instanciación de objetos
  - Abstracción del problema mediante la clase

#### `programacion_poo/main.py`
- **Enfoque:** Orientado a Objetos (Consumidor)
- **Características:**
  - Crea múltiples instancias de la clase `Mascota`
  - Demuestra el uso de objetos y sus métodos
  - Iteración sobre colecciones de objetos
  - Organización clara del código

---

## 🚀 Cómo Ejecutar

### Ejecutar la solución tradicional:
```bash
python programacion_tradicional/tradicional.py
```
**Resultado esperado:** El programa solicita datos de una mascota por teclado y los muestra ordenados.

### Ejecutar la solución orientada a objetos:
```bash
python programacion_poo/main.py
```
**Resultado esperado:** Se crean tres objetos Mascota predefinidos, se muestra su información y el sonido que hace cada una.

---

## 🔍 Reflexión: Diferencias entre Programación Tradicional y POO

### **Programación Tradicional**
- **Organización:** Centrada en funciones y datos separados
- **Estructura:** Secuencial y procedural
- **Reutilización:** Limitada; requiere copiar código o parámetros adicionales
- **Mantenimiento:** Difícil cuando el proyecto crece
- **Abstracción:** Baja; el usuario debe entender la lógica interna
- **Estado:** Global; fácil de causar efectos secundarios
- **Ejemplo:** `registrar_mascota()` y `mostrar_mascota()` trabajan independientemente

### **Programación Orientada a Objetos**
- **Organización:** Centrada en objetos que combinan datos y métodos
- **Estructura:** Modular y jerárquica
- **Reutilización:** Alta; instanciación de objetos con diferentes estados
- **Mantenimiento:** Más fácil; cambios en la clase afectan a todos los objetos
- **Abstracción:** Alta; se oculta la complejidad interna
- **Estado:** Encapsulado en objetos; menos efectos secundarios
- **Ejemplo:** La clase `Mascota` encapsula atributos y métodos juntos

### **Ventajas de la POO en este contexto:**

1. **Encapsulamiento:** Los datos de una mascota (nombre, especie, edad) se agrupan con sus métodos (mostrar_informacion, hacer_sonido).

2. **Reutilización:** Crear nuevas mascotas es trivial; solo instanciar `Mascota(nombre, especie, edad)`.

3. **Escalabilidad:** Añadir nuevas especies o comportamientos es simple; solo modificar la clase.

4. **Polimorfismo:** Se puede extender la clase para diferentes tipos de mascotas (perro vs. gato) con comportamiento específico.

5. **Claridad:** El código es más legible y autodescriptivo; un objeto `mascota1` tiene clara intención.

### **Cuándo usar cada uno:**

- **Tradicional:** Scripts pequeños, automatizaciones simples, tareas puntuales
- **POO:** Proyectos medianos/grandes, aplicaciones complejas, código que será mantenido por múltiples personas

---

## 📊 Conceptos POO Demostrados

✅ **Clase:** `Mascota` define la estructura y comportamiento  
✅ **Objetos:** `mascota1`, `mascota2`, `mascota3` son instancias  
✅ **Atributos:** `nombre`, `especie`, `edad` almacenan estado  
✅ **Métodos:** `mostrar_informacion()`, `hacer_sonido()` definen comportamiento  
✅ **Constructor:** `__init__()` inicializa objetos  
✅ **Abstracción:** El usuario no conoce cómo se determina el sonido, solo lo llama  

---

## 🎯 Conclusión

Aunque ambas soluciones resuelven el mismo problema, la **Programación Orientada a Objetos** proporciona:
- Mejor organización del código
- Mayor reutilización mediante instanciación
- Facilidad de mantenimiento y extensión
- Modelado más natural del mundo real

La POO es el paradigma recomendado para proyectos profesionales y aplicaciones complejas.

---

**Fecha de Desarrollo:** Junio 2026  
**Curso:** Programación Orientada a Objetos  
**Institución:** Universidad Estatal Amazónica

