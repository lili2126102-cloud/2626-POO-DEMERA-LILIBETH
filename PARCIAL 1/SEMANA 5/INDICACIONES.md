# INDICACIONES PARA EJECUTAR EL PROGRAMA - SEMANA 5

## 🖥️ Requisitos Previos

- **Python 3.7 o superior** instalado en tu equipo
- Una terminal o símbolo del sistema (PowerShell, CMD, Bash)

## 📍 Ubicación del Proyecto

La estructura del proyecto SEMANA 5 se encuentra en:

```
2626-POO-DEMERA-LILIBETH/
└── PARCIAL 1/
    └── SEMANA 5/
        └── restaurante_app/
            ├── modelos/
            │   ├── __init__.py
            │   ├── producto.py
            │   └── cliente.py
            ├── servicios/
            │   ├── __init__.py
            │   └── restaurante.py
            └── main.py
```

## 🚀 Pasos para Ejecutar

### Opción 1: Ejecución desde PowerShell / CMD

1. Abre PowerShell o CMD en tu equipo

2. Navega a la carpeta del proyecto:
   ```powershell
   cd "C:\Users\LILIBETH DEMERA\OneDrive\Desktop\Segundo semestre\PROGRAMACIÓN ORIENTADA A OBJETOS\2626-POO-DEMERA-LILIBETH\PARCIAL 1\SEMANA 5\restaurante_app"
   ```

3. Ejecuta el programa con Python:
   ```powershell
   python main.py
   ```
   
   O si Python está registrado como python3:
   ```powershell
   python3 main.py
   ```

### Opción 2: Desde un IDE (PyCharm, VS Code, etc.)

1. Abre el IDE de tu preferencia (PyCharm, Visual Studio Code, etc.)
2. Abre la carpeta `restaurante_app`
3. Haz clic derecho en el archivo `main.py`
4. Selecciona "Run" o "Ejecutar"

### Opción 3: Ejecución desde la carpeta padre

```powershell
cd "C:\Users\LILIBETH DEMERA\OneDrive\Desktop\Segundo semestre\PROGRAMACIÓN ORIENTADA A OBJETOS\2626-POO-DEMERA-LILIBETH\PARCIAL 1\SEMANA 5"
python -m restaurante_app.main
```

## 📊 Salida Esperada

Cuando ejecutes el programa, verás una salida similar a esta:

```
============================================================
CREANDO PRODUCTOS...
============================================================
✓ Producto creado: Pasta Carbonara
✓ Producto creado: Ensalada César
✓ Producto creado: Pizza Margherita

============================================================
CREANDO CLIENTES...
============================================================
✓ Cliente creado: Juan García
✓ Cliente creado: María López
✓ Cliente creado: Carlos Rodríguez

============================================================
INFORMACIÓN DEL RESTAURANTE
============================================================
Restaurante: La Delizia
Ubicación: Calle Principal 123, Centro
Año de fundación: 2010
Total de productos: 3
Total de clientes: 3
Miembros frecuentes: 2

--- Productos disponibles en La Delizia ---
  • Producto: Pasta Carbonara | Precio: $12.50 | Stock: 15 | Estado: Disponible
  • Producto: Ensalada César | Precio: $8.75 | Stock: 20 | Estado: Disponible
  • Producto: Pizza Margherita | Precio: $10.00 | Stock: 10 | Estado: No disponible

--- Clientes registrados en La Delizia ---
  • Cliente: Juan García | Email: juan.garcia@email.com | Teléfono: 555-1234 | Miembro | Visitas: 5
  • Cliente: María López | Email: maria.lopez@email.com | Teléfono: 555-5678 | Cliente regular | Visitas: 1
  • Cliente: Carlos Rodríguez | Email: carlos.rodriguez@email.com | Teléfono: 555-9999 | Miembro | Visitas: 8

============================================================
DEMOSTRANDO MÉTODOS DE GESTIÓN...
============================================================
✓ Registrada visita para María López
  Nuevas visitas: 2
✓ María López convertido a miembro frecuente
✓ Se vendieron 3 unidades de Pasta Carbonara
  Stock restante: 12
✓ Se agregaron 5 unidades de Pizza Margherita
  Nuevo stock: 15
✓ Pizza Margherita ahora está disponible

============================================================
INFORMACIÓN ACTUALIZADA DEL RESTAURANTE
============================================================
Restaurante: La Delizia
Ubicación: Calle Principal 123, Centro
Año de fundación: 2010
Total de productos: 3
Total de clientes: 3
Miembros frecuentes: 3

--- Productos disponibles en La Delizia ---
  • Producto: Pasta Carbonara | Precio: $12.50 | Stock: 12 | Estado: Disponible
  • Producto: Ensalada César | Precio: $8.75 | Stock: 20 | Estado: Disponible
  • Producto: Pizza Margherita | Precio: $10.00 | Stock: 15 | Estado: Disponible

--- Clientes registrados en La Delizia ---
  • Cliente: Juan García | Email: juan.garcia@email.com | Teléfono: 555-1234 | Miembro | Visitas: 5
  • Cliente: María López | Email: maria.lopez@email.com | Teléfono: 555-5678 | Miembro | Visitas: 2
  • Cliente: Carlos Rodríguez | Email: carlos.rodriguez@email.com | Teléfono: 555-9999 | Miembro | Visitas: 8

============================================================
¡PROGRAMA FINALIZADO EXITOSAMENTE!
============================================================
```

## 🔍 Verificación de Funcionamiento

Para verificar que el programa funciona correctamente, debes observar:

1. ✅ Se crean 3 productos correctamente
2. ✅ Se crean 3 clientes correctamente
3. ✅ Se muestran las listas de productos y clientes
4. ✅ Se demuestran métodos de gestión (registrar visita, convertir a miembro, etc.)
5. ✅ La información se actualiza correctamente
6. ✅ No hay errores de importación

## 🛠️ Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'modelos'"

**Solución:** Asegúrate de estar ejecutando el programa desde la carpeta `restaurante_app`:
```powershell
cd "...\SEMANA 5\restaurante_app"
python main.py
```

### Problema: "python: command not found" o similar

**Solución:** Python no está en el PATH. Opciones:
1. Instala Python desde python.org
2. Añade Python al PATH durante la instalación (opción recomendada)
3. Usa la ruta completa de Python, ejemplo:
   ```powershell
   "C:\Python39\python.exe" main.py
   ```

### Problema: Errores de sintaxis

**Solución:** Verifica que todos los archivos estén en la carpeta correcta y que no haya errores de tipeo.

## 📞 Contacto

Si tienes preguntas sobre cómo ejecutar el programa:
- Revisa el archivo `README.md` en la misma carpeta
- Verifica que Python esté correctamente instalado
- Asegúrate de que los archivos no hayan sido modificados

---

**Estudiante:** LILIBETH DEMERA  
**Asignatura:** Programación Orientada a Objetos  
**Semana:** 5
