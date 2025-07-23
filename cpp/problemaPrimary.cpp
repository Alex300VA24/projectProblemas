// Problema: Primary Arithmetic

/* Referencia bibliográfica:
 * Skiena, S. S., & Revilla, M. A. (2003). 
 * Programming Challenges: The Programming Contest Training Manual
 * Springer-Verlag. https://i.cs.hku.hk/~provinci/files/b2-programming_challenges.pdf
*/

#include <iostream>   
#include <fstream>    // Leitura de arquivo/*

using namespace std;

int main() {

    // Operandos (até 18 dígitos)
    unsigned long long a, b;           

    // Abre o arquivo
    ifstream arquivo("../archivos/valoresEntradaPrimary.txt"); 
    //Verificar se o arquivo foi aberto corretamente
    if (!arquivo) {
        cerr << "O arquivo de entrada não pôde ser aberto!" << endl;
        return 1; // Sair se o arquivo não puder ser aberto
    }

    /* Lê pares de números até encontrar “0 0”.
       A expressão (a != 0 || b != 0) garante que “0 0” encerra o loop. */
    while (arquivo >> a >> b && (a != 0 || b != 0)) {

        int carries = 0;   // Contador de operações de carry
        int carry   = 0;   // Vai‑um atual (0 ou 1)

        /* Processa os dígitos menos significativos primeiro,
           dividindo cada número por 10 a cada iteração.          */
        while (a > 0 || b > 0) {

            // Soma dos dígitos + o anterior
            int soma = (a % 10) + (b % 10) + carry; 

            if (soma > 9) {    // Houve novo carry
                carry = 1;
                ++carries;     // Incrementa o total de carries
            } else {
                carry = 0;     // Sem carry nesta posição
            }

            a /= 10;  // Remove o dígito já processado
            b /= 10;
        }

        /* Emite a mensagem apropriada conforme o número de carries encontrados */
        if (carries == 0)
            cout << "No carry operation.\n";
        else if (carries == 1)
            cout << "1 carry operation.\n";
        else
            cout << carries << " carry operations.\n";
    }

    return 0; 
}