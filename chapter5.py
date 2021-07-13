# Chapter 5: Warp perspective -> Rotar un fragmento de la imagen (cambiar perspectiva)
import cv2
import numpy as np

img = cv2.imread("Resources/cards.jpg")

width, height = 250, 350
pts1 = np.float32([[111, 219], [287, 188], [154, 482], [352, 440]]) # Coordenadas de la carta cuya perspectiva se quiere cambiar (visto con Paint, por ejemplo)
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])   # Definir qué puntos de los anteriores son cada esquina (superior izquierda, superior derecha, etc)
matrix = cv2.getPerspectiveTransform(pts1, pts2)    # Matriz transformada -> Necesaria para cambiar la perspectiva
imgOutput = cv2.warpPerspective(img, matrix, (width, height))   # Cambio de perspectiva de la parte de la imagen seleccionada

cv2.imshow("Imagen", img)
cv2.imshow("Salida", imgOutput)
# Nota: Si se cambian los pts2, se puede ver qué es lo que hace esta función realmente
cv2.waitKey(0)