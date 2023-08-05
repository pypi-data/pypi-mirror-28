from PyQt5.QtWidgets import QApplication, QSlider
from PyQt5.QtCore import QTranslator, Qt, QRectF
from PyQt5 import QtCore, QtGui


import os
import sys
import chroma.Error as Error
from shutil import (SameFileError, copyfile)
import locale
import webbrowser
#import pickle
from functools import (partial, lru_cache)

from chroma.MainGui import MainGui
from chroma.Config import Config
from chroma.Chroma import Chroma
from chroma.Cursor import CustomCursor
from chroma.Utils import (Colors as C, Utils as U, skimage)

_t = QtCore.QCoreApplication.translate


class Manager():
    EXIT_CODE_REBOOT = -2316623

    def __init__(self, args):
        # Exit Code for first round
        self.exit_code = Manager.EXIT_CODE_REBOOT

        self.args = args

        self.logger = args.logger

        # State 0 is 1. part | State 1 is also 2. part
        self.state = 0

        # Application directory
        self.app_path = os.path.dirname(os.path.realpath(__file__))

        # Config file path
        self.config_path = os.path.abspath(self.args.config)

        # Path to internal config.json - Is fallback if new version have new attributes not in the old One
        fallback_path = os.path.join(self.app_path, 'config.json')

        # Check if config file exists
        # Raise an error if config path name is invalid
        if not os.path.isfile(self.config_path):
            try:
                copyfile(fallback_path, self.config_path)
            except (SameFileError, IOError):
                self.logger.error("Cannot copy chromadingsda config file to {}".format(self.config_path))
                raise
            except Exception as e:
                self.logger.error("Unexpected error: {}".format(e))
                raise

        # Read in config
        self.config = Config.read_create_config(self.config_path, fallback_path, self.logger)

        # Channel names sorted by keys (0, 1, 10, 100, ...)
        self.config_channel_names = sorted(list(self.config.config.channel_names.keys()))

        # # Create Qt5 application
        # self.app = QApplication([args])
        #
        self.lib_path = os.path.dirname(__file__)
        #
        # # Load current translation file
        # translator = self.set_localistaion(locale.getdefaultlocale()[0])  # os.environ.get("LANGUAGE"))
        # self.app.installTranslator(translator)

        # Debug info
        self.logger.info("Application path: {}".format(self.app_path))
        self.logger.info("Lib path: {}".format(self.lib_path))

        # Info
        self.logger.info(
            "Config path: {}, Minimum Pixel Size: {}, Channel count: {}, Last save folder: {}, Last image folder: {}"
                .format(os.path.expanduser(self.config_path),
                        self.config.config.minimum_pixel_size,
                        len(self.config.config.channel_names.keys()),
                        os.path.expanduser(self.config.config.last_save_folder),
                        os.path.expanduser(self.config.config.last_image_folder)))



        # Pen for zooming rectangle
        self.pen_selection_line = QtGui.QPen(QtGui.QColor(*C.hex_to_rgb(self.config.config.color_of_selection_lines)))
        self.pen_selection_line.setWidth(1)
        self.penYellow = QtGui.QPen(QtGui.QColor(255, 255, 0))
        self.penYellow.setWidth(1)
        self.penRed = QtGui.QPen(QtGui.QColor(255, 0, 0))
        self.penRed.setWidth(1)
        self.penGreen = QtGui.QPen(QtGui.QColor(0, 255, 0))
        self.penGreen.setWidth(1)
        self.penBlue = QtGui.QPen(QtGui.QColor(0, 0, 255))
        self.penBlue.setWidth(1)
        self.penYellowK = QtGui.QPen(QtGui.QColor(255, 255, 0))
        self.penYellowK.setWidth(3)
        self.penRedK = QtGui.QPen(QtGui.QColor(255, 0, 0))
        self.penRedK.setWidth(3)


        self.is_initiated = False
        """
        Status flag. Is True if first image is loaded
        """

        self.last_right_click = None
        """
        Store the last right mouse click.

        This is important for mouse dragging actions
        Is of type ev.scenePos()
        """

        self.last_left_click = None
        """
        Store the last right mouse click.

        This is important for mouse dragging actions
        Is of type ev.scenePos()
        """

        self.rect1 = None
        """
        Drawing rect for dragging actions in orig ZW
        """

        self.rect2 = None
        """
            Drawing rect for dragging actions in mask ZW
        """

        self.merging_enabled = False
        self.selected_chromosomes = set()
        self.selection_enabled = False
        self.selection_line = None

        self.karyo_rect_hover = None
        self.karyo_rect_click = None

        # Pixmap saved for simply removing
        self.border_pixmap = []
        self.karyotype_pixmap = []

        # Selected chromosome in karyotype
        self.sel_chromosome = None

        # If set then use it for save_project()
        self.last_save_folder = self.config.config.last_save_folder
        self.save_filename = None
        self.karyotype_filename = "karyotype.png"

        # Maskink of chromosme level
        self.chr_last_left_click = []
        self.chr_last_right_click = []
        self.rects = []

        self.exit_code = 0

    def run(self):
        """
        Start the Gui. Is called by the main.py. Returns error code of the app.
        :return: int
        """

        # Create Qt5 application
        self.app = QApplication([self.args])

        # Load current translation file
        translator = self.set_localistaion(locale.getdefaultlocale()[0])  # os.environ.get("LANGUAGE"))
        self.app.installTranslator(translator)

        self.lib_path = os.path.dirname(__file__)

        self.gui = MainGui(self)

        self.chroma = Chroma(self)

        # Show Gui
        self.gui.show()

        # Start app
        #while True:
        self.exit_code = self.app.exec()

        # Run app as long it is not rebooted
        #while True:
        #    if self.exit_code != Manager.EXIT_CODE_REBOOT:
        #        self.gui.close()


    def set_localistaion(self, lang):
        """
        Install the correct language translator
        :param lang: String i.e. de, en, es, us
        :return: translator
        """
        # Create translation object
        translator = QTranslator()
        translator.load("chromadingsda_de", directory=os.path.join(self.lib_path, "lang", lang[:2]))

        return translator

    # MainGui Function Calls
    def load_next_channel(self, pos):

        # Open image dialog box
        filename = U.open_image_dialog(self.gui, _t("Manager", "Load Channel"), self.config.config.last_image_folder,
                                       _t("Manager", "Images (*.png *.tif *.tiff *.jpg)"))

        if filename:
            try:
                # Initiate state 1 if not already done
                if not self.is_initiated:
                    self.init_state_1()

                # Load the next channel
                index, cube = self.chroma.load_channel(U.read_gray_image_from_file(filename))

                if index == -1:
                    self.logger.error("No more free channels. Can not load image: '{}'!".format(filename))
                    return

                # Save last image folder
                dir = os.path.dirname(filename)
                self.logger.info("Load next channel: {}, file: {}".format(index, filename))
                self.config.config.last_image_folder = dir
                self.config.update()

                self.init_channel(index)

                # Get cb_states after enabling checkBoxes
                cb_states = self.get_checkbox_states()

                # Update ZWs
                if index == 0:  # for DAPI
                    self.update_view_0(cb_states)
                else:  # for other channels
                    self.update_view(cb_states)

            except Error.WrongImageShapeError as e:
                self.logger.error("Could not load image: '{}'! Error: {}".format(filename, e))
            except:
                self.logger.error("Could not load image: '{}'! Error: {}".format(filename, sys.exc_info()[0]))
                raise

    def get_checkbox_states(self):
        """
        Returns a list of all checkbox indices which are checked
        :return: list
        """
        return [y for x,y in zip(self.gui.checkBoxes, range(0,len(self.gui.checkBoxes))) if x.isChecked()]

    def _disconnect(self, func):
        try:
            func.disconnect()
        except:
            pass

    def init_state_1(self):
        self.logger.info(_t("Manager", "Enter state 1:"))

        self.state = 0

        image_path = os.path.join(self.app_path, "images", "chroma.png")

        self.is_initiated = True
        self.gui.ZW1.setEnabledZooming(True)
        self.gui.ZW1.zoomView.setCursor(Qt.ArrowCursor)

        # Disconnect slots for ZW1
        self._disconnect(self.gui.ZW1.scene.mouseLeftClicked)
        self._disconnect(self.gui.ZW1.scene.mouseLeftReleased)
        self._disconnect(self.gui.ZW1.scene.mouseRightClicked)
        self._disconnect(self.gui.ZW1.scene.mouseRightReleased)
        self._disconnect(self.gui.ZW1.scene.mouseMoved)
        self._disconnect(self.gui.ZW1.scene.mouseWheel)

        self.gui.ZW2.zoomView.setCursor(CustomCursor(type="CIRCLE").cursor)

        # Disconnect slots for ZW2
        self._disconnect(self.gui.ZW2.scene.mouseLeftClicked)
        self._disconnect(self.gui.ZW2.scene.mouseLeftReleased)
        self._disconnect(self.gui.ZW2.scene.mouseRightClicked)
        self._disconnect(self.gui.ZW2.scene.mouseRightReleased)
        self._disconnect(self.gui.ZW2.scene.mouseWheel)
        self._disconnect(self.gui.ZW2.scene.mouseMoved)

        self.gui.ZW3.zoomView.setCursor(Qt.ArrowCursor)

        # Disconnect slots for ZW3
        self._disconnect(self.gui.ZW3.scene.mouseLeftClicked)
        self._disconnect(self.gui.ZW3.scene.mouseLeftReleased)
        self._disconnect(self.gui.ZW3.scene.mouseRightClicked)
        self._disconnect(self.gui.ZW3.scene.mouseRightReleased)
        self._disconnect(self.gui.ZW3.scene.mouseWheel)
        self._disconnect(self.gui.ZW3.scene.mouseMoved)

        self.gui.ZW1.scene.mouseLeftClicked.connect(self.origLeftClick)
        self.gui.ZW2.scene.mouseLeftClicked.connect(self.maskLeftClick)
        self.gui.ZW3.scene.mouseLeftClicked.connect(self.selectLeftClick)
        self.gui.ZW1.scene.mouseLeftReleased.connect(self.origLeftRelease)
        self.gui.ZW2.scene.mouseLeftReleased.connect(self.maskLeftRelease)
        self.gui.ZW3.scene.mouseLeftReleased.connect(self.selectLeftRelease)
        self.gui.ZW1.scene.mouseRightClicked.connect(self.origRightClick)
        self.gui.ZW2.scene.mouseRightClicked.connect(self.maskRightClick)
        self.gui.ZW3.scene.mouseRightClicked.connect(self.selectRightClick)
        self.gui.ZW1.scene.mouseRightReleased.connect(self.origRightRelease)
        self.gui.ZW2.scene.mouseRightReleased.connect(self.maskRightRelease)
        self.gui.ZW3.scene.mouseRightReleased.connect(self.selectRightRelease)
        self.gui.ZW1.scene.mouseMoved.connect(partial(self.dragMouseMove, self.gui.ZW1, 0))
        self.gui.ZW1.scene.mouseWheel.connect(partial(self.zoomMouseWheel, self.gui.ZW1, 0))
        self.gui.ZW2.scene.mouseWheel.connect(partial(self.zoomMouseWheel, self.gui.ZW2, 0))
        self.gui.ZW3.scene.mouseWheel.connect(partial(self.zoomMouseWheel, self.gui.ZW3, 0))
        self.gui.ZW2.scene.mouseMoved.connect(self.maskMouseMove)
        self.gui.ZW3.scene.mouseMoved.connect(self.selectMouseMove)

        self.gui.ZW3.keyIsPressed.connect(self.keyPressed)
        self.gui.ZW3.keyIsReleased.connect(self.keyReleased)
        self.gui.ZW3.mouseLeave.connect(self.mouseLeaved)
        self.gui.ZW3.mouseEnter.connect(self.mouseEnterd)

        self.gui.pb_clear_mask.setEnabled(True)
        self.gui.pb_next.setEnabled(True)
        self.gui.saveKaryoAction.setEnabled(False)

        self.gui.ZW2.setEnabledZooming(True)
        self.gui.ZW3.setEnabledZooming(True)
        self.gui.pb_clear_mask.setEnabled(True)

        self._disconnect(self.gui.ZW_karyotype.scene.mouseMoved)
        self._disconnect(self.gui.ZW_karyotype.scene.mouseLeftClicked)
        self._disconnect(self.gui.pb_next.clicked)
        self.gui.pb_next.clicked.connect(self.next_button_clicked)
        self.gui.pb_next.setText(_t("MainGui", "Next"))

        for channel in range(self.chroma.num_channels_loaded):
            self.gui.sliders_threshold[channel].setEnabled(True)
            self.gui.sliders_noise[channel].setEnabled(True)

        # Enable Menu
        self.gui.addAction.setEnabled(True)

        self.gui.select_chromosome_cb.setEnabled(False)
        self.gui.select_chromosome_cb.clear()

        for widget in self.gui.chr_widgets:
            widget.setEnabled(False)
            if isinstance(widget, (QSlider,)):
                widget.setValue(0)

        for channel in range(self.chroma.channel_count):
            zw = self.gui.chr_ZWs[channel]
            zw.setEnabled(False)

            zw.zoomView.setCursor(Qt.ArrowCursor)

            zw.zoomSlider.setValue(1)

            self._disconnect(zw.scene.mouseWheel)

            self._disconnect(zw.scene.mouseLeftClicked)
            self._disconnect(zw.scene.mouseLeftReleased)
            self._disconnect(zw.scene.mouseRightClicked)
            self._disconnect(zw.scene.mouseRightReleased)
            self._disconnect(zw.scene.mouseMoved)
            zw.loadImage(file=image_path)

        self.gui.ZW_karyotype.loadImage(file=image_path)
        self.gui.ZW_karyotype.zoomView.setCursor(Qt.ArrowCursor)

        self.gui.saveKaryoAction.setEnabled(False)
        self.gui.button_flip.setEnabled(False)
        self.gui.button_clear_mask.setEnabled(False)
        self.gui.button_mv_left.setEnabled(False)
        self.gui.button_mv_right.setEnabled(False)

        self.karyo_rect_click = None
        self.karyo_rect_hover = None

        self.chroma.rot_chromosomes.reset()

        self.sel_chromosome = None

    ## Switch to chromosomen state
    def init_state_2(self):
        self.logger.info(_t("Manager", "Enter state 2:"))
        self.state = 1
        # Deactivate part 1
        self.gui.ZW1.scene.mouseLeftReleased.disconnect(self.origLeftRelease)

        self.gui.ZW2.setEnabledZooming(False)
        self.gui.ZW2.scene.mouseLeftClicked.disconnect(self.maskLeftClick)
        self.gui.ZW2.scene.mouseLeftClicked.connect(self.origLeftClick)
        self.gui.ZW2.scene.mouseLeftReleased.disconnect(self.maskLeftRelease)
        #self.gui.ZW2.scene.mouseRightClicked.disconnect(self.maskRightClick)
        self.gui.ZW2.scene.mouseRightReleased.disconnect(self.maskRightRelease)
        self.gui.ZW2.scene.mouseMoved.disconnect(self.maskMouseMove)
        self.gui.ZW2.scene.mouseMoved.connect(partial(self.dragMouseMove, self.gui.ZW2, 0))
        self.gui.ZW2.zoomView.setCursor(Qt.ArrowCursor)

        self.gui.ZW3.setEnabledZooming(False)
        self.gui.ZW3.scene.mouseLeftClicked.disconnect(self.selectLeftClick)
        self.gui.ZW3.scene.mouseLeftClicked.connect(self.origLeftClick)
        self.gui.ZW3.scene.mouseLeftReleased.disconnect(self.selectLeftRelease)
        self.gui.ZW3.scene.mouseRightClicked.disconnect(self.selectRightClick)
        self.gui.ZW3.scene.mouseRightClicked.connect(self.origRightClick)
        self.gui.ZW3.scene.mouseRightReleased.disconnect(self.selectRightRelease)
        self.gui.ZW3.scene.mouseMoved.disconnect(self.selectMouseMove)
        self.gui.ZW3.scene.mouseMoved.connect(partial(self.dragMouseMove, self.gui.ZW3, 0))

        self.gui.ZW2.scene.mouseRightClicked.connect(self.origRightClick)
        self.gui.ZW2.scene.mouseRightReleased.connect(self.origRightRelease)
        self.gui.ZW3.scene.mouseRightClicked.connect(self.origRightClick)
        self.gui.ZW3.scene.mouseRightReleased.connect(self.origRightRelease)

        self.gui.ZW_karyotype.scene.mouseMoved.connect(partial(self.karyotypeMouseMove, self.gui.ZW_karyotype, 0))
        self.gui.ZW_karyotype.scene.mouseLeftClicked.connect(partial(self.karyotypeLeftClick, self.gui.ZW_karyotype, 0))

        self.gui.pb_clear_mask.setEnabled(False)
        self._disconnect(self.gui.pb_next.clicked)
        self.gui.pb_next.clicked.connect(self.back_button_clicked)
        self.gui.pb_next.setText(_t("MainGui","Back"))
        #self.gui.pb_next.setEnabled(False)

        for slider in self.gui.sliders_threshold:
            slider.setEnabled(False)

        for slider in self.gui.sliders_noise:
            slider.setEnabled(False)

        # Disable Menu
        self.gui.addAction.setEnabled(False)

        # Reset selection window
        self.merging_enabled = False
        self.selected_chromosomes = set()
        self.reset_border_ZW3()

        for channel in range(self.chroma.channel_count):
            if channel <= self.chroma.num_channels_loaded - 1:
                zw = self.gui.chr_ZWs[channel]
                zw.setEnabled(True)

                zw.zoomView.setCursor(CustomCursor(type="CIRCLE").cursor)
                zw.scene.mouseWheel.connect(partial(self.zoomMouseWheel, zw, channel))

                zw.scene.mouseLeftClicked.connect(partial(self.chr_maskLeftClick, zw, channel))
                zw.scene.mouseLeftReleased.connect(partial(self.chr_maskLeftRelease, zw, channel))
                zw.scene.mouseRightClicked.connect(partial(self.chr_maskRightClick, zw, channel))
                zw.scene.mouseRightReleased.connect(partial(self.chr_maskRightRelease, zw, channel))
                zw.scene.mouseMoved.connect(partial(self.chr_maskMouseMove, zw, channel))

                for widget in self.gui.chr_widgets[channel * 3:channel * 3 + 3]:
                    widget.setEnabled(True)

        self.gui.saveKaryoAction.setEnabled(True)
        self.gui.button_flip.setEnabled(True)
        self.gui.button_clear_mask.setEnabled(True)
        self.gui.button_mv_left.setEnabled(True)
        self.gui.button_mv_right.setEnabled(True)
        self.gui.select_chromosome_cb.setEnabled(True)
        self.karyo_rect_click = None
        self.karyo_rect_hover = None

    def open_project(self):
        filename = U.get_open_dialog(self.gui, "Open Project", self.last_save_folder, 'chroma.cpro')

        if filename:
            self.save_filename = filename

            dir = os.path.dirname(self.save_filename)
            self.logger.info(_t("Manager", "Open Project: {}".format(filename)))

            self.chroma.num_channels_loaded = 0

            # Reset
            for cb in self.gui.checkBoxes:
                cb.setEnabled(False)
                cb.setCheckState(Qt.Unchecked)

            for slider in self.gui.sliders_threshold:
                slider.setEnabled(False)
                slider.setValue(0)

            for slider in self.gui.sliders_noise:
                slider.setEnabled(False)
                slider.setValue(0)

            self.chroma.rot_chromosomes.reset()

            # Update Windows
            self.init_state_1()

            # Load data from save file
            d = self.chroma.load(self.save_filename)

            self.chroma.init_zero(d['cube_orig'].get_layer(0))

            # Reload Data
            self.chroma.cube_orig = d['cube_orig']
            self.chroma.cube_mask_otsu_ret = d['thresholds_mask']
            self.chroma.cube_mask_noise = d['thresholds_noise']
            self.chroma.point_array = d['point_array']
            self.chroma.cube_mask_otsu = d['cube_mask_otsu']
            self.chroma.cube_mask_plus = d['cube_mask_plus']
            self.chroma.cube_mask_minus = d['cube_mask_minus']
            self.chroma.np_b_mask_select = d['b_mask_select']
            self.chroma.rot_chromosomes = d['rot_chromosomes']
            self.chroma.chromosomes = d['chromosomes']

            for channel in range(d['cube_orig'].get_count_layers()):
                self.init_channel(channel)
                self.chroma.num_channels_loaded += 1

            cb_states = self.get_checkbox_states()

            self.update_view_0(cb_states)

            if d['state'] == 1:
                self.init_state_2()

                # Load chromosomes into combobox selection
                self.gui.select_chromosome_cb.addItems(
                    [str(i + 1) for i in list(range(len(self.chroma.rot_chromosomes)))])

                img = self.highlight_selected_chromosome(self.chroma.chromosomes[0])

                self.update_ZW3(img)

                self.load_karyotype(dapi=0 in cb_states)

                # Run to create red selection border in karyotype
                self.combo_box_changed(self.gui.select_chromosome_cb)

    def init_channel(self, index):
        """
        Initate widgets for each channel
        :param index:
        :return:
        """
        # Update Checkboxes - Enable and checkit
        self.gui.checkBoxes[index].setEnabled(True)
        self.gui.checkBoxes[index].setCheckState(Qt.Checked)

        # Set the threshold slider
        self.gui.sliders_threshold[index].setEnabled(True)
        self.gui.sliders_threshold[index].setValue(self.chroma.getThresholdValue(index))

        # Set the noise slider
        self.gui.sliders_noise[index].setEnabled(True)
        self.gui.sliders_noise[index].setValue(self.chroma.getNoiseValue(index))

        # Initiate chromosome level masking
        self.chr_last_left_click.append(None)
        self.chr_last_right_click.append(None)
        self.rects.append(None)

    def update_view(self, cb_states):
        self.gui.ZW1.updateImage(numpy=self.chroma.cube_orig.get_overlay(cb_states))  # getNpImage(index))

        if 0 in cb_states:
            dapi = True
        else:
            dapi = False

        # Do masking
        cubes = [self.chroma.cube_mask_otsu, self.chroma.cube_mask_minus, self.chroma.cube_mask_plus]

        M0, iRes = self.chroma.get_masking(cb_states, cubes)

        self.gui.ZW2.updateImage(numpy=self.chroma.get_color_img(iRes, dapi))

        return M0

    def update_view_0(self, cb_states):
        # Get masking
        iM0 = self.update_view(cb_states)

        # Draw selection lines in masking
        iM0[self.chroma.process_selection_lines()] = 0

        self.chroma.get_selecting(iM0)

        # Draw yellow lines
        self.chroma.np_selection[self.chroma.np_b_mask_select] = C.hex_to_rgb(self.config.config.color_of_selection_lines)

        self.update_chromosome_count()

        self.gui.ZW3.updateImage(numpy=self.chroma.np_selection)


    def checkBoxChanged(self, checkbox, index, state):
        """
        Is executed when main checkboxes were clicked
        :param checkbox: the checkbox itself
        :param index: channel
        :param state: checked or not
        :return:
        """
        if checkbox.isEnabled():
            cb_states = self.get_checkbox_states()

            # One checkbox must be checked at all
            if len(cb_states) == 0:
                checkbox.setCheckState(2)
            else:
                self.update_view(cb_states)

            # Update chr_views when available
            if self.state == 1:
                self.update_chr_view(index)

    @lru_cache(maxsize=64)
    def highlight_selected_chromosome(self, chromosome):
        # Highlight selected chromosome
        img = U.get_empty_color_image_4(self.chroma.img_shape)

        if chromosome:
            img = self.add_border(chromosome, C.hex_to_rgb(self.config.config.color_for_border_highlight))

            for chr in self.selected_chromosomes:
                img[chr.get_border(thickness=self.config.config.border_thickness,
                               only_border_highlight=self.config.config.only_border_highlight)] = \
                C.hex_to_rgb(self.config.config.color_for_border_selection)
        return img

    def update_chromosome_count(self):
        """
        Update chromosome count
        :return:
        """
        # Update chromosome count
        chromosomes = self.chroma.chromosomes.get_chromosomes()

        s = set()
        for c in chromosomes:
            s.add(tuple(self.chroma.point_array.get_merged_chrs(c, self.chroma.chromosomes)))

        # Update chromosome counter
        self.gui.label_count.setText(str(len(s)))


    def clear_button_clicked(self):
        indices = self.get_checkbox_states()
        self.chroma.clear_manual_mask(indices)
        # Update ZW2, ZW3
        if 0 in indices:
            self.update_view_0(indices)
        else:
            self.update_view(indices)

    def origLeftClick(self, ev):
        pass

    def maskLeftClick(self, ev):
        self.last_left_click = ev.scenePos()

    def selectLeftClick(self, ev):
        pos = (int(ev.scenePos().y()), int(ev.scenePos().x()))

        # Test if pos in window
        if 0 < pos[1] < self.chroma.img_shape[1] and 0 < pos[0] < self.chroma.img_shape[0]:
            modifiers = QApplication.keyboardModifiers()

            # CRTL + left mouse click
            if modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier) or modifiers == QtCore.Qt.ControlModifier:
                chr = self.chroma.chromosomes.get_chromosome_by_pos_QPointF(ev.scenePos())
                self.gui.ZW3.zoomView.setCursor(CustomCursor(type="PLUS1").cursor)

                # Clear highlighting cache
                self.highlight_selected_chromosome.cache_clear()

                if chr:
                    if chr not in self.selected_chromosomes:
                        # Add point to point-array
                        self.chroma.merge_chromosomes(pos)

                        self.selected_chromosomes.add(chr)

                        # Update color of chromosomes
                        self.chroma.update_chromosome_colors()

                        # Highlight selected chromosome
                        img = self.add_border(chr, C.hex_to_rgb(self.config.config.color_for_border_selection))

                        # Convert to QPixmap
                        nimg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_ARGB32)
                        pixmap = QtGui.QPixmap.fromImage(nimg)

                        # Add QPixmap to scene
                        self.border_pixmap.append(self.gui.ZW3.scene.addPixmap(pixmap))

                        self.gui.ZW3.updateImage(numpy=self.chroma.np_selection)
            else:
                self.merging_enabled = False


                self.selected_chromosomes = set()
                index = len(self.chroma.point_array) - 1

                # Start selection
                if self.selection_enabled:
                    if self.chroma.point_array[-1]['type'] == 'line':
                        if index >= 0 and self.chroma.point_array[-1]['point'][-1] == pos:
                            pass
                        else:
                            self.chroma.point_array.add_point(pos, "line", last=True)
                else:
                    self.selection_enabled = True
                    self.chroma.point_array.add_point(pos,"line", last=False)

    def origLeftRelease(self, ev):
        pass

    def maskLeftRelease(self, ev):
        indices = self.get_checkbox_states()
        if self.rect2:
            rect = self.rect2.rect()

            # set rectangle to mask
            for index in indices:
                mask_minus = self.chroma.cube_mask_minus.get_layer(index)
                mask_plus = self.chroma.cube_mask_plus.get_layer(index)

                mask_plus[int(rect.top()):int(rect.bottom()), int(rect.left()):int(rect.right())] = False # 1 minus 2 plus
                mask_minus[int(rect.top()):int(rect.bottom()), int(rect.left()):int(rect.right())] = False

            # Remove rectangle
            self.gui.ZW2.scene.removeItem(self.rect2)
            self.rect2 = None
        else:
            # set rectangle to mask
            for index in indices:
                mask_minus = self.chroma.cube_mask_minus.get_layer(index)
                mask_plus = self.chroma.cube_mask_plus.get_layer(index)

                circle_radius = 6

                f = circle_radius / min(self.gui.ZW1.scale_factor)

                mask_plus[skimage.circle(self.last_left_click.y() + f / self.gui.ZW1.zoom,
                                                                self.last_left_click.x() + f / self.gui.ZW1.zoom,
                                                                circle_radius / self.gui.ZW1.zoom / min(self.gui.ZW1.scale_factor),
                                                                self.gui.ZW1.img_orig.shape)] = False

                mask_minus[skimage.circle(self.last_left_click.y() + f / self.gui.ZW1.zoom,
                                                                self.last_left_click.x() + f / self.gui.ZW1.zoom,
                                                                circle_radius / self.gui.ZW1.zoom / min(self.gui.ZW1.scale_factor),
                                                                self.gui.ZW1.img_orig.shape)] = False

        # Update selection window also
        if 0 in indices:
            self.update_view_0(indices)
        else:
            self.update_view(indices)

    def selectLeftRelease(self, ev):
        pos = (int(ev.scenePos().y()), int(ev.scenePos().x()))

        # Test if pos in window
        if 0 < pos[1] < self.chroma.img_shape[1] and 0 < pos[0] < self.chroma.img_shape[0]:
            if self.chroma.point_array and self.chroma.point_array[-1]['type'] == 'line':
                if self.chroma.point_array[-1]['point'][-1] != pos:
                    self.chroma.point_array[-1]['point'].append((int(ev.scenePos().y()), int(ev.scenePos().x())))

                if len(self.chroma.point_array[-1]['point']) > 1:
                    self.update_view_0(self.get_checkbox_states())

        self.update_chromosome_count()


    def origRightClick(self, ev):
        self.last_right_click = ev.scenePos()

    def maskRightClick(self, ev):
        self.last_right_click = ev.scenePos()

    def selectRightClick(self, ev):
        if ev:
            self.last_right_click = ev.scenePos()

        self.highlight_selected_chromosome.cache_clear()

        # Stop merging chromosomes
        if self.merging_enabled:
            self.merging_enabled = False
            self.selected_chromosomes = set()
            self.reset_border_ZW3()
            self.gui.ZW3.zoomView.setCursor(CustomCursor(type="PLUS2").cursor)
            return

        # Stop drawing lines
        if self.selection_enabled:
            self.selection_enabled = False
            # Remove old line
            self.gui.ZW3.scene.removeItem(self.selection_line)
            self.selection_line = None
            self.reset_border_ZW3()
            return

        # Delete last entry
        if self.chroma.point_array:
            self.chroma.point_array.remove_last_group()

        self.update_view_0(self.get_checkbox_states())

    def origRightRelease(self, ev):
        # Remove rect
        if self.rect1:
            self.gui.ZW1.scene.removeItem(self.rect1)

            rect = self.rect1.rect()

            self.gui.ZW1.zoomingTo(rect)

    def maskRightRelease(self, ev):
        indices = self.get_checkbox_states()
        # Remove rect
        if self.rect2:
            rect = self.rect2.rect()

            # set rectangle to mask
            for index in indices:
                mask_minus = self.chroma.cube_mask_minus.get_layer(index)
                mask_plus = self.chroma.cube_mask_plus.get_layer(index)

                mask_minus[int(rect.top()):int(rect.bottom()), int(rect.left()):int(rect.right())] = True  # 1 minus 2 plus
                mask_plus[int(rect.top()):int(rect.bottom()),int(rect.left()):int(rect.right())] = True

            self.gui.ZW2.scene.removeItem(self.rect2)
            self.rect2 = None

        # Remove circle from mask
        else:
            circle_radius = 6

            f = circle_radius / min(self.gui.ZW1.scale_factor)

            # set rectangle to mask
            for index in indices:
                mask_minus = self.chroma.cube_mask_minus.get_layer(index)
                mask_plus = self.chroma.cube_mask_plus.get_layer(index)

                mask_minus[skimage.circle(self.last_right_click.y() + f / self.gui.ZW1.zoom,
                                          self.last_right_click.x() + f / self.gui.ZW1.zoom,
                                          circle_radius / self.gui.ZW1.zoom / min(self.gui.ZW1.scale_factor),
                                          self.gui.ZW1.img_orig.shape)] = True

                mask_plus[skimage.circle(self.last_right_click.y() + f / self.gui.ZW1.zoom,
                                         self.last_right_click.x() + f / self.gui.ZW1.zoom,
                                         circle_radius / self.gui.ZW1.zoom / min(self.gui.ZW1.scale_factor),
                                         self.gui.ZW1.img_orig.shape)] = True

        # Update selection window also
        if 0 in indices:
            self.update_view_0(indices)
        else:
            self.update_view(indices)

    def selectRightRelease(self, ev):
        self.update_chromosome_count()

    def dragMouseMove(self, zw, index, ev):
        x = int(ev.scenePos().x())
        y = int(ev.scenePos().y())

        if x >= 0 and x < self.chroma.img_shape[1] and y >= 0 and y < self.chroma.img_shape[0]:
            status_bar_msg = ""

            for layer in range(self.chroma.cube_orig.get_count_layers()):
                status_bar_msg += "{c}:({v:}) ".format(v=self.chroma.cube_orig.get_layer(layer)[y, x], c=self.config.config.channel_names["1" + "0" * layer])


            self.gui.statusBar().showMessage(_t("Manager", status_bar_msg))


        if ev.buttons() == Qt.LeftButton:
            zw.scrollHorizontral(ev.screenPos().x() - ev.lastScreenPos().x())
            zw.scrollVertical(ev.screenPos().y() - ev.lastScreenPos().y())
        elif ev.buttons() == Qt.RightButton:
            # TODO Find a way to remove the last item or constrain rect size to current view
            # TODO removeItem(rect1) does not work if rect is dragged ouside of view
            if self.rect1:
                zw.scene.removeItem(self.rect1)

            deltaPF = ev.scenePos() - self.last_right_click

            x = self.last_right_click.x()
            y = self.last_right_click.y()

            width = deltaPF.x()
            height = deltaPF.y()

            # Convert negative rects to positiv
            if width < 0:
                x = self.last_right_click.x() + width
                width = abs(width)

            if height < 0:
                y = self.last_right_click.y() + height
                height = abs(height)

            rect = QRectF(x, y, width, height)

            if rect.right() > zw.img_orig.shape[1]:
                rect.setRight(zw.img_orig.shape[1])
            elif rect.left() < 0:
                rect.setLeft(0)

            if rect.bottom() > zw.img_orig.shape[0]:
                rect.setBottom(zw.img_orig.shape[0])
            elif rect.top() < 0:
                rect.setTop(0)

            self.rect1 = zw.scene.addRect(rect, self.penYellow)



            zw.scene.update()

    def karyotypeMouseMove(self, zw, index, ev):
        chr = self.chroma.rot_chromosomes.get_karyo_chromosome_by_pos_QPointF(ev.scenePos())

        # Highlight karyotype selection
        self.karyo_rect_hover = self.add_karyotype_selection_border(chr, self.penYellowK, self.karyo_rect_hover)


    def karyotypeLeftClick(self, zw, index, ev):
        chr = self.chroma.rot_chromosomes.get_karyo_chromosome_by_pos_QPointF(ev.scenePos())

        index = self.chroma.rot_chromosomes.get_chromosome_index(chr)

        if index is not None:
            self.gui.select_chromosome_cb.setCurrentIndex(index)

        # Highlight karyotype selection
        self.karyo_rect_click = self.add_karyotype_selection_border(chr, self.penRedK, self.karyo_rect_click)

        self.sel_chromosome = chr


    def zoomMouseWheel(self, zw, index, ev):
        if ev.delta() > 0:
            # Zoom in
            zw.zoomSlider.setValue(zw.zoomSlider.value() + 1)
        else:
            # Zoom out
            zw.zoomSlider.setValue(zw.zoomSlider.value() - 1)

    def maskMouseMove(self, ev):
        if ev.buttons() == Qt.LeftButton:
            if self.rect2:
                self.gui.ZW2.scene.removeItem(self.rect2)

            deltaPF = ev.scenePos() - self.last_left_click

            x = self.last_left_click.x()
            y = self.last_left_click.y()

            width = deltaPF.x()
            height = deltaPF.y()

            # Convert negative rects to positiv
            if width < 0:
                x = self.last_left_click.x() + width
                width = abs(width)

            if height < 0:
                y = self.last_left_click.y() + height
                height = abs(height)

            rect = QRectF(x, y, width, height)

            if rect.right() > self.gui.ZW2.img_orig.shape[1]:
                rect.setRight(self.gui.ZW2.img_orig.shape[1])
            elif rect.left() < 0:
                rect.setLeft(0)

            if rect.bottom() > self.gui.ZW2.img_orig.shape[0]:
                rect.setBottom(self.gui.ZW2.img_orig.shape[0])
            elif rect.top() < 0:
                rect.setTop(0)

            self.rect2 = self.gui.ZW2.scene.addRect(rect, self.penRed)

            self.gui.ZW2.scene.update()
        elif ev.buttons() == Qt.RightButton:
            if self.rect2:
                self.gui.ZW2.scene.removeItem(self.rect2)

            deltaPF = ev.scenePos() - self.last_right_click

            x = self.last_right_click.x()
            y = self.last_right_click.y()

            width = deltaPF.x()
            height = deltaPF.y()

            # Convert negative rects to positiv
            if width < 0:
                x = self.last_right_click.x() + width
                width = abs(width)

            if height < 0:
                y = self.last_right_click.y() + height
                height = abs(height)

            rect = QRectF(x, y, width, height)

            if rect.right() > self.gui.ZW2.img_orig.shape[1]:
                rect.setRight(self.gui.ZW2.img_orig.shape[1])
            elif rect.left() < 0:
                rect.setLeft(0)

            if rect.bottom() > self.gui.ZW2.img_orig.shape[0]:
                rect.setBottom(self.gui.ZW2.img_orig.shape[0])
            elif rect.top() < 0:
                rect.setTop(0)

            self.rect2 = self.gui.ZW2.scene.addRect(rect, self.penGreen)

            self.gui.ZW2.scene.update()

    def selectMouseMove(self, ev):

        pos = (int(ev.scenePos().y()), int(ev.scenePos().x()))

        chr = self.chroma.chromosomes.get_chromosome_by_pos_QPointF(ev.scenePos())

        cb_states = self.get_checkbox_states()

        modifiers = QApplication.keyboardModifiers()

        self.reset_border_ZW3()

        # Highlight chromosome if chr(cached function)
        img = self.highlight_selected_chromosome(chr)

        self.update_ZW3(img)

        # Draw selection path
        if ev.buttons() == Qt.LeftButton:
            if modifiers != QtCore.Qt.ControlModifier:
                # Test if pos in window
                if 0 < pos[1] < self.chroma.img_shape[1] and 0 < pos[0] < self.chroma.img_shape[0]:
                    index = len(self.chroma.point_array) - 1

                    if self.chroma.point_array[-1]['type'] == 'line':
                        if index >= 0 and self.chroma.point_array[-1]['point'][-1] == pos:
                            pass
                        else:
                            self.chroma.point_array.add_point(pos, "line", last=True)
                            self.update_view_0(cb_states)
        else:
            if modifiers != QtCore.Qt.ControlModifier:
                # Draw yellow selection line when in selecting mode
                if self.selection_enabled:
                    if self.selection_line:
                        # Remove old line
                        if self.selection_line in self.gui.ZW3.scene.items():
                            self.gui.ZW3.scene.removeItem(self.selection_line)
                            #self.selection_line = None

                    # Test if pos in window
                    if 0 < pos[1] < self.chroma.img_shape[1] and 0 < pos[0] < self.chroma.img_shape[0]:
                        if self.chroma.point_array[-1]['type'] == 'line':
                            start_pos = self.chroma.point_array[-1]['point'][-1]
                            self.selection_line = self.gui.ZW3.scene.addLine(start_pos[1], start_pos[0], pos[1], pos[0],
                                                                             self.pen_selection_line)


                    else:
                        # Mouse leave window - stops selecting mode
                        self.selection_enabled = False
                        if self.selection_line in self.gui.ZW3.scene.items():
                            self.gui.ZW3.scene.removeItem(self.selection_line)

                        self.selection_line = None

    def threshold_changed(self, slider, index, val):
        """
        Is executed when the threshold slider value of the masking window was changed
        :param slider:
        :param index:
        :param val:
        :return:
        """

        self.chroma.calc_threshold(self.chroma.cube_orig, self.chroma.cube_mask_otsu, self.chroma.cube_mask_otsu_ret,
                                   index, val)

        # Update selection window also
        if index == 0:
            self.update_view_0(self.get_checkbox_states())
        else:
            self.update_view(self.get_checkbox_states())

    def chr_threshold_changed(self, slider, index, val):
        """
        Is executed when the threshold slider values of the chromosome windows were changed
        :param slider:
        :param index: slider index equates to channel
        :param val:
        :return:
        """
        self.chroma.calc_threshold(self.sel_chromosome.cube_orig, self.sel_chromosome.cube_mask_otsu,
                                   self.sel_chromosome.cube_mask_otsu_ret, index, val)

        self.update_chr_view(index)

    def noise_changed(self, slider, index, val):
        # Update selection window also
        if index == 0:
            self.update_view_0(self.get_checkbox_states())
        else:
            self.update_view(self.get_checkbox_states())

    def keyIsPressed(self, ev):
        if ev.key() == Qt.Key_Control:
            # Stops selection mode
            if self.selection_enabled and self.selection_line:
                self.selection_enabled = False
                # Remove old line
                self.gui.ZW3.scene.removeItem(self.selection_line)
                self.selection_line = None

    def add_border(self, chr, border_color):
        """
        Merge chromosome
        :param chr:
        :return:
        """
        self.reset_border_ZW3()

        merged_hashes = self.chroma.point_array.get_merged_chrs(chr, self.chroma.chromosomes)

        img = U.get_empty_color_image_4(self.chroma.img_shape)

        if self.merging_enabled:  # merging enabled
            for c in self.chroma.chromosomes:
                if hash(c) in merged_hashes:
                    img[c.get_border(thickness=self.config.config.border_thickness,
                                       only_border_highlight=self.config.config.only_border_highlight)] = border_color
        else:
            for c in self.chroma.chromosomes:
                if hash(c) in merged_hashes:
                    img[c.get_border(thickness=self.config.config.border_thickness,
                                       only_border_highlight=self.config.config.only_border_highlight)] = border_color

        return img

    def reset_border_ZW3(self):
        for pixmap in self.border_pixmap:
            if pixmap in self.gui.ZW3.scene.items():
                self.gui.ZW3.scene.removeItem(pixmap)

        self.border_pixmap = []

    def next_button_clicked(self):
        # Activate part 2
        self.init_state_2()

        # Update chromosomes (Create cube with all channels)
        cubes = [self.chroma.cube_mask_otsu, self.chroma.cube_mask_minus, self.chroma.cube_mask_plus]

        M0, iRes = self.chroma.get_masking([0], cubes)
        M0[self.chroma.process_selection_lines()] = 0

        # Update Chromosomes don't remove
        self.chroma.get_selecting(M0)

        # Create rotated chromosomes
        for chr in self.chroma.chromosomes:
            self.chroma.rot_chromosomes.add_chromosome(chr.get_rotated_chromosome())

        # Sort chromosomes by size
        self.chroma.rot_chromosomes.sort()
        self.chroma.chromosomes.sort()

        cb_states = self.get_checkbox_states()
        self.load_karyotype(dapi=0 in cb_states)

        # Load chromosomes into combobox selection
        self.gui.select_chromosome_cb.addItems([str(i + 1) for i in list(range(len(self.chroma.rot_chromosomes)))])

        img = self.highlight_selected_chromosome(self.chroma.chromosomes[0])

        self.update_ZW3(img)

        # Run to create red selection border in karyotype
        self.combo_box_changed(self.gui.select_chromosome_cb)
        self.update_chr_view(0)

    def back_button_clicked(self):
        self.init_state_1()

    def update_ZW3(self, img):
        # Convert to QPixmap
        nimg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(nimg)

        # Add QPixmap to scene
        self.border_pixmap.append(self.gui.ZW3.scene.addPixmap(pixmap))

    def combo_box_changed(self, cb):
        # Current chromosome selection
        index = cb.currentIndex()

        self.sel_chromosome = self.chroma.rot_chromosomes[index]

        # Update ZW3 selection view
        self.reset_border_ZW3()
        img = self.highlight_selected_chromosome(self.sel_chromosome.parent)  # self.chroma.chromosomes[index])
        self.update_ZW3(img)

        channels = list(range(self.chroma.num_channels_loaded))
        # Change chromosome view
        for channel in range(self.chroma.channel_count):
            if channel > self.chroma.num_channels_loaded - 1:
                # load empty image
                self.gui.chr_ZWs[channel].loadImage(numpy=U.get_empty_uint8_mask(self.sel_chromosome.Resolution[::-1], 0))
            else:
                if channel == 0:
                    self.gui.chr_ZWs[channel].loadImage(numpy=self.chroma.get_color_img(self.chroma.get_masking(channels, self.sel_chromosome.get_cubes(), filter_artifacts=False)[1]))
                else:
                    self.gui.chr_ZWs[channel].loadImage(numpy=U.booleanArray2byte(self.chroma.merge_masks(self.sel_chromosome.get_cubes(), channel)))

                self.gui.chr_widgets[channel * 3].setValue(self.chroma.rot_chromosomes[index].cube_mask_otsu_ret[channel])

        # Draw border around selected chromosome in karyotype window
        self.karyo_rect_click = self.add_karyotype_selection_border(self.sel_chromosome, self.penRedK, self.karyo_rect_click)

    def load_karyotype(self, dapi):
        cb_states = self.get_checkbox_states()
        self.gui.ZW_karyotype.loadImage(numpy=self.chroma.get_color_img(self.chroma.rot_chromosomes.get_chromosome_table(cb_states), dapi=dapi))

    def remove_karyotype_border(self, scene_object):
        if scene_object in self.gui.ZW_karyotype.scene.items():
            self.gui.ZW_karyotype.scene.removeItem(scene_object)



    def add_karyotype_selection_border(self, chr, color_pen, scene_object):
        """

        :param chr:
        :return:
        """
        # Remove old highlight
        if scene_object is not None:
            self.remove_karyotype_border(scene_object)

        if chr:
            return self.gui.ZW_karyotype.scene.addRect(chr.karyo_box, color_pen)

    def save_project(self):
        """
        Save the current project to actual project file
        :return:
        """
        if self.save_filename:
            self.logger.info(_t("Manager", "Save Project:"))
            self.chroma.save(self.save_filename)
        else:
            self.save_as_project()

    def save_as_project(self):
        """
        Save the current project to file
        :return:
        """
        filename= U.get_save_as_dialog(self.gui, "Save Project As", self.last_save_folder, 'chroma.cpro')

        if filename:
            self.save_filename = filename

            dir = os.path.dirname(self.save_filename)
            self.logger.info(_t("Manager", "Save Project As: {}".format(filename)))

            # Update config file
            self.config.config.last_save_folder = dir
            self.config.update()

            self.chroma.save(filename)

    def save_karyotype(self):
        """
                Save the current project to file
                :return:
                """
        filename = U.get_save_as_dialog(self.gui, "Save Karyotype As", self.last_save_folder, "karyotype.png", filter="ChromaWizard Karyotype (*.png);;All Files (*)")

        if filename:
            self.karyotype_filename = filename

            dir = os.path.dirname(self.karyotype_filename)
            self.logger.info(_t("Manager", "Save Karyotype As: {}".format(filename)))


            # Save karyotype to file
            cb_states = self.get_checkbox_states()
            if 0 in cb_states:
                U.numpy_to_file(self.chroma.get_color_img(self.chroma.rot_chromosomes.get_chromosome_table(cb_states), dapi=True), filename)
            else:
                U.numpy_to_file(
                    self.chroma.get_color_img(self.chroma.rot_chromosomes.get_chromosome_table(cb_states), dapi=False),
                    filename)

    def flip_clicked(self):
        self.sel_chromosome.get_rot180_chromosome()

        self.update_chr_view(0)

        # Reload karyotype
        cb_states = self.get_checkbox_states()
        self.load_karyotype(dapi=0 in cb_states)

        self.karyo_rect_click = self.add_karyotype_selection_border(self.sel_chromosome, self.penRedK, None)

    def move_left_clicked(self):
        index = self.chroma.rot_chromosomes.get_chromosome_index(self.sel_chromosome)

        if index > 0:
            # Change chromosome order
            self.chroma.rot_chromosomes.exchange_chromosome(index, index - 1)

            # Reload karyotype
            cb_states = self.get_checkbox_states()
            self.load_karyotype(dapi=0 in cb_states)

            # Reset chromosome combobox
            self.gui.select_chromosome_cb.clear()
            self.gui.select_chromosome_cb.addItems([str(i + 1) for i in list(range(len(self.chroma.rot_chromosomes)))])
            self.gui.select_chromosome_cb.setCurrentIndex(index - 1)

    def move_right_clicked(self):
        index = self.chroma.rot_chromosomes.get_chromosome_index(self.sel_chromosome)

        if index < len(self.chroma.rot_chromosomes) - 1:
            # Change chromosome order
            self.chroma.rot_chromosomes.exchange_chromosome(index, index + 1)

            # Reload karyotype
            cb_states = self.get_checkbox_states()
            self.load_karyotype(dapi=0 in cb_states)

            # Reset chromosome combobox
            self.gui.select_chromosome_cb.clear()
            self.gui.select_chromosome_cb.addItems([str(i + 1) for i in list(range(len(self.chroma.rot_chromosomes)))])
            self.gui.select_chromosome_cb.setCurrentIndex(index + 1)

    def clear_mask_clicked(self, ZW, channel):
        self.sel_chromosome.clear_manual_masks(channel)

        self.update_chr_view(channel)

    def chr_maskLeftClick(self, zw, channel, ev):
        self.chr_last_left_click[channel] = ev.scenePos()

    def chr_maskLeftRelease(self, zw, channel, ev):
        # set rectangle to mask
        mask_minus = self.sel_chromosome.cube_mask_minus.get_layer(channel)
        mask_plus = self.sel_chromosome.cube_mask_plus.get_layer(channel)

        if self.rects[channel]:
            rect = self.rects[channel].rect()

            mask_plus[int(rect.top()):int(rect.bottom()),
            int(rect.left()):int(rect.right())] = False  # 1 minus 2 plus
            mask_minus[int(rect.top()):int(rect.bottom()), int(rect.left()):int(rect.right())] = False

            # Remove rectangle
            zw.scene.removeItem(self.rects[channel])
            self.rects[channel] = None
        else:
            circle_radius = 6

            f = circle_radius / min(zw.scale_factor)

            mask_plus[skimage.circle(self.chr_last_left_click[channel].y() + f / zw.zoom,
                                     self.chr_last_left_click[channel].x() + f / zw.zoom,
                                     circle_radius / zw.zoom / min(zw.scale_factor),
                                     zw.img_orig.shape)] = False

            mask_minus[skimage.circle(self.chr_last_left_click[channel].y() + f / zw.zoom,
                                      self.chr_last_left_click[channel].x() + f / zw.zoom,
                                      circle_radius / zw.zoom / min(zw.scale_factor),
                                      zw.img_orig.shape)] = False

        self.update_chr_view(channel)

    def chr_maskRightClick(self, zw, channel, ev):
        self.chr_last_right_click[channel] = ev.scenePos()

    def chr_maskRightRelease(self, zw, channel, ev):

        # set rectangle to mask
        mask_minus = self.sel_chromosome.cube_mask_minus.get_layer(channel)
        mask_plus = self.sel_chromosome.cube_mask_plus.get_layer(channel)

        if self.rects[channel]:
            rect = self.rects[channel].rect()

            mask_plus[int(rect.top()):int(rect.bottom()),
            int(rect.left()):int(rect.right())] = True  # 1 minus 2 plus
            mask_minus[int(rect.top()):int(rect.bottom()), int(rect.left()):int(rect.right())] = True

            # Remove rectangle
            zw.scene.removeItem(self.rects[channel])
            self.rects[channel] = None
        else:
            circle_radius = 6

            f = circle_radius / min(zw.scale_factor)

            mask_plus[skimage.circle(self.chr_last_right_click[channel].y() + f / zw.zoom,
                                     self.chr_last_right_click[channel].x() + f / zw.zoom,
                                     circle_radius / zw.zoom / min(zw.scale_factor),
                                     zw.img_orig.shape)] = True

            mask_minus[skimage.circle(self.chr_last_right_click[channel].y() + f / zw.zoom,
                                      self.chr_last_right_click[channel].x() + f / zw.zoom,
                                      circle_radius / zw.zoom / min(zw.scale_factor),
                                      zw.img_orig.shape)] = True

        self.update_chr_view(channel)

    def update_chr_view(self, channel):
        indices = self.get_checkbox_states()
        cubes = self.sel_chromosome.get_cubes()

        M0 = self.chroma.merge_masks(cubes, 0)


        self.gui.chr_ZWs[0].loadImage(numpy=self.chroma.get_color_img(self.chroma.get_masking(indices, cubes, filter_artifacts=False)[1], dapi=0 in indices))
        self.karyo_rect_click = None
        self.karyo_rect_hover = None

        if channel == 0:
            for ch in range(1, self.chroma.num_channels_loaded):
                # Change chromosome view
                self.gui.chr_ZWs[ch].loadImage(
                    numpy=U.booleanArray2byte(M0 & self.chroma.merge_masks(cubes, ch)))
        else:
            self.gui.chr_ZWs[channel].loadImage(numpy=U.booleanArray2byte(M0 & self.chroma.merge_masks(cubes, channel)))

        # Update karyotype
        self.load_karyotype(dapi=0 in indices)

        self.karyo_rect_click = self.add_karyotype_selection_border(self.sel_chromosome, self.penRedK,
                                                                    self.karyo_rect_click)

    def chr_maskMouseMove(self, zw, channel, ev):
        if ev.buttons() == Qt.LeftButton:
            if self.rects[channel]:
                zw.scene.removeItem(self.rects[channel])

            deltaPF = ev.scenePos() - self.chr_last_left_click[channel]

            x = self.chr_last_left_click[channel].x()
            y = self.chr_last_left_click[channel].y()

            width = deltaPF.x()
            height = deltaPF.y()

            # Convert negative rects to positiv
            if width < 0:
                x = self.chr_last_left_click[channel].x() + width
                width = abs(width)

            if height < 0:
                y = self.chr_last_left_click[channel].y() + height
                height = abs(height)

            rect = QRectF(x, y, width, height)

            if rect.right() > zw.img_orig.shape[1]:
                rect.setRight(zw.img_orig.shape[1])
            elif rect.left() < 0:
                rect.setLeft(0)

            if rect.bottom() > zw.img_orig.shape[0]:
                rect.setBottom(zw.img_orig.shape[0])
            elif rect.top() < 0:
                rect.setTop(0)

            self.rects[channel] = zw.scene.addRect(rect, self.penRed)

            zw.scene.update()
        elif ev.buttons() == Qt.RightButton:
            if self.rects[channel]:
                zw.scene.removeItem(self.rects[channel])

            deltaPF = ev.scenePos() - self.chr_last_right_click[channel]

            x = self.chr_last_right_click[channel].x()
            y = self.chr_last_right_click[channel].y()

            width = deltaPF.x()
            height = deltaPF.y()

            # Convert negative rects to positiv
            if width < 0:
                x = self.chr_last_right_click[channel].x() + width
                width = abs(width)

            if height < 0:
                y = self.chr_last_right_click[channel].y() + height
                height = abs(height)

            rect = QRectF(x, y, width, height)

            if rect.right() > zw.img_orig.shape[1]:
                rect.setRight(zw.img_orig.shape[1])
            elif rect.left() < 0:
                rect.setLeft(0)

            if rect.bottom() > zw.img_orig.shape[0]:
                rect.setBottom(zw.img_orig.shape[0])
            elif rect.top() < 0:
                rect.setTop(0)

            self.rects[channel] = zw.scene.addRect(rect, self.penGreen)

            zw.scene.update()

    def open_acib_link(self, ev):
        webbrowser.open("http://www.acib.at")

    def keyPressed(self, ev):
        if ev.key() == QtCore.Qt.Key_Control:
            if self.merging_enabled:
                self.gui.ZW3.zoomView.setCursor(CustomCursor(type="PLUS1").cursor)
            else:
                self.gui.ZW3.zoomView.setCursor(CustomCursor(type="PLUS2").cursor)

    def keyReleased(self, ev):
        if ev.key() == QtCore.Qt.Key_Control:
            self.gui.ZW3.zoomView.setCursor(Qt.ArrowCursor)

    def mouseLeaved(self,ev):
        self.gui.ZW3.zoomView.setCursor(Qt.ArrowCursor)
        self.merging_enabled = False

    def mouseEnterd(self,ev):
        modifiers = QApplication.keyboardModifiers()

        if modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier) or modifiers == QtCore.Qt.ControlModifier:
            if self.merging_enabled:
                self.gui.ZW3.zoomView.setCursor(CustomCursor(type="PLUS1").cursor)
            else:
                self.gui.ZW3.zoomView.setCursor(CustomCursor(type="PLUS2").cursor)

    def open_legend(self):
        U.open_legend_dialog(self.gui, self.config)

    def about(self):
        U.open_about_dialog(self.gui, self)