# Project 3: Detección de matrículas haciendo uso de la webcam -> Uso de Viola-Jones
import cv2

# Parámetros
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap.set(3, frameWidth)
cap.set(4, frameWidth)
cap.set(10, 150)

nPlateCascade = cv2.CascadeClassifier("HaarCascades/haarcascade_russian_plate_number.xml") # Clasificador para matrículas rusas
minArea = 500   # Tamaño mínimo del rectángulo para que se tenga en cuenta (matrícula)
color = (255, 0, 255)
count = 0   # Lleva la cuenta de las matrículas que ha capturado

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:  # Filtro para asegurar que es una matrícula
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, "NumberPlate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            imgRoi = img[y:y+h, x:x+w]  # Recorta la imagen -> Se queda solo con la matrícula
            cv2.imshow("ROI", imgRoi)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("Resources/Scanned/NoPlate_"+str(count)+".jpg", imgRoi) # Guarda las matrículas que capta en la carpeta "Scanned"
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)   # Dibuja un rectángulo en la imagen completa para saber que se ha capturado
        cv2.putText(img, "Scan saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
        cv2.imshow("Result", img)
        cv2.waitKey(500)    # Un delay para poder ver bien lo que se ha capturado
        count += 1


