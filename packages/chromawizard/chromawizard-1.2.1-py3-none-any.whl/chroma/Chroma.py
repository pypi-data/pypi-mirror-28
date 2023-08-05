import numpy as np
import cv2

from chroma.Utils import PointArray, Colors as C, Utils as U
from chroma.Cube import Cube
import chroma.Error as Error
from chroma.Chromosomes import Chromosomes
from chroma.Chromosome import Chromosome
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt

import pickle


class Chroma:
    def __init__(self, manager):
        """
        Initiate Chroma
        :param gui:
        :return:
        """
        self.m = manager

        self.logger = self.m.logger

        self.logger.debug("__init__ Chroma")

        # Initate Colors
        C.set_colors(self.m.config.config.segment_colors)
        self.logger.debug("Set colors for selection window: {}".format(self.m.config.config.segment_colors))

        # How many color channels available
        self.channel_count = len(self.m.config.config.channel_names)

        # How many channels currently loaded
        self.num_channels_loaded = 0

        # Original Images - DAPI + Channels (Color)
        #self.original_images = [None] * self.channel_count

        self.img_shape = None

        # Orig. Images Cube
        self.cube_orig = None

        # OTSU mask Cube
        self.cube_mask_otsu = None
        self.cube_mask_otsu_ret = []
        self.cube_mask_noise = []

        # Manual plus mask Cube
        self.cube_mask_plus = None

        # Manual minus mask Cube
        self.cube_mask_minus = None

        # Chromosomes
        self.chromosomes = Chromosomes()
        self.rot_chromosomes = Chromosomes()

        # Manual selection mask (yellow lines)
        self.np_b_mask_select = None  # numpy bool

        # Array for saving line
        #self.selection_array = []
        self.point_array = PointArray()

        self.np_selection = None

    def save(self, filename):
        """
        Pickle (save) project to file
        :param filename:
        :return:
        """
        data = {'point_array': self.point_array,
                'chromosomes': self.chromosomes,
                'rot_chromosomes': self.rot_chromosomes,
                'selected_chromosomes': self.m.selected_chromosomes,
                'cube_orig': self.cube_orig,
                'cube_mask_otsu': self.cube_mask_otsu,
                'cube_mask_plus': self.cube_mask_plus,
                'cube_mask_minus': self.cube_mask_minus,
                'thresholds_mask': self.cube_mask_otsu_ret,
                'thresholds_noise': self.cube_mask_noise,
                'b_mask_select': self.np_b_mask_select,
                'config': self.m.config.config.__dict__,
                'state': self.m.state
                 }
        try:
            with open(filename, 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

            self.m.config.save(filename + ".conf.json")

        except Exception as e:
            raise e

    def load(self, filename):
        """
        Unpickle (load) project
        :param filename:
        :return:
        """
        try:
            with open(filename, 'rb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                d = pickle.load(f)

            self.m.config = self.m.config.read_create_config(filename + ".conf.json")

        except Exception as e:
            raise e

        return d

    def getThresholdValue(self, channel_nr):
        return self.cube_mask_otsu_ret[channel_nr]

    def getNoiseValue(self, channel_nr):
        return self.cube_mask_noise[channel_nr]

    def get_color_img(self, np_img, dapi=True):
        """
        Takes a uint8 img with coded pixels (2**index) and convereted it to channel colored [*,*,3] numpy image for
        presentation
        :param npimg: uint8 shape [*,*]
        :return: colored numpy uint8 image with shape [*,*,3]
        """
        col_mask = np.zeros((*np_img.shape, 3), dtype=np.uint8)

        col_mask[np_img > 1] = C.hex_to_rgb(self.m.config.config.color_for_not_defined)

        m_chromosomes = [(str(m_chr['channel']), m_chr['color']) for m_chr in self.m.config.config.chromosomes]

        for key, color in m_chromosomes:
            b = int(key, 2)

            # Have to remove the DAPI channel if selected because it is never in any channel combination
            if b != 1 and dapi:
                b += 1  # Add 1 to binary instead of subtracting 1 from each pixel in npimg

            col_mask[np_img == b] = C.hex_to_rgb(color)

        return col_mask

    def load_channel(self, np_img):
        """
        Load new channel
        :return: (int, Cube) - last added index, orig. images Cube
        """
        # Is image
        try:
            # Return -1 if more channels as channel_count are loaded
            if self.num_channels_loaded >= self.channel_count:
                return -1, self.cube_orig

            if self.num_channels_loaded > 0:
                shape0 = self.cube_orig.get_layer(0).shape
                if shape0 != np_img.shape:
                    self.logger.error("Image has different size than the DAPI file")
                    raise Error.WrongImageShapeError(np_img.shape, shape0)
                else:
                    self.cube_orig.add_layer(np_img)
                    self.cube_mask_otsu.add_layer(None)
                    self.cube_mask_plus.add_layer(None)
                    self.cube_mask_minus.add_layer(None, True)
            else:
                self.init_zero(np_img)

            # Add noise value
            self.cube_mask_noise.append(0)
            self.cube_mask_otsu_ret.append(0)
            self.calc_otsu(self.num_channels_loaded)

            # Update loaded channels nummer
            self.num_channels_loaded += 1

        except Error.WrongImageShapeError:
            raise
        except:
            raise Error.ImageError()

        return self.num_channels_loaded - 1, self.cube_orig

    def init_zero(self, np_img):
        """
        Initiate all variables before the first channel could be loaded
        :param np_img:
        :return:
        """
        # Initialize Cubes
        self.cube_orig = Cube([np_img])

        # Set shape of first loaded image
        self.img_shape = np_img.shape

        # Create otsu/threshold cube
        self.cube_mask_otsu = Cube([np.zeros_like(np_img, dtype=np.bool)])

        # Create manual mask cubes
        self.cube_mask_plus  = Cube([np.zeros_like(np_img, dtype=np.bool)])
        self.cube_mask_minus = Cube([np.ones_like(np_img, dtype=np.bool)])

        # Initialize selection lines mask
        self.np_b_mask_select = np.zeros_like(np_img, dtype=np.bool)

        # Initialize selection image
        self.np_selection = U.get_empty_color_image_3(self.img_shape)

        self.cube_mask_noise = []
        self.cube_mask_otsu_ret = []

        self.chr_last_left_click = []
        self.chr_last_right_click = []
        self.rects = []

    def calc_otsu(self, channel):
        # Otsu's thresholding
        ret, th = cv2.threshold(self.cube_orig.get_layer(channel), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.cube_mask_otsu_ret[channel] = ret
        self.cube_mask_otsu.set_layer(th > 0, channel)

    def calc_threshold(self, cube_orig, cube_otsu, cube_otsu_ret, channel, threshold):
        ret, th = cv2.threshold(cube_orig.get_layer(channel), threshold, 255, cv2.THRESH_BINARY)
        cube_otsu_ret[channel] = ret
        cube_otsu.set_layer(th > 0, channel)

    def get_masking(self, indices, cubes, filter_artifacts=True):
        """
        Sum up all masks and return masks for the selection ZW and the mask ZW
        :param indices:
        :return: iM0: Mask for selection ZW, iRes: Combined mask for masking ZW

        Combined mask is depending on indicies
        """
        iRes = U.get_empty_uint8_mask(cubes[0].shape, 0)
        min_pixel_size = self.m.config.config.minimum_pixel_size

        M0 = self.merge_masks(cubes, 0)

        # Get Components from M
        ret, markers = cv2.connectedComponents(U.booleanArray2byte(M0))

        # For selection window without small artifacts
        iM0 = U.get_empty_uint8_mask(cubes[0].shape, 0)
        # iM0small = self.get_empty_uint8_mask(0)

        # Needed for the speedup of threshold/noise Sliders
        # Looping over all markers takes to long
        frequency = {key: 0 for key in range(ret)}

        # Get frequency of segments (very fast)
        for x in np.nditer(markers):
            frequency[int(x)] += 1

        inlist = []

        # Divide in artifacts and chromosomes
        if filter_artifacts:
            [inlist.append(i) for i in frequency if i != 0 and frequency[i] >= min_pixel_size]
        else:
            [inlist.append(i) for i in frequency if i != 0]

        # Create in- / out- masks iM0 is for selection window without artifacts
        iM0[np.in1d(markers, inlist).reshape(cubes[0].shape)] = 1

        # Get value from noise slider
        noise_value = self.m.gui.sliders_noise[0].value()

        # iM0 finished for selecting window
        for i in range(noise_value):
            iM0 = cv2.bilateralFilter(iM0, 5, 75, 75)

        # Now for all channels
        for index in indices: # TODO: check if index 0 also has to run
            # Create Channel Mask
            M = self.merge_masks(cubes, index)

            iM = U.booleanArray2byte(M)

            # Get value from noise slider
            noise_value = self.m.gui.sliders_noise[index].value()

            for i in range(noise_value):
                iM = cv2.bilateralFilter(iM, 5, 75, 75)

            # Subtract DAPI mask M0
            M = U.byteArray2bool(iM)

            # Calculate Mask
            iRes[M & iM0 > 0] += 2 ** index

        # M0 = noised selection mask without small chromosomes | iRes masking matrix with small chromosomes
        return iM0, iRes

    def update_chromosome_colors(self):
        # Merge compound chromosomes
        groups = self.point_array.get_chromosome_groups(self.chromosomes)

        for group in groups:
            if len(group) > 1:
                c = groups[group][0]
                # Remove not merged chromosome
                self.chromosomes.remove_chromosome(groups[group][0])

                for chr in groups[group][1:]:
                    c += chr
                    self.chromosomes.remove_chromosome(chr)

                self.chromosomes.add_chromosome(c)

                self.np_selection[c.coords] = chr.color



    def get_selecting(self, iM0):
        """
        Get colored numpy array for the selection window
        :param iM0:
        :return:
        """
        # Get Components from noise reducted iM0
        ret, markers = cv2.connectedComponents(iM0, cv2.CV_16U)

        # Reset color table to get always same color for chromosomes
        C.reset()

        # Reset selection image
        self.np_selection[:] = [0, 0, 0]

        # Empty old chromosomes
        self.chromosomes.reset()

        for mark in range(1, markers.max() + 1):
            color = C.get_color()

            pixels = np.where(markers == mark)
            self.np_selection[pixels] = color
            # Create chromosome
            chr = Chromosome(pixels, self.cube_orig.get_copy(filter=pixels),
                             self.cube_mask_otsu.get_copy(filter=pixels), self.cube_mask_minus.get_copy(filter=pixels),
                             self.cube_mask_plus.get_copy(filter=pixels), self.cube_mask_otsu_ret.copy(), color)

            # Add chromosome to chromosomes
            self.chromosomes += chr

        self.update_chromosome_colors()


    def process_selection_lines(self):
        """
        Convert selection lines to a boolean numpy array
        :return:
        """
        # Reset mask
        self.np_b_mask_select[:] = False

        # Draws selection line
        for item in self.point_array.get_type("line"):
            l_path = len(item['point'])
            if l_path > 1:
                for i in range(l_path - 1):
                    rr, cc = U.line_aa(*item['point'][i], *item['point'][i + 1])
                    self.np_b_mask_select[rr, cc] = True

        return self.np_b_mask_select

    def clear_manual_mask(self, cb_states):
        for index in cb_states:
            self.cube_mask_minus.get_layer(index)[:, :] = True
            self.cube_mask_plus.get_layer(index)[:, :] = False

    def remove_pos(self, pos):
        self.point_array.remove_last_group()

    def merge_chromosomes(self, pos):
        if self.m.merging_enabled:
            self.point_array.add_point(pos, "chr", last=True, hash=hash(self.chromosomes.get_chromosome_by_pos_Point(pos)))
        else:
            self.m.merging_enabled = True
            self.point_array.add_point(pos, "chr", last=False, hash=hash(self.chromosomes.get_chromosome_by_pos_Point(pos)))

    def merge_masks(self, cubes:list, channel=0):
        return (cubes[0].cube[:, :, channel] & cubes[1].cube[:, :, channel]) | cubes[2].cube[:, :, channel]

    def merge_chromosome_masks(self, chr, channel=0):
        return (chr.cube_mask_otsu.cube[:, :, channel] & chr.cube_mask_minus.cube[:, :, channel]) | \
               chr.cube_mask_plus.cube[:, :, channel]

    def save_karyotype(self, ZW, filename):
        # Get Image
        pix = QPixmap(ZW.scene.width, ZW.scene.height)
        painter = QPainter(pix)
        ZW.scene.render(painter)
        pix.save("capture.jpg", "JPG")