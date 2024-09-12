import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import mplcursors as tooltip
from difflib import SequenceMatcher

def diffString( s1, s2):
  return SequenceMatcher(None, s1, s2).ratio() 

def showImage(img, name='img'):
	cv2.imshow(name, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def graficarProyeccion(proyeccion, eje='any'):
  plt.plot(proyeccion)
  plt.title(f'Proyección {eje}')
  plt.show()

def redLineOverGraphX( listIndex, color='r'):
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


def wordsInImage(image, words, hover=True):
    fig, ax = plt.subplots()
    ax.imshow(image)

    if hover:
        # Crear una anotación que se actualizará con cada hover
        annotation = ax.annotate("", xy=(0,0), xytext=(20,20),
                                  textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
                                  arrowprops=dict(arrowstyle="->"))
        annotation.set_visible(False)

    rects = []
    for word in words:
        rect = patches.Rectangle((word["x"], word["y"]), word["w"], word["h"], linewidth=2, edgecolor='b', facecolor='blue', alpha=0.5)
        ax.add_patch(rect)
        rects.append((rect, word["label"]))

        if not hover:
            # Agregar el texto en color rojo dentro del rectángulo si hover es False
            ax.text(word["x"] + word["w"]/2, word["y"] + word["h"]/2, word["label"], 
                    color='red', ha='center', va='center', fontsize=12)

    if hover:
        def update_annotation(ind):
            # Obtener el rectángulo y el texto correspondiente
            rect, label = rects[ind["ind"][0]]
            annotation.xy = (rect.get_x(), rect.get_y())
            annotation.set_text(label)
            annotation.get_bbox_patch().set_facecolor('y')
            annotation.set_visible(True)
            fig.canvas.draw_idle()

        def hover_event(event):
            # Comprobar si el cursor está sobre un rectángulo
            vis = annotation.get_visible()
            if event.inaxes == ax:
                for ind, (rect, label) in enumerate(rects):
                    contains, _ = rect.contains(event)
                    if contains:
                        update_annotation({"ind": [ind]})
                        return
            if vis:
                annotation.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover_event)

    ax.axis('off')
    plt.show()

def distancia_levenshtein(a, b):
    if len(a) > len(b):
        a, b = b, a

    distances = range(len(a) + 1)
    for i2, c2 in enumerate(b):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(a):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def similaridad(a, b):
    if len(a) < len(b):
        a, b = b, a
    return 1 - distancia_levenshtein(a, b) / len(a)