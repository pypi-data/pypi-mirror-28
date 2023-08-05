import numpy as np
from PyQt5.QtCore import (QPointF, QRectF)
from chroma.Chromosome import Chromosome
#from chroma.Utils import Utils as U

class Chromosomes:
    """
    Class manages a set of Chromosomes
    """
    def __init__(self):
        self.reset()
        self.index = 0

    def __len__(self):
        return len(self.chromosomes)

    def __iter__(self):
        return self

    def __next__(self):
        l = len(self.chromosomes)
        if self.index < l:
            c = self.chromosomes[self.index]
            self.index += 1

            return c
        else:
            self.index = 0
            raise StopIteration

    def __getitem__(self, item):
        return self.chromosomes[item]

    def __add__(self, other):
        if isinstance(other, Chromosomes):
            c = Chromosomes()
            c.chromosomes.extend(self.chromosomes)
            c.chromosomes.extend(other.chromosomes)
            return c
        if isinstance(other, Chromosome):
            c = Chromosomes()
            c.chromosomes.extend(self.chromosomes)
            c.chromosomes.append(other)
            return c

    def __radd__(self, other):
        self.__add__(other)

    def __iadd__(self, other):
        if isinstance(other, Chromosomes):
            self.chromosomes.extend(other.chromosomes)
            return self
        if isinstance(other, Chromosome):
            self.chromosomes.append(other)
            return self

    def get_chromosome_index(self, chr):
        l = [i for i,c in enumerate(self.chromosomes) if c is chr]

        if l:
            return l[0]


    def add_chromosome(self, chromosome):
        self.chromosomes.append(chromosome)

    def extend_chromosome(self, chromosomes):
        self.chromosomes.extend(chromosomes)

    def get_chromosome_count(self):
        return len(self.chromosomes)

    def get_chromosomes(self):
        return self.chromosomes[:]

    def remove_chromosome(self, chromosome):
        del self.chromosomes[self.chromosomes.index(chromosome)]

    def reset(self):
        self.chromosomes = []

    def get_chromosome_by_pos_QPointF(self, pos: QPointF):
        for chr in self.chromosomes:
            if chr.is_chromosome_at_QPointF(pos):
                 # chr.set_selection_point((int(pos.y()),int(pos.x())))
                 return chr

        return None

    def get_chromosome_by_pos_Point(self, pos: tuple):
        for chr in self.chromosomes:
            if chr.is_chromosome_at_Point(pos):
                # chr.set_selection_point(pos)
                return chr

    def get_karyo_chromosome_by_pos_QPointF(self, pos: QPointF):
        for chr in self.chromosomes:
            if chr.is_karyo_chromosome_at_QPointF(pos):

                 return chr

        return None

    def sort(self):
        self.chromosomes.sort(reverse=True)

    def get_chromosome_table(self, indices):
        if len(self.chromosomes) > 0:
            width = sum([c.Resolution[0] for c in self.chromosomes])
            height = max([c.Resolution[1] for c in self.chromosomes])

            table = np.zeros((height, width), dtype=np.uint8)
            x = 0

            for chr in self.chromosomes:
                chr.set_karyo_box(QRectF(QPointF(x, 0), QPointF(x + chr.Resolution[0], height)))
                table[0:chr.Resolution[1], x: x + chr.Resolution[0]] = chr.get_bit_mask_image(indices)
                x += chr.Resolution[0]

            return table

    def exchange_chromosome(self, index_a, index_b):
        self.chromosomes[index_a], self.chromosomes[index_b] = self.chromosomes[index_b], self.chromosomes[index_a]


if __name__ == "__main__":
    img = np.zeros((500, 500), dtype=np.uint8)

    img0 = np.zeros((500, 500), dtype=np.uint8)
    img0[0:2, 1:5] = 255  # (255,255,255)
    #print(img0)

    img[140:170, 5:30] = 255  # (255,255,255)
    img[450:470, 450:480] = 255  # (255,255,255)
    img[200:270, 200:270] = 255  # (255,255,255)
    img[400:480, 400:420] = 255

    # pixel_coord = [np.where(img > 0)]

    img[150:160, 10:20] = 0  # (255,255,255)

    # pixel_coord.append(np.where(img > 0))

    img2 = np.zeros((500, 500), dtype=np.uint8)
    img2[450:470, 450:480] = 255  # (255,255,255)
    img2[200:270, 200:270] = 255
    img2[450:460, 410:420] = 0
    img2[450:460, 410:420] = 0
    img2[50:55, 40:42] = 255

    # pixel_coord.append(np.where(img2 > 0))

    # c = Chromosome(pixel_coord, (255, 0, 0),(500, 500))

    from Cube import Cube
    c = Cube(np.stack([img, img2]))
    c1 = Chromosome(c, c, c, c, [10,20])
    c2 = Chromosome(c, c, c, c, [10,20])
    c3 = Chromosome(c, c, c, c, [10,20])

    C = Chromosomes()

    C += c1

    C += c2

    # Check iterator
    print(next(C))
    print(next(C))
    print(list(C))
    print(list(C))
    print(list(C))