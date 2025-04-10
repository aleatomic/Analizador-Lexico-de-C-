#include <iostream>
#define PI 3.1416

using namespace std;

int main() {
    int edad = 25;
    float altura = 1.75;
    char letra = 'A';
    string saludo = "Hola, mundo!";
    
    if (edad > 18) {
        cout << "Eres mayor de edad." << endl;
    } else {
        cout << "Eres menor de edad." << endl;
    }

    for (int i = 0; i < 5; i++) {
        cout << "Iteración: " << i << endl;
    }

    return 0;
}
