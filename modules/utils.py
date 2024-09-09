import cv2
import matplotlib.pyplot as plt

def showImage(img, name='img'):
  cv2.imshow(name, img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def graficarProyeccion(proyeccion, eje='any'):
  plt.plot(proyeccion)
  plt.title(f'Proyección {eje}')
  plt.show()

def redLineOverGraphX( listIndex, color='r'):
  print(len(listIndex))
  for lineIndex in listIndex:
    plt.axvline(x=lineIndex, color=color, linestyle='-')

def redLineOverGraphY(listIndex, color='r'):
  for lineIndex in listIndex:
    plt.axhline(y=lineIndex, color=color, linestyle='-')

def conicidenciaDeListas( list1, list2 ):
  set1 = set(list1)
  set2 = set(list2)
  elementos_comunes = len(set1.intersection(set2))
  total_elementos = len(set1.union(set2))
  porcentaje = (elementos_comunes / total_elementos) * 100
  return porcentaje / 100
