from mascota import Mascota


def main():
    # Crear al menos dos objetos de la clase Mascota
    mascota1 = Mascota('Luna', 'Gato', 3)
    mascota2 = Mascota('Max', 'Perro', 5)

    mascotas = [mascota1, mascota2]

    # Ejecutar los métodos definidos y mostrar la información de cada objeto
    for m in mascotas:
        print('-' * 30)
        m.mostrar_informacion()
        m.hacer_sonido()
    print('-' * 30)


if __name__ == '__main__':
    main()

