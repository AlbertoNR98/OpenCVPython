# Pruebas 1 -> Detector de caras con webcam -> Parecido al capítulo 9
import cv2
frameWidth = 1280
frameHeight = 720
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)  # Para utilizar una webcam, poner 0 (para la webcam por defecto) -> Puede cambiar el número si hay más de una cámara -> El CAP_DSHOW hace que funcione con la cámara externa
cap.set(3, frameWidth)  # Anchura con id = 3
cap.set(4, frameHeight)  # Longitud con id = 4
cap.set(10, 250)  # Brillo con id = 10

faceCascade = cv2.CascadeClassifier("HaarCascades/haarcascade_frontalface_default.xml")

while True:
    successWC, img = cap.read()
    if successWC:
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Pasa a gris el frame leído
        faces = faceCascade.detectMultiScale(imgGray, 1.9, 4)  # Detector
        for (x, y, w, h) in faces:  # Coordenadas de las caras
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dibuja un rectángulo sobre las caras
            cv2.putText(img, "Prueba", (x, y + 20), cv2.FONT_ITALIC, 0.8, (0, 0, 255), 2)
        cv2.imshow("VentanaCam", img)  # Muestra el frame original capturado y el rectángulo que rodea la cara
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyWindow("VentanaCam")