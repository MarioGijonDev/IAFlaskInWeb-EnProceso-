#Imports
import modules.HandTrackingModule as htm
import cv2
import numpy as np
import time
import os

#Obtenemos la instancia de la clase Hand Tracking Module
detector = htm.HandDetector(detectionCon=0.85)

#Directorio donde se encuentran las imagenes de las pinturas
folderPath = "img/PainterImages"

#Lista con todos los elementos de la carpeta ordenados
myList = sorted(os.listdir(folderPath))

#Lista que contendrá las imagenes
overlayList = []

#Recorre la lista de los elementos de una carpeta
for imPath in myList:
    #Obtiene las imagenes de la carpeta
    image = cv2.imread(f'{folderPath}/{imPath}')
    #Añade las imagenes a una lista
    overlayList.append(image)

#Esta es la imagen superpuesta donde dibujaremos
imgCanvas = np.zeros((720, 1280), np.uint8)

def main(cap):

    #Cabecera inicial será la de borrar
    header = overlayList[5]

    #Color del dibujo
    drawColor = (255, 0, 255)

    #Valores de los ejes previos (Vistos al final del codigo)
    #Almacenarán el valor previo de x e y
    xp, yp = 0, 0
    
    cTime = 0
    pTime = 0
    while True:
        #Obtiene las imagenes de la camara
        success, img = cap.read()

        #Comprobar fallo
        if not success:
            break

        else:

            #Volteamos la imagen para simular el modo espejo
            img = cv2.flip(img, 1)
            
            #Ajustamos el header al video
            img[0:55, 0:1280] = header

            #Detectar manos
            img = detector.findHands(img)

            #Obtener datos de los dedos
            lmList = detector.findPosition(img)

            if len(lmList) != 0 :
                #Localización ejes x, y para el punto 8 (índice)
                x1, y1 = lmList[8][1:]
                #Localización ejes x, y para el punto 12 (corazón)
                x2, y2 = lmList[12][1:]

                #Recibir valores 
                fingers = detector.fingersUp(mirror = True)

                #Si está el dedo índice y corazón arriba, está en selection mode
                if fingers[1] and fingers[2]:
                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
                    #print("Selection Mode")

                    #Comprobar donde está seleccionando de la cabecera
                    
                    if y1 < 55:
                        if 95 < x1 < 175:
                            header = overlayList[0]
                            drawColor = (255, 0, 0)
                        elif 260 < x1 < 360:
                            header = overlayList[1]
                            drawColor = (0, 128, 0)
                        if 430 < x1 < 510:
                            header = overlayList[2]
                            drawColor = (0, 0, 255)
                        elif 610 < x1 < 710:
                            header = overlayList[3]
                            drawColor = (0, 0, 0)
                        if 810 < x1 < 910:
                            header = overlayList[4]
                            drawColor = (255, 255, 255)
                        elif 1070 < x1 < 1115:
                            header = overlayList[5]
                            drawColor = (255, 0, 0)
                    

                #Si solo el dedo índice está arriba, está en drawing mode
                if fingers[1] and fingers[2] == False:
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

                    #Si los dos valores previos son 0, significa que son los valores iniciales y los igualamos
                    #a los valores actuales
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    #Dibujar la linea
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, 15)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 15)

                    xp, yp = x1, y1

                    #print("Drawing mode")
           
            #Calcular FPS
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            #Mostrar FPS
            cv2.putText(img, f'FPS: {str(int(fps))}', (15,38), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 1)
            
            #Codificar en bytes
            suc, encode = cv2.imencode('.jpg', img)
            img = encode.tobytes()

            #Retornar los valores para la web
            yield(b'--img\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            #yield(b'--img\r\n'b'Content-Type: image/jpeg\r\n\r\n' + imgCanvas + b'\r\n')