from modules.PDFProcessor import PDFProcessor
from modules.utils import *
from modules.ImageProcessor import ImageProcessor
from modules.OCR import OCR
from modules.ExcelProcessor import ExcelProcessor
import os
import numpy as np
from modules.SignalProcessor import SignalProcessor

imager = ImageProcessor()
ocr = OCR()
pdfer = PDFProcessor()
imager = ImageProcessor()
exceler = ExcelProcessor()
singer = SignalProcessor()

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




















def tableImageToList(pdfPath):
  images = pdfer.dpf2images(pdfPath)
  image = imager.unifyImagesVertically(images)
  imageTable = imager.getTableImage(image)
  
  spliceOfContentX = imager.getBorderLinesPositionX(imageTable, 15)
  _, borderPositionY = imager.getBorderLinesPosition(imageTable)
  rows = imager.getSliceYFromBorderPositions(imageTable, borderPositionY)

  table = []
  for row in rows:
    words = ocr.processImageToText(row)
    table.append(
      exceler.defineListOfCol(words, spliceOfContentX)
    )
  print('')
  return table

def allDataSections( filePath ):
  images = pdfer.dpf2images(filePath)
  unfyImage = imager.unifyImagesVertically(images)
  sectionImg = sectionImages(unfyImage)

  globalDc = {}
  for index, section in enumerate(sectionImg):
    datosConvenientes = []
    words = ocr.processImageToText(section)
    data = ocr.groupByProp(words, 'y', 5)
    for line in data:
      newLine = ocr.groupByXW(line, 10)
      for groups in newLine:
        datosConvenientes.append(' '.join([ word["label"] for word in groups]))

    dc = crear_diccionario(datosConvenientes)
    
    for key, value in dc.items():
      globalDc[key] = value

    if index == 3:
      break

  return globalDc



def run():
  currentPath = os.getcwd()
  pathDir = rf'{currentPath}\documentos\existentes'
  fileNames = os.listdir(pathDir)


  df = []
  totalIndex = len(fileNames)
  for index, fileName in enumerate(fileNames):
    filePath = rf'{pathDir}\{fileName}'
    print( f'Iniciando con {fileName}')
    print( f'{index + 1} / {totalIndex}')

    metadataToFind = {
      'Datos del Documento': ['Codigo Unico de Factura - CUFE :', 'Numero de Factura:', 'Fecha de Emision:'],
      'Datos del Emisor / Vendedor': ['Razon Social:', 'Nit del Emisor:'],
      'Datos del Adquiriente / Comprador': ['Nombre o Razon Social:', 'Numero Documento:']
    }

    pdfMetaData = allDataSections( filePath )

    metaDataOut = {}
    
    # la logica al crearlo es clara y sin dudar. citicamente esta horrible.
    for keySectionToFind, listKeysToFind in metadataToFind.items():
      for keyFound, valueFound in pdfMetaData.items():
        if diffString(keySectionToFind, keyFound) > 0.7:
          for key, value in valueFound.items():
            for keyToFind in listKeysToFind:
              if diffString(key, keyToFind) > 0.7:
                metaDataOut[keyToFind] = value

    sortedOut = [valor for clave, valor in sorted(metaDataOut.items())]

    table = tableImageToList(filePath)
    headerDetection = True # Future
    for row in table:
      for out in sortedOut:
        row.insert(0, out)
      
      if headerDetection:
        df.append(row)

    break

  exceler.guardar_datos_en_excel(df, 'result_revision')

if __name__ == '__main__':
  run()