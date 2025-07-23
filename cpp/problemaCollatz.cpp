// Problema 3n + 1 Collatz

/*
 * Referencia bibliográfica:
 * Skiena, S. S., & Revilla, M. A. (2003). 
 * Programming Challenges: The Programming Contest Training Manual
 * Springer-Verlag. https://i.cs.hku.hk/~provinci/files/b2-programming_challenges.pdf
 */

#include <iostream>
#include <fstream> // Para leitura de arquivos externos

using namespace std;

int main(){
    
    // declarar variáveis 
    int i; // i é o limite inferior
	int j; // j é o limite superior

	// ler arquivo entrada.txt 
	ifstream entrada("../archivos/valoresEntradaCollatz.txt");

    //Verificar se o arquivo foi aberto corretamente
    if (!entrada) {
        cerr << "O arquivo de entrada não pôde ser aberto!" << endl;
        return 1; // Sair se o arquivo não puder ser aberto
    }

    // dados de entrada i,j
    while(entrada >> i >> j){
		int inferior = i;
		int superior = j;
		int longitudMax = 0; 

		if (i > j){
			// se i for maior que j
			// inverte os valores de i e j
			swap(i, j);
		}
	
		// laço para calcular sequência de Collatz
		for (int a = i; a <= j; a++){
			int aux = a;
			int contador = 1;
			while(aux != 1){

				// se o número for par
				// dividir por 2
				if (aux % 2 == 0){
					aux = aux / 2;
				
				// se o número for ímpar
				// multiplique por 3 j adicione 1
				}else{ // se o número for ímpar multiplique por 3 j adicione 1
					aux = (aux * 3) + 1;
					
				}
				// contador de comprimento de sequência
				// incrementa em 1
				contador++;
			}
			// se o contador for maior que o comprimento máximo 
			// o valor do contador é atribuído ao comprimento máximo
			if (contador > longitudMax) {
				longitudMax = contador;
			}
		}
		//Saida de dados
    	cout << inferior << " " << superior << " " << longitudMax << endl; 
	}

    return 0;
}
