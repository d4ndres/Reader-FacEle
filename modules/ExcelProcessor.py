
import pandas as pd
import os

class ExcelProcessor:
  def __init__(self):
    pass

  def defineListOfCol(self, words, _range):
    groups = [[] for _ in range(len(_range) - 1)]


    for word in words:
      x = word["x"]
      if len(_range):
        for i in range(len(_range) - 1):
          if _range[i] <= x < _range[i+1]:
            groups[i].append(word)
            break
    
    row = []
    for group in groups:
      sortedGroup = sorted(group, key=lambda d: (d['y'], d['x']))
      row.append(
        ' '.join([word['label'] for word in sortedGroup])
      )
    
    return row
  
  def guardar_datos_en_excel(self, data, file_path="datos"):
    df = pd.DataFrame(data)
    df.to_excel(f'{file_path}.xlsx', index=False, header=False)
