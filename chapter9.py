# Chapter 9: Face detection -> Algoritmo Viola - Jones -> Paper: https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf

import cv2

faceCascade = cv2.CascadeClassifier("HaarCascades/haarcascade_frontalface_default.xml")    # Clasificación en cascada -> Haar cascade = Rectángulos para formar la imagen integral (Haar-like features)
    # Nota: Para ver qué features son mejores para detectar caras, se ha entrenado con imágenes de caras y de otras cosas y se ha visto el porcentaje de acierto
    # OpenCV proporciona diferentes cascades ("nodos" de decisión para clasificar) según el tipo de imagen -> En los .xml se muestran sus características -> Cambiar según la imagen
    # También se pueden crear cascades para detectar otros objetos (buscar "make Haar Cascade OpenCV") usando el mismo algoritmo, aunque el objetivo principal de este es usar caras
img = cv2.imread("Resources/QUEEN.jpg")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Para ejecutar Viola-Jones hay que pasar la imagen a blanco y negro

faces = faceCascade.detectMultiScale(imgGray, 1.9, 4)   # detectMultiScale para detectar las caras -> Los parámetros introducidos pueden variar
    # Nota: Este cascade no es muy preciso pero es rápido
for (x, y, w, h) in faces:  # Coordenadas de las caras
    cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)    # Dibuja un rectángulo sobre las caras

cv2.imshow("Resultado", img)
cv2.waitKey(0)

# Vïdeo adicional sobre los Haar features -> https://www.youtube.com/watch?v=F5rysk51txQ
# Vídeo adicional sobre Viola-Jones -> https://www.youtube.com/watch?v=uEJ71VlUmMQ