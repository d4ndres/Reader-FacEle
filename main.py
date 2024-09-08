from modules.PDFProcessor import PDFProcessor
from modules.utils import *
from modules.ImageProcessor import ImageProcessor



def run():
  pdfer = PDFProcessor()
  imager = ImageProcessor()
  # pdfPath = "./documentos/FE-11834.pdf"
  pdfPath = "./documentos/DSN13.pdf"
  images = pdfer.dpf2images(pdfPath)
  image = imager.unifyImagesVertically(images)
  imageTable = imager.getTableImage(image)
  [borderPositionX, borderPositionY] = imager.getBorderLinesPosition(imageTable)
  rows = imager.getSliceXFromBorderPositions(imageTable, borderPositionX)
  for row in rows:
    showImage(row)

if __name__ == '__main__':
  run()