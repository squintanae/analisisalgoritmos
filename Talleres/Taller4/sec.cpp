//Taller 4: secuencia creciente dentro de una matriz cuadrada

/*
Elaborado por:
    -María José Niño
    -Santiago Quintana
*/

#include <bits/stdc++.h>


using namespace std;

struct indices{
    int x;
    int y;
};

void impM(vector<vector<int>>m, int n){
    cout<<endl;
    for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cout<<" "<<m[i][j]<<" ";
		}
		cout<<endl;
	}
}

void impMemo(vector<vector<indices>>m, int n){
    cout<<endl;
    for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cout<<" "<<m[i][j].x<<","<<m[i][j].y<<" ";
		}
		cout<<endl;
	}
}

int buscCamino(int i, int j, vector<vector<int>>m, vector<vector<int>>&memo,vector<vector<indices>> &tabIndices, int n){
    //si se desborda de la matriz

	if (i < 0 || i >= n || j < 0 || j >= n){
	    return 0;
	}
	if (memo[i][j] != -1){
        return memo[i][j];
	}
    //caminos
	int der = -1, izq = -1, arriba = -1, abajo = -1;

	//Mira el de la derecha
	if( !(j+1==n)) {
        if (((m[i][j] + 1) == m[i][j + 1])){
            tabIndices[i][j].x = 1;
            tabIndices[i][j].y = 0;
            der = 1 + buscCamino(i, j + 1, m, memo,tabIndices, n);
        }
	}

	//Mira el de la izquierda
	if( !(j - 1==-1)){
        if ( (m[i][j] + 1 == m[i][j - 1])){
            tabIndices[i][j].x = -1;
            tabIndices[i][j].y = 0;
            izq = 1 + buscCamino(i, j - 1, m, memo,tabIndices,n);
        }
	}

	//Mira el de arriba
	if( !(i-1 == -1)){
        if ((m[i][j] + 1 == m[i - 1][j])){
            tabIndices[i][j].x = 0;
            tabIndices[i][j].y = -1;
            arriba = 1 + buscCamino(i - 1, j, m, memo,tabIndices,n);
        }
	}

	//Mira el de abajo
	if( !(i+1==n)){
        if ( (m[i][j] + 1 == m[i + 1][j])){
            tabIndices[i][j].x = 0;
            tabIndices[i][j].y = 1;
            abajo = 1 + buscCamino(i + 1, j, m, memo,tabIndices,n);
        }
	}
    memo[i][j] = max({der, izq, abajo, arriba, 1});
	return memo[i][j];
}

void secuenciaLarga(vector<vector<int>>m, int n){
	int maxsecuencia = 1;
	indices maxIndice;
	maxIndice.x=0;
	maxIndice.y=0;
    //Tabla memoización
    //impM(m,n);
	vector<vector<int>> memo(n, vector<int> (n, -1));

	vector<vector<indices>> tabIndices;

	for(int i=0; i<n; i++){
            std::vector <indices> indi;
            for(int j=0; j<n; j++)
            {
                 indices indAux;
                 indAux.x=0;
                 indAux.y=0;
                 indi.push_back( indAux );
            }
            tabIndices.push_back(indi);
    }

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (memo[i][j] == -1){
                buscCamino(i, j, m, memo,tabIndices,n);
			}
			if(memo[i][j]>maxsecuencia){
                maxsecuencia=memo[i][j];
                maxIndice.x = i;
                maxIndice.y = j;
			}
		}
	}
	//impM(memo, n);
	//impMemo(tabIndices, n);
    cout<<endl;
    cout<<"La secuencia mas larga en una matriz de tamaño "<<n<<"x"<<n<<" es: ";
	while( !(tabIndices[maxIndice.x][maxIndice.y].x==0 && tabIndices[maxIndice.x][maxIndice.y].y==0) ){
        cout<<m[maxIndice.x][maxIndice.y]<<" ";
        int aux= maxIndice.x;
        maxIndice.x += tabIndices[maxIndice.x][maxIndice.y].y;
        maxIndice.y += tabIndices[aux][maxIndice.y].x;
	}
    cout<<m[maxIndice.x][maxIndice.y];
    cout<<endl;
}

void experimentos(){
    for(int i=10; i<=100;i=i+10){
        vector<vector<int>> mat;
        int p=1;
        for(int k=0; k<i; k++){
                std::vector <int> au;
                for(int j=0; j<i; j++)
                {
                     au.push_back( p );
                     p++;
                }
                mat.push_back(au);
        }
        //impM(mat, i);

        for(int q=0; q<i*4; q++){
            int iaux1 = rand() % i;
            int jaux1 = rand() % i;
            int iaux2 = rand() % i;
            int jaux2 = rand() % i;
            int aux = mat[iaux1][jaux1];
            mat[iaux1][jaux1]= mat[iaux2][jaux2];
            mat[iaux2][jaux2]= aux;
        }

        int n= mat.size();
        secuenciaLarga(mat,i);
	}
}

// Función principal
int main()
{
    vector<vector<int>> m{
        {10, 16,15,12},
        {9, 8, 7,13},
        {2, 5, 6,14},
        {3, 4, 1,11}
    };
    int n= m.size();
	secuenciaLarga(m,n);

	experimentos();



	return 0;
}

