#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <deque>
#include <queue>
#include <unordered_map>
#include <algorithm>

using namespace std;

queue<string> cola_lectores;
vector<string> historial;
deque<tuple<string, string, string>> cola_prestamos;
unordered_map<string, string> libros_prestados;
unordered_map<string, vector<string>> libros_reservados;
unordered_map<string, string> lectores;
vector<string> biblioteca;

// Función para agregar operación al historial
void apilar_operacion(const string& operacion) {
    historial.push_back(operacion);
}

// Función para mostrar el historial
void ver_historial() {
    cout << "\n--- Historial de Operaciones ---\n";
    if (historial.empty()) {
        cout << "No hay historial de operaciones.\n";
    } else {
        int count = 0;
        for (auto it = historial.rbegin(); it != historial.rend() && count < 10; ++it, ++count) {
            cout << count + 1 << ") " << *it << endl;
        }
    }
}

// Mostrar menú principal
void mostrar_menu() {
    cout << "\n--- Biblioteca Virtual ---\n";
    cout << "1) Pedir libro\n";
    cout << "2) Devolver libro\n";
    cout << "3) Ver biblioteca\n";
    cout << "4) Ver historial\n";
    cout << "5) Salir\n";
}

// Registrar préstamo en el archivo y en el historial
void registrar_prestamo(const string& dni, const string& nombre, const string& titulo) {
    ofstream archivo("solicitudes.txt", ios::app);
    archivo << dni << "," << nombre << "," << titulo << "\n";
    apilar_operacion(nombre + " (DNI: " + dni + ") ha solicitado el libro '" + titulo + "'.");
}

vector<string> cargar_biblioteca() {
    vector<string> libros;
    ifstream archivo("biblioteca.txt");
    string linea;
    while (getline(archivo, linea)) {
        if (!linea.empty()) {
            libros.push_back(linea);
        }
    }
    return libros;
}

void ver_biblioteca() {
    biblioteca = cargar_biblioteca();
    cout << "\nLibros disponibles en la biblioteca:\n";
    for (const string& libro : biblioteca) {
        cout << "- " << libro.substr(0, libro.find(',')) << endl;
    }
}

void pedir_libro() {
    cout << "\n--- Solicitar un Libro ---\n";
    string nombre, dni;
    cout << "Introduce tu nombre (o escribe 'cancelar' para volver): ";
    cin >> nombre;
    if (nombre == "cancelar") return;

    cout << "Introduce tu DNI: ";
    cin >> dni;
    if (dni == "cancelar") return;

    if (libros_prestados.find(dni) != libros_prestados.end()) {
        cout << "Ya tienes un libro en préstamo: '" << libros_prestados[dni] << "'. Devuélvelo antes de solicitar otro.\n";
        return;
    }

    cout << "\nLibros disponibles para préstamo:\n";
    for (size_t i = 0; i < biblioteca.size(); ++i) {
        cout << i + 1 << ") " << biblioteca[i].substr(0, biblioteca[i].find(',')) << endl;
    }

    int seleccion;
    cout << "Elige el número del libro que quieres (o '0' para cancelar): ";
    cin >> seleccion;
    if (seleccion == 0) return;

    string titulo_elegido = biblioteca[seleccion - 1].substr(0, biblioteca[seleccion - 1].find(','));
    libros_prestados[dni] = titulo_elegido;
    registrar_prestamo(dni, nombre, titulo_elegido);
    cout << "Solicitud registrada: " << nombre << " ha solicitado '" << titulo_elegido << "'.\n";
}

void devolver_libro() {
    cout << "\n--- Devolver Libro ---\n";
    string dni;
    cout << "Introduce tu DNI (o escribe 'cancelar' para volver): ";
    cin >> dni;
    if (dni == "cancelar") return;

    if (libros_prestados.find(dni) == libros_prestados.end()) {
        cout << "No tienes ningún libro en préstamo.\n";
        return;
    }

    string libro_devuelto = libros_prestados[dni];
    libros_prestados.erase(dni);
    cout << dni << " ha devuelto el libro: '" << libro_devuelto << "'.\n";

    ofstream archivo("solicitudes.txt", ios::app);
    archivo << "DEVOLUCIÓN," << dni << "," << dni << "," << libro_devuelto << "\n";
    apilar_operacion(dni + " ha devuelto el libro '" + libro_devuelto + "'.");
}

void ejecutar_menu() {
    biblioteca = cargar_biblioteca();

    while (true) {
        mostrar_menu();
        int opcion;
        cout << "Elige una opción: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                pedir_libro();
                break;
            case 2:
                devolver_libro();
                break;
            case 3:
                ver_biblioteca();
                break;
            case 4:
                ver_historial();
                break;
            case 5:
                cout << "Saliendo de la biblioteca virtual...\n";
                return;
            default:
                cout << "Opción no válida, por favor intenta de nuevo.\n";
        }
    }
}

int main() {
    ejecutar_menu();
    return 0;
}
