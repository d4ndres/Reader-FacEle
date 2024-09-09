from modules.PDFProcessor import PDFProcessor
from modules.utils import *
from modules.ImageProcessor import ImageProcessor
from modules.OCR import OCR
from modules.ExcelProcessor import ExcelProcessor
import numpy as np


import matplotlib.pyplot as plt
import matplotlib.patches as patches


def run():

  imager = ImageProcessor()
  ocr = OCR()
  pdfer = PDFProcessor()
  imager = ImageProcessor()
  exceler = ExcelProcessor()


  # pdfPath = "./documentos/FE-11834.pdf"
  # pdfPath = "./documentos/DSN13.pdf"
  pdfPath = "./documentos/existentes/A-52298.pdf"
  images = pdfer.dpf2images(pdfPath)
  image = imager.unifyImagesVertically(images)
  imageTable = imager.getTableImage(image)
  
  spliceOfContentX = imager.getBorderLinesPositionX(imageTable, 15)
  _, borderPositionY = imager.getBorderLinesPosition(imageTable)
  rows = imager.getSliceYFromBorderPositions(imageTable, borderPositionY)

  
  for row in rows:
    words = ocr.processImageToText(row)
    singleRow = exceler.defineListOfCol(words, spliceOfContentX)
    print(singleRow)
    


if __name__ == '__main__':
  run()