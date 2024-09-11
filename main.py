from modules.PDFProcessor import PDFProcessor
from modules.utils import *
from modules.ImageProcessor import ImageProcessor
from modules.OCR import OCR
from modules.ExcelProcessor import ExcelProcessor
import os
import numpy as np

imager = ImageProcessor()
ocr = OCR()
pdfer = PDFProcessor()
imager = ImageProcessor()
exceler = ExcelProcessor()

def pdf2image(pdfPath):
  images = pdfer.dpf2images(pdfPath)
  return imager.unifyImagesVertically(images)

def tableImageToList(image):
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

def keyValueToFind(image, keys):
  sectionImages = imager.getSectionImages(image)
  return ocr.findKeyValueFromImage( sectionImages, keys)

def run():

  currentPath = os.getcwd()
  pathDir = rf'{currentPath}\documentos\existentes'
  fileNames = os.listdir(pathDir)


  data = []
  totalIndex = len(fileNames)
  for index, fileName in enumerate(fileNames):
    print( f'{index}/{totalIndex}')

    image = pdf2image(rf'{pathDir}\{fileName}')
    keysMetaData = [
    'NIT del adquiriente',
    'Razon social',
    'Fecha de generacion',
    'Fecha de Emision:',
    'Numero documento soporte',
    'Numero de Factura:'
    ]
    metadata = keyValueToFind(image, keysMetaData )
    print(metadata)

    table = tableImageToList(image)
    for row in table:
      row.insert(0, fileName)
      # for key in keysMetaData:
      #   row.insert(0, metadata[key])
      data.append(row)

    break

  exceler.guardar_datos_en_excel(data, 'result_revision')

if __name__ == '__main__':
  run()