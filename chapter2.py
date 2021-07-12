# Chapter 2: Basic functions
import cv2
import numpy as np

img = cv2.imread("Resources/Collage Jazz.png")
kernel = np.ones((5,5), np.uint8)   # Matriz de uint8 (8 bits cada valor) de 5x5 rellena SOLO DE UNOS

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Cambia el color de la imagen. En OpenCV, se usa BGR en lugar de RGB por convención
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0) # Desenfoca la imagen. Los parámetros introducidos varían el modo de desenfoque. (7,7) es el tamaño del kernel (7x7)
imgCanny = cv2.Canny(img, 150, 200) # Algoritmo de Canny -> Detecta los bordes de la imagen (gradiente). Los parámetros (threesold) varían el resultado del algoritmo
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)   # Dilatación. Requiere de una matriz (kernel) para funcionar, que se crea con la librería numpy.
imgEroded = cv2.erode(imgDialation, kernel, iterations=1)   # Erosión de la imagen. Opuesto a dialation. Reduce los bordes
cv2.imshow("ImagenGris", imgGray)
cv2.imshow("ImagenDesenfocada", imgBlur)
cv2.imshow("ImagenCanny", imgCanny)
cv2.imshow("ImagenDilatada", imgDialation)
cv2.imshow("ImagenErode", imgEroded)
cv2.waitKey(0)  # Nota: Para que no salgan todas las imágenes a la vez, poner waitKey entre llamadas de imshow