import os
import cv2 # http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QFileDialog, QDialog, QColorDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel)
from PyQt5.QtGui import (QColor, QPixmap)
import numpy as np
from math import sqrt
import time
from functools import partial
import chroma.Settings as S

_t = QtCore.QCoreApplication.translate

class AboutDlg(QDialog):
    def __init__(self, manager, *qdialog):
        super().__init__(*qdialog)

        self.m = manager

        Level1_verticalLayout = QVBoxLayout(self)

        image_path_logo = os.path.join(self.m.app_path, "images", "logo.png")
        image_path_acib = os.path.join(self.m.app_path, "images", "acib.png")

        image_logo = QPixmap(image_path_logo)
        image_logo_Label = QLabel()
        image_logo_Label.setPixmap(image_logo)

        image_acib = QPixmap(image_path_acib)
        image_acib_Label = QLabel()
        image_acib_Label.setPixmap(image_acib)

        Level1_verticalLayout.addWidget(image_logo_Label)
        Level1_verticalLayout.addSpacing(30)
        Level1_verticalLayout.addWidget(QLabel("Author: {} - {}".format(S.__author__, S.__email__)))
        Level1_verticalLayout.addWidget(QLabel("Version: {}".format(S.__version__)))
        Level1_verticalLayout.addWidget(QLabel("Build: {}".format(S.__updated__)))
        Level1_verticalLayout.addSpacing(30)
        Level1_verticalLayout.addWidget(QLabel("Copyright: Acib GmbH"))
        Level1_verticalLayout.addWidget(image_acib_Label)

    def closeEvent(self, event):
        # Reset Utils.dlg
        Utils.dlg_about = None


class LegendDlg(QDialog):
    def __init__(self, config, *qdialog):
        super().__init__(*qdialog)

        # Get chromosome names and color from config.json
        chromosomes_meta = config.config.chromosomes

        # Sort them by 'order'
        chromosomes_meta.sort(key=lambda obj: obj['order'])

        Level1_verticalLayout = QVBoxLayout(self)

        max_label_size = 0
        labels = []

        for m_chr in chromosomes_meta:
            Level2_horizontalLayout = QHBoxLayout()

            label = QLabel(m_chr['name'])
            label_width = label.fontMetrics().boundingRect(label.text()).width()

            max_label_size = label_width if label_width > max_label_size else max_label_size

            btn = QPushButton()
            btn.setStyleSheet("background-color: {};\nborder:none;\nborder-radius: 6px;".format(m_chr['color']))
            btn.clicked.connect(partial(self.color_pick, btn, m_chr, config))

            Level2_horizontalLayout.addWidget(btn)
            Level2_horizontalLayout.addSpacing(30)
            Level2_horizontalLayout.addWidget(label)

            Level1_verticalLayout.addLayout(Level2_horizontalLayout)

            labels.append(label)

        # Add not defined color button
        Level2_horizontalLayout = QHBoxLayout()
        btn = QPushButton()
        btn.setStyleSheet("background-color: {};\nborder:none;\nborder-radius: 6px;".format(config.config.color_for_not_defined))
        btn.clicked.connect(partial(self.color_pick, btn, None, config))

        label = QLabel(_t("Utils", "Not defined"))
        label_width = label.fontMetrics().boundingRect(label.text()).width()
        max_label_size = label_width if label_width > max_label_size else max_label_size
        labels.append(label)

        Level2_horizontalLayout.addWidget(btn)
        Level2_horizontalLayout.addSpacing(30)
        Level2_horizontalLayout.addWidget(label)

        Level1_verticalLayout.addLayout(Level2_horizontalLayout)

        # Get max. label width
        for label in labels:
            label.setFixedWidth(max_label_size + 1)


        btn_close = QPushButton(_t("Utils", "Close"), self)
        btn_close.clicked.connect(self.close)

        Level1_verticalLayout.addWidget(btn_close)

        self.setLayout(Level1_verticalLayout)

    def closeEvent(self, event):
        # Reset Utils.dlg
        Utils.dlg = None

    def color_pick(self, btn, m_chr, config):
        dlg = QColorDialog(self)

        if m_chr:
            dlg.setCustomColor(0, QColor(m_chr['color']))

            # Open Color-Picker Dialog
            color = dlg.getColor(QColor(m_chr['color']), self)
        else:
            not_def_color = config.config.color_for_not_defined
            dlg.setCustomColor(0, QColor(not_def_color))

            # Open Color-Picker Dialog
            color = dlg.getColor(QColor(not_def_color), self)

        if color.isValid():
            if m_chr:
                index = [index for index, chr in enumerate(config.config.chromosomes) if chr['channel'] == m_chr['channel']][0]
                config.config.chromosomes[index]['color'] = color.name()
            else:
                config.config.color_for_not_defined = color.name()

            # Update color in legend
            btn.setStyleSheet("background-color: {};\nborder:none;\nborder-radius: 6px;".format(color.name()))

            # Save updated config
            config.update()


class Utils:
    dlg = None
    dlg_about = None
    @staticmethod
    def numpy_to_file(np_image, filename):
        # Convert RGB to cv BGR
        np_image[:, :, 0], np_image[:, :, 2] = np_image[:, :, 2], np_image[:, :, 0].copy()

        cv2.imwrite(filename, np_image)

    @staticmethod
    def open_legend_dialog(parent, config):
        if Utils.dlg is None:
            # Inform WM-Manager to be always on top
            Utils.dlg = LegendDlg(config, parent, QtCore.Qt.WindowStaysOnTopHint)
            #dlg.resize(200, 500)
            Utils.dlg.setWindowTitle(_t("Utils", "Chromosome Legend"))
            # Make dialog modeless (non-modal)
            Utils.dlg.show()
        else:
            Utils.dlg.setFocus()

    @staticmethod
    def open_about_dialog(parent, manager):
        if Utils.dlg_about is None:
            # Inform WM-Manager to be always on top
            Utils.dlg_about = AboutDlg(manager, parent, QtCore.Qt.WindowStaysOnTopHint)
            # dlg.resize(200, 500)
            Utils.dlg_about.setWindowTitle(_t("Utils", "About"))
            # Make dialog modeless (non-modal)
            Utils.dlg_about.show()
        else:
            Utils.dlg_about.setFocus()

    @staticmethod
    # Open a open file dialog for the DAPI file
    def open_image_dialog(parent, msg, last_image_folder, name_filter):
        dlg = QFileDialog(parent, caption=msg)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setDirectory(os.path.expanduser(last_image_folder))
        dlg.setNameFilter(name_filter)
        dlg.setViewMode(QFileDialog.Detail)

        if dlg.exec_():
            filename = dlg.selectedFiles()
            dlg.close()

            return filename[0]
        else:
            return None

    @staticmethod
    def get_save_as_dialog(parent, msg, last_project_folder, filename, filter="ChromaWizard Project (*.cpro);;All Files (*)"):
        fileName, _ = QFileDialog.getSaveFileName(parent, msg,
                                                  os.path.join(os.path.expanduser(last_project_folder), filename),
                                                  filter)
        return fileName

    @staticmethod
    def get_open_dialog(parent, msg, last_project_folder, filename, filter="ChromaWizard Project (*.cpro);;All Files (*)"):
        fileName, _ = QFileDialog.getOpenFileName(parent, msg,
                                                  os.path.join(os.path.expanduser(last_project_folder), filename),
                                                  filter)

        return fileName

    @staticmethod
    def get_empty_color_image_3(shape):
        return np.zeros(shape + (3,), dtype=np.uint8)

    @staticmethod
    def get_empty_color_image_4(shape):
        return np.zeros(shape + (4,), dtype=np.uint8)

    @staticmethod
    def get_empty_boolean_mask(shape, value):
        return np.full(shape, value, dtype=np.bool)

    @staticmethod
    def get_empty_uint8_mask(shape, value):
        return np.full(shape, value, dtype=np.uint8)

    @staticmethod
    def booleanArray2byte(array):
        a = Utils.get_empty_uint8_mask(array.shape, 0)
        a[array] = 255

        return a

    @staticmethod
    def byteArray2bool(array):
        a = Utils.get_empty_boolean_mask(array.shape, False)
        a[array > 0] = True
        return a

    @staticmethod
    def read_gray_image_from_file(filename):
        return cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def line_aa(y0, x0, y1, x1):
        """Generate anti-aliased line pixel coordinates.
        Parameters
        ----------
        y0, x0 : int
            Starting position (row, column).
        y1, x1 : int
            End position (row, column).
        Returns
        -------
        rr, cc, val : (N,) ndarray (int, int, float)
            Indices of pixels (`rr`, `cc`) and intensity values (`val`).
            ``img[rr, cc] = val``.
        References
        ----------
        .. [1] A Rasterizing Algorithm for Drawing Curves, A. Zingl, 2012
               http://members.chello.at/easyfilter/Bresenham.pdf
        Examples
        --------
        >>> from skimage.draw import line_aa
        >>> img = np.zeros((10, 10), dtype=np.uint8)
        >>> rr, cc, val = line_aa(1, 1, 8, 8)
        >>> img[rr, cc] = val * 255
        >>> img
        array([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
               [  0, 255,  56,   0,   0,   0,   0,   0,   0,   0],
               [  0,  56, 255,  56,   0,   0,   0,   0,   0,   0],
               [  0,   0,  56, 255,  56,   0,   0,   0,   0,   0],
               [  0,   0,   0,  56, 255,  56,   0,   0,   0,   0],
               [  0,   0,   0,   0,  56, 255,  56,   0,   0,   0],
               [  0,   0,   0,   0,   0,  56, 255,  56,   0,   0],
               [  0,   0,   0,   0,   0,   0,  56, 255,  56,   0],
               [  0,   0,   0,   0,   0,   0,   0,  56, 255,   0],
               [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=uint8)
        """
        rr = list()
        cc = list()

        dx = abs(x0 - x1)
        dx_prime = None

        dy = abs(y0 - y1)

        err = dx - dy

        if x0 < x1:
            sign_x = 1
        else:
            sign_x = -1

        if y0 < y1:
            sign_y = 1
        else:
            sign_y = -1

        if dx + dy == 0:
            ed = 1
        else:
            ed = sqrt(dx * dx + dy * dy)

        x, y = x0, y0
        while True:
            cc.append(x)
            rr.append(y)

            err_prime = err
            x_prime = x

            if (2 * err_prime) >= -dx:
                if x == x1:
                    break
                if (err_prime + dy) < ed:
                    cc.append(x)
                    rr.append(y + sign_y)

                err -= dy
                x += sign_x

            if 2 * err_prime <= dy:
                if y == y1:
                    break
                if (dx - err_prime) < ed:
                    cc.append(x_prime + sign_x)
                    rr.append(y)

                err += dx
                y += sign_y

        return (np.array(rr, dtype=np.intp),
                np.array(cc, dtype=np.intp))

    # Stop time of function calls
    @staticmethod
    def stop_time(func, *args, **kargs):
        start = time.time()

        result = func(*args, **kargs)

        end = time.time()
        print("Function {} takes {:.3} seconds".format(func.__name__, end - start))
        return result

class Colors:
    not_def_color = "#FFFFFF"
    multi_color_count = 5
    new_color_table = dict()
    seg_colors = []
    chr_colors = []

    current_color_index = -1
    hex_colors = []

    @classmethod
    def hex_to_rgb(cls, value):
        value = value.lstrip('#')

        [int(value[i:i + 2], 16) for i in range(0, len(value), 2)]
        return [int(value[i:i + 2], 16) for i in range(0, len(value), 2)]

    @classmethod
    def get_color(cls):
        cls.current_color_index += 1
        if cls.current_color_index == len(cls.hex_colors):
            cls.current_color_index = 0

        return cls.hex_to_rgb(cls.hex_colors[cls.current_color_index])

    @classmethod
    def set_colors(cls, colors):
        cls.hex_colors = colors

    @classmethod
    def get_channel_colors(cls, config):
        if len(cls.chr_colors) == 0:
            cls._init_colors(config)

        return cls.chr_colors


    @classmethod
    def get_color_legend(cls, config):
        if len(cls.chr_colors) == 0:
            cls._init_colors(config)

        return cls.new_color_table

    @classmethod
    def reset(cls):
        cls.current_color_index = 0


class Rect:
    def __init__(self, x0, y0, x1=None, y1=None):
        self.X0 = x0
        self.Y0 = y0

        if x1:
            self.X1 = x1
        else:
            self.X1 = x0

        if y1:
            self.Y1 = y1
        else:
            self.Y1 = y0

    def __str__(self):
        return "Rect:\nX0 : {0.X0}, Y0 : {0.Y0}\nX1 : {0.X1}, Y1 : {0.Y1}".format(self)

    def set_bbox(self, y0, x0, y1, x1):
        self.X0 = x0
        self.Y0 = y0
        self.X1 = x1
        self.Y1 = y1

    def set_start(self, x0, y0):
        self.X0 = x0
        self.Y0 = y0
        self.X1 = x0
        self.Y1 = y0

    def set_end(self, x1, y1):
        self.X1 = x1
        self.Y1 = y1

    def get_width(self):
        return abs(self.X1 - self.X0)

    def get_height(self):
        return abs(self.Y1 - self.Y0)

    def get_top_left(self):
        return self.X0 if self.X0 < self.X1 else self.X1, self.Y0 if self.Y0 < self.Y1 else self.Y1

    def get_bottom_right(self):
        return self.X0 if self.X0 > self.X1 else self.X1, self.Y0 if self.Y0 > self.Y1 else self.Y1


class PointArray():
    """
    Save line and chromosome coordiantes
    """
    def __init__(self):
        self._point_array = []

    def add_point(self, pos, type, last=False, hash=None):
        if last:
            if self._point_array and self._point_array[-1]['type'] == type:
                if pos not in self._point_array[-1]['point']:
                    self._point_array[-1]['point'].append(pos)
                    self._point_array[-1]['hash'].append(hash)
            else:
                self._point_array.append({'type':type, 'point':[pos], 'hash':[hash]})

        else:
            self._point_array.append({'type': type, 'point': [pos], 'hash':[hash]})

    def remove_last_group(self):
        if self._point_array:
            #if len(self._point_array[-1]['point']) < 2:
            del self._point_array[-1]
            #else:
            #    del self._point_array[-1]['point'][-1]
            #    del self._point_array[-1]['hash'][-1]

    def remove_chr(self, chr):
        indices = [(index, i) for index, grp in enumerate(self._point_array) if grp['type'] == "chr" for i, h in
                  enumerate(grp['hash']) if h == hash(chr)]

        del self._point_array[indices[0]['point'][indices[1]]]

    # def get_chr_index_in_point_array(self, chr):
    #     hashes = [(h, index) for index, grp in enumerate(self._point_array) if grp['type'] == "chr" for h in grp['hash']]
    #
    #     for h in hashes:
    #         if hash(chr) == h[0]:
    #             print(h)
    #             return h[1]

    def get_merged_chrs(self, chr, chromosomes):
        """
        Test chromosome if it is merged with others and return a set() of chromosome hashes
        :param chr:
        :param chromosomes:
        :return: set() of merged chromosome hashes
        """
        merged = set([hash(chr)])
        last_size_merged = 0
        size_merged = 1

        while size_merged != last_size_merged:
            last_size_merged = size_merged

            merged = {hash(chromosomes.get_chromosome_by_pos_Point(p)) for grp in self._point_array if grp['type'] == "chr"
                      and merged.intersection([hash(chromosomes.get_chromosome_by_pos_Point(p)) for p in grp['point']])
                      for p in grp['point']}

            size_merged = len(merged)

        if not merged:
            merged = set([hash(chr)])

        return merged

    def get_chromosome_groups(self, chromosomes):
        groups = {}
        for chr in chromosomes:
            merged = tuple(self.get_merged_chrs(chr, chromosomes))
            if merged in groups:
                groups[merged].append(chr)
            else:
                groups[merged] = [chr]

        return groups


    def get_type(self, type):
        for item in self._point_array:
            if item['type'] == type:
                yield item

    def get_last(self):
        return self._point_array[-1]

    def __getitem__(self, index):
        return self._point_array[index]

    # def __iter__(self):
    #     for item in  self._point_array:
    #         yield item

    def __len__(self):
        return len(self._point_array)

class skimage:
    # The folowing parts were taken from the scikit-image project: scikit-image/skimage/draw/draw.py
    # To avoid the whole scikit-image installation
    @staticmethod
    def _ellipse_in_shape(shape, center, radiuses):
        """Generate coordinates of points within ellipse bounded by shape."""
        r_lim, c_lim = np.ogrid[0:float(shape[0]), 0:float(shape[1])]
        r, c = center
        ry, rx = radiuses
        distances = ((r_lim - r) / ry) ** 2 + ((c_lim - c) / rx) ** 2
        return np.nonzero(distances < 1)

    @staticmethod
    def circle(r, c, radius, shape=None):
        """Generate coordinates of pixels within circle.
        Parameters
        ----------
        r, c : double
            Centre coordinate of ellipse.
        radius : double
            Minor and major semi-axes. ``(x/xradius)**2 + (y/yradius)**2 = 1``.
        shape : tuple, optional
            Image shape which is used to determine the maximum extent of output pixel
            coordinates. This is useful for circles which exceed the image size.
            By default the full extent of the circles are used.
        Returns
        -------
        rr, cc : ndarray of int
            Pixel coordinates of circle.
            May be used to directly index into an array, e.g.
            ``img[rr, cc] = 1``.
        Examples
        --------
        >>> from skimage.draw import circle
        >>> img = np.zeros((10, 10), dtype=np.uint8)
        >>> rr, cc = circle(5, 5, 4)
        >>> img[rr, cc] = 1
        >>> img
        array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
               [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
        """

        center = np.array([r, c])
        radiuses = np.array([radius, radius])

        # The upper_left and lower_right corners of the
        # smallest rectangle containing the circle.
        upper_left = np.ceil(center - radiuses).astype(int)
        lower_right = np.floor(center + radiuses).astype(int)

        if shape is not None:
            # Constrain upper_left and lower_right by shape boundary.
            upper_left = np.maximum(upper_left, np.array([0, 0]))
            lower_right = np.minimum(lower_right, np.array(shape[:2]) - 1)

        shifted_center = center - upper_left
        bounding_shape = lower_right - upper_left + 1

        rr, cc = skimage._ellipse_in_shape(bounding_shape, shifted_center, radiuses)
        rr.flags.writeable = True
        cc.flags.writeable = True
        rr += upper_left[0]
        cc += upper_left[1]
        return rr, cc

    @staticmethod
    def line_aa(y0, x0, y1, x1):
        """Generate anti-aliased line pixel coordinates.
        Parameters
        ----------
        y0, x0 : int
            Starting position (row, column).
        y1, x1 : int
            End position (row, column).
        Returns
        -------
        rr, cc, val : (N,) ndarray (int, int, float)
            Indices of pixels (`rr`, `cc`) and intensity values (`val`).
            ``img[rr, cc] = val``.
        References
        ----------
        .. [1] A Rasterizing Algorithm for Drawing Curves, A. Zingl, 2012
               http://members.chello.at/easyfilter/Bresenham.pdf
        Examples
        --------
        >>> from skimage.draw import line_aa
        >>> img = np.zeros((10, 10), dtype=np.uint8)
        >>> rr, cc, val = line_aa(1, 1, 8, 8)
        >>> img[rr, cc] = val * 255
        >>> img
        array([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
               [  0, 255,  56,   0,   0,   0,   0,   0,   0,   0],
               [  0,  56, 255,  56,   0,   0,   0,   0,   0,   0],
               [  0,   0,  56, 255,  56,   0,   0,   0,   0,   0],
               [  0,   0,   0,  56, 255,  56,   0,   0,   0,   0],
               [  0,   0,   0,   0,  56, 255,  56,   0,   0,   0],
               [  0,   0,   0,   0,   0,  56, 255,  56,   0,   0],
               [  0,   0,   0,   0,   0,   0,  56, 255,  56,   0],
               [  0,   0,   0,   0,   0,   0,   0,  56, 255,   0],
               [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=uint8)
        """
        rr = list()
        cc = list()

        dx = abs(x0 - x1)
        dx_prime = None

        dy = abs(y0 - y1)

        err = dx - dy

        if x0 < x1:
            sign_x = 1
        else:
            sign_x = -1

        if y0 < y1:
            sign_y = 1
        else:
            sign_y = -1

        if dx + dy == 0:
            ed = 1
        else:
            ed = sqrt(dx * dx + dy * dy)

        x, y = x0, y0
        while True:
            cc.append(x)
            rr.append(y)

            err_prime = err
            x_prime = x

            if (2 * err_prime) >= -dx:
                if x == x1:
                    break
                if (err_prime + dy) < ed:
                    cc.append(x)
                    rr.append(y + sign_y)

                err -= dy
                x += sign_x

            if 2 * err_prime <= dy:
                if y == y1:
                    break
                if (dx - err_prime) < ed:
                    cc.append(x_prime + sign_x)
                    rr.append(y)

                err += dx
                y += sign_y

        return (np.array(rr, dtype=np.intp),
                np.array(cc, dtype=np.intp))