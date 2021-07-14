# Chapter 6: Joining images
import cv2
import numpy as np

img = cv2.imread("Resources/cards.jpg")

imgHor = np.hstack((img, img))  # Unión horizontal de dos matrices -> Unión horizontal de dos imágenes
imgVer = np.vstack((img, img))  # Unión vertical de dos matrices. Nota: Con este método no se puede cambiar el tamaño de la imagen directamente. También tienen ambas imágenes el mismo número de canales
cv2.imshow("JoinHorizontal", imgHor)
cv2.imshow("JoinVertical", imgVer)
cv2.waitKey(0)

# Función para poder reescalar las imágenes y añadir imágenes vertical y horizontalmente a la vez
def stackImages(scale, imgArray):   # imgArray puede ser de tamaño MxN
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)   # Si el primer argumento introducido es una lista (array de imágenes)
    width = imgArray[0][0].shape[1] # Shape para saber el tamaño -> Shape: (height, width)
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range (0, rows):
            for y in range (0, cols):
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
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgStack = stackImages(0.5, ([img, img, img], [img, img, img], [img, img, img])) # Función -> Reescala a 0,5 y une 6 imágenes: 3 en una fila y 3 en otra. Nota: Las imágenes pueden ser distintas entre sí
imgStack2 = stackImages(0.5, ([img, img, img], [img, img, img], [np.zeros((img.shape[1], img.shape[0], 3), np.uint8), img, np.zeros((img.shape[1], img.shape[0], 3), np.uint8)])) # En esta llamada, en la última fila se dejan dos huecos en negro
imgStack3 = stackImages(0.5, ([imgGray, img, img], [img, imgGray, img], [img, img, imgGray])) # En esta llamada se usan dos imágenes distintas
cv2.imshow("ImagenFuncion", imgStack)
cv2.imshow("ImagenFuncion2", imgStack2)
cv2.imshow("ImagenFuncion3", imgStack3)
cv2.waitKey(0)