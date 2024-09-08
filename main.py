from getCeldFromTable import getCeldFromTable
import numpy as np
import cv2
from doctr.models import crnn_mobilenet_v3_small


def run():
  table_path = 'table.jpg'
  listOfCelds = getCeldFromTable(table_path)

  for celd in listOfCelds:
    print(f'Fila: {celd["fila"]}, Columna: {celd["columna"]}, Texto: {celd["texto"]}')
    # cv2.imshow('celda', celd['imagen'])
    # cv2.waitKey(0)

if __name__ == '__main__':
  run()