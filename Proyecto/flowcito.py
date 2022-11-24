##Elaborado por:
# - María José Niño Rodriguez
# - David Santiago Quintana


#Librerias usadas
import time
from matplotlib import offsetbox
import pygame, sys
import numpy as np
from pygame.math import Vector2


#Clase cuadrado, contiene la información de cada cuadricula
class CUADRADO:
    def __init__(self, color, punto, puntoColor): 
        self.color = color #Color actual de la celda
        self.punto = punto #booleano indica si es un punto
        self.puntoColor = puntoColor #en caso de ser punto, indica su color
        self.direccionSiguiente = Vector2(0,0)
        self.puntoAnterior = Vector2(-1,-1)
        self.longitud = 0
        self.bordes =0 
        self.ordenados= []
        
    def constructor(self):
        self.color = 0 #Color actual de la celda
        self.punto = False #booleano indica si es un punto
        self.puntoColor = -1 #en caso de ser punto, indica su color
        self.direccionSiguiente = Vector2(0,0)
        self.puntoAnterior = Vector2(-1,-1)
        self.longitud = 0
        

#Clase Tablero, cuenta con la información del juego
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
        self.historial =[]
    
    #Al solucionarse solo el juego, primero se le asigna a los nodos que son puntos su color  
    def colorInicial(self):
        for i in range(numCeldas+2): 
            for j in range(numCeldas+2): 
                if self.tablero[i][j].puntoColor>1:
                    self.tablero[i][j].color = self.tablero[i][j].puntoColor
                if i == 0 or j == 0 or i == numCeldas+1 or j == numCeldas+1  :
                    self.tablero[i][j].color =1
        
       
                
                
    #Se carga el tablero con borde de 1 
    def cargarTableroSolu(self, dim):
        nomArc = 'tabRes'+ str(dim)+'.txt'
        auxColores = np.loadtxt(nomArc,dtype=int) 
        for i in range(numCeldas+2):
            self.tablero.append([])
            for j in range(numCeldas+2):
                punto = False
                colorPunto = 0
                if(auxColores[i][j]!=0 and auxColores[i][j]>=2 ):
                    punto=True
                    colorPunto = auxColores[i][j]
                cuadrado = CUADRADO( 0, punto,colorPunto)
                self.tablero[i].append(cuadrado)

    #Dibuja las cedas en el caso de el programa se este solucionando por si mismo 
    def dibujarCeldasSolu(self):
        for i in range(1,numCeldas+1):
            for j in range(1,numCeldas+1):
                if self.tablero[j][i].punto== True:
                    if self.tablero[j][i].color!=0:  
                        test_surface = pygame.Surface((tamCuadrito+1, tamCuadrito+1 ))
                        test_surface.fill(colores[self.tablero[j][i].color])
                        screen.blit(test_surface,(offsetX+grosorCuadricula+((i-1)*(tamCuadrito+grosorCuadricula)),offsetY+ grosorCuadricula+((j-1)*(tamCuadrito+grosorCuadricula))))
                    else: 
                        test_surface = pygame.Surface((tamCuadrito+1, tamCuadrito+1 ))
                        test_surface.fill(colores[self.tablero[j][i].color])
                        screen.blit(test_surface,(offsetX+grosorCuadricula+((i-1)*(tamCuadrito+grosorCuadricula)),offsetY+ grosorCuadricula+((j-1)*(tamCuadrito+grosorCuadricula))))

                    pygame.draw.circle(screen, negro, (offsetX+grosorCuadricula+((i-1)*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ,offsetY+ grosorCuadricula+((j-1)*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ), (tamCuadrito/2))
                    pygame.draw.circle(screen, colores[self.tablero[j][i].puntoColor], (offsetX+grosorCuadricula+((i-1)*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ,offsetY+ grosorCuadricula+((j-1)*(tamCuadrito+grosorCuadricula))+ tamCuadrito/2 ), (tamCuadrito/2) -3)
                else: 
                    test_surface = pygame.Surface((tamCuadrito+1, tamCuadrito+1 ))
                    test_surface.fill(colores[self.tablero[j][i].color])
                    screen.blit(test_surface,(offsetX+grosorCuadricula+((i-1)*(tamCuadrito+grosorCuadricula)),offsetY+ grosorCuadricula+((j-1)*(tamCuadrito+grosorCuadricula))))

    #Carga la infomración inicial al momento solucionarse por si mismo
    def inicioSolucion(self):
        self.tablero = []
        self.cargarTableroSolu(numCeldas)
        self.dibujarCeldasSolu()

        global ganoJueg

        if ganoJuego == False:
            self.borrar()
            self.colorInicial()
            self.dibujarCeldasSolu()
            pygame.display.update()

            for fila in range (1,numCeldas+1):  #Recorre la matriz
                for columna in range(1,numCeldas+1):
                    color = self.tablero[fila][columna].puntoColor
                    if self.tablero[fila][columna].color >0: #Si es un color, revisar si es una bola  
                        if color in self.nodosInicio: #busca cuales son los nodos de final a medida que recorre
                            self.nodosFinal[color] = [fila,columna]   
                            self.dists[color] = abs(fila-self.nodosInicio[color][0]) + abs(columna-self.nodosInicio[color][1]) #DISTANCIA ENTRE AMBOS  NODOS, SUMA LA DIF EN X Y EN Y
                        else: #si no el nodo es un nodo inicial 
                            self.nodosInicio[color] = [fila,columna]        
        return self.solucion()
    
    #Revisa la heuristica para validar si la posición actual del tablero es valida o no 
    def revisar(self):
        for i in range (1,numCeldas+1): 
            for j in range (1,numCeldas+1): 
                if self.tablero[i][j].color >0:
                    color = self.tablero[i][j].color
                    #CASO IDEAL
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
        return True

    #Función recursiva que evalua los posibles movimientos de los nodos hasta llegar a una solución del tablero 
    def solucion(self):
        self.dibujarCeldasSolu()
        pygame.display.update()
        time.sleep(0.001) #Tiempo en segundos de retraso, para poder visualizar los movimientos
        if self.revisar() == False:
            return False
        if self.ganamos() == True:
            return True
        #Recorre los nodos de colores
        for color in self.nodosInicio:
            nodoInicio = self.nodosInicio[color]
            nodoFinal = self.nodosFinal[color]
            #Si la distancia entre los nodos del mismo color es mayor a 1, no estan conectados los nodos
            if  ( (abs(nodoFinal[0]-nodoInicio[0]) + abs(nodoFinal[1]-nodoInicio[1]))>1):
                direcciones = []

                #Evalua los posibles movimientos del nodo, en caso de cumplir se agrega al arreglo de direcciones
                if self.tablero[ nodoInicio[0] ][nodoInicio[1]+1].color ==0 :
                    direcciones.append("derecha")
        
                if self.tablero[ nodoInicio[0] ][nodoInicio[1]-1].color==0 :
                    direcciones.append("toy")

                if self.tablero[ nodoInicio[0]+1 ][nodoInicio[1]].color==0 :
                    direcciones.append("abajo")
                
                if self.tablero[ nodoInicio[0]-1 ][nodoInicio[1]].color==0 :
                    direcciones.append("arriba")

                if len(direcciones)==0:
                    return False

                #Recorre las direcciones y se desplaza el nodo para evaluar si con ese movimiento se encuentra la solución 
                #Se genera el llamado recursivo, en caso de no cumplir como solución se devuelve el movimiento
                for d in direcciones:
                    if d == "derecha" :
                        nodoInicio[1]+=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[1]-=1
                    

                    elif d == "toy" :
                        nodoInicio[1]-=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color 
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[1]+=1

                    elif d == "arriba":
                        nodoInicio[0]-=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[0]+=1

                    elif d == "abajo" :
                        nodoInicio[0]+=1
                        self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = color
                        if self.solucion() == True:
                            return True
                        else:
                            self.tablero[ nodoInicio[0] ][nodoInicio[1]].color = 0
                            nodoInicio[0]-=1
                    
                return False 

    #Retorna si el tablero ya cuenta con solucion o no
    def ganamos(self):
        ganador = True
        for i in range(1,numCeldas+1):
            for j in range(1,numCeldas+1):
                if self.tablero[i][j].color == 0:
                    ganador = False
        return ganador
                
    #Funciones para el juego libre del jugador
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
            pygame.display.update()

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
                    return False
        if ganador == True:
            global ganoJuego
            ganoJuego = True
            return True
            

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
   
    
#Inicio 
pygame.init() 

#Variables 
tabMin= 4
tabMax =8
tamJuego = 600
tamCuadricula = 350
numCeldas = 4
grosorCuadricula = 2
offsetX = 120
offsetY = 120
tamCuadrito = (tamCuadricula- ((numCeldas+1)*grosorCuadricula))/numCeldas
colorCuadricula = (141, 117, 117)
colorFondo = (0, 0, 0 )

#Colores 
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
colores = [negro, quintana, rojo, verde, azul, amarillo,naranja, magenta,celeste,morado,vinotinto]

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
            aux = main_game.verificar()
            if aux:
                font = pygame.font.Font("NotoSans-Bold.ttf", 23)
                textsurface = font.render('Ganaste :)', False, (230,192,233))
                screen.blit(textsurface,(240, 505))
                pygame.display.update()
                

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
                    font = pygame.font.Font("NotoSans-Bold.ttf", 23)
                    textsurface = font.render('Ganaste, pero con trampa ;(', False, (230,192,233))
                    screen.blit(textsurface,(140, 470))
                    pygame.display.update()
                    ganoJuego = True
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
    if ganoJuego == False:
        main_game.draw_elements()
        pygame.display.update()
    clock.tick(60) #no correra mas rapido que 60 por segundo