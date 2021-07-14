# Project 1: Virtual paint -> Detecta con una webcam el color del rotulador y dibuja una línea que sigue su trayectoria -> -> Necesita el archivo ColorPicker.py
import cv2
import numpy as np
frameWidth = 1280
frameHeight = 720
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)   # Para utilizar una webcam, poner 0 (para la webcam por defecto) -> Puede cambiar el número si hay más de una cámara -> El CAP_DSHOW hace que funcione con la cámara externa
cap.set(3, frameWidth)   # Anchura con id = 3
cap.set(4, frameHeight)   # Longitud con id = 4
cap.set(10, 150)  # Brillo con id = 10


myColors = [[93, 195, 0, 127, 255, 255], [0, 0, 15, 122, 223, 255]]  # Lista de colores a detectar (punta de los rotuladores) -> Un elemento en este caso -> Tienen los mínimos y los máximos de HSV (hmin, smin, vmin, hmax, smax, vmax)-> Sacados de ColorPicker
    # [[Azul], [Verde manzana]] -> NOTA: Los valores pueden cambiar según la luz de la habitación -> Ajustar
myColorValues = [[255, 0, 0], [51, 255, 153]]    # Valores BGR de los colores de arriba -> Se usarán para dibujar la línea
myPoints = []   # [x, y, colorId] -> Puntos que forman la línea -> Se mostrarán por pantalla a medida que se vayan obteniendo


def findColor(img, myColors, myColorValues): # Función para detectar el color -> Capítulo 7 -> Debe tener los valores de referencia obtenidos con colorPicker
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convertir imagen de BGR a HSV (Matiz, saturación, valor - HSV, saturation, value)
    count = 0   # Por cada cuenta, un color distinto
    newPoints = []
    for color in myColors:  # Para detectar todos los colores
        lower = np.array(color[0:3])   # Array con los mínimos valores -> h_min, s_min y v_min son los tres primeros elementos de cada ítem de la lista myColors
        upper = np.array(color[3:6])   # Array con los máximos valores -> h_max, s_max y v_max son los tres últimos elementos de cada ítem de la lista myColors
        mask = cv2.inRange(imgHSV, lower, upper)    # Muestra los píxeles cuyos valores están entre el mínimo y el máximo
        x, y = getContours(mask)   # Dibuja un contorno en la zona generada
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)  # Dibuja un punto en la punta del rectángulo
        if x != 0 and y != 0:
            newPoints.append([x, y, count]) # Añade el punto (coordenadas y el color que es)
        count += 1  # Así se puede dibujar el punto del color del rectángulo
        # cv2.imshow(str(color[0]), mask)   # Para ver si ha detectado la zona -> Solo de prueba
    return newPoints


# Generar un contorno que rodee a la zona de cada color detectado -> Versión simplificada de la función del capítulo 8
def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3) # No hace falta dibujarlo realmente
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y # Devuelve las coordenadas del centro del boundingBox != centro del polígono


# Dibuja los puntos obtenidos para formar la línea
def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 20, myColorValues[point[2]], cv2.FILLED)


# Código para leer de la cámara -> Capítulo 1
while True:    # Bucle para procesar cada fotograma
    successWC, img = cap.read()   # El fotograma se guarda en img. Si se hace con éxito, success = True
    imgResult = img.copy()  # Imagen que se va a manipular
    newPoints = findColor(img, myColors, myColorValues)  # Llamada a la función que encuentra el color
    if len(newPoints) != 0:
        for newP in newPoints:  # Para llamar a drawOnCanvas, se debe hacer punto a punto
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)   # Dibuja los puntos obtenidos previamente

    cv2.imshow("VirtualPaint", imgResult) # Muestra el frame procesado
    if cv2.waitKey(1) & 0xFF == ord('e'):
        myPoints = []   # Para borrar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
