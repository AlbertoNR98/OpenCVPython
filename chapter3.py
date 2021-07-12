# Chapter 3: Crop (recorta) and Resize
import cv2
# Nota: En OpenCv, las coordenadas (0, 0) están arriba a la izquierda en la imagen, por lo que el eje Y tiene sentido POSITIVO hacia ABAJO. El eje X tiene sentido positivo hacia la derecha
img = cv2.imread("Resources/Collage Jazz.png")
print(img.shape)    # Muestra el tamaño de la imagen: (Alto, Ancho, Canales (BGR))

imgResize = cv2.resize(img, (350,240))  # Cambia el tamaño: (Ancho, Alto) -> Al revés que el return de la función shape
print(imgResize.shape)

imgCropped = img[0:200, 200:500]  # Recorta la imagen. En la matriz se pone qué píxeles se desea conservar. Conserva los primeros 200 píxeles de ancho y la coordenada y entre 200 y 500
print(imgCropped.shape)

cv2.imshow("ImagenOriginal", img)
cv2.imshow("ImagenResize", imgResize)
cv2.imshow("ImagenRecortada", imgCropped)
cv2.waitKey(0)