class Libro:
    def __init__(self, titulo, autor, paginas, editorial, disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
        self.editorial = editorial
        self.disponible = disponible

    def mostrar_informacion(self):
        disponibilidad = "Sí" if self.disponible else "No"
        print(f"Título: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Páginas: {self.paginas}")
        print(f"Editorial: {self.editorial}")
        print(f"Disponible: {disponibilidad}")

    def prestar(self):
        if self.disponible:
            self.disponible = False
            print(f"El libro '{self.titulo}' ha sido prestado.")
        else:
            print(f"El libro '{self.titulo}' no está disponible.")

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            print(f"El libro '{self.titulo}' ha sido devuelto.")
        else:
            print(f"El libro '{self.titulo}' ya está disponible.")


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


if __name__ == "__main__":
    main()
