// Problema: Vito's Family

/* Referencia bibliográfica:
 * Skiena, S. S., & Revilla, M. A. (2003). 
 * Programming Challenges: The Programming Contest Training Manual
 * Springer-Verlag. https://i.cs.hku.hk/~provinci/files/b2-programming_challenges.pdf
*/

#include <iostream>   
#include <vector>     // Estrutura dinâmica para armazenar os endereços
#include <algorithm>  // Função sort()
#include <cmath>      // Função abs() para valor absoluto
#include <fstream>    // Leitura de arquivo

using namespace std;

int main() {

    ifstream arquivo("../archivos/valoresEntradaVitos.txt"); // Abre o arquivo de entrada
    //Verificar se o arquivo foi aberto corretamente
    if (!arquivo) {
        cerr << "O arquivo de entrada não pôde ser aberto!" << endl;
        return 1; // Sair se o arquivo não puder ser aberto
    }

    // Número de casos de teste
    int numeroCases;                 
    arquivo >> numeroCases;
    while (numeroCases--) {          
        int cantidadParentes;             // Quantidade de parentes (endereços)
        arquivo >> cantidadParentes;
        
        // Armazena os endereços
        vector<int> ruas(cantidadParentes);
        
        // Lê os cantidadParentes endereços
        for (int i = 0; i < cantidadParentes; ++i) { 
            arquivo >> ruas[i];
        }
        
        // Ordena para encontrar a mediana
        sort(ruas.begin(), ruas.end());  

        // Mediana (índice inteiro → posição central)
        int mediana = ruas[cantidadParentes / 2];       

        // Soma das distâncias absolutas
        int totalDistance = 0;           
        for (int i = 0; i < cantidadParentes; ++i) {
            totalDistance += abs(ruas[i] - mediana); // |endereço_i − mediana|
        }

        // Imprime a menor soma possível
        cout << totalDistance << endl;   
    }
    return 0; 
}
