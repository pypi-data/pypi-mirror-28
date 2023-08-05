import cv2
from PyQt5.QtCore import (QPointF, QRectF)
from math import ceil
import numpy as np
import hashlib
from chroma.Utils import Utils as U
from chroma.Cube import Cube


class Chromosome:
    def __init__(self, coords, orig_cube, threshold_cube, minus_cube, plus_cube, thresholds, color, parent=None):
        # Chromosome coordinates
        self.coords = coords

        # Orig. Images Cube
        self.cube_orig = orig_cube

        # OTSU mask Cube
        self.cube_mask_otsu = threshold_cube
        self.cube_mask_otsu_ret = thresholds

        # Manual plus mask Cube
        self.cube_mask_plus = plus_cube

        # Manual minus mask Cube
        self.cube_mask_minus = minus_cube

        # Representing color in selection window
        self.color = color

        # Rotation and shift matrix
        self.M = None

        # Rotation and shift shape
        self.Resolution = None

        # Link to parent chromosome (not rotatated)
        self.parent = parent

        # Calculates unique hash of chromosome - Use hashlib because hash() differs between sessions and loaded projects fail
        m = hashlib.md5()
        m.update(self.cube_orig.get_layer(0)[self.coords].tobytes())
        self._hash = int.from_bytes(m.digest(), byteorder='little')

        # Positon box in karyotype
        self.karyo_box = None

    def __hash__(self):
        return self._hash

    def __lt__(self, other):
        return self.get_size() < other.get_size()

    def __le__(self, other):
        return self.get_size() <= other.get_size()

    def __gt__(self, other):
        return self.get_size() > other.get_size()

    def __ge__(self, other):
        return self.get_size() >= other.get_size()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return self.__hash__() != other.__hash__()

    def __str__(self):
        return str(self.get_image(0))

    def __iadd__(self, other):
        if isinstance(other, Chromosome):
            self.coords = (np.append(self.coords[0], other.coords[0]), np.append(self.coords[1], other.coords[1]))

            self.cube_orig.merge_cube_with(other.cube_orig)
            self.cube_mask_otsu.merge_cube_with(other.cube_mask_otsu)
            self.cube_mask_minus.merge_cube_with(other.cube_mask_minus)
            self.cube_mask_plus.merge_cube_with(other.cube_mask_plus)

            self._hash = hash(self.cube_orig.get_layer(0)[self.coords].tobytes())

        return self

    def merge_masks(self, channel=0):
        return (self.cube_mask_otsu.cube[:, :, channel] & self.cube_mask_minus.cube[:, :, channel]) | \
               self.cube_mask_plus.cube[:, :, channel]

    def get_bit_mask_image(self, indices):
        img = np.zeros(self.cube_orig.get_layer(0).shape, dtype=np.uint8)

        for channel in indices: #range(self.get_channel_count()):
            img[self.merge_masks(channel) > 0] += 2 ** channel

        img[self.merge_masks(0) == 0] = 0

        return img

    def is_chromosome_at_QPointF(self, pos: QPointF):
        if (int(pos.y()), int(pos.x())) in zip(*np.where(self.cube_orig.get_layer(0))):
            return True
        else:
            return False

    def is_chromosome_at_Point(self, pos: tuple):
        if self.cube_orig.get_layer(0)[pos[0], pos[1]]:
            return True
        else:
            return False

    def is_karyo_chromosome_at_QPointF(self, pos: QPointF):
        if self.karyo_box.contains(pos):
            return True
        else:
            return False


    def get_size(self):
        return len(self.coords[0])

    def get_channel_count(self):
        return self.cube_orig.num_channels

    def get_image(self, channel):
        return self.cube_orig.get_layer(channel)

    def get_color_image(self, channel, color):
        img = self.cube_orig.get_layer(channel)

        img2 = np.zeros(img.shape + (4,), dtype=np.uint8)

        img2[img > 0] = color

        return img2

    def get_orig_image(self, channel):
        img = self.cube_orig.get_layer(channel)

        img2 = np.zeros(img.shape, dtype=np.uint8)

        img2[img > 0] = 255

        return img2

    def get_mask_otsu(self, channel):
        return self.cube_mask_otsu.get_layer(channel)

    def get_mask_plus(self, channel):
        return self.cube_mask_plus.get_layer(channel)

    def get_mask_minus(self, channel):
        return self.cube_mask_minus.get_layer(channel)


    def get_border(self, thickness=2, only_border_highlight=True):
        img = U.booleanArray2byte(self.merge_masks(0))

        if only_border_highlight:
            img_out = U.get_empty_uint8_mask(img.shape, 0)
            im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            return np.where(
            cv2.drawContours(img_out, contours, -1, 255, thickness))  # -1 all contours , color, border thickness = 2
        else:
            return np.where(img)

    def clear_manual_masks(self, index):
        self.cube_mask_minus.get_layer(index)[:, :] = True
        self.cube_mask_plus.get_layer(index)[:, :] = False
    # TODO check for speed
    # def get_border2(self, img):  # TODO refactor to get_border() because its faster
    #     # image = self.cube_mask_otsu.get_layer(0)
    #     #img = np.zeros(mask.shape, dtype=np.int8)
    #
    #     #img2 = np.zeros(self.images[0].shape, dtype=np.int8)
    #
    #     #img[image > 0] = 1
    #
    #     img = np.vstack([np.zeros((1, img.shape[1]), dtype=np.int8), img])
    #     img = np.hstack([np.zeros((img.shape[0] + 1, 1), dtype=np.int8), img])
    #
    #     border_y = np.diff(img, axis=0)
    #     border_x = np.diff(img, axis=1)
    #
    #     # Calculate border - 4 junctions
    #     index_y_left = np.where(border_y > 0)
    #     index_y_right = np.where(border_y < 0)
    #     index_x_left = np.where(border_x > 0)
    #     index_x_right = np.where(border_x < 0)
    #
    #     index = (np.concatenate([index_y_left[0], index_y_right[0] - 1, index_x_left[0] - 1, index_x_right[0] - 1]),
    #              np.concatenate([index_y_left[1] - 1, index_y_right[1] - 1, index_x_left[1], index_x_right[1] - 1]))
    #
    #     return index

    def calculate_matrix(self):
        """
        Calculate rotation and shift Matrix. Returns shape of the new cropped rotated image
        :param matrix:
        :return: tuple
        """
        # Get border coordinates
        coords_border = self.get_border(thickness=1)

        # Get convex hull
        hull = cv2.convexHull(np.dstack((coords_border[1], coords_border[0])))

        # Get minimal bounding box
        rect = cv2.minAreaRect(hull)

        # Get height of chromosome
        diameter = ceil(max(rect[1]))

        # Get width of chromosome
        width = ceil(min(rect[1]))

        # Get offset from rect-img to rect-img_rot
        offset = (rect[0][1] - diameter // 2 - 4, rect[0][0] - width // 2 - 4)

        # Create rotating matrix
        # Switch 90° if chromosome is landscape oriented
        if rect[1][0] > rect[1][1]:
            self.M = cv2.getRotationMatrix2D(rect[0], rect[2] + 90, 1)
        else:
            self.M = cv2.getRotationMatrix2D(rect[0], rect[2], 1)

        # Offset translation
        self.M[0, 2] -= offset[1]   # third column of matrix holds translation, which takes effect after rotation.
        self.M[1, 2] -= offset[0]

        self.Resolution = (width + 8, diameter + 8)

    def get_cubes(self):
        return [self.cube_mask_otsu, self.cube_mask_minus, self.cube_mask_plus]

    def get_numpy_in_chr_color(self, channel, np_image):
        color_img = np.zeros(np_image.shape + (4,), dtype=np.uint8)
        #img = np.zeros(np_image.shape + (4,), dtype=np.uint8)

        color_img[np_image > 0] = self.color
        return  color_img

    def set_karyo_box(self, rect: QRectF):
        self.karyo_box = rect

    def get_rotated_chromosome(self):
        if self.M is None:
            self.calculate_matrix()

        orig_images = []
        otsu_masks = []
        plus_masks = []
        minus_masks = []

        for channel in range(self.get_channel_count()):
            img = self.cube_orig.get_layer(channel)
            otsu = U.booleanArray2byte(self.cube_mask_otsu.get_layer(channel))
            plus = U.booleanArray2byte(self.cube_mask_plus.get_layer(channel))
            minus = U.booleanArray2byte(self.cube_mask_minus.get_layer(channel))

            orig_images.append(cv2.warpAffine(img, self.M, self.Resolution))
            otsu_masks.append(U.byteArray2bool(cv2.warpAffine(otsu, self.M, self.Resolution)))
            plus_masks.append(U.byteArray2bool(cv2.warpAffine(plus, self.M, self.Resolution)))
            minus_masks.append(U.byteArray2bool(cv2.warpAffine(minus, self.M, self.Resolution)))

        chr = Chromosome(np.where(orig_images[0]), Cube(orig_images), Cube(otsu_masks), Cube(minus_masks), Cube(plus_masks), self.cube_mask_otsu_ret, self.color, parent=self)
        chr.Resolution = self.Resolution

        return chr

    def get_rot180_chromosome(self):

        orig_images = []
        otsu_masks = []
        plus_masks = []
        minus_masks = []

        for channel in range(self.get_channel_count()):
            orig_images.append(np.rot90(self.cube_orig.get_layer(channel), 2))
            otsu_masks.append(np.rot90(self.cube_mask_otsu.get_layer(channel), 2))
            plus_masks.append(np.rot90(self.cube_mask_plus.get_layer(channel), 2))
            minus_masks.append(np.rot90(self.cube_mask_minus.get_layer(channel), 2))

        # Chromosome coordinates
        self.coords = np.where(orig_images[0])

        # Orig. Images Cube
        self.cube_orig = Cube(orig_images)

        # OTSU mask Cube
        self.cube_mask_otsu = Cube(otsu_masks)
        self.cube_mask_otsu_ret = self.cube_mask_otsu_ret

        # Manual plus mask Cube
        self.cube_mask_plus = Cube(plus_masks)

        # Manual minus mask Cube
        self.cube_mask_minus = Cube(minus_masks)

        # Calculates unique hash of chromosome
        self._hash = hash(self.cube_orig.get_layer(0)[self.coords].tobytes())

        return self

    # def get_rotated_color_image(self, channel, color):
    #     img = cv2.warpAffine(self.get_image(channel), self.M, self.Resolution)
    #     img2 = np.zeros(img.shape + (4,), dtype=np.uint8)
    #     img2[img > 0] = color
    #
    #     return img2

if __name__ == "__main__":
    img0 = np.zeros((10, 10), dtype=np.uint8)
    img1 = np.zeros((10, 10), dtype=np.uint8)
    img2 = np.zeros((10, 10), dtype=np.uint8)
    img3 = np.zeros((10, 10), dtype=np.uint8)

    img1[1:3, 1:5] = 255  # (255,255,255)
    img1[5:8, 5:8] = 125
    img2[1:2, 2:4] = 255  # (255,255,255)
    img3[4:7, 8:9] = 255  # (255,255,255)
    img3[1:4, 2:3] = 255  # (255,255,255)
    # print(img0)

    from Cube import Cube
    c = Cube(np.stack([img1, img2, img3]))
    c1 = Chromosome(np.where(img1 == 125), c, c, c, c, [10, 20])

    print(hash(c1))

    print(c1.is_chromosome_at_QPointF(QPointF(449.9,452)))

    img0[c1.get_border()] = 255
    print(img0)

    img0[c1.get_border2()] = 100
    print(img0)

    print(c1.get_rotated_image(0))
