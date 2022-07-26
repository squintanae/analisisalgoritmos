import pandas as pd
import time


def burbuja(vector):
    for i in range(len(vector)):
        for j in range(len(vector)-1):
            if vector[j+1] < vector[j]:
                aux = vector[j]
                vector[j] = vector[j+1]
                vector[j+1] = aux
                
def burbujaMejorada(vector):
    for i in range(len(vector)):
        for j in range(len(vector)-i-1):
            if vector[j+1] < vector[j]:
                aux = vector[j]
                vector[j] = vector[j+1]
                vector[j+1] = aux
                
def insercion(vector):
    j=1
    for j in range(len(vector)):
        k = vector[j]
        i = j-1
        while((-1 < i) and (k < vector[i])):
            vector[i+1] = vector[i]
            i = i-1
        vector[i+1] = k
 
def main():
    lecOrdenado = pd.read_excel('datos.xlsx',header=None, usecols="A",names=None, index_col=0, sheet_name="ordenado")    
    ordenado= lecOrdenado.index.values
    
    lecOrdenadoRev = pd.read_excel('datos.xlsx',header=None, usecols="A",names=None, index_col=0, sheet_name="ordenadorev")    
    ordenadoRev= lecOrdenadoRev.index.values
    
    lecAleatorio = pd.read_excel('datos.xlsx',header=None, usecols="A",names=None, index_col=0, sheet_name="aleatorio")    
    aleatorio= lecAleatorio.index.values
    
    ordenadoRev1 = ordenadoRev.tolist()
    ordenadoRev2 = ordenadoRev.tolist()
    ordenadoRev3 = ordenadoRev.tolist()
    
    aleatorio1 = aleatorio.tolist()
    aleatorio2 = aleatorio.tolist()
    aleatorio3 = aleatorio.tolist()
    
    inicio = time.time()
    burbuja(ordenadoRev1)
    fin = time.time()
    diferenciaBurbuja =  fin - inicio
    
    inicio = time.time()
    burbujaMejorada(ordenadoRev2)
    fin = time.time()
    diferenciaBurbujaMejorado =  fin - inicio
    
    inicio = time.time()
    insercion(ordenadoRev3)
    fin = time.time()
    diferenciaInsercion =  fin - inicio
    
    
    print("Tiempo de burbuja: ", diferenciaBurbuja)
    print("Tiempo de burbuja mejorado: ", diferenciaBurbujaMejorado)
    print("Tiempo de insercion: " , diferenciaInsercion)
    
        
if __name__ == "__main__":
    main()

     