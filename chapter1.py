# Chapter 1: Read images, videos and webcam
import cv2
print("Package imported")

image = cv2.imread("Resources/Collage Jazz.png")  # Lee la imagen (la importa)
cv2.imshow("Ventana1", image) # imshow para mostrar la imagen. Se debe poner el nombre de la ventana en la que se mostrará
cv2.waitKey(0)  # Argumento = tiempo que permanece abierta la ventana en ms. Si es cero, estará abierta hasta que el usuario la cierre. Si no, se cierra transcurrido ese tiempo

cap = cv2.VideoCapture("Resources/FinComedia.mp4")   # Abre el vídeo
fps = cap.get(cv2.CAP_PROP_FPS)
interval = int(1000/fps)
while True: # Bucle para procesar cada fotograma
    success, img = cap.read()   # El fotograma se guarda en img. Si se hace con éxito, success = True
    if success == True: # Si lee el frame con éxito, lo muestra
        cv2.imshow("VentanaVideo", img)
        if cv2.waitKey(interval) & 0xFF == ord('q'):   # "Ord" para leer un carácter. Si se presiona la tecla 'q', se cierra el vídeo. El delay varía según los FPS del vídeo
            break
    else:
        break
cap.release()   # Acaba de capturar cuando se acaba el vídeo
cv2.destroyWindow("VentanaVideo")   # Cierra la ventana solo (no es necesario)

capWC = cv2.VideoCapture(0 + cv2.CAP_DSHOW) # Para utilizar una webcam, poner 0 (para la webcam por defecto) -> Puede cambiar el número si hay más de una cámara -> El CAP_DSHOW hace que funcione con la cámara externa
capWC.set(3, 1280)   # Anchura con id = 3
capWC.set(4, 720)   # Longitud con id = 4
capWC.set(10, 150)  # Brillo con id = 10
while True: # Bucle para procesar cada fotograma
    successWC, imgWC = capWC.read()   # El fotograma se guarda en img. Si se hace con éxito, success = True
    if successWC == True:
        cv2.imshow("VentanaCam", imgWC)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
capWC.release()
cv2.destroyWindow("VentanaCam")

