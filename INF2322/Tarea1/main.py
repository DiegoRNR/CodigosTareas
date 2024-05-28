# INTEGRANTE: DIEGO NEGRIN

import pygame
import time
import threading
import random

# INICIALIZACION DE PYGAME
pygame.init()

# INICIALIZACION DE SEMAFOROS
trenesCiudadA = threading.Semaphore(5)
trenesCiudadB = threading.Semaphore(5)
mutexSalidaCiudadA = threading.Semaphore(1)
mutexSalidaCiudadB = threading.Semaphore(1)
trenesEsperando = threading.Semaphore(0)
maxTrenesPuente = threading.Semaphore(2)
trenEntroPuente = threading.Semaphore(0)
trenSalioPuente = threading.Semaphore(0)
puenteLibre = threading.Semaphore(1)
mutexPuente = threading.Lock()

# INICIALIZACION DE VARIABLE GLOBAL DEL SENTIDO
# 0: LIBRE      1: DERECHA      2: IZQUIERDA
sentido = 0

# DECLARACION DE COLORES
colorNegro = (0, 0, 0)
colorBlanco = (255, 255, 255)
colorRojo = (255, 0, 0)
colorVerde = (0, 255, 0)
colorMostaza = (255, 219, 88)
colorAnaranjado = (234, 170, 0)
colorAzul = (0, 0, 255)
colorCeleste = (0, 255, 255)
colorAmarillo = (255, 255, 0)
colorMorado = (153, 0, 204)
colorMagenta = (255, 0, 255)
colorGris = (128, 128, 128)
colorRosado = (255, 153, 204)
colorCafe = (153, 102, 51)
colorTurquesa = (64, 184, 168)
colorBurdeos = (153, 0, 0)

# DECLARACION DE POSICIONES
casillasCiudadA = [
    [(95 + 10, 320 + 50), threading.Semaphore(1)],
    [(95 + 45, 320 + 50), threading.Semaphore(1)],
    [(95 + 80, 320 + 50), threading.Semaphore(1)],
    [(95 + 115, 320 + 50), threading.Semaphore(1)],
    [(95 + 150, 320 + 50), threading.Semaphore(1)],
    [(95 + 10, 480 - 70), threading.Semaphore(0)],
    [(95 + 45, 480 - 70), threading.Semaphore(0)],
    [(95 + 80, 480 - 70), threading.Semaphore(0)],
    [(95 + 115, 480 - 70), threading.Semaphore(0)],
    [(95 + 150, 480 - 70), threading.Semaphore(0)]
]
casillasCiudadB = [
    [(695 + 10, 320 + 50), threading.Semaphore(0)],
    [(695 + 45, 320 + 50), threading.Semaphore(0)],
    [(695 + 80, 320 + 50), threading.Semaphore(0)],
    [(695 + 115, 320 + 50), threading.Semaphore(0)],
    [(695 + 150, 320 + 50), threading.Semaphore(0)],
    [(695 + 10, 480 - 70), threading.Semaphore(1)],
    [(695 + 45, 480 - 70), threading.Semaphore(1)],
    [(695 + 80, 480 - 70), threading.Semaphore(1)],
    [(695 + 115, 480 - 70), threading.Semaphore(1)],
    [(695 + 150, 480 - 70), threading.Semaphore(1)],
]

casillasCaminoSuperiorA = [
    [(280 + 130, 348), threading.Semaphore(1)],
    [(280 + 99, 328), threading.Semaphore(1)],
    [(280 + 66, 328), threading.Semaphore(1)],
    [(280 + 33, 328), threading.Semaphore(1)],
    [(280, 328), threading.Semaphore(1)]
]
casillasCaminoInferiorA = [
    [(280, 448), threading.Semaphore(1)],
    [(280 + 33, 448), threading.Semaphore(1)],
    [(280 + 66, 448), threading.Semaphore(1)],
    [(280 + 99, 448), threading.Semaphore(1)],
    [(280 + 130, 428), threading.Semaphore(1)]
]
casillasCaminoSuperiorB = [
    [(670, 328), threading.Semaphore(1)],
    [(670 - 33, 328), threading.Semaphore(1)],
    [(670 - 66, 328), threading.Semaphore(1)],
    [(670 - 99, 328), threading.Semaphore(1)],
    [(670 - 129, 348), threading.Semaphore(1)]
]
casillasCaminoInferiorB = [
    [(670 - 129, 428), threading.Semaphore(1)],
    [(670 - 99, 448), threading.Semaphore(1)],
    [(670 - 66, 448), threading.Semaphore(1)],
    [(670 - 33, 448), threading.Semaphore(1)],
    [(670, 448), threading.Semaphore(1)]
]

casillasPuente = [
    [(410, 387), threading.Semaphore(1)],
    [(410 + 33, 387), threading.Semaphore(1)],
    [(410 + 66, 387), threading.Semaphore(1)],
    [(410 + 99, 387), threading.Semaphore(1)],
    [(541, 387), threading.Semaphore(1)]
]

# DIMENSIONES DE LOS TRENES
dimensionTren = (25, 25)

# POSICIONES DE TRENES EN CIUDADEDS
trenesA = [
    [colorMorado, casillasCiudadA[9]],
    [colorAmarillo, casillasCiudadA[8]],
    [colorAzul, casillasCiudadA[7]],
    [colorRosado, casillasCiudadA[6]],
    [colorGris, casillasCiudadA[5]],
]
trenesB = [
    [colorCeleste, casillasCiudadB[0]],
    [colorMagenta, casillasCiudadB[1]],
    [colorTurquesa, casillasCiudadB[2]],
    [colorBurdeos, casillasCiudadB[3]],
    [colorCafe, casillasCiudadB[4]],
]

# LISTAS DE ESPERA DEL PUENTE
trenesAEsperando = []
trenesBEsperando = []

# INICIALIZACION DE VENTANA DEL PROGRAMA
ventana = pygame.display.set_mode((1000, 800))
ventana.fill(colorNegro)

# GRAFICOS DE ELEMENTOS DEL PROGRAMA
# CIUDADES
pygame.draw.rect(ventana, colorBlanco, ((95, 320), (185, 160)), 1)
pygame.draw.rect(ventana, colorBlanco, ((695, 320), (185, 160)), 1)

# TRENES
trenes = trenesA + trenesB
for train in trenes:
    pygame.draw.rect(ventana, train[0], (train[1][0], dimensionTren))

# CAMINOS CIUDAD A
pygame.draw.line(ventana, colorBlanco, (280, 320), (440, 320), 1)
pygame.draw.line(ventana, colorBlanco, (280, 360), (400, 360), 1)

pygame.draw.line(ventana, colorBlanco, (280, 440), (400, 440), 1)
pygame.draw.line(ventana, colorBlanco, (280, 480), (440, 480), 1)

# CAMINOS CIUDAD B
pygame.draw.line(ventana, colorBlanco, (695, 320), (535, 320), 1)
pygame.draw.line(ventana, colorBlanco, (695, 360), (575, 360), 1)

pygame.draw.line(ventana, colorBlanco, (695, 440), (575, 440), 1)
pygame.draw.line(ventana, colorBlanco, (695, 480), (535, 480), 1)

# CONEXIONES CAMINOS A PUENTE
pygame.draw.line(ventana, colorBlanco, (400, 360), (400, 440), 1)
pygame.draw.line(ventana, colorBlanco, (440, 320), (440, 480), 1)

pygame.draw.line(ventana, colorBlanco, (575, 360), (575, 440), 1)
pygame.draw.line(ventana, colorBlanco, (535, 320), (535, 480), 1)

# PUENTE
pygame.draw.rect(ventana, colorAnaranjado, ((400, 380), (176, 40)))

# SEMAFOROS
pygame.draw.circle(ventana, colorVerde, (370, 400), 20)
pygame.draw.circle(ventana, colorVerde, (605, 400), 20)

# MOSTRAR GRAFICOS EN LA VENTANA
pygame.display.update()


def entrarCiudad(tren, casillasCiudad):
    # MUEVE EL TREN A UNA CASILLA LIBRE DE LA CIUDAD DESTINO
    i = 0
    while not casillasCiudad[i][1].acquire(False):
        i += 1
    tren[1][1].release()
    pygame.draw.rect(ventana, colorNegro, (tren[1][0], dimensionTren))
    tren[1] = casillasCiudad[i]
    pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
    pygame.display.update()


def moverTrenAPuente(tren, casillasCamino):
    # MUEVE EL TREN DESDE UNA CIUDAD HASTA LA ENTRADA DEL PUENTE A TRAVES DEL CAMINO INDICADO
    for casilla in casillasCamino:
        casilla[1].acquire()
        tren[1][1].release()
        pygame.draw.rect(ventana, colorNegro, (tren[1][0], dimensionTren))
        tren[1] = casilla
        pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
        pygame.display.update()
        time.sleep(1)


def pasarPuenteDesdeA(tren):
    # MUEVE EL TREN A TRAVES DEL PUENTE CON SENTIDO HACIA LA DERECHA
    casillasPuente[0][1].acquire()
    tren[1][1].release()
    pygame.draw.rect(ventana, colorNegro, (tren[1][0], dimensionTren))
    tren[1] = casillasPuente[0]
    pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
    pygame.display.update()
    time.sleep(1)
    for i in range(1, 5):
        casillasPuente[i][1].acquire()
        tren[1][1].release()
        pygame.draw.rect(ventana, colorAnaranjado, (tren[1][0], dimensionTren))
        tren[1] = casillasPuente[i]
        pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
        pygame.display.update()
        time.sleep(1)


def pasarPuenteDesdeB(tren):
    # MUEVE EL TREN A TRAVES DEL PUENTE CON SENTIDO HACIA LA IZQUIERDA
    casillasPuente[4][1].acquire()
    tren[1][1].release()
    pygame.draw.rect(ventana, colorNegro, (tren[1][0], dimensionTren))
    tren[1] = casillasPuente[4]
    pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
    pygame.display.update()
    time.sleep(1)
    for i in range(3, -1, -1):
        casillasPuente[i][1].acquire()
        tren[1][1].release()
        pygame.draw.rect(ventana, colorAnaranjado, (tren[1][0], dimensionTren))
        tren[1] = casillasPuente[i]
        pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
        pygame.display.update()
        time.sleep(1)


def moverTrenACiudad(tren, casillasCamino):
    # MUEVE EL TREN A TRAVES DEL CAMINO HACIA CIUDAD B
    for i in range(1, len(casillasCamino)):
        casillasCamino[i][1].acquire()
        tren[1][1].release()
        pygame.draw.rect(ventana, colorNegro, (tren[1][0], dimensionTren))
        tren[1] = casillasCamino[i]
        pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
        pygame.display.update()
        time.sleep(1)


def salirPuenteDesdeA(tren):
    # MUEVE EL TREN DEL PUENTE AL CAMINO HACIA CIUDAD B
    casillasCaminoInferiorB[0][1].acquire()
    tren[1][1].release()
    pygame.draw.rect(ventana, colorAnaranjado, (tren[1][0], dimensionTren))
    tren[1] = casillasCaminoInferiorB[0]
    pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
    pygame.display.update()
    time.sleep(1)


def salirPuenteDesdeB(tren):
    # MUEVE EL TREN DEL PUENTE AL CAMINO HACIA CIUDAD A
    casillasCaminoSuperiorA[0][1].acquire()
    tren[1][1].release()
    pygame.draw.rect(ventana, colorAnaranjado, (tren[1][0], dimensionTren))
    tren[1] = casillasCaminoSuperiorA[0]
    pygame.draw.rect(ventana, tren[0], (tren[1][0], dimensionTren))
    pygame.display.update()
    time.sleep(1)


def verdeParaA():
    # DIBUJA SEMAFORO VERDE PARA SENTIDO DERECHA Y SEMAFORO ROJO PARA SENTIDO IZQUIERDA
    pygame.draw.circle(ventana, colorVerde, (370, 400), 20)
    pygame.draw.circle(ventana, colorRojo, (605, 400), 20)
    pygame.display.update()


def verdeParaB():
    # DIBUJA SEMAFORO VERDE PARA SENTIDO IZQUIERDA Y SEMAFORO ROJO PARA SENTIDO DERECHA
    pygame.draw.circle(ventana, colorRojo, (370, 400), 20)
    pygame.draw.circle(ventana, colorVerde, (605, 400), 20)
    pygame.display.update()


def entradaPuente(sentidoTren, trenesOpuestosEsperando, trenesMismoEsperando):
    # CONTROLA SI EL TREN PUEDE O NO PUEDE PASAR POR EL PUENTE
    # RETORNA TRUE EN CASO DE QUE PUEDA, Y FALSE EN CASO CONTRARIO
    global sentido
    mutexPuente.acquire()
    if sentido:
        if sentido == sentidoTren:
            if len(trenesOpuestosEsperando) > 0:
                if trenesOpuestosEsperando[0][1] > 0:
                    trenesOpuestosEsperando[0][1] -= 1
                else:
                    sentido = 1 if sentidoTren == 2 else 2
        else:
            if trenesMismoEsperando[0][1] > 0:
                trenesMismoEsperando[0][1] -= 1
            else:
                sentido = 1 if sentidoTren == 2 else 2
    else:
        sentido = sentidoTren
    mutexPuente.release()
    return sentido == sentidoTren


def activarTrenCiudadA():
    # ACTIVA TREN EN CIUDAD A Y LO MUEVE A CIUDAD B
    time.sleep(random.randrange(2, 20))
    mutexSalidaCiudadA.acquire()
    tren = trenesA[0]
    trenesA.remove(tren)
    mutexSalidaCiudadA.release()
    moverTrenAPuente(tren, casillasCaminoInferiorA)
    trenesEsperando.release()
    trenesAEsperando.append([tren, 2])
    while not entradaPuente(1, trenesBEsperando, trenesAEsperando):
        puenteLibre.acquire()
    trenesAEsperando.pop(0)
    maxTrenesPuente.acquire()
    verdeParaA()
    trenEntroPuente.release()
    pasarPuenteDesdeA(tren)
    salirPuenteDesdeA(tren)
    trenSalioPuente.release()
    maxTrenesPuente.release()
    moverTrenACiudad(tren, casillasCaminoInferiorB)
    entrarCiudad(tren, casillasCiudadB)
    trenesB.append(tren)
    trenesCiudadB.release()


def activarTrenCiudadB():
    # ACTIVA TREN EN CIUDAD B Y LO MUEVE A CIUDAD A
    time.sleep(random.randrange(2, 20))
    mutexSalidaCiudadB.acquire()
    tren = trenesB[0]
    trenesB.remove(tren)
    mutexSalidaCiudadB.release()
    moverTrenAPuente(tren, casillasCaminoSuperiorB)
    trenesEsperando.release()
    trenesBEsperando.append([tren, 2])
    while not entradaPuente(2, trenesAEsperando, trenesBEsperando):
        puenteLibre.acquire()
    trenesBEsperando.pop(0)
    maxTrenesPuente.acquire()
    verdeParaB()
    trenEntroPuente.release()
    pasarPuenteDesdeB(tren)
    salirPuenteDesdeB(tren)
    trenSalioPuente.release()
    maxTrenesPuente.release()
    moverTrenACiudad(tren, casillasCaminoSuperiorA)
    entrarCiudad(tren, casillasCiudadA)
    trenesA.append(tren)
    trenesCiudadA.release()


def expedirTrenCiudadA():
    # ACTIVA HEBRAS PARA MOVER TRENES PRESENTES EN CIUDAD A
    # DEJA DE ACTIVAR HEBRAS CUANDO ACTIVA LOS TRENES ORIGINALES Y LOS TRENES DE LA OTRA CIUDAD UNA VEZ
    for i in range(10):
        trenesCiudadA.acquire()
        threading.Thread(target=activarTrenCiudadA).start()


def expedirTrenCiudadB():
    # ACTIVA HEBRAS PARA MOVER TRENES PRESENTES EN CIUDAD B
    # DEJA DE ACTIVAR HEBRAS CUANDO ACTIVA LOS TRENES ORIGINALES Y LOS TRENES DE LA OTRA CIUDAD UNA VEZ
    for i in range(10):
        trenesCiudadB.acquire()
        threading.Thread(target=activarTrenCiudadB).start()


def puente():
    # INDICA CUANDO EL PUENTE SE ENCUENTRA LIBRE
    # DIBUJA AMBOS SEMAFOROS EN VERDE CUANDO SE ENCUENTRA LIBRE
    global sentido
    while True:
        trenEntroPuente.acquire()
        trenesEnPuente = 1
        while trenesEnPuente != 0:
            if trenEntroPuente.acquire(False):
                trenesEnPuente += 1
            if trenSalioPuente.acquire(False):
                trenesEnPuente -= 1
        puenteLibre.release()
        sentido = 0
        pygame.draw.circle(ventana, colorVerde, (370, 400), 20)
        pygame.draw.circle(ventana, colorVerde, (605, 400), 20)
        pygame.display.update()


# ACTIVAR HEBRAS DE LAS CIUDADES Y EL PUENTE
threading.Thread(target=puente, daemon=True).start()
threading.Thread(target=expedirTrenCiudadA).start()
threading.Thread(target=expedirTrenCiudadB).start()
