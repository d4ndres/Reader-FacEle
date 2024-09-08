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

def redLineOverGraph( listIndex):
  print(len(listIndex))
  for lineIndex in listIndex:
    plt.axvline(x=lineIndex, color='r', linestyle='-')
