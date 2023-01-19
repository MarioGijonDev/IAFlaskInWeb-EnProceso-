#Imports
import modules.HandTrackingModule as htm
import cv2
import time
import numpy as np
import math
import alsaaudio

#Variables de alsaaudio
m = alsaaudio.Mixer()

#Crear instancia de la clase HandDetector
detector = htm.HandDetector()

def main(cap):
    cTime = 0
    pTime = 0
    while True:
        #Obtiene los frames y el succes
        succes, img = cap.read()
        if not succes:
            break
        else:

            #Detectar manos
            img = detector.findHands(img)

            #Obtener datos de los dedos
            lmList = detector.findPosition(img)

            #Obtener datos de la lista
            if len(lmList) != 0:
                #Mostrar datos de los puntos definidos por consola
                #print(lmList[4], lmList[8])

                #Sacar ejex de cada punto
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]

                #Obtener punto medio entre ambos
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                #Configurar puntos definidos
                cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

                #Distancia entre los dos puntos
                lenght = math.hypot(x2 - x1, y2 - y1)

                #Mostrar el punto de intermedio entre los dos puntos
                if lenght < 30:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

                #Hand range 30 - 180
                #Volume range 0 - 100
                
                #Proporción de volumen
                vol = int(np.interp(int(lenght), [30, 170], [0, 100]))
                #Proporción de barra de volumen
                volBar = int(np.interp(int(lenght), [30, 170], [400, 150]))
                #Proporción porcentaje de volumen
                volPer = int(np.interp(int(lenght), [30, 170], [0, 100]))

                #Modificamos el volumen del dispositivo
                if vol == 0:
                    m.setmute(1)
                else:
                    m.setmute(0)
                    m.setvolume(int(vol))
                
                #Añadimos dibujos para ver el volumen del dispositivo
                cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 1)
                cv2.rectangle(img, (50, volBar), (85, 400), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, f'{volPer} %', (40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)


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