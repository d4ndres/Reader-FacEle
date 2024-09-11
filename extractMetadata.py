from modules.ImageProcessor import ImageProcessor
from modules.PDFProcessor import PDFProcessor
from modules.utils import *
import matplotlib.pyplot as plt
from modules.SignalProcessor import SignalProcessor
import numpy as np
# from modules.OCR import OCR
import matplotlib.patches as patches

imager = ImageProcessor()
pdfer = PDFProcessor()
singer = SignalProcessor()
# ocrer = OCR()

def signalShowNone(s1, s2, threshold=0.001):
    # Asegúrate de que s1 y s2 sean arrays numpy
    s1 = np.array(s1)
    s2 = np.array(s2)
    # Suma de las señales
    suma = s1 - s2
    # Crear un array de salida
    resultado = np.where(suma == 0, 1, 0)
    return resultado

def obtener_rangos_altos(señal, minSize=0):
    rangos = []
    en_alto = False
    inicio = 0
    
    for i, valor in enumerate(señal):
        if valor == 1:
            if not en_alto:
                inicio = i
                en_alto = True
        else:
            if en_alto:
                rangos.append((inicio, i - 1))
                en_alto = False
    
    if en_alto:
        rangos.append((inicio, len(señal) - 1))
    
    return [ rango for rango in rangos if abs(rango[1] - rango[0]) > minSize ]


def getWhiteBlocks( image ):
  maskColor = imager.detectGreenLines(image)
  iPy = singer.projectiveIntegral(maskColor, 'y')
  iPyN, _ = singer.normalization(iPy)
  
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
  maskInv = cv2.bitwise_not(mask)
  iPyTex = singer.projectiveIntegral(maskInv, 'y')
  iPyTextN, _ = singer.normalization(iPyTex)
  
  noneValues = signalShowNone(iPyTextN, iPyN)
  rangosAltos = obtener_rangos_altos(noneValues, 30)
  return rangosAltos

def sectionImages( image ):
  rangosAltos = getWhiteBlocks(image)
  mediaDeRangoAltos = [ int(rango[0] + (rango[1] - rango[0])/2 ) for rango in rangosAltos]
  return imager.getSliceYFromBorderPositions(image, mediaDeRangoAltos)
  

def run():
  # filePath = './documentos/existentes/A-52298.pdf'
  filePath = './documentos/existentes/DSN14.pdf'
  images = pdfer.dpf2images(filePath)
  image = imager.unifyImagesVertically(images)
  sectionImg = sectionImages(image)


if __name__ == '__main__':
  run()