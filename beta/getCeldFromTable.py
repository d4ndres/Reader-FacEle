import cv2
import numpy as np
import matplotlib.pyplot as plt
from openai import OpenAI
# from gptocr import OCR

# 
# client = OpenAI(api_key=KEY)

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


# cambio brusco en la proyección
def detectBraveChange(proyeccion, threshold, distanceTolerance=5):
  listIndex = []
  for i in range(1, len(proyeccion)):
    prev_value = proyeccion[i-1]
    current_value = proyeccion[i]
    max_value = max(prev_value, current_value)
    
    if max_value != 0 and abs(prev_value - current_value) / max_value >= threshold:
      listIndex.append(i)

  # reduce by a distance tolerance
  reduce = []
  start = listIndex[0]
  for i in range(1, len(listIndex)):
    current_value = listIndex[i]
    prev_value = listIndex[i-1]
    
    if current_value - prev_value <= distanceTolerance:
      continue
    else:
      reduce.append(start)
      start = current_value

  reduce.append(start)
  return reduce

def getLinesTable(mask_dilated):
  DISTANCE_TOLERANCE = 15
  iPx = integralProyectiva(mask_dilated, 'x')
  iPx_norm, max_iPx = normalizarProyeccion(iPx)
  listIndexX = detectBraveChange(iPx_norm, 0.1, DISTANCE_TOLERANCE)

  iPy = integralProyectiva(mask_dilated, 'y')
  iPy_norm, max_iPy = normalizarProyeccion(iPy)
  listIndexY = detectBraveChange(iPy_norm, 0.1, DISTANCE_TOLERANCE)

  return ( listIndexX, listIndexY )

def getCeldFromTable(img_path):

  img = cv2.imread(img_path)
  img = cv2.copyMakeBorder(img, 0, 20, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
  
  mask_dilated = detectGreenLines(img)
  (columnas, filas) = getLinesTable(mask_dilated)



  lista_celdas = []
  # Crear las celdas y almacenarlas en la lista de diccionarios
  for i in range(len(filas) - 1):
    for j in range(len(columnas) - 1):
      # Definir las coordenadas de la celda
      izquierda = columnas[j]
      superior = filas[i]
      derecha = columnas[j+1]
      inferior = filas[i+1]

      # Recortar la celda de la imagen original
      celda = img[superior:inferior, izquierda:derecha]
      
      
      # text = OCR(client, celda)
      # print(i,j)
      text = 'some text'
      # print(text)
      # Almacenar la celda en un diccionario con las coordenadas y la imagen
      celda_info = {
          "fila": i + 1,  # Número de fila
          "columna": j + 1,  # Número de columna
          "imagen": celda,  # Imagen de la celda,
          "texto": text
      }

      # Añadir el diccionario a la lista
      lista_celdas.append(celda_info)

  return lista_celdas
  

  # crea un archivo csv tenido en cuenta las filas y columnas
  # with open('table_data.csv', 'w') as f:
  #   f.write('Fila,Columna,Texto\n')
  #   for celda in lista_celdas:
  #     f.write(f"{celda['fila']},{celda['columna']},{celda['texto']}\n")
  # print("Table data saved to table_data.csv")    

