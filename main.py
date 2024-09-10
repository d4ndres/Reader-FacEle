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


def run():

  currentPath = os.getcwd()
  pathDir = rf'{currentPath}\documentos\existentes'
  fileNames = os.listdir(pathDir)


  data = []
  totalIndex = len(fileNames)
  for index, fileName in enumerate(fileNames):
    print( f'{index}/{totalIndex}')
    table = tableImageToList(rf'{pathDir}\{fileName}')
    for row in table:
      row.insert(0, fileName)
      data.append(row)

  exceler.guardar_datos_en_excel(data, 'result_revision')

if __name__ == '__main__':
  run()