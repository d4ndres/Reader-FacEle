from pdf2image import convert_from_path # type: ignore
POPPLER_PATH = r"C:\pdf2img\poppler-0.68.0\bin"

class PDFProcessor:
  def dpf2images(self, path: str) -> list:
    dpi = 200  # puntos por pulgada
    return convert_from_path(path, dpi, poppler_path=POPPLER_PATH)