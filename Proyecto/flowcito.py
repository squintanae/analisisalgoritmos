import time
from matplotlib import offsetbox
import pygame, sys
import numpy as np
from pygame.math import Vector2



class CUADRADO:
    def __init__(self, color, punto, puntoColor): 
        self.color = color #Color actual de la celda
        self.punto = punto #booleano indica si es un punto
        self.puntoColor = puntoColor #en caso de ser punto, indica su color
        self.direccionSiguiente = Vector2(0,0)
        self.puntoAnterior = Vector2(-1,-1)
        self.longitud = 0
        self.bordes =0 
    def constructor(self):
        self.color = 0 #Color actual de la celda
        self.punto = False #booleano indica si es un punto
        self.puntoColor = -1 #en caso de ser punto, indica su color
        self.direccionSiguiente = Vector2(0,0)
        self.puntoAnterior = Vector2(-1,-1)
        self.longitud = 0
        
class TABLERO:

    def __init__(self):
        self.tablero = [] #matriz de cuadrados
        self.cargarTablero(numCeldas)
        self.colorActual = 0
        self.posActual = Vector2(0,0)
        self.activo = False
        self.nodosInicio = {} #GUARDA LA FILA Y LA COLUMA, ES UNA DUPLA [row,column]  
        self.nodosFinal = {}
        self.nodos = []
        self.dists = {}
        self.ordenados = []
    
    def bordes(self):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].puntoColor>0:
                    self.tablero[i][j].color = self.tablero[i][j].puntoColor
                if i == 0 and j== 0 :
                    self.tablero[i][j].bordes = 1
                    
                elif  i == 0 and j== numCeldas-1 :
                    self.tablero[i][j].bordes = 2
                    
                    
                elif  i == numCeldas-1 and j== 0 :
                    self.tablero[i][j].bordes = 3

                elif  i == numCeldas-1 and j==numCeldas-1 :
                    self.tablero[i][j].bordes = 4                
                elif  i == 0 :
                    self.tablero[i][j].bordes = 5
                elif  j== 0 :
                    self.tablero[i][j].bordes = 6
                elif  i == numCeldas-1 :
                    self.tablero[i][j].bordes = 7
                elif  j== numCeldas-1 :
                    self.tablero[i][j].bordes = 8

                else :
                    self.tablero[i][j].bordes = 0


    def ordenar(self):
        numeros=list(self.dists)
        for i in range(0,len(self.dists)):
            min=self.dists[numeros[0]]
            for numero in self.dists:
                if self.dists[numero]<min:
                    min=self.dists[numero]
            self.ordenados.append(numero)         
            self.dists.pop(numero)

    def inicioSolucion(self):
        
        global ganoJueg
        if ganoJuego == False:
            self.borrar()
            self.bordes()
            
            for fila in range (numCeldas):  #Recorre la matriz
                for columna in range (numCeldas):
                    color = self.tablero[fila][columna].puntoColor
                    if self.tablero[fila][columna].punto == True: #Si es un color, revisar si es una bola  
                        if color in self.nodosInicio: #busca cuales son los nodos de final a medida que recorre
                            self.nodosFinal[color] = [fila,columna]   
                            self.dists[color] = abs(fila-self.nodosInicio[color][0]) + abs(columna-self.nodosInicio[color][1]) #DISTANCIA ENTRE AMBOS  NODOS, SUMA LA DIF EN X Y EN Y
                        else: #si no el nodo es un nodo inicial 
                            self.nodosInicio[color] = [fila,columna]   
                        self.nodos.append([fila,columna,color]) #CONTIENE TODOS LOS PUNTOS SEA INICIO O FINAL
        self.ordenar()
        return self.solucion()

    def revisar(self):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color >0:
                    color = self.tablero[i][j].color
                    #CASO IDEAL
                    if self.tablero[i][j].bordes == 0:
                        if self.tablero[i+1][j].color >0  and  self.tablero[i+1][j].color != color:
                            if self.tablero[i-1][j].color >0  and  self.tablero[i-1][j].color != color:
                                if self.tablero[i][j+1].color >0  and  self.tablero[i][j+1].color != color:
                                    if self.tablero[i][j-1].color >0  and  self.tablero[i][j-1].color != color:
                                        return False
                    
                        if self.tablero[i+1][j].color == color and self.tablero[i-1][j].color == color and self.tablero[i][j+1].color == color:
                            return False
                        elif self.tablero[i+1][j].color == color and self.tablero[i-1][j].color == color and self.tablero[i][j-1].color == color:
                            return False
                        elif self.tablero[i+1][j].color == color and self.tablero[i][j+1].color == color and self.tablero[i][j-1].color == color:
                            return False
                        elif self.tablero[i-1][j].color == color and self.tablero[i][j+1].color == color and self.tablero[i][j-1].color == color:
                            return False

                    #CASO ESQUINA IZQUIERDA ARRIBA
                    elif self.tablero[i][j].bordes == 1:
                        if self.tablero[i+1][j].color >0  and  self.tablero[i+1][j].color != color:
                            if self.tablero[i][j+1].color >0  and  self.tablero[i][j+1].color != color:
                                return False

                    #CASO ESQUINA DERECHA ARRIBA
                    elif self.tablero[i][j].bordes == 2:
                        if self.tablero[i+1][j].color >0  and  self.tablero[i+1][j].color != color:
                            if self.tablero[i][j-1].color >0  and  self.tablero[i][j-1].color != color:
                                return False

                    #CASO ESQUINA IZQUIERDA ABAJO
                    elif self.tablero[i][j].bordes == 3:
                        
                        if self.tablero[i-1][j].color >0  and  self.tablero[i-1][j].color != color:
                            if self.tablero[i][j+1].color >0  and  self.tablero[i][j+1].color != color:
                                return False

                    #CASO ESQUINA DERECHA ABAJO
                    elif self.tablero[i][j].bordes == 4:
                        if self.tablero[i-1][j].color >0  and  self.tablero[i-1][j].color != color:
                            if self.tablero[i][j-1].color >0  and  self.tablero[i][j-1].color != color:
                                return False
                                
                    #BORDE SUPERIOR
                    elif self.tablero[i][j].bordes == 5:
                        if self.tablero[i+1][j].color >0  and  self.tablero[i+1][j].color != color:
                            if self.tablero[i][j+1].color >0  and  self.tablero[i][j+1].color != color:
                                if self.tablero[i][j-1].color >0  and  self.tablero[i][j-1].color != color:
                                    return False
        
                        if self.tablero[i+1][j].color == color and self.tablero[i][j+1].color == color and self.tablero[i][j-1].color == color:
                            return False
                    
                    #BORDE IZQUIERDO
                    elif self.tablero[i][j].bordes == 6:
                        if self.tablero[i+1][j].color >0  and  self.tablero[i+1][j].color != color:
                            if self.tablero[i-1][j].color >0  and  self.tablero[i-1][j].color != color:
                                if self.tablero[i][j+1].color >0  and  self.tablero[i][j+1].color != color:
                                    return False
                    
                        if self.tablero[i+1][j].color == color and self.tablero[i-1][j].color == color and self.tablero[i][j+1].color == color:
                            return False
                    
                    #BORDE INFERIOR
                    elif self.tablero[i][j].bordes == 7:
                        if self.tablero[i-1][j].color >0  and  self.tablero[i-1][j].color != color:
                            if self.tablero[i][j+1].color >0  and  self.tablero[i][j+1].color != color:
                                if self.tablero[i][j-1].color >0  and  self.tablero[i][j-1].color != color:
                                    return False
        
                        if self.tablero[i-1][j].color == color and self.tablero[i][j+1].color == color and self.tablero[i][j-1].color == color:
                            return False
                        
                    #BORDE DERECHO
                    elif self.tablero[i][j].bordes == 8:
                        if self.tablero[i+1][j].color >0  and  self.tablero[i+1][j].color != color:
                            if self.tablero[i-1][j].color >0  and  self.tablero[i-1][j].color != color:
                                if self.tablero[i][j-1].color >0  and  self.tablero[i][j-1].color != color:
                                    return False
                    
                        if self.tablero[i+1][j].color == color and self.tablero[i-1][j].color == color and self.tablero[i][j-1].color == color:
                            return False
        return True

    def solucion(self):
        self.dibujarCeldas()
        pygame.display.update()
        time.sleep(0.2)
        if self.revisar() == False:
            return False
        if self.ganamos() == True:
            return True
        
        for color in self.ordenados:
            
            nodoInicio = self.nodosInicio[color]
            nodoFinal = self.nodosFinal[color]
            if  ( (abs(nodoFinal[0]-nodoInicio[0]) + abs(nodoFinal[1]-nodoInicio[1]))>1):
                direcciones = []
                #CASO IDEAL 
                if self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==0:
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]+1].color ==0:
                        direcciones.append("derecha")
                    
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]-1].color==0:
                        direcciones.append("toy")

                    if self.tablero[ nodoInicio[0]+1 ][nodoInicio[1]].color==0:
                        direcciones.append("abajo")
                    
                    if self.tablero[ nodoInicio[0]-1 ][nodoInicio[1]].color==0:
                        direcciones.append("arriba")

                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==1:
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]+1].color ==0:
                        direcciones.append("derecha")

                    if self.tablero[ nodoInicio[0]+1 ][nodoInicio[1]].color==0:
                        direcciones.append("abajo")
                #CASO ESQUINA DERECHA ARRIBA
                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==2:
                    
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]-1].color==0:
                        direcciones.append("izquierda")

                    if self.tablero[ nodoInicio[0]+1 ][nodoInicio[1]].color==0:
                        direcciones.append("abajo")
                    
                #CASO ESQUINA IZQUIERDA ABAJO 
                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==3:

                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]+1].color ==0:
                        direcciones.append("derecha")
                    
                    if self.tablero[ nodoInicio[0]-1 ][nodoInicio[1]].color==0:
                        direcciones.append("arriba")

                #CASO ESQUINA DERECHA ABAJO
                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==4:

                    
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]-1].color==0:
                        direcciones.append("toy")

                    if self.tablero[ nodoInicio[0]-1 ][nodoInicio[1]].color==0:
                        direcciones.append("arriba")
                
                #CASO BORDE SUPERIOR
                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==5:

                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]+1].color ==0:
                        direcciones.append("derecha")
                    
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]-1].color==0:
                        direcciones.append("toy")

                    if self.tablero[ nodoInicio[0]+1 ][nodoInicio[1]].color==0:
                        direcciones.append("abajo")
                    
                #CASO BORDE IZQUIERDO
                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==6:

                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]+1].color ==0:
                        direcciones.append("derecha")
  
                    if self.tablero[ nodoInicio[0]+1 ][nodoInicio[1]].color==0:
                        direcciones.append("abajo")
                    
                    if self.tablero[ nodoInicio[0]-1 ][nodoInicio[1]].color==0:
                        direcciones.append("arriba")
                
                #CASO BORDE ABAJO
                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==7:

                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]+1].color ==0:
                        direcciones.append("derecha")
                    
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]-1].color==0:
                        direcciones.append("toy")
                    
                    if self.tablero[ nodoInicio[0]-1 ][nodoInicio[1]].color==0:
                        direcciones.append("arriba")

                #CASO BORDE DERECHO
                elif self.tablero[ nodoInicio[0] ][nodoInicio[1]].bordes ==8:
                    
                    if self.tablero[ nodoInicio[0] ][nodoInicio[1]-1].color==0:
                        direcciones.append("toy")

                    if self.tablero[ nodoInicio[0]+1 ][nodoInicio[1]].color==0:
                        direcciones.append("abajo")
                    
                    if self.tablero[ nodoInicio[0]-1 ][nodoInicio[1]].color==0:
                        direcciones.append("arriba")
                

                if len(direcciones)==0:
                    return False
                
                for d in direcciones:
                    if d == "derecha" and nodoInicio[1]+1 < numCeldas:
                        nodoInicio[1]+=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[1]-=1
                    
                    elif d == "toy" and nodoInicio[1]-1 >= 0:
                        nodoInicio[1]-=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color 
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[1]+=1

                    elif d == "arriba" and nodoInicio[0]-1 >= 0:
                        nodoInicio[0]-=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[0]+=1

                    elif d == "abajo" and nodoInicio[0] < numCeldas:
                        nodoInicio[0]+=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[0]-=1
        return False                
              

    def ganamos(self):
        ganador = True
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color == 0:
                    ganador = False
        return ganador
                

    def borrar(self):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color > 0:
                    self.tablero[i][j].color=0
                    self.tablero[i][j].direccionSiguiente = Vector2(0,0)
                    self.tablero[i][j].longitud = 0

    def Mover(self,direccion):
        long = self.tablero[ int(self.posActual[1])][ int(self.posActual[0])].longitud 
        movAux = self.posActual + direccion
        posAnteriorX = self.posActual[0]
        posAnteriorY = self.posActual[1]
        atras = False
        if self.activo == True:
            if movAux[0] >=0 and movAux[0]<numCeldas and  movAux[1] >=0 and movAux[1]<numCeldas:   
                if self.tablero[ int(movAux[1])][ int(movAux[0])].punto == False or self.tablero[ int(movAux[1])][ int(movAux[0])].puntoColor == self.colorActual:
                    self.tablero[ int( self.posActual[1])][int(self.posActual[0])].direccionSiguiente = direccion
                    if self.tablero[ int(movAux[1]) ][ int(movAux[0])].longitud == self.tablero[ int(self.posActual[1]) ][ int(self.posActual[0])].longitud-1 and self.tablero[int( movAux[1]) ][ int(movAux[0])].color == self.colorActual:
                        self.tablero[ int( self.posActual[1])][int( self.posActual[0] )].constructor()
                        atras = True

                    #me movi
                    self.posActual += direccion # vector (x,y)
                    posX = int(self.posActual[0])
                    posY = int(self.posActual[1])

                    if self.tablero[ posY ][posX].color != self.colorActual and  self.tablero[ posY ][posX].color != 0 and self.tablero[ posY ][posX].punto != True:
                        self.cortar(self.tablero[ posY ][posX].color, self.tablero[ posY ][posX].longitud)

                    if self.tablero[ posY ][posX].color == self.colorActual and self.tablero[ posY ][posX].longitud< long+1:
                        self.cortar(self.tablero[ posY ][posX].color, self.tablero[ posY ][posX].longitud)
                        self.tablero[ posY ][posX].direccionSiguiente = Vector2(0,0)

                    elif self.tablero[ posY ][posX].punto == True and self.tablero[ posY ][posX].longitud==1:
                        self.reiniciar(self.colorActual)
                        self.tablero[ posY ][posX].direccionSiguiente = Vector2(0,0)
                    else: 
                        self.tablero[ posY ][posX].puntoAnterior= Vector2(posAnteriorX, posAnteriorY)

                        
                        if atras == False and self.tablero[ posY ][posX].punto == False:
                            self.tablero[ posY ][posX].longitud = long+1
                        self.tablero[ posY ][posX].color = self.colorActual

                        if  self.tablero[ posY ][posX].punto == True and self.tablero[ posY ][posX].longitud!=1:
                            self.activo = False

    def cortar(self, color, longitud):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color == color and self.tablero[i][j].longitud > longitud:
                    self.tablero[i][j].constructor()
                if self.tablero[i][j].color == color and self.tablero[ i ][j].punto == True and self.tablero[i][j].longitud!=1:
                    self.tablero[i][j].color =0
                    self.tablero[i][j].puntoAnterior = Vector2(0,0)

    def reiniciar(self, color):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color == color and self.tablero[i][j].punto == False:
                    self.tablero[i][j].constructor()

    def cargarTablero(self, dim):
        nomArc = 'tab'+ str(dim)+'.txt'
        auxColores = np.loadtxt(nomArc,dtype=int) 
        for i in range(numCeldas):
            self.tablero.append([])
            for j in range(numCeldas):
                punto = False
                colorPunto = 0
                if(auxColores[i][j]!=0):
                    punto=True
                    colorPunto = auxColores[i][j]
                cuadrado = CUADRADO( 0, punto,colorPunto)
                self.tablero[i].append(cuadrado)


    def dibujarCuadricula(self):
        for i in range(numCeldas+1): #lineas verticales
            test_surface = pygame.Surface((tamCuadricula, grosorCuadricula ))
            test_surface.fill(colorCuadricula)
            screen.blit(test_surface, (offsetX,offsetY+ (grosorCuadricula+tamCuadrito)*i))
            test_surface = pygame.Surface((grosorCuadricula, tamCuadricula ))
            test_surface.fill(colorCuadricula)
            screen.blit(test_surface, (offsetX + (grosorCuadricula+tamCuadrito)*i,offsetY))
        
        if numCeldas != tabMin: 
            izqIma = pygame.image.load('izq.png')
            screen.blit(izqIma,(120, 500))

        if numCeldas != tabMax:
            derIma = pygame.image.load('der.png')
            screen.blit(derIma,(375, 500))

        boton = pygame.image.load('botoncitoo.png')
        screen.blit(boton,(193, 525))
        
        mov = -7
        movY= 20
        font = pygame.font.Font("NotoSans-Regular.ttf", 70)
        textsurface = font.render('f', False, rojo)
        screen.blit(textsurface,(160+mov, movY))
        textsurface = font.render('l', False, verde)
        screen.blit(textsurface,(186+mov, movY))
        textsurface = font.render('o', False, azul)
        screen.blit(textsurface,(200+mov, movY))
        textsurface = font.render('w', False, amarillo)
        screen.blit(textsurface,(240+mov, movY))
        textsurface = font.render('free', False, (200, 200, 200))
        screen.blit(textsurface,(320+mov, movY))

        global ganoJueg
        if ganoJuego == True:
            font = pygame.font.Font("NotoSans-Bold.ttf", 23)
            textsurface = font.render('Ganaste :)', False, (230,192,233))
            screen.blit(textsurface,(240, 505))

    def dibujarCeldas(self):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[j][i].punto== True:
                    if self.tablero[j][i].color!=0:  
                        test_surface = pygame.Surface((tamCuadrito+1, tamCuadrito+1 ))
                        test_surface.fill(colores[self.tablero[j][i].color])
                        screen.blit(test_surface,(offsetX+grosorCuadricula+(i*(tamCuadrito+grosorCuadricula)),offsetY+ grosorCuadricula+(j*(tamCuadrito+grosorCuadricula))))
                    else: 
                        test_surface = pygame.Surface((tamCuadrito+1, tamCuadrito+1 ))
                        test_surface.fill(colores[self.tablero[j][i].color])
                        screen.blit(test_surface,(offsetX+grosorCuadricula+(i*(tamCuadrito+grosorCuadricula)),offsetY+ grosorCuadricula+(j*(tamCuadrito+grosorCuadricula))))

                    pygame.draw.circle(screen, negro, (offsetX+grosorCuadricula+(i*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ,offsetY+ grosorCuadricula+(j*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ), (tamCuadrito/2))
                    pygame.draw.circle(screen, colores[self.tablero[j][i].puntoColor], (offsetX+grosorCuadricula+(i*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ,offsetY+ grosorCuadricula+(j*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ), (tamCuadrito/2) -3)
                else: 
                    test_surface = pygame.Surface((tamCuadrito+1, tamCuadrito+1 ))
                    test_surface.fill(colores[self.tablero[j][i].color])
                    screen.blit(test_surface,(offsetX+grosorCuadricula+(i*(tamCuadrito+grosorCuadricula)),offsetY+ grosorCuadricula+(j*(tamCuadrito+grosorCuadricula))))

    def puntoSeleccionado(self, pos):

        x = int(pos[0])
        y = int(pos[1])
        
        if self.tablero[y][x].punto == True:
            for i in range(numCeldas):
                for j in range(numCeldas):
                    if self.tablero[y][x].puntoColor == self.tablero[i][j].color:
                        self.tablero[i][j].color = 0
                        self.tablero[i][j].longitud=0

            self.tablero[y][x].color = self.tablero[y][x].puntoColor
            self.colorActual = self.tablero[y][x].color
            self.posActual = Vector2(x,y)
            self.tablero[y][x].longitud = 1
            self.activo = True
        elif self.tablero[y][x].color !=0:
            self.cortar(self.tablero[y][x].color, self.tablero[y][x].longitud)
            self.posActual = Vector2(x,y)
            self.colorActual = self.tablero[y][x].color
            self.activo = True

    def verificarGanador(self):
        ganador=True
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color == 0:
                    ganador = False
        if ganador == True:
            global ganoJuego
            ganoJuego = True
            

class MAIN:
    def __init__(self):
        self.tab = TABLERO()
    def draw_elements(self):
        self.tab.dibujarCuadricula()
        self.tab.dibujarCeldas()
    def seleccionarPunto(self, pos):
        self.tab.puntoSeleccionado(pos)
    def verificar(self):
        if ganoJuego == False:
            self.tab.verificarGanador()
   
    

pygame.init() 
tabMin= 4
tabMax =10
tamJuego = 600
tamCuadricula = 350
numCeldas = 4
grosorCuadricula = 2
offsetX = 120
offsetY = 120
tamCuadrito = (tamCuadricula- ((numCeldas+1)*grosorCuadricula))/numCeldas

colorCuadricula = (141, 117, 117)
colorFondo = (0, 0, 0 )


rojo=(253,1,0) 
verde=(0,141,0) 
azul=(12,42,254)
amarillo=(233,224,0)
naranja=(250,137,0) 
magenta=(255,10,201) 
celeste=(7,252,253) 
morado=(129,0,127)
vinotinto=(167,42,40)

negro =(38, 33, 40 )
quintana = ( 101, 22, 32 )
colores = [negro, rojo, verde, azul, amarillo,naranja, magenta,celeste,morado,vinotinto, quintana]

ganoJuego = False

screen = pygame.display.set_mode((tamJuego,tamJuego))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

def posMouse(x,y):
    if x < grosorCuadricula + offsetX or x > (grosorCuadricula+tamCuadrito)*numCeldas +grosorCuadricula + offsetX:
        return (-1,-1)

    if y < grosorCuadricula + offsetY or y > (grosorCuadricula+tamCuadrito)*numCeldas +grosorCuadricula + offsetY:
        return (-1,-1) 

    i = (((grosorCuadricula+tamCuadrito)*numCeldas +grosorCuadricula + offsetX) - x ) / (grosorCuadricula+ tamCuadrito)
    j = (((grosorCuadricula+tamCuadrito)*numCeldas +grosorCuadricula + offsetY) - y ) / (grosorCuadricula+ tamCuadrito)
    return ((int(i)-(numCeldas-1))*(-1),(int(j)-(numCeldas-1))*(-1))

selecInicial = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.verificar()
                

        if event.type == pygame.MOUSEBUTTONUP:
            selecInicial= True
            pos = pygame.mouse.get_pos()
            if pos[0]>121 and pos[0]<211 and pos[1]>503 and pos[1]<541:
                if numCeldas != tabMin:
                    ganoJuego = False
                    numCeldas= numCeldas-1
                    tamCuadrito = (tamCuadricula- ((numCeldas+1)*grosorCuadricula))/numCeldas
                    main_game = MAIN()
            
            if pos[0]>375 and pos[0]<470 and pos[1]>502 and pos[1]<542:
                if numCeldas != tabMax:
                    ganoJuego = False
                    numCeldas= numCeldas+1
                    tamCuadrito = (tamCuadricula- ((numCeldas+1)*grosorCuadricula))/numCeldas
                    main_game = MAIN()

            if pos[0]>222 and pos[0]<364 and pos[1]>553 and pos[1]<580:
                resul = main_game.tab.inicioSolucion()
                if resul == True:
                    print("Solucionado")
                else:
                    print("No solucionado")

            indi= posMouse(pos[0], pos[1])
            if indi[0]!=-1:
                main_game.seleccionarPunto(indi)

        if selecInicial==True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main_game.tab.Mover( Vector2(0,-1) )
                if event.key == pygame.K_RIGHT:
                    main_game.tab.Mover( Vector2(1,0) )
                if event.key == pygame.K_DOWN:
                    main_game.tab.Mover( Vector2(0,1) )
                if event.key == pygame.K_LEFT:
                    main_game.tab.Mover( Vector2(-1,0) )

    screen.fill(colorFondo)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60) #no correra mas rapido que 60 por segundo