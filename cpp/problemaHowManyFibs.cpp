// Problema: How Many Fibs?


// Bibliotecas importantes
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <fstream>

using namespace std;

//soma de inteiros grandes representados como strings
string somar(const string& a, const string& b) {
    string res;
    int i = int(a.size()) - 1, j = int(b.size()) - 1, carry = 0;

    // percorre de trás para frente adicionando dígito a dígito
    while (i >= 0 || j >= 0 || carry) {
        int soma = carry;
        if (i >= 0) soma += a[i--] - '0';
        if (j >= 0) soma += b[j--] - '0';
        res.push_back(char('0' + (soma % 10)));
        carry = soma / 10;
    }
    reverse(res.begin(), res.end());
    return res;
}

// comparação de dois inteiros grandes em string ---- retorna -1 se a<b, 0 se a==b, 1 se a>b                           
int comparar(const string& a, const string& b) {
    if (a.size() != b.size())
        return (a.size() < b.size()) ? -1 : 1;
    return a.compare(b);               // tamanhos iguais → lexicográfico
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // pré‑cálculo dos Fibonacci até exceder 10^100
    vector<string> fib = {"1", "2"};   // F1 = 1, F2 = 2
    const string LIM = "100000000000000000000000000000000000000000000000000000000000"
                       "000000000000000000000000000000000000";   // 10^100

    while (true) {
        string prox = somar(fib[fib.size() - 1], fib[fib.size() - 2]);
        if (comparar(prox, LIM) > 0) break;  // se passou de 10^100, parar
        fib.push_back(prox);
    }

    //leitura dos casos até “0 0”
    ifstream arquivo("../archivos/valoresEntradaHowManyFibs.txt");
    string a, b;
    while (arquivo >> a >> b, !(a == "0" && b == "0")) {
        if (comparar(a, b) > 0) swap(a, b);  // garantir a ≤ b

        // primeiro Fibonacci ≥ a
        auto lo = lower_bound(fib.begin(), fib.end(), a,
                              [](const string& f, const string& val) {
                                  return comparar(f, val) < 0;
                              });

        // primeiro Fibonacci > b
        auto hi = upper_bound(fib.begin(), fib.end(), b,
                              [](const string& val, const string& f) {
                                  return comparar(val, f) < 0;
                              });

        cout << (hi - lo) << '\n';  // quantidade dentro do intervalo
    }
    return 0;
}
