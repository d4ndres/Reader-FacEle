from modules.ImageProcessor import ImageProcessor
from modules.PDFProcessor import PDFProcessor
from modules.utils import *
from modules.SignalProcessor import SignalProcessor
import numpy as np
from modules.OCR import OCR

imager = ImageProcessor()
pdfer = PDFProcessor()
singer = SignalProcessor()
ocrer = OCR()

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


def getWhiteBlocks( image, minSize=30 ):
  maskColor = imager.detectGreenLines(image)
  iPy = singer.projectiveIntegral(maskColor, 'y')
  iPyN, _ = singer.normalization(iPy)
  
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
  maskInv = cv2.bitwise_not(mask)
  iPyTex = singer.projectiveIntegral(maskInv, 'y')
  iPyTextN, _ = singer.normalization(iPyTex)
  
  noneValues = signalShowNone(iPyTextN, iPyN)
  rangosAltos = obtener_rangos_altos(noneValues, minSize=minSize)
  return rangosAltos

def sectionImages( image, threshold=60 ):
  rangosAltos = getWhiteBlocks(image)
  mediaDeRangoAltos = [ int(rango[0] + (rango[1] - rango[0])/2 ) for rango in rangosAltos]
  candidates =  imager.getSliceYFromBorderPositions(image, mediaDeRangoAltos, thresholdHeight=threshold)
  result = []
  for img in candidates:
    maskColor = imager.detectGreenLines(img)
    iPy = singer.projectiveIntegral(maskColor, 'y')
    iPyN, _ = singer.normalization(iPy)
    if( max(iPyN) == 1 ):
      result.append(img)
  return result

def crear_diccionario(datos):
  # Crear el diccionario secundario vacío
  diccionario_secundario = {}

    # Recorrer la lista de datos comenzando desde el segundo elemento
  for i in range(1, len(datos)):
    if datos[i].endswith(':'):
      # Inicializar el valor como None
      valor = None
      # Si el siguiente elemento no termina con ':', lo usamos como valor
      if i + 1 < len(datos) and not datos[i + 1].endswith(':'):
        valor = datos[i + 1]
      diccionario_secundario[datos[i]] = valor

    # Crear el diccionario principal

  title = None
  for candidate in datos:
    if (diffString(candidate, 'Representacion') < 0.7 and 
        diffString(candidate, 'Grafica') < 0.7 ):
      title = candidate
      break

  diccionario_principal = {title: diccionario_secundario}
  return diccionario_principal

def run():
  filePath = './documentos/existentes/A-52298.pdf'
  # filePath = './documentos/existentes/DSN14.pdf'
  images = pdfer.dpf2images(filePath)
  image = imager.unifyImagesVertically(images)
  sectionImg = sectionImages(image)

  globalDc = {}
  for section in sectionImg:
    datosConvenientes = []
    words = ocrer.processImageToText(section)
    data = ocrer.groupByProp(words, 'y', 5)
    for line in data:
      newLine = ocrer.groupByXW(line, 10)
      for groups in newLine:
        datosConvenientes.append(' '.join([ word["label"] for word in groups]))

    dc = crear_diccionario(datosConvenientes)
    
    for key, value in dc.items():
      globalDc[key] = value

  print(globalDc)

if __name__ == '__main__':
  run()