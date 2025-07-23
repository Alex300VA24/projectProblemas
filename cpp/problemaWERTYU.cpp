// Problema: WERTYU

/* Referencia bibliográfica:
 * Skiena, S. S., & Revilla, M. A. (2003). 
 * Programming Challenges: The Programming Contest Training Manual
 * Springer-Verlag. https://i.cs.hku.hk/~provinci/files/b2-programming_challenges.pdf
*/

#include <iostream>         
#include <unordered_map>    // Mapa hash (associação chave-valor)
#include <string>           // Para manipular strings
#include <fstream>          // Para leitura de arquivos

using namespace std;

int main() {

    // Abre o arquivo que contém os textos digitados erroneamente
    ifstream arquivo("../archivos/valoresEntradaWERTYU.txt");
    if (!arquivo.is_open()) {
        cerr << "O arquivo de entrada não pôde ser aberto!";
        return 1;
    }

    
    // Constrói o mapeamento de correção: cada tecla pressionada será associada
    // à tecla que está à sua esquerda no teclado QWERTY (baseado em layout americano).
    
    const string teclado = "`1234567890-=QWERTYUIOP[]\\ASDFGHJKL;'ZXCVBNM,./";
    
    // Mapa que armazena os pares: tecla errada → tecla correta
    unordered_map<char, char> mp; 
    for (size_t i = 1; i < teclado.size(); i++) {

        // Para cada tecla, associa à tecla anterior
        mp[teclado[i]] = teclado[i - 1]; 
    }

    string linha;
    // Lê o arquivo linha por linha
    while (getline(arquivo, linha)) {
        for (char &c : linha) {
            // Se não for espaço, tenta substituir pelo caractere correto
            if (c != ' '){
                c = mp[c];
            }  
        }
        // Imprime a linha corrigida
        cout << linha << '\n'; 
    }

    return 0;
}

