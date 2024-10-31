"""LISTA DE NOMBRES, AUTORES Y ISBN DE LIBROS
Naruto Vol. 1, Masashi Kishimoto, 9781569319000
Naruto Vol. 2, Masashi Kishimoto, 9781569319277
Naruto Vol. 3, Masashi Kishimoto, 9781569319864
Naruto Vol. 4, Masashi Kishimoto, 9781591163589
Naruto Vol. 5, Masashi Kishimoto, 9781591163596
Los juegos del hambre, Suzanne Collins, 9780439023481
A Good Girl's Guide to Murder, Holly Jackson, 9781984896360
El ladrón de libros,  Markus Zusak, 9780375842207
Cien años de soledad, Gabriel Garcia Marquez, 9780062315008
Ruination, Anthony Reynolds, 9780316469258"""

from queue import Queue
from collections import deque

# Cola y pila para gestionar solicitudes y el historial de operaciones
cola_lectores = Queue()  
historial = []  # Pila para almacenar el historial de operaciones
cola_prestamos = deque()  # Cola para gestionar las solicitudes de préstamo
libros_prestados = {}  # Almacena qué libro tiene cada lector (por DNI)
libros_reservados = {}  # Diccionario para gestionar los libros reservados y sus solicitudes
lectores = {}  # Diccionario para gestionar los lectores y su estado

# Funciones para el historial
def apilar_operacion(operacion):
    """Agrega una operación al historial."""
    historial.append(operacion)

def ver_historial():
    """Muestra los últimos movimientos registrados en el historial."""
    print("\n--- Historial de Operaciones ---")
    if not historial:
        print("No hay historial de operaciones.")
    else:
        for i, operacion in enumerate(reversed(historial[-10:]), 1):
            print(f"{i}) {operacion}")

def mostrar_menu():
    print("\n--- Biblioteca Virtual ---")
    print("1) Pedir libro")
    print("2) Devolver libro")
    print("3) Ver biblioteca")
    print("4) Ver historial")
    print("5) Salir")

# Función para registrar préstamos en el archivo y en el historial
def registrar_prestamo(dni, nombre, titulo):
    with open('solicitudes.txt', 'a', encoding='ISO-8859-1') as archivo:
        archivo.write(f"{dni},{nombre},{titulo}\n")
    apilar_operacion(f"{nombre} (DNI: {dni}) ha solicitado el libro '{titulo}'.")

def pedir_libro():
    print("\n--- Solicitar un Libro ---")
    prestamos = cargar_prestamos()

    if not prestamos:  
        print("No hay usuarios registrados. Por favor, crea un nuevo usuario para continuar.")

    nombre = input("Introduce tu nombre (o escribe 'cancelar' para volver): ").strip()
    if nombre.lower() == 'cancelar':
        print("Solicitud cancelada. Volviendo al menú principal...")
        return

    dni = input("Introduce tu DNI: ").strip()
    if dni.lower() == 'cancelar':
        print("Solicitud cancelada. Volviendo al menú principal...")
        return

    # Verificar si el usuario ya tiene un libro en préstamo
    if dni in libros_prestados:
        print(f"Ya tienes un libro en préstamo: '{libros_prestados[dni]}'. Devuélvelo antes de solicitar otro.")
        return

    print("\nLibros disponibles para préstamo:")
    titulos_disponibles = [libro.split(",")[0] for libro in biblioteca]
    for i, titulo in enumerate(titulos_disponibles, 1):
        print(f"{i}) {titulo}")

    while True:
        seleccion = input("Elige el número del libro que quieres (o 'cancelar' para volver): ").strip()
        if seleccion.lower() == 'cancelar':
            print("Solicitud cancelada. Volviendo al menú principal...")
            return

        if seleccion.isdigit() and 1 <= int(seleccion) <= len(titulos_disponibles):
            titulo_elegido = titulos_disponibles[int(seleccion) - 1]
            break
        else:
            print("Selección no válida, intenta de nuevo.")

    # Verificar si el libro ya está en préstamo
    if any(titulo_elegido == libro for libro in libros_prestados.values()):
        print(f"El libro '{titulo_elegido}' ya está en préstamo. Tu solicitud será añadida a la cola de espera.")
        cola_prestamos.append((nombre, dni, titulo_elegido)) 
        apilar_operacion(f"{nombre} (DNI: {dni}) ha sido añadido a la cola de espera para '{titulo_elegido}'.")
        return 

    # Si el libro está disponible, realizar el préstamo
    libros_prestados[dni] = titulo_elegido  
    registrar_prestamo(dni, nombre, titulo_elegido)
    print(f"Solicitud registrada: {nombre} ha solicitado '{titulo_elegido}'.")


def devolver_libro():
    print("\n--- Devolver Libro ---")

    dni = input("Introduce tu DNI (o escribe 'cancelar' para volver): ").strip()
    if dni.lower() == 'cancelar':
        print("Devolución cancelada. Volviendo al menú principal...")
        return

    if dni not in libros_prestados:
        print("No tienes ningún libro en préstamo.")
        return

    libro_devuelto = libros_prestados[dni]
    nombre = dni

    del libros_prestados[dni]
    print(f"{nombre} ha devuelto el libro: '{libro_devuelto}'.")
    with open('solicitudes.txt', 'a', encoding='ISO-8859-1') as archivo:
        archivo.write(f"DEVOLUCIÓN,{dni},{nombre},{libro_devuelto}\n")
    apilar_operacion(f"{nombre} (DNI: {dni}) ha devuelto el libro '{libro_devuelto}'.")

    for i, (nombre_solicitante, dni_solicitante, titulo) in enumerate(cola_prestamos):
        if titulo == libro_devuelto:
            libros_prestados[dni_solicitante] = titulo
            print(f"El libro '{titulo}' ha sido asignado a {nombre_solicitante} (DNI: {dni_solicitante}).")
            cola_prestamos.remove((nombre_solicitante, dni_solicitante, titulo))
            registrar_prestamo(dni_solicitante, nombre_solicitante, titulo)
            break
    else:
        print("No hay solicitudes pendientes para este libro.")

    print("Devolución procesada exitosamente.")

def cargar_prestamos():
    try:
        with open('solicitudes.txt', 'r', encoding='ISO-8859-1', errors='ignore') as archivo:
            return [linea.strip() for linea in archivo.readlines() if linea.strip()]
    except FileNotFoundError:
        print("El archivo 'solicitudes.txt' no se encontró. Se creará uno nuevo.")
        with open('solicitudes.txt', 'w') as archivo:
            pass
        return []

def cargar_biblioteca():
    try:
        with open('biblioteca.txt', 'r', encoding='ISO-8859-1', errors='ignore') as archivo:
            return [linea.strip() for linea in archivo.readlines() if linea.strip()]
    except FileNotFoundError:
        print("El archivo 'biblioteca.txt' no se encontró. Se creará uno nuevo.")
        return []

def ver_biblioteca():
    global biblioteca
    biblioteca = cargar_biblioteca()

    print("\nLibros disponibles en la biblioteca:")
    for libro in biblioteca:
        titulo = libro.split(",")[0]
        print(f"- {titulo}")

    while True:
        print("\nSubmenú:")
        print("1) Agregar un nuevo libro")
        print("2) Ordenar biblioteca")
        print("3) Buscar un libro")
        print("4) Volver al menú principal")

        opcion_submenu = input("Elige una opción: ")

        if opcion_submenu == '1':
            agregar_libro()
        elif opcion_submenu == '2':
            biblioteca = quicksort(biblioteca)
            print("\nBiblioteca ordenada:")
            for libro in biblioteca:
                titulo = libro.split(",")[0]
                print(f"- {titulo}")
            apilar_operacion("Biblioteca ordenada.")
        elif opcion_submenu == '3':
            buscar_libro()
        elif opcion_submenu == '4':
            break
        else:
            print("Opción no válida, intenta de nuevo.")

def agregar_libro():
    titulo = input("Introduce el título del libro: ")
    autor = input("Introduce el autor del libro: ")
    isbn = input("Introduce el ISBN del libro: ")
    nuevo_libro = f"{titulo},{autor},{isbn}"
    biblioteca.append(nuevo_libro)
    with open('biblioteca.txt', 'a', encoding='ISO-8859-1') as archivo:
        archivo.write(nuevo_libro + "\n")
    apilar_operacion(f"Libro '{titulo}' agregado a la biblioteca.")
    print(f"Libro '{titulo}' agregado exitosamente.")

def quicksort(libros):
    if len(libros) <= 1:
        return libros
    else:
        pivot = libros[0]
        menores = [libro for libro in libros[1:] if libro < pivot]
        mayores = [libro for libro in libros[1:] if libro >= pivot]
        return quicksort(menores) + [pivot] + quicksort(mayores)

def buscar_libro():
    while True:
        print("\nOpciones de búsqueda:")
        print("1) Buscar por título")
        print("2) Buscar por autor")
        print("3) Buscar por ISBN")
        print("4) Volver al submenú")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            valor = input("Introduce el título a buscar: ")
            resultados = [libro for libro in biblioteca if valor.lower() in libro.split(',')[0].lower()]
        elif opcion == '2':
            valor = input("Introduce el autor a buscar: ")
            resultados = [libro for libro in biblioteca if valor.lower() in libro.split(',')[1].lower()]
        elif opcion == '3':
            valor = input("Introduce el ISBN a buscar: ")
            resultados = [libro for libro in biblioteca if valor == libro.split(',')[2]]
        elif opcion == '4':
            break
        else:
            print("Opción no válida, intenta de nuevo.")
            continue

        if resultados:
            print("\nResultados de búsqueda:")
            for libro in resultados:
                titulo, autor, isbn = libro.split(',')
                print(f"- Título: {titulo}, Autor: {autor}, ISBN: {isbn}")
        else:
            print("No se encontraron resultados para la búsqueda.")

def ejecutar_menu():
    global biblioteca
    biblioteca = cargar_biblioteca()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == '1':
            pedir_libro()
        elif opcion == '2':
            devolver_libro()
        elif opcion == '3':
            ver_biblioteca()
        elif opcion == '4':
            ver_historial()
        elif opcion == '5':
            print("Saliendo de la biblioteca virtual...")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")

# Ejecutar el menú
ejecutar_menu()
