/*
Elaborado por:
-María José Niño
-Santiago Quintana
*/

#include <iostream>
#include <math.h>

int inversoBinario(int n);
int inversoBinarioAuxiliar (int n , int b, int e, int t);
int mascara(int n , int b, int e);
int inversoBinarioIterativo(int n);
using namespace std;

int main()
{
    int n;
    int contador=0;
   // cout<<"Entrada n, Salida Dividit y vencer, Salida I";
    do{
        n = rand()%10000;
        cout << n<<","<<inversoBinario(n) <<","<<inversoBinarioIterativo(n)<< endl;
        contador ++;
    }while(contador!=100);
    return 0;
}

int inversoBinario(int n){
    if (n==0)
        return 0;
    return inversoBinarioAuxiliar(n , 0 ,floor(log2(n))+1,floor(log2(n))+1);
}

int inversoBinarioAuxiliar (int n , int b, int e, int t){
    if(b == e){
        if(n==0)
            return 0;
        else
            return pow( 2 , (t-e-1));
    }
    int q = floor((b+e)/2);
    int n1 = mascara(n,b,q);
    int n2 = mascara(n,q+1,e);
    return inversoBinarioAuxiliar(n1,b, q, t) + inversoBinarioAuxiliar(n2, q+1, e, t) ;
}

int mascara(int n , int b, int e){ //      0 3  101011001
    int masc = pow( 2 , ((e-b))+1) -1; //            1111
    masc = masc<<b;                //           000001111
    masc = n & masc;//                          000001001
    return masc;  //||
}


int inversoBinarioIterativo(int n){
    int tam = floor(log2(n));
    int res = 0;
    while(n!=0){
        res = res+( pow(2,tam)*(n%2));
        n=n/2;
        tam--;
    }
    return res;
}

