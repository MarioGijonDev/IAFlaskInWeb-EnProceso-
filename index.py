
from flask import Flask, render_template, Response
import cv2
import pyScripts.VolumeHandControl as vhc
import pyScripts.FingerCounting as fc
import pyScripts.VirtualPainter as vp

wCam, hCam = 1280, 720

#Crear variable de video captura
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#############################################################################################

#Crea app Flask
app = Flask(__name__)

#############################################################################################

#RUTA INICIAL
@app.route("/")
def index():
    return render_template('index.html')

#############################################################################################

#RUTA PARA VOLUME HAND CONTROL
@app.route("/volume_hand_control.html")
def volumeHandControl():
    return render_template('/volume_hand_control.html')

#############################################################################################

#RUTA PARA EL VIDEO DE VOLUME HAND CONTROL
@app.route("/volume_hand_control.html/volumehandcontrol")
def video_VolumeHandControl():
    return Response(vhc.main(cap), mimetype='multipart/x-mixed-replace; boundary=img')

#############################################################################################

#RUTA PARA VOLUME FINGER COUNTING
@app.route("/finger_counting.html")
def fingerCounting():
    return render_template('/finger_counting.html')

#############################################################################################

#RUTA PARA EL VIDEO DE FINGER COUNTING
@app.route("/finger_counting.html/fingercounting")
def video_FingerCounting():
    return Response(fc.main(cap), mimetype='multipart/x-mixed-replace; boundary=img')

#############################################################################################

#RUTA PARA VIRTUAL PAINTER
@app.route("/virtual_painter.html")
def virtualPainter():
    return render_template('/virtual_painter.html')

#############################################################################################

#RUTA PARA EL VIDEO DE VIRTUAL PAINTER
@app.route("/virtual_painter.html/virtualpainter")
def video_VirtualPainter():
    return Response(vp.main(cap), mimetype='multipart/x-mixed-replace; boundary=img')

#Main
if(__name__ == "__main__"):
    app.run()