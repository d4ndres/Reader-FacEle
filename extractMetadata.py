from modules.ImageProcessor import ImageProcessor
from modules.PDFProcessor import PDFProcessor
from modules.utils import *
import matplotlib.pyplot as plt
from modules.SignalProcessor import SignalProcessor
import numpy as np
from modules.OCR import OCR
import matplotlib.patches as patches
from  difflib import SequenceMatcher

imager = ImageProcessor()
pdfer = PDFProcessor()
singer = SignalProcessor()
ocrer = OCR()


def encontrar_valor(data, tofind, threshold=0.8):
  for row_index, item in enumerate(data):
    similarity = SequenceMatcher(None, tofind, item).ratio()
    print( f'{tofind} === {item} -> %{similarity}')
    if similarity >= threshold:
      return None
  return None

def run( toFind ):
  filePath = './documentos/DSN13.pdf'
  images = pdfer.dpf2images(filePath)
  image = imager.unifyImagesVertically(images)



  maskColor = imager.detectGreenLines(image)
  iPy = singer.projectiveIntegral(maskColor, 'y')
  iPyN, _ = singer.normalization(iPy)
  lines = singer.identifyMajorTransitions(iPyN)
  sectionImages = imager.getSliceYFromBorderPositions(image, lines, 150)
  
  result = { key: None for key in toFind }

  for img in sectionImages:
    words = ocrer.processImageToText(img)
    groups = ocrer.groupByGrid(words)
    
    for line in groups:
      print(line)

    for key, value in result.items():
      if value == None:
        out = encontrar_valor(groups, key)
        result[f'{key}'] = out


    if all( value is not None for value in result.values() ):
      break

  return result


if __name__ == '__main__':
  valuesFound = run([
  'Numero documento soporte',
  'Fecha de generacion',
  'Razon social',
  'NIT del adquiriente',
  ])

  for key, value in valuesFound.items():
    print(f'{key}: {value}')