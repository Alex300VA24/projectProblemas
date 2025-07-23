// Problema: Jolly Jumpers

/*
 * Referencia bibliográfica:
 * Skiena, S. S., & Revilla, M. A. (2003). 
 * Programming Challenges: The Programming Contest Training Manual
 * Springer-Verlag. https://i.cs.hku.hk/~provinci/files/b2-programming_challenges.pdf
 */

#include <iostream>   
#include <vector>     // Estrutura de dados dinâmica para armazenar a sequência
#include <cmath>      // Função abs() para valor absoluto
#include <set>        // Conjunto para armazenar diferenças únicas
#include <fstream>    // Para leitura de arquivos externos

using namespace std;

int main() {

    /* Tenta abrir o arquivo de entrada contendo as sequências.
       Cada sequência no arquivo começa com um inteiro n (tamanho),
       seguido de n inteiros que compõem a própria sequência.         */
    ifstream arquivo("../archivos/valoresEntradaJolly.txt");
    if (!arquivo.is_open()) {
        cerr << "O arquivo de entrada não pôde ser aberto!";
        return 1;  
    }

    // Armazena os resultados “Jolly” ou “Not Jolly”
    vector<string> saida;
    
    // Tamanho da sequência (n)
    int numero;

    // Lê n; sai do loop quando EOF            
    while (arquivo >> numero) {

        // Vetor para guardar a sequência           
        vector<int> sequenca(numero);     
        
        for (int i = 0; i < numero; ++i) {
            
            // Lê os n inteiros sucessivos
            arquivo >> sequenca[i];       
        }

        // Armazena diferenças únicas
        set<int> setDiferencas;           
        for (int i = 1; i < numero; ++i) {

            // Valor absoluto da diferença de valores sequenciais
            int diferenca = abs(sequenca[i] - sequenca[i - 1]); 
            
            // Registra somente diferenças válidas (entre 1 e n-1).
            if (diferenca >= 1 && diferenca <= numero - 1) {
                setDiferencas.insert(diferenca);
            }
        }

        // Verifique se é "Jolly" ou "Not Jolly"
        if ((int)setDiferencas.size() == numero - 1) {
            saida.push_back("Jolly");
        } else {
            saida.push_back("Not Jolly");
        }
    }

    // Imprime os resultados na mesma ordem das sequências lidas.
    for (const string &cadena : saida) {
        cout << cadena << endl;
    }

    return 0;
}
