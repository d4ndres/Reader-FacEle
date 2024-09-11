import cv2
import numpy as np
from modules.SignalProcessor import SignalProcessor
from modules.utils import *

class ImageProcessor:
  def __init__(self):
    self.signalProcessor = SignalProcessor()

  def unifyImagesVertically(self, images):
    unify = np.vstack(images)
    originalColors = cv2.cvtColor(unify, cv2.COLOR_BGR2RGB)
    return originalColors
  
  def detectGreenLines(self, image):
    # Convertir a HSV para detectar color verde
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir el rango de color verde en HSV
    lower_green = np.array([40, 40, 40])  # Límite inferior de verde
    upper_green = np.array([90, 255, 255])  # Límite superior de verde

    # Crear una máscara que detecta solo las áreas verdes
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Realizamos una operación de dilatación para mejorar la detección de líneas gruesas
    kernel = np.ones((5, 5), np.uint8)
    mask_dilated = cv2.dilate(mask, kernel, iterations=2)
    return mask_dilated
  
  def getSectionImages(self, image) -> list:
    maskColor = self.detectGreenLines(image)
    iPy = self.signalProcessor.projectiveIntegral(maskColor, 'y')
    iPyN, _ = self.signalProcessor.normalization(iPy)
    lines = self.signalProcessor.identifyMajorTransitions(iPyN)
    return self.getSliceYFromBorderPositions(image, lines, 150)
  
  def getTableImage(self, image):
    mask = self.detectGreenLines(image)
    iPy = self.signalProcessor.projectiveIntegral(mask, 'y')
    iPyN, _ = self.signalProcessor.normalization(iPy)
    listCandidates = self.signalProcessor.indexesFromAtributeTable(iPyN)
    rangeTable = self.signalProcessor.selectRangeTable(listCandidates, 200)
    # redLineOverGraph(rangeTable)
    # graficarProyeccion(iPyN)
    return image[rangeTable[0]-10:rangeTable[1] + 10, :]
  
  def getBorderLinesPositionX( self, imageTable, distanceTolerance=15 ):
    mask = self.detectGreenLines(imageTable)

    iPx = self.signalProcessor.projectiveIntegral(mask, 'x')
    iPxN, _ = self.signalProcessor.normalization(iPx)
    return self.signalProcessor.identifyMajorTransitions(iPxN, distanceTolerance=distanceTolerance)

  def getBorderLinesPositionY( self, imageTable, distanceTolerance=15 ):
    mask = self.detectGreenLines(imageTable)

    iPy = self.signalProcessor.projectiveIntegral(mask, 'y')
    iPyN, _ = self.signalProcessor.normalization(iPy)
    return self.signalProcessor.identifyMajorTransitions(iPyN, distanceTolerance=distanceTolerance)

  def getBorderLinesPosition( self, imageTable ):
    mask = self.detectGreenLines(imageTable)

    iPx = self.signalProcessor.projectiveIntegral(mask, 'x')
    iPxN, _ = self.signalProcessor.normalization(iPx)
    listCandidatesX = self.signalProcessor.identifyMajorTransitions(iPxN)

    # Perfecto 
    iPy = self.signalProcessor.projectiveIntegral(mask, 'y')
    iPyN, _ = self.signalProcessor.normalization(iPy)
    listCandidatesY = self.signalProcessor.identifyMajorTransitions(iPyN)

    return [listCandidatesX, listCandidatesY]
    
  def getSliceYFromBorderPositions(self, image, borderPositions, thresholdHeight=20):
    rows = []
    for i in range(1, len(borderPositions)):
      if borderPositions[i] - borderPositions[i-1] > thresholdHeight:
        rows.append(image[borderPositions[i-1]:borderPositions[i], :])
    return rows

  def getSliceXFromBorderPositions(self, image, borderPositions, thresholdHeight=20):
    cols = []
    for i in range(1, len(borderPositions)):
      if borderPositions[i] - borderPositions[i-1] > thresholdHeight:
        cols.append(image[:, borderPositions[i-1]:borderPositions[i]])
    return cols