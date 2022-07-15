#game of life
import pygame
from pygame.locals import *
import numpy as np
import time

#Inicializamos las clases que usaremos
class Cell:
    state = 0   #El estado de la celula
    verts = 0   #los vértices de cada celula que se muestran
    #funcion que se ejecuta al instanciar una clase, toma como parámetro los vértices y el estado de la célula
    def __init__(self, verts, state):
        self.state = state
        self.verts = verts
    #funcion para dibujar las celulas, toma como parametro la superficie en donde se dibujará la célula
    def draw(self, surface):
        pygame.draw.polygon(surface, (255, 255, 255) if self.state else (0, 0, 0) , self.verts, 0 if self.state else 1)

#Clases heredadas de Cell
class BadCell(Cell):
    def __init__(self, verts, state):
        super().__init__(verts, state)
    def draw(self, surface):
        pygame.draw.polygon(surface, (255, 0, 0) if self.state != 0 else (0, 0, 0) , self.verts, 0 if self.state != 0 else 1)

class AnotherCell(Cell):
    def __init__(self, verts, state):
        super().__init__(verts, state)
    def draw(self, surface):
        pygame.draw.polygon(surface, (0, 255, 0) if self.state != 0 else (0, 0, 0) , self.verts, 0 if self.state != 0 else 1)

def main():
    #Definimos las variables que usaremos
    width , height = 700 , 700  #ancho y alto de la pantalla
    celX, celY = 200, 200   #cantidad de celulas en X e Y
    tmX, tmY = width/celX, height/celY  #tamaño de cada celula en X e Y
    delay = .1 #tiempo de espera entre cada iteración
    states = np.zeros((celX,celY))  #matriz de estados de las celulas
    temp = int(input("Ingrese el número de células malignas : "))   #cantidad de células malignas al iniciar
    numberBadCell = temp
    numberBadCellCount = 0

    #Doble for para generar las celulas
    for y in range(celX):
        for x in range(celY):
            temp = np.random.randint(0,100)
            if  temp > 60:
                states[x,y] = 1

    #Posición del tejido
    tempX = np.random.randint(0,celX)
    tempY = np.random.randint(0,celY)
    tamCelulaFinal = 5
    #Doble for para generar el tejido final
    for i in range(0,tamCelulaFinal):
        for j in range(0,tamCelulaFinal):
            states[(tempX+i)%celX,(tempY+j)%celY] = 3;

    #While para generar las celulas malignas
    while numberBadCell > numberBadCellCount:
        states[np.random.randint(0,celX-1),np.random.randint(0,celY-1)] = 2
        numberBadCellCount += 1
    
    #Variables para verificar la cantidad de celulas malignas
    badCellsCreated = 0
    tempBadCellsCreated = 0
    iterationTemp = 0;

    pygame.init()   #Inicializamos pygame
    pygame.display.set_caption("Simulador de propagación - {} colonias".format(numberBadCell))  #Título de la ventana
    screen = pygame.display.set_mode((width, height))   #Definimos el tamaño de la ventana
    tiempo = time.time()    #Variable para controlar el tiempo
    final = False   #Booleano para controlar el final del juego

    #Bucle del juego
    while True:
        badCellsCreated = 0 #En cada iteración se reinicia el contador de celulas malignas
        #Doble for para contar las celulas malignas
        for i in range(celX):
            for j in range(celY):
                if states[i,j] == 2:
                    badCellsCreated += 1
        tempBadCellsCreated = badCellsCreated   #Almacenamos la cantidad de celulas malignas en una variable temporal
        #For para obtener los eventos de la ventana, en este casi el evento de salir
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        #Si final es verdadero, entonces acabó el juego y se ejecuta esto, que sirve para seguir dibujando las células
        if final:
            screen.fill((125, 125, 125))
            for y in range(celX):
                    for x in range(celY):
                        verts = [(x*tmX, y*tmY), ((x+1)*tmX, y*tmY), ((x+1)*tmX, (y+1)*tmY), (x*tmX, (y+1)*tmY)]
                        if states[x,y] == 0 or states[x,y] == 1:
                            celula = Cell(verts, states[x,y])
                        elif states[x,y] == 2:
                            celula = BadCell(verts, states[x,y])
                        else:
                            celula = AnotherCell(verts, states[x,y])
                        celula.draw(screen)            
        else: #De lo contrario
            #Si el tiempo actual es menor al tiempo mas el delay, entonces se dibuja la última generación de células
            if time.time() < tiempo + 0.01:
                screen.fill((125, 125, 125))
                for y in range(celX):
                    for x in range(celY):
                        verts = [(x*tmX, y*tmY), ((x+1)*tmX, y*tmY), ((x+1)*tmX, (y+1)*tmY), (x*tmX, (y+1)*tmY)]
                        if states[x,y] == 0 or states[x,y] == 1:
                            celula = Cell(verts, states[x,y])
                        elif states[x,y] == 2:
                            celula = BadCell(verts, states[x,y])
                        else:
                            celula = AnotherCell(verts, states[x,y])
                        celula.draw(screen)
            else:#De lo contrario se ejecuta la lógica
                newStates = np.copy(states) #Copiamos la matriz de estados
                screen.fill((125, 125, 125))    #Limpiamos la pantalla
                #Iteración para recoger la matriz de células
                for y in range(celX):
                    for x in range(celY):
                        #Coordenadas de las células alrededor de la actual
                        coordsX =[(x-1)%celX ,x%celX,(x+1)%celX, (x-1)%celX,(x+1)%celX,(x-1)%celX, x%celX,(x+1)%celX]
                        coordsY =[(y-1)%celY, (y-1)%celY, (y-1)%celY,y%celY, y%celY, (y+1)%celY, (y+1)%celY, (y+1)%celY]
                        vecinosBuenos = 0
                        vecinosMalos = 0
                        #Iteración para recoger las células alrededor de la actual y determinar si son buenas o malas
                        for i in range(0,8):
                            vecinosBuenos = vecinosBuenos + (1 if states[coordsX[i],coordsY[i]] == 1 else 0)
                            vecinosMalos = vecinosMalos +(1 if states[coordsX[i],coordsY[i]] == 2 else 0)
                        #Si la célula actual está vacía
                        if states[x, y] == 0:
                            #Si tiene 2 vecinos buenos, entonces se crea una célula buena
                            if vecinosBuenos == 2:
                                newStates[x, y] = 1
                            elif vecinosBuenos < 5 and vecinosMalos > 0:    #De lo contrario si tiene menos de 5 vecinos buenos y al menos 1 vecino malo, entonces se crea una célula maligna
                                newStates[x, y] = 2
                        #Si la célula es buena
                        if states[x, y] == 1:
                            if vecinosMalos == 0: #Si no tiene vecinos malos, entonces se mantiene buena y sigue las reglas del juego de la vida
                                if vecinosBuenos < 2 or vecinosBuenos > 3:
                                    newStates[x, y] = 0
                            elif vecinosMalos > 6:  #Si tiene más de 6 vecinos malos, entonces se vuelve una célula maligna
                                newStates[x, y] = 2
                        #Si la célula es maligna
                        if states[x, y] == 2:
                            #Si tiene más de 4 vecinos buenos
                            if vecinosBuenos > 4:
                                #Cada celula vacia que tenga alrededor se vuelve una celula buena
                                for i in range(0,8):
                                    if states[coordsX[i],coordsY[i]] == 0:
                                        newStates[coordsX[i],coordsY[i]] = 1
                        #Si es el tejido final
                        if states[x, y] == 3:
                            #Si tiene al menos un vecino malo, acaba el juego por propagación
                            if vecinosMalos > 0:
                                pygame.display.set_caption("Fin de la simulación - El cáncer se propagó a más órganos")
                                final = True
                        #Vertices de cada celula
                        verts = [(x*tmX, y*tmY), ((x+1)*tmX, y*tmY), ((x+1)*tmX, (y+1)*tmY), (x*tmX, (y+1)*tmY)]
                        #Verificamos que tipo de celula es y la dibujamos
                        if states[x,y] == 0 or states[x,y] == 1:
                            celula = Cell(verts, states[x,y])
                        elif states[x,y] == 2:
                            celula = BadCell(verts, states[x,y])
                        else:
                            celula = AnotherCell(verts, states[x,y])
                        celula.draw(screen)

                states = np.copy(newStates) #Copiamos la matriz de estados
                badCellsCreated = 0 #Contador de células malas creadas
                for i in range(celX):
                    for j in range(celY):
                        if states[i,j] == 2:
                            badCellsCreated += 1
                if badCellsCreated == tempBadCellsCreated: #Si no se crearon nuevas células malas en 3 turnos, entonces termina el juego por no expansión
                            iterationTemp += 1
                            if iterationTemp > 3:
                                pygame.display.set_caption("Fin de la simulación - El cáncer no se expande")
                                final = True
                else:
                    #De lo contrario se reinicia el contador de turnos
                    iterationTemp = 0
                tiempo = time.time() + delay    #Se actualiza el tiempo de la siguiente iteración
        pygame.display.flip()   #Terminamos de dibujar el fotograma actual
            
#Función para ejecutar el juego
if __name__ == "__main__":
    main()

