import cv2
import numpy as np
import matplotlib.pyplot as plt

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


def run():
  img_path = "./table.jpg"
  img = cv2.imread(img_path)
  mask_dilated = detectGreenLines(img)

  DISTANCE_TOLERANCE = 15
  iPx = integralProyectiva(mask_dilated, 'x')
  iPx_norm, max_iPx = normalizarProyeccion(iPx)
  listIndexX = detectBraveChange(iPx_norm, 0.1, DISTANCE_TOLERANCE)

  iPy = integralProyectiva(mask_dilated, 'y')
  iPy_norm, max_iPy = normalizarProyeccion(iPy)
  listIndexY = detectBraveChange(iPy_norm, 0.1, DISTANCE_TOLERANCE)


  print(len(listIndexX))
  fig, (ax1, ax2) = plt.subplots(2, 1)

  for idx, index in enumerate(listIndexX):
    ax1.axvline(x=index, color='r')
    ax1.axvline(x=index+DISTANCE_TOLERANCE, color='b')

  ax1.plot(iPx_norm)
  ax1.set_title('Proyección x')

  print(len(listIndexY))

  for idx, index in enumerate(listIndexY):
    ax2.axvline(x=index, color='r')
    ax2.axvline(x=index+DISTANCE_TOLERANCE, color='b')

  ax2.plot(iPy_norm)
  ax2.set_title('Proyección y')

  plt.show()



  cv2.imshow('mask', mask_dilated)
  cv2.waitKey(0)


if __name__ == '__main__':
  run()