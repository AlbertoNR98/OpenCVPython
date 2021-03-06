# Chapter 7: Color detection -> Para imagen
import cv2
import numpy as np


def empty(a):    # Función llama el trackbar cuando hay cambios. Esta función no hace nada
    pass


def stackImages(scale, imgArray):    # Función para agrupar imágenes (solo para mostrar mejor el resultado final)
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

# Trackbar -> Para encontrar los valores HSV entre los que están los colores que se quieren detectar
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)
cv2.createTrackbar("Hue min", "Trackbars", 0, 179, empty)    # Se crea el trackbar que detectará el mínimo hue encontrado -> Se le pasa un mínimo y máximo antes de empezar (variará cuando se manipule) -> NOTA: ESTOS VALORES SE HAN PUESTO PARA QUE ESTÉN CERCA DEL COLOR QUE SE QUIERE DETECTAR, PERO PUEDEN SER CUALESQUIERA
cv2.createTrackbar("Hue max", "Trackbars", 19, 179, empty)    # Se crea el trackbar que detectará el máximo hue encontrado -> Se le pasa un mínimo y máximo antes de empezar (variará cuando se manipule)
cv2.createTrackbar("Sat min", "Trackbars", 110, 255, empty)    # Se crea el trackbar que detectará el mínimo valor de saturación encontrado -> Se le pasa un mínimo y máximo antes de empezar (variará cuando se manipule)
cv2.createTrackbar("Sat max", "Trackbars", 240, 255, empty)    # Se crea el trackbar que detectará el máximo valor de saturación encontrado -> Se le pasa un mínimo y máximo antes de empezar (variará cuando se manipule)
cv2.createTrackbar("Val min", "Trackbars", 153, 255, empty)    # Se crea el trackbar que detectará el mínimo valorencontrado -> Se le pasa un mínimo y máximo antes de empezar (variará cuando se manipule)
cv2.createTrackbar("Val max", "Trackbars", 255, 255, empty)    # Se crea el trackbar que detectará el máximo valor encontrado -> Se le pasa un mínimo y máximo antes de empezar (variará cuando se manipule)

path = 'Resources/lambo.png'    # Ruta de la imagen

# Almacenamiento de los valores del trackbar -> Se leerán constantemente
while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convertir imagen de BGR a HSV (Matiz, saturación, valor - HSV, saturation, value)
    h_min = cv2.getTrackbarPos("Hue min", "Trackbars")  # Obtiene el HUE mínimo seleccionado con el trackbar
    h_max = cv2.getTrackbarPos("Hue max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val max", "Trackbars")
    print(h_min, h_max, s_min, s_max, v_min, v_max) # Estos valores nos permitirán filtrar la imagen, encontrando el color
    lower = np.array([h_min, s_min, v_min]) # Array con los mínimos
    upper = np.array([h_max, s_max, v_max])    # Array con los máximos
    mask = cv2.inRange(imgHSV, lower, upper)    # Muestra los píxeles cuyos valores están entre el valor seleccionado en el trackbar y el máximo -> Manipulando los trackbar (poniendo los valores HSV del color a detectar) se puede llegar a mostrar solo la zona con ese color
    imgResult = cv2.bitwise_and(img, img, mask=mask) # Imagen con la parte del color deseado resaltada

    imgStack = stackImages(0.6, ([img, imgHSV], [mask, imgResult])) # Imagen original, imagen pasada a HSV, imagen con máscara e imagen con el color seleccionado resaltado
    cv2.imshow("ImagenesApiladas", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
