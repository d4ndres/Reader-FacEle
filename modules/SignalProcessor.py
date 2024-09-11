import numpy as np


class SignalProcessor:
  def projectiveIntegral(self, image, eje):
    if eje == 'x':
      return np.sum(image, axis=0)
    elif eje == 'y':
      return np.sum(image, axis=1)
    else:
      raise ValueError('El eje debe ser x o y')
    
  def normalization(self, signal):
    return (signal / np.max(signal), np.max(signal))
  
  def invNormalization(self, signal, maximo):
    return signal * maximo
  
  def indexesFromAtributeTable(self, iPy):
    tableIndex = []
    maxValue = max(iPy)
    minValue = min(iPy)
    for index, value in enumerate(iPy):
      if abs(value - maxValue) > 0.05 and abs(value - minValue) > 0.05:
        tableIndex.append(index)
    return tableIndex

  def selectRangeTable(self, listCandidates, threshold=100):
    rangeTable = []
    start = listCandidates[0]
    for i in range(1, len(listCandidates)):
      current_value = listCandidates[i]
      prev_value = listCandidates[i-1]
      
      if current_value - prev_value < threshold:
        continue
      else:
        rangeTable.append((start, prev_value))
        start = current_value

    rangeTable.append((start, listCandidates[-1]))

    #biggest range
    return max(rangeTable, key=lambda x: x[1] - x[0])


  def identifyMajorTransitions(self, signal, threshold=0.1, distanceTolerance=5, type='all'):
    # podria mejorar teniendo en cuenta solo cambios en subida, o solo en bajada, o una alternos subida -> bajada -> subida, all
    # default All

    listIndex = []
    for i in range(1, len(signal)):
      prev_value = signal[i-1]
      current_value = signal[i]
      max_value = max(prev_value, current_value)
      
      if max_value != 0 and abs(prev_value - current_value) / max_value >= threshold:
        if type == 'all':
          listIndex.append(i)
        elif type == 'down' and (prev_value - current_value) > 0 :
          listIndex.append(i)
        elif type == 'up' and (prev_value - current_value) < 0 :
          listIndex.append(i)

    # reduce by a distance tolerance
    reduce = []
    start = listIndex[0]
    for i in range(1, len(listIndex)):
      current_value = listIndex[i]
      prev_value = listIndex[i-1]
      
      if current_value - prev_value <= distanceTolerance:
        continue
      else:
        reduce.append(start)
        start = current_value

    reduce.append(start)
    return reduce