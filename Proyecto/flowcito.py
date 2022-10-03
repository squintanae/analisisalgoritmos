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

    def printCol(self):
        for i in range(numCeldas):
            for j in range(numCeldas):
                print(self.tablero[i][j].color)
            print("")
        print("acabe print color")
        for i in range(numCeldas):
            for j in range(numCeldas):
                print(self.tablero[i][j].punto)
            print("")
        print("acabe print punto")
        for i in range(numCeldas):
            for j in range(numCeldas):
                print(self.tablero[i][j].puntoColor)
            print("")
        print("acabe print puntoColor")

    def borrar(self):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color==0:
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
                        print("corte aqui")
                        self.cortar(self.tablero[ posY ][posX].color, self.tablero[ posY ][posX].longitud)

                    if self.tablero[ posY ][posX].color == self.colorActual and self.tablero[ posY ][posX].longitud< long+1:
                        print("corte en el otro aqui")
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
                    print("entreee aquiiii ")
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

       

    def dibujarCeldas(self):
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[j][i].punto== True:
                    if self.tablero[j][i].color!=0:  
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

    def verificarGandaor(self):

        ganador=True
        for i in range(numCeldas):
            for j in range(numCeldas):
                if self.tablero[i][j].color == 0:
                    ganador = False
        if ganador == True:
            print("GANOOOOO")

class MAIN:
    def __init__(self):
        self.tab = TABLERO()
    def draw_elements(self):
        self.tab.dibujarCuadricula()
        self.tab.dibujarCeldas()
    def seleccionarPunto(self, pos):
        self.tab.puntoSeleccionado(pos)
    def verificar(self):
        self.tab.verificarGandaor()
    

pygame.init() 
tamJuego = 600
tamCuadricula = 350
numCeldas = 6
grosorCuadricula = 2
offsetX = 120
offsetY = 120
tamCuadrito = (tamCuadricula- ((numCeldas+1)*grosorCuadricula))/numCeldas

colorCuadricula = (141, 117, 117)
colorFondo = (61, 38, 38 )
rojo = (234, 63, 63)
amarillo = (246, 242,7)
azul = (30, 60, 246)
verde = (30, 246, 57)
lila = (255, 10, 201)
naranja = (250, 137, 0)

negro =(38, 33, 40 )

colores = [negro, rojo, amarillo, azul, verde,lila, naranja]



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