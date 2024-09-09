import os
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
  