# Chapter 4: Shapes and text
import cv2
import numpy as np

img = np.zeros((512,512,3), np.uint8) # Matriz de ceros = imagen en negro de tamaño 512x512 y tres canales
print(img.shape)    # Imprime el tamaño de la imagen
cv2.imshow("ImagenNegro", img)
cv2.waitKey(0)

img[:] = 255,0,0 # Pone todos los píxeles de la imagen en azul (BGR) -> Con [:] se refiere a todos los elementos de la matriz.
cv2.imshow("ImagenAzul", img)
cv2.waitKey(0)

img[200:300, 100:300] = 0,0,0   # Pone algunos píxeles ([alto:ancho]) en negro
cv2.imshow("ImagenAzulyNegro", img)
cv2.waitKey(0)

img[:] = 0,0,0
cv2.line(img, (200,200), (350,300), (0,255,0),thickness=3)   # Para dibujar líneas, poner imagen, puntos de inicio y fin, color y grosor
cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (0,0,255), 3) # En este caso, las coordenadas son relativas al tamaño de la imagen -> Nota: En esta función, largo y ancho están al revés que en la función shape
cv2.imshow("Linea", img)
cv2.waitKey(0)

img[0:512, 0:512] = 0,0,0 # Igual que [:]
cv2.rectangle(img, (0,0), (250, 250), (0,0,255),2)  # Rectángulos
cv2.imshow("Rectangulo", img)
cv2.waitKey(0)

img[0:512, 0:512] = 0,0,0 # Igual que [:]
cv2.rectangle(img, (0,0), (250, 250), (0,0,255),cv2.FILLED)  # Rectángulos
cv2.imshow("RectanguloRelleno", img)
cv2.waitKey(0)

img[:] = 0, 0, 0
cv2.circle(img, (400, 50), 10, (255, 255, 0), 5)  # Círculo -> Se pasan las coordenadas del centro y el radio, además del color y el grosor
cv2.imshow("Circunferencia", img)
cv2.waitKey(0)

img[:] = 0, 0, 0
cv2.putText(img, "OPENCV", (300, 200), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,150,0), 2)    # Poner texto sobre la imagen. OpenCV contiene algunas fuentes ya definidas. Punto de inicio, escala de la letra y grosor
cv2.imshow("Texto", img)
cv2.waitKey(0)