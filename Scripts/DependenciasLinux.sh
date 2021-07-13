#!/bin/bash
echo Instalador de modulos pip para Python 3.9.x
echo Dependencias: OpenCV y NumPy
sudo pip install opencv-python #OpenCV requiere NumPy, por lo que lo instala automaticamente
echo -e
read -p "Presione una tecla para continuar..."