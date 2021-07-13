@echo off
echo Instalador de modulos de pip para Python 3.9.x
echo Dependencias: OpenCV y NumPy
pip install opencv-python & REM OpenCV requiere de NumPy, por lo que lo instala automaticamente
echo.
pause
exit