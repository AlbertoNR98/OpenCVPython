# Chapter 8: Contours / shape detection
import cv2
import numpy as np


def stackImages(scale, imgArray):    # Para mostrar de forma más cómoda el resultado
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


# Función para detectar las aristas de los polígonos -> Se obtendrá a partir de ahí el número de esquinas y el área encerrada entre ellas -> Con esta información, se puede obtener la figura
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)    # RETR_EXTERNAL: Recupera la parte externa del contorno (vértices exteriores). CHAIN_APPROX_NONE para obtener toda la información sobre los contornos, y no valores comprimidos de los puntos
    print(str(len(contours))+ " figuras detectadas")    # El número de contornos es el número de figuras
    for cnt in contours:
        area = cv2.contourArea(cnt) # Área encerrada en el contorno
        print(area)
        if area > 500:  # Para evitar ruido
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)  # -1 para dibujar todos los contornos en otra imagen (podría ser en la misma que entra como parámetro) -> También se ha seleccionado el color y grosor
            peri = cv2.arcLength(cnt, True) # Medición de la longitud del contorno cerrado  -> Para aproximar las esquinas (número y posición)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True) # Aproximación del polígono dada la curva (contorno) -> La variación de épsilon hará que la aproximación del número de esquinas sea más cercana
            print(len(approx))   # El resultado es el número de esquinas encontradas y sus coordenadas (si no se pone len) -> Si da más de cuatro en este caso, es un círculo
            objCor = len(approx)    # Número de esquinas
            x, y, w, h = cv2.boundingRect(approx)  # Rectángulo que recubre los puntos dados -> Se obtienen las coordenadas y tamaño del rectángulo creado

            if objCor == 3:
                objectType = "Triangle"  # Si tiene 3 esquinas es un triángulo
            elif objCor == 4:   # Con 4 esquinas puede ser un cuadrado (relación de aspecto 1) o un rectángulo (relación de aspecto distinta a 1)
                aspRatio = w / float(h)
                if aspRatio > 0.98 and aspRatio < 1.03: # Como es una aproximación, el valor será cercano a 1, en lugar de valer 1
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor > 4:
                objectType = "Circle"   # En la imagen de prueba, si tiene más de 4 esquinas es un círculo
            else:
                objectType = "None" # Si está fuera de estos parámetros, figura indeterminada

        cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0, 255, 0), 2)    # Dibuja el rectángulo recubridor de cada figura
        cv2.putText(imgContour, objectType, (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 0, 0), 2) # Pone el tipo de objeto en el rectángulo recubridor aproximadamente



path = 'Resources/shapes.png'   # Este código funciona mejor en esta imagen
img = cv2.imread(path)
imgContour = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)   # Matriz de 7x7 para hacer el desenfoque (kernel)
imgCanny = cv2.Canny(imgBlur, 50, 50)   # Canny ayuda a resaltar las aristas de las figuras -> También se deberán detectar los ángulos
imgBlank = np.zeros_like(img)   # Matriz de ceros del tamaño de la imagen
getContours(imgCanny)

imgStack = stackImages(0.8, ([img, imgGray, imgBlur], [imgCanny, imgContour, imgBlank]))    # Se puede observar que el contorno está pintado en azul
cv2.imshow("Salida", imgStack)
cv2.waitKey(0)