import os
from modules.utils import *
os.environ['USE_TORCH'] = '1'
from doctr.models import ocr_predictor

class OCR:
  def __init__(self):
    self.predictor = ocr_predictor(pretrained=True)

  def processImageToText(self, image):
      result = self.predictor([image])
      humanResult = result.export()["pages"][0]
      pageDimension = humanResult["dimensions"]
      lines = humanResult["blocks"][0]["lines"]

      words = []
      for line in lines:
        for index, word in enumerate(line["words"]):
          print("#", end='')
          height, width = pageDimension
          (xmin, ymin), (xmax, ymax) = word["geometry"]
          x, w = xmin * width, (xmax - xmin) * width
          y, h = ymin * height, (ymax - ymin) * height



          words.append(
            {
              "label": word['value'],
              "confidence": f'{word['confidence']:.2%}',
              "parentPageDimension": pageDimension,
              "x": x,
              "y": y,
              "w": w,
              "h": h
            }
          )
      return words
  
  def group_by_x(self, data, threshold=1):
    data = sorted(data, key=lambda item: item['x'])

    result = []
    current_group = []

    for item in data:
      # Si el grupo actual está vacío, agrega el primer elemento
      if not current_group:
        current_group.append(item)
      else:
        # Compara el valor 'y' del último elemento del grupo actual con el elemento actual
        if abs(item['x'] - (current_group[-1]['x'] + current_group[-1]['w']) ) <= threshold:
          current_group.append(item)
        else:
          # Si el valor de 'y' excede el umbral, agrega el grupo actual al resultado y empieza un nuevo grupo
          result.append(' '.join([item['label'] for item in current_group]))
          current_group = [item]
    
    # Agrega el último grupo si no está vacío
    if current_group:
      result.append(' '.join([item['label'] for item in current_group]))
    return result
    

  def groupByGrid(self, data, threshold=5):
    data = sorted(data, key=lambda x: x['y'])
    data = [
      {
        "label": item["label"] ,
        "y": item["y"],
        "x": item["x"],
        "w": item["w"],
      }
      for item in data
    ]
    result = []
    current_group = []
    
    # Itera sobre los datos ordenados
    for item in data:
        # Si el grupo actual está vacío, agrega el primer elemento
        if not current_group:
            current_group.append(item)
        else:
            # Compara el valor 'y' del último elemento del grupo actual con el elemento actual
            if abs(item['y'] - current_group[-1]['y']) <= threshold:
                current_group.append(item)
            else:
                # Si el valor de 'y' excede el umbral, agrega el grupo actual al resultado y empieza un nuevo grupo
                result.append(self.group_by_x(current_group))
                current_group = [item]
    
    # Agrega el último grupo si no está vacío
    if current_group:
      result.append(self.group_by_x(current_group))
    return result
  
  
  def encontrar_valor(self, data, clave, umbral=0.80):
    for sublista in data:
      for index, lista in enumerate(sublista):
        if isinstance(lista, list) and len(lista) > 1:
          texto = ' '.join(lista)
          if similaridad(clave, texto) >= umbral:
            return sublista[index + 1][0]  # Retorna el valor siguiente a la clave
    return None
  
  def findKeyValueFromImage(self, images, toFind : list):
    result = { key: None for key in toFind }

    for img in images:
      words = self.processImageToText(img)
      groups = self.groupByGrid(words)

      for line in groups:
        print(line)

      for key, value in result.items():
        if value == None:
          out = self.encontrar_valor(groups, key)
          # print(f'key {key}, value {value}, out {out}')
          result[f'{key}'] = out
      if all( value is not None for value in result.values() ):
        break

    return result