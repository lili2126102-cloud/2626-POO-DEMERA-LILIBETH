# Explicación del programa de orientación a objetos

Este programa en Python representa un objeto real usando una clase. El ejemplo utiliza la clase `Libro` para modelar las características y acciones de un libro.

## 1. ¿Qué es una clase?
Una clase es una plantilla o modelo que define cómo es un objeto. En este caso, la clase `Libro` describe qué datos tiene un libro (`titulo`, `autor`, `paginas`, `editorial`, `disponible`) y qué puede hacer (`mostrar_informacion`, `prestar`, `devolver`).

## 2. La clase `Libro`
```python
class Libro:
    def __init__(self, titulo, autor, paginas, editorial, disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
        self.editorial = editorial
        self.disponible = disponible
```

- `class Libro:` declara la clase.
- `def __init__(...)` es el método constructor. Se ejecuta automáticamente cuando creas un libro nuevo.
- `self` es una referencia al objeto que estamos creando o usando.
- `self.titulo = titulo` guarda el valor que recibe el objeto. Cada libro tendrá sus propios valores.
- `disponible=True` significa que, por defecto, el libro está disponible para prestar.

## 3. Método `mostrar_informacion`
```python
    def mostrar_informacion(self):
        disponibilidad = "Sí" if self.disponible else "No"
        print(f"Título: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Páginas: {self.paginas}")
        print(f"Editorial: {self.editorial}")
        print(f"Disponible: {disponibilidad}")
```

- Este método muestra en pantalla los datos del libro.
- Usa `self` para acceder a los atributos del libro actual.
- La línea con `disponibilidad = ...` convierte el valor booleano (`True`/`False`) en texto amigable (`Sí`/`No`).

## 4. Método `prestar`
```python
    def prestar(self):
        if self.disponible:
            self.disponible = False
            print(f"El libro '{self.titulo}' ha sido prestado.")
        else:
            print(f"El libro '{self.titulo}' no está disponible.")
```

- Este método intenta prestar el libro.
- Si `self.disponible` es `True`, el libro se marca como prestado (`False`).
- Si ya fue prestado, muestra un mensaje indicando que no se puede prestar otra vez.

## 5. Método `devolver`
```python
    def devolver(self):
        if not self.disponible:
            self.disponible = True
            print(f"El libro '{self.titulo}' ha sido devuelto.")
        else:
            print(f"El libro '{self.titulo}' ya está disponible.")
```

- Este método devuelve el libro a la biblioteca.
- Si el libro no está disponible, lo marca como disponible.
- Si ya está disponible, muestra un mensaje indicando que no hay necesidad de devolverlo.

## 6. Función `main()`
```python
def main():
    libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", 417, "Editorial Sudamericana")
    libro2 = Libro("El principito", "Antoine de Saint-Exupéry", 96, "Reynal & Hitchcock", disponible=False)

    print("Información del primer libro:")
    libro1.mostrar_informacion()
    print()

    print("Información del segundo libro:")
    libro2.mostrar_informacion()
    print()

    libro1.prestar()
    libro1.prestar()  # Intento de prestar de nuevo
    libro1.devolver()
    libro1.devolver()  # Intento de devolver de nuevo
```

- `main()` es una función que organiza la ejecución del programa.
- Crea dos objetos `Libro`, cada uno con valores distintos.
- Llama a `mostrar_informacion()` para ver los datos de cada libro.
- Usa `prestar()` y `devolver()` para simular el uso real del objeto.
- Los comentarios `# ...` explican acciones adicionales del programa.

## 7. Punto de entrada del programa
```python
if __name__ == "__main__":
    main()
```

- Esta parte comprueba si el archivo se ejecuta directamente.
- Si es así, llama a `main()`.
- Si el archivo se importa desde otro programa, no ejecuta `main()` automáticamente.

## 8. Conceptos clave de Programación Orientada a Objetos (POO)
- Objeto: una entidad que tiene datos y puede realizar acciones.
- Clase: el molde o plantilla que describe a los objetos.
- Atributo: una característica del objeto (por ejemplo, `titulo`).
- Método: una acción que el objeto puede hacer (por ejemplo, `prestar`).
- Instancia: un objeto creado a partir de una clase.

## 9. Resumen
Este código demuestra cómo:
- definir una clase en Python,
- crear objetos con atributos propios,
- usar métodos para cambiar el estado interno,
- y ejecutar el programa de forma ordenada con `main()`.

¡Es una buena base para aprender POO con ejemplos claros y fáciles de seguir!