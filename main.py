import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path # type: ignore
POPPLER_PATH = r"C:\pdf2img\poppler-0.68.0\bin"

def dpf2images(path):
  dpi=200 # puntos por pulgada
  return convert_from_path(path, dpi, poppler_path=POPPLER_PATH)

def unifyImagesVertically(images):
  unify = np.vstack(images)
  originalColors = cv2.cvtColor(unify, cv2.COLOR_BGR2RGB)
  return originalColors

def showImage(img, name='img'):
  cv2.imshow(name, img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def detectGreenLines(image):
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

def integralProyectiva(image, eje):
  if eje == 'x':
    return np.sum(image, axis=0)
  elif eje == 'y':
    return np.sum(image, axis=1)
  else:
    raise ValueError('El eje debe ser x o y')
  
def normalizarProyeccion(proyeccion):
  return (proyeccion / np.max(proyeccion), np.max(proyeccion))

def invNormalizarProyeccion(proyeccion, maximo):
  return proyeccion * maximo

def graficarProyeccion(proyeccion, eje='any'):
  plt.plot(proyeccion)
  plt.title(f'Proyección {eje}')
  plt.show()

def rangeClusters1D(proyeccion, threshold):
  # codigo a completar
  listIndex = []
  for i in range(1, len(proyeccion)):
      prev_value = proyeccion[i-1]
      current_value = proyeccion[i]
      max_value = max(prev_value, current_value)
      
      if max_value != 0 and abs(prev_value - current_value) / max_value >= 0.1:
          # listIndex.append((i, current_value))
          listIndex.append(i)

  # Crear la lista de pares de valores (rango) a partir de la lista listIndex
  range_pairs = []
  start = listIndex[0]  # Iniciar con el primer valor de la lista

  for i in range(1, len(listIndex)):
      current_value = listIndex[i]
      previous_value = listIndex[i - 1]

      # Si la diferencia es menor a 100, el rango se extiende
      if current_value - previous_value < threshold:
          end = current_value
      else:
          # Si la diferencia es mayor o igual a 100, se cierra el rango actual y se inicia uno nuevo
          range_pairs.append((start, previous_value))
          start = current_value

  # Añadir el último rango
  range_pairs.append((start, listIndex[-1]))

  return range_pairs

def getBiggestRange(clusters):
  return max(clusters, key=lambda x: x[1] - x[0])

def getTableImage(img, iPyN, range_pairs):
  biggest_range = getBiggestRange(range_pairs)

  tableIndex = []
  maxValue = max(iPyN)
  minValue = min(iPyN)
  for index, value in enumerate(iPyN):
    if abs(value - maxValue) > 0.05 and abs(value - minValue) > 0.05:
      tableIndex.append(index)


  initYTable = 0
  endYTable = 0

  for index in tableIndex:
    if index > biggest_range[0] and index <= biggest_range[1]:
        if initYTable == 0 or index < initYTable:
            initYTable = index
        if index > endYTable:
            endYTable = index

  return img[initYTable:endYTable, :]

def run():
  # pdf_path = "./documentos/DSN13.pdf"
  pdf_path = "./documentos/FE-11834.pdf"
  pages = dpf2images(pdf_path)
  combined_image_rgb = unifyImagesVertically(pages)
  # cv2.imwrite('combined_image.jpg', combined_image_rgb)
  mask = detectGreenLines(combined_image_rgb)
  # cv2.imwrite('mask.jpg', mask)

  iPy = integralProyectiva(mask, 'y')
  iPyN, maximo = normalizarProyeccion(iPy)
  range_pairs = rangeClusters1D(iPyN, 120)

  imageTable = getTableImage( combined_image_rgb, iPyN, range_pairs)
  showImage(imageTable)


if __name__ == '__main__':
  run()