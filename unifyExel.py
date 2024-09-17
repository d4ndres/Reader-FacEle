import pandas as pd
import glob

def unir_archivos_excel(ruta_archivos, archivo_salida):
    # Lista para almacenar los DataFrames
    dfs = []

    # Lista de nombres de los meses
    meses = [
          'ENERO',
          'FEBRERO',
          'MARZO',
          'ABRIL',
          'MAYO',
          'JUNIO',
          'JULIO',
          'AGOSTO',
          'SEPTIEMBRE'
        ]

    # Leer cada archivo Excel y agregarlo a la lista de DataFrames
    for mes in meses:
        archivo = f"{ruta_archivos}/felipe_rivera_{mes}.xlsx"
        try:
            df = pd.read_excel(archivo, header=None)
            dfs.append(df)
        except FileNotFoundError:
            print(f"No se encontró el archivo: {archivo}")

    # Concatena todos los DataFrames en uno solo
    df_unificado = pd.concat(dfs, ignore_index=True)

    # Guarda el DataFrame unificado en un nuevo archivo Excel
    df_unificado.to_excel(archivo_salida, index=False, header=False)
    print(f"Archivo unificado guardado como: {archivo_salida}")

if __name__ == "__main__":
    ruta_archivos = '.'  # Ruta actual
    archivo_salida = 'felipe_rivera_lectura.xlsx'
    unir_archivos_excel(ruta_archivos, archivo_salida)
