#Imports
import modules.HandTrackingModule as htm
import cv2
import time
import os

#Ruta de la carpeta de imagenes
folderPath = "img/FingerImages"

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

#Obtenemos la instancia de la clase Hand Tracking Module
detector = htm.HandDetector()

#Puntos de los dedos de la mano
tipIds = [4, 8, 12, 16, 20]

#Almacenará el numero de dedos levantados
totalFingers = 0

def main(cap):
    cTime = 0
    pTime = 0
    totalFingers = 0
    while True:
        #Obtiene las imagenes de la camara
        success, img = cap.read()

        #Comprobar fallo
        if not success:
            break

        else:
            #Detecta las manos de las imagenes
            img = detector.findHands(img)

            #Describe la posición de cada punto neuronal
            lmList = detector.findPosition(img, draw=False)

            #Comprobamos que haya detectado los puntos de la mano
            if len(lmList) != 0:
                #Matriz que describe que numeros están arriba(1) y cuales abajo (0)
                fingers = detector.fingersUp()

                #Numeros de 1 que se encuentran en la lista
                totalFingers = fingers.count(1)
                print(totalFingers)
                
                #Obtiene el ancho y alto de las imagenes del overlayList
                #-1 para que cuando valga cero, se vaya al final de la lista
                h, w, c = overlayList[totalFingers-1].shape

                #Superponemos en la imagen del cv, nuestra imagen del overlayList
                #Los corchetes nos indican la posición que va a tomar en la imagen
                img[0:h, 0:w] = overlayList[totalFingers-1]

                #Dibuja un rectangulo con los números
                cv2.rectangle(img, (25, 330), (190, 520), (50, 0, 0), cv2.FILLED)
                cv2.putText(img, str(totalFingers), (60, 475), cv2.FONT_HERSHEY_PLAIN, 10, (255, 255, 255), 15)
           
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