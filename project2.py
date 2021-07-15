# Project 2: Document scanner
import cv2
import numpy as np

# Parámetros de la imagen
widthImg = 640
heightImg = 480

# Parámetros de la webcam -> El tamaño viene dado por la imagen, así que no hace falta configurarlo aquí
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap.set(10, 150)    # Brillo


# Preprocesamiento de la imagen
def preProcessing(img):
    kernel = np.ones((5,5)) # Matriz de unos con tamño 5x5
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # A gris
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # Desenfoca
    imgCanny = cv2.Canny(imgBlur, 200, 200) # Resalta los bordes
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)    # Dilata los bordes
    imgThres = cv2.erode(imgDial, kernel, iterations=1) # Estrecha los bordes -> El resultado está entre imgCanny e imgDial aproximadamente
    return imgThres


# Obtiene el contorno del documento
def getContours(img):
    biggest = np.array([])  # Guarda las coordenadas del contorno rectangular más grande (bordes del documento)
    maxArea = 0     # Área del documento -> Encerrada en un contorno de cuatro lados
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:  # Para evitar ruido
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4: # Solo selecciona el mayor contorno de cuatro lados (bordes del documento) -> útil cuando el mismo documento tiene otros cuadrados dentro (serán de menor tamaño)
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest  # Mayor contorno de cuatro lados -> Coordenadas de las esquinas


# Para agrupar las imágenes
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
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
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


# Reordena los puntos
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2)) # Redimensiona el array a uno de 4 elementos y dos coordenadas -> Si no se hace, la forma (shape) sería por defecto (4, 1, 2) -> Ese 1 no es necesario
    myPointsNew = np.zeros((4, 1, 2), np.int32) # La salida, para que funcione con la otra función, debe tener shape = (4, 1, 2) -> Se añade el 1 de nuevo
    add = myPoints.sum(1)   # Suma las dos coordenadas de cada punto, dando lugar a un solo elemento (1 eje) -> Devuelve un array de 4 valores: uno por cada punto (x e y sumadas)
    print("add", add) # El menor valor de add será la esquina origen (0, 0), e irá en la posición 0 de myPoints. El mayor valor será la esquina opuesta al origen (width, height), e irá en la última posición del array -> Esta esquina está en la misma diagonal
    myPointsNew[0] = myPoints[np.argmin(add)]   # Primera posición = menor
    myPointsNew[3] = myPoints[np.argmax(add)]   # Última posición = mayor
    print("NewPoints", myPointsNew)
    diff = np.diff(myPoints, axis=1)    # Diferencia entre los dos puntos que no son ni máximo ni mínimo
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew  # Puntos reordenados


# Para tener solo en la imagen la parte que está dentro del contorno (y cambiar la perspectiva) -> Obtiene el contorno a partir de las cuatro esquinas -> Similar al capítulo 5
def getWarp(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # "Traslada" las esquinas del contorno (pts1) a las posiciones dadas (pts2)

    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]  # Quita parte del fondo tras el documento -> Mejor ajuste
    imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))  # Redimensiona la imagen al tamaño elegido

    return imgCropped


while True:
    success, img = cap.read()
    img = cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThres = preProcessing(img)
    biggest = getContours(imgThres)
    if biggest.size != 0:   # Muestra el documento si lo detecta solo
        imgWarped = getWarp(img, biggest)
        imageArray = ([img,imgThres], [imgContour,imgWarped])
        #imageArray = ([imgContour, imgWarped])
        cv2.imshow("ImageWarped", imgWarped)
    else:
        imageArray = ([img, imgThres], [img, img])
        #imageArray = ([imgContour, img])

    stackedImages = stackImages(0.6, imageArray)
    cv2.imshow("WorkFlow", stackedImages)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
