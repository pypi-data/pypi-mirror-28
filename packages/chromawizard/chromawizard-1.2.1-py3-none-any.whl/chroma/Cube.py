import numpy as np

import chroma.Error as Error

class Cube:
    """
    A cube instance hold the image or mask information for all channels
    """
    def __init__(self, np_images):
        self.shape = np_images[0].shape
        self.num_channels = len(np_images)

        self.cube = np.dstack(np_images)

    def get_bit_image(self):
        """
        Reduce cube to the bit sum. Every Layer adds 2^n to the image. Starting from n=0
        :return: 2D array - dtype=np.uint8
        """
        img = np.zeros(self.shape, dtype=np.uint8)

        for i in range(self.num_channels + 1):
            img[self.cube[:, :, i] > 0] += 2 ** i

        return img

    def add_layer(self, np_img=None, val=False):
        if np_img is None:
            np_img = np.full_like(self.cube[:, :, 0], val)

        self.cube = np.dstack((self.cube, np_img))
        self.num_channels += 1

    def set_layer(self, np_img, channel):
        self.cube[:, :, channel] = np_img

    def update_layer(self, np_img, index):
        self.cube[:, :, index] = np_img

    def get_overlay(self, indices):
        return (np.add.reduce(self.cube[:, :, indices], 2) / len(indices)).astype(np.uint8)

    def get_layer(self, index):
        return self.cube[:, :, index]

    def get_copy(self, filter=None):
        images = []
        for i in range(self.cube.shape[2]):
            images.append(self.cube[:, :, i].copy())

            if filter:
                mask = np.ones(images[0].shape, dtype=np.bool)
                mask[filter] = False

                for img in images:
                    img[mask] = 0

        return Cube(images)

    def get_count_layers(self):
        return self.cube.shape[2]

    def merge_cube_with(self, cube):
        """
        Combine to areas (Merge chromosomes)
        :param cube:
        :return:
        """
        self.cube |= cube.cube


if __name__ == "__main__":
    n = np.zeros((5,7), dtype=np.uint8) # np.bool
    n[2:4,2:4] = 100

    m = n .copy()
    m[3:5,3:6] = 200
    m[0,:] = 255

    n[1, :] = 1

    l = [n, m, None, None]
    c = Cube(l)

    print(c.cube)
    print(c.get_bit_image())

    try:
        Cube([n])
    except Error.CubeLayerError as e:
        print(e)

    c.add_layer(n)

    print(c.cube)
    print(c.get_bit_image())
