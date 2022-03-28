import random

def drawMap(map):
    c = '▓░+. '
    c = ' ░'
    my_string = ''
    print(' ' + '_'*len(map[0]))
    for x in map:
        my_string += '|'
        for y in x:
            my_string += c[(int(y))]
        my_string += '|\n'
    my_string += '|' + '_'*len(map[0]) + '|'
    print(my_string)


class Map():
    def __init__(self, y, x):
        self.x, self.y = x, y
        self.div = 8
        if not x % 8 == 0 or not y % 8 == 0:
            raise ValueError("Map dimensions must be multiples of 8")
            exit()
        self.level = []
        self.layers = []
        _layers = 2
        min = 0
        inc = 1.0 / _layers
        for i in range(_layers):
            max = min + inc
            my_dict = {}
            my_dict['label'] = i
            my_dict['min'] = min
            my_dict['max'] = max
            my_dict['count'] = 0
            self.layers.append(my_dict)
            min += inc

    def get_slice(self, y, x, height, width):
        new_slice = []
        if y < 0 or y > self.y - height or x < 0 or x > self.x - width: return new_slice
        for i in range(y, y + height):
            new_slice.append([])
            for j in range(x, x + width):
                out = self.level[i][j]
                new_slice[i-y].append(out)
        return new_slice

    def get_slice_string(self, y, x, height, width):
        new_slice = []
        if y < 0 or y > self.y - height or x < 0 or x > self.x - width: return new_slice
        for i in range(y, y + height):
            my_string = ''
            for j in range(x, x + width):
                out = self.level[i][j]
                if out == 1:
                    my_string += '░'
                else:
                    my_string += ' '
            new_slice.append(my_string)
        return new_slice

    def add_floor(self, y):
        for i in range(self.y):
            for j in range(self.x):
                if i > self.y - y:
                    self.level[i][j] = 1
        # drawMap(self.level)


    def generate(self):
          base = []
          y = 2 * self.y
          # clear out layer_counter
          for l in self.layers:
              l['count'] = 0
          # seed
          for i in range(y):
              base.append([])
              for j in range(self.x):
                  base[i].append(random.random())
          for _ in range(3):
              # smooth
              for i in range(y):
                  for j in range(self.x):
                      if i > 1 and i < y-1 and j > 1 and j < self.x-1:
                          surrounds = 0
                          surrounds += base[i][j+1]
                          surrounds += base[i][j-1]
                          surrounds += base[i+1][j]
                          surrounds += base[i+1][j+1] #
                          surrounds += base[i+1][j-1] #
                          surrounds += base[i-1][j]
                          surrounds += base[i-1][j+1] #
                          surrounds += base[i-1][j-1] #
                          base[i][j] = base[i][j] + surrounds
                          base[i][j] /= 9
              # add blur
              for i in range(y):
                  for j in range(self.x):
                      bj = round(j/self.div)
                      bi = round(i/self.div)
                      base[i][j] = 0.8 * base[i][j] + 0.2 * base[bi][bj]
                      # base[i][j] = base[bi][bj]

              # normalise map
              max_val = 0
              min_val = 1000000000000
              for i in range(y):
                  for j in range(self.x):
                      if max_val < base[i][j]:
                          max_val = base[i][j]
                      if min_val > base[i][j]:
                          min_val = base[i][j]
              for i in range(y):
                  for j in range(self.x):
                      base[i][j] = (base[i][j] - min_val) / max_val

          #read map and then figure out layers:
          for i in range(y):
              for j in range(self.x):
                  for l in self.layers:
                      if base[i][j] > l['min'] and base[i][j] < l['max']:
                          l['count'] += 1
          my_arr = []
          for l in self.layers:
              my_arr.append(l['count'])
          my_arr.sort(reverse=True)
          for i, v in enumerate(my_arr):
              for l in self.layers:
                  if l['count'] == v:
                      l['label'] = i
          # remap map:
          for i in range(y):
              for j in range(self.x):
                  for l in self.layers:
                      if base[i][j] > l['min'] and base[i][j] < l['max']:
                          base[i][j] = int(l['label'])
          new_base = []
          for i, v in enumerate(base):
              if (i % 2 == 0):
                  new_base.append(v)
          self.level = new_base
