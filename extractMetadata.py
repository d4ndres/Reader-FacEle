from modules.ImageProcessor import ImageProcessor
from modules.PDFProcessor import PDFProcessor
from modules.utils import *
import matplotlib.pyplot as plt
from modules.SignalProcessor import SignalProcessor
import numpy as np
from modules.OCR import OCR
import matplotlib.patches as patches

imager = ImageProcessor()
pdfer = PDFProcessor()
singer = SignalProcessor()
ocrer = OCR()


def encontrar_valor(data, clave, umbral=0.80):
  for sublista in data:
    for index, lista in enumerate(sublista):
      if isinstance(lista, list) and len(lista) > 1:
        texto = ' '.join(lista)
        if similaridad(clave, texto) >= umbral:
          return sublista[index + 1][0]  # Retorna el valor siguiente a la clave
  return None

def run():
  filePath = './documentos/DSN13.pdf'
  images = pdfer.dpf2images(filePath)
  image = imager.unifyImagesVertically(images)
  maskColor = imager.detectGreenLines(image)
  iPy = singer.projectiveIntegral(maskColor, 'y')
  iPyN, _ = singer.normalization(iPy)
  lines = singer.identifyMajorTransitions(iPyN)
  sectionImages = imager.getSliceYFromBorderPositions(image, lines, 150);
  
  numero_documento_soporte = None
  fecha_generacion = None
  razon_social = None
  nit_del_adquiriente = None
  for img in sectionImages:
    words = ocrer.processImageToText(img)
    groups = ocrer.groupByGrid(words)
    
    if not numero_documento_soporte:
      numero_documento_soporte = encontrar_valor(groups, 'Numero documento soporte:')
    
    if not fecha_generacion:
      fecha_generacion = encontrar_valor(groups, 'Fecha de generacion:')
    if not razon_social:
      razon_social = encontrar_valor(groups, 'Razon social:')
    if not nit_del_adquiriente:
      nit_del_adquiriente = encontrar_valor(groups, 'NIT del adquiriente:')

    if (numero_documento_soporte != None and 
        fecha_generacion != None and
        razon_social != None and
        nit_del_adquiriente != None
        ):
      break

  print('Numero documento soporte:', numero_documento_soporte)
  print('Fecha de generacion:', fecha_generacion)
  print('Razon social:', razon_social)
  print('NIT del adquiriente:', nit_del_adquiriente)


if __name__ == '__main__':
  run()