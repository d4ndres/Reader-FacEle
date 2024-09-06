import os
import cv2
import numpy as np
from pdf2image import convert_from_path
POPPLER_PATH = r"C:\pdf2img\poppler-0.68.0\bin"


def run():
  pdf_path = "./documentos/DSN13.pdf"
  pages = convert_from_path(pdf_path, 200, poppler_path=POPPLER_PATH)
  for i, page in enumerate(pages):
    cv2.imshow(f"Page {i+1}", np.array(page))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
  run()