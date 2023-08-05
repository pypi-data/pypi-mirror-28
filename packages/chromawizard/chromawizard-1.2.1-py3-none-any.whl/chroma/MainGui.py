import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QToolTip, QAction, QPushButton, QLabel, QCheckBox, QComboBox,
                             QSlider, QScrollArea, QMenuBar, QStatusBar, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QSpacerItem, QMessageBox)
from PyQt5.QtGui import (QPainter, QIcon, QFont, QPixmap, QMouseEvent)
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5 import QtCore

from functools import partial

from chroma.ZoomWindow import ZoomWindow
from chroma.Cursor import CustomCursor
from chroma.Chroma import Chroma

# Translation
_t = QtCore.QCoreApplication.translate

class ExtendedQLabel(QLabel):
    mouseClicked = pyqtSignal(QMouseEvent)

    def __init__(self, parent):
        QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.mouseClicked.emit(ev)



class VerticalLabel(QLabel):
    """
    90° rotatated QLabel label class fpr vertical labeling
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedWidth(15)
        self.setFixedHeight(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QtCore.Qt.black)
        painter.translate(12, self.height()-1)
        painter.rotate(-90)

        if self.text():
            painter.drawText(0, 0, self.text())

        painter.end()

class MainGui(QMainWindow):
    def __init__(self, manager, parent=None):
        super().__init__(parent)

        # Save arguments
        self.m = manager

        # Create MainWindow
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        # Set fixed size
        self.centralwidget.setFixedHeight(823)
        self.centralwidget.setFixedWidth(1400)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1141, 25))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(False)
        self.setStatusBar(self.statusbar)

        # Bold Font
        boldFont = QFont()
        boldFont.setBold(True)

        # Main Widgets for fixed size settings
        self.topWg = QWidget()
        self.middleWg = QWidget()

        self.topWg.setFixedHeight(323)
        # self.topWg.setStyleSheet("QWidget { background-color: gray }")

        self.middleWg.setFixedHeight(500)
        # self.middleWg.setStyleSheet("QWidget { background-color: gray }")

        # Main Layout
        self.Level1_verticalLayout = QVBoxLayout(self.centralwidget)
        self.Level1_verticalLayout.setObjectName("verticalLayout")

        # Main Row Layouts
        self.Level2_horizontalLayout_top = QHBoxLayout(self.topWg)
        self.Level2_horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.Level2_horizontalLayout_middle = QHBoxLayout(self.middleWg)
        self.Level2_horizontalLayout_middle.setObjectName("horizontalLayout_middle")

        # Part 1
        # Checkbox Layout
        self.Level3_verticalLayout_checkboxes = QVBoxLayout()
        self.Level3_verticalLayout_checkboxes.setObjectName("verticalLayout_checkboxes")

        # Slider Layout
        self.Level3_verticalLayout_sliders = QVBoxLayout()
        self.Level3_verticalLayout_sliders.setObjectName("verticalLayout_sliders")

        # Chromosome Count Layout
        self.Level3_verticalLayout_count = QVBoxLayout()
        self.Level3_verticalLayout_count.setObjectName("verticalLayout_count")

        # Noise Slider
        self.Level4_horizontalLayout_noise = QHBoxLayout()
        self.Level4_horizontalLayout_noise.setObjectName("horizontalLayout_noise")

        self.Level4_horizontalLayout_noiseL = QHBoxLayout()
        self.Level4_horizontalLayout_noiseL.setObjectName("horizontalLayout_noiseL")

        # Threshold Slider
        self.Level4_horizontalLayout_thres = QHBoxLayout()
        self.Level4_horizontalLayout_thres.setObjectName("horizontalLayout_thres")

        self.Level4_horizontalLayout_thresL = QHBoxLayout()
        self.Level4_horizontalLayout_thresL.setObjectName("horizontalLayout_thresL")

        self.label_noise = QLabel(self.centralwidget)
        self.label_noise.setObjectName("label_noise")
        self.label_noise.setFont(boldFont)

        self.label_threshold = QLabel(self.centralwidget)
        self.label_threshold.setObjectName("label_threshold")
        self.label_threshold.setFont(boldFont)

        self.label_count = QLabel("0")
        self.label_count.setFont(boldFont)
        self.label_count.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_count.setAlignment(Qt.AlignCenter)

        self.label_chr_count = QLabel()
        self.label_chr_count.setFont(boldFont)
        self.label_chr_count.setAlignment(Qt.AlignCenter)

        self.Level3_verticalLayout_sliders.addWidget(self.label_noise)
        self.Level3_verticalLayout_sliders.addLayout(self.Level4_horizontalLayout_noiseL)
        self.Level3_verticalLayout_sliders.addLayout(self.Level4_horizontalLayout_noise)
        self.Level3_verticalLayout_sliders.addWidget(self.label_threshold)
        self.Level3_verticalLayout_sliders.addLayout(self.Level4_horizontalLayout_thresL)
        self.Level3_verticalLayout_sliders.addLayout(self.Level4_horizontalLayout_thres)

        # Part 2
        # Chromosome Chrom Layout
        widget = QWidget()
        widget.setFixedWidth(210)
        self.Level3_verticalLayout_chrom_left = QVBoxLayout(widget)
        self.Level3_verticalLayout_chrom_left.setObjectName("verticalLayout_chrom_left")
        self.Level3_verticalLayout_chrom_right = QVBoxLayout()
        self.Level3_verticalLayout_chrom_right.setObjectName("verticalLayout_chrom_right")
        self.Level4_horizontalLayout_chrom_right = QHBoxLayout()
        self.Level4_horizontalLayout_chrom_right.setObjectName("horizontalLayout_chrom_right")
        self.Level4_horizontalLayout_chrom_buttons = QHBoxLayout()
        self.Level4_horizontalLayout_chrom_buttons.setObjectName("horizontalLayout_chrom")
        self.Level2_horizontalLayout_middle.addWidget(widget)

        # Create Scroll Area
        scrollAreaContents = QWidget()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setWidget(scrollAreaContents)
        self.scrollArea.setWidgetResizable(True)

        # Inner Layout of ScrollAreaContents
        self.Level4_horizontalLayout_scroll = QHBoxLayout(scrollAreaContents)

        # Logo
        logo_path = os.path.join(self.m.app_path, "images", "acib.png")
        logo2_path = os.path.join(self.m.app_path, "images", "logo.png")


        self.label_logo = ExtendedQLabel(self)
        pixmap = QPixmap(logo_path)
        self.label_logo.setPixmap(pixmap)
        self.label_logo.mouseClicked.connect(self.m.open_acib_link)
        self.label_logo.setToolTip('<p style="white-space:pre"> Open <b>http://acib.at</b>')

        self.label_logo2 = ExtendedQLabel(self)
        pixmap = QPixmap(logo2_path)
        self.label_logo2.setPixmap(pixmap)


        # Optional, resize window to image size
        #self.resize(pixmap.width(), pixmap.height())


        # Create menubar and status line
        self.initMenubar()

        # Fill Gui
        self.initUI()

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.Level1_verticalLayout.addWidget(self.topWg)
        self.Level1_verticalLayout.addWidget(self.middleWg)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_t("MainWindow", "ChromaWizard"))
        self.label_noise.setText(_t("MainWindow", "Reduce noise"))
        self.label_threshold.setText(_t("MainWindow", "Set threshold"))
        self.label_chr_count.setText(_t("MainWindow", "Chromosome\nCount"))

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setWindowTitle('ChromaWizard')

        # Part 1
        self.checkBoxes = []
        self.sliders_threshold = []
        self.sliders_noise = []
        self.chr_ZWs = []

        image_path = os.path.join(self.m.app_path, "images", "chroma.png")

        # DAPI ZoomWindow Window
        self.ZW1 = ZoomWindow(image_path, self.centralwidget, (280, 280), "DAPI", zoom_slider_enabled=False, track_mouse_move=True)
        self.ZW1.setObjectName("ZW1")
        self.ZW1.zoomView.setCursor(CustomCursor(type="NEW").cursor)
        self.ZW1.scene.mouseLeftClicked.connect(self.m.load_next_channel)

        # Masking ZoomWindow Window
        self.ZW2 = ZoomWindow(image_path, self.centralwidget, (280, 280), "Masking", zoom_slider=False)
        self.ZW2.setObjectName("ZW2")
        self.ZW2.zoomView.setCursor(CustomCursor(type="NEW").cursor)
        self.ZW2.scene.mouseLeftClicked.connect(self.m.load_next_channel)

        # Selection ZoomWindow Window
        self.ZW3 = ZoomWindow(image_path, self.centralwidget, (280, 280), "Separation", zoom_slider=False, track_mouse_move=True)
        self.ZW3.setObjectName("ZW3")
        self.ZW3.zoomView.setCursor(CustomCursor(type="NEW").cursor)
        self.ZW3.scene.mouseLeftClicked.connect(self.m.load_next_channel)

        self.ZW1.add_sync(self.ZW2)
        self.ZW1.add_sync(self.ZW3)
        self.ZW2.add_sync(self.ZW3)

        sI = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.Level3_verticalLayout_checkboxes.addItem(sI)

        self.pb_clear_mask = QPushButton(_t("MainGui", "Clear\nmanual\nmask"))
        self.pb_clear_mask.clicked.connect(self.m.clear_button_clicked)
        self.pb_clear_mask.setEnabled(False)

        self.pb_next = QPushButton()
        self.pb_next.setEnabled(False)

        # Dynamically create comboboxes
        for index, channel in enumerate(self.m.config_channel_names):
            # Vertical Labels
            channel_name = _t("MainWindow",self.m.config.config.channel_names[channel])
            vL1 = VerticalLabel(self.centralwidget)
            vL1.setText(channel_name)
            vL2 = VerticalLabel(self.centralwidget)
            vL2.setText(channel_name)

            # Checkboxes
            cB = QCheckBox(self.centralwidget)
            cB.setEnabled(False)
            cB.setCheckable(True)
            cB.setObjectName("cB_{}".format(channel_name))
            cB.setText(channel_name)
            cB.cid = channel_name
            cB.stateChanged.connect(partial(self.m.checkBoxChanged, cB, index)) # with partial the reference itself is added
            self.checkBoxes.append(cB)
            self.Level3_verticalLayout_checkboxes.addWidget(cB)

            # Sliders Threshold
            sT = QSlider(self.centralwidget)
            sT.setEnabled(False)
            sT.setOrientation(QtCore.Qt.Vertical)
            sT.setObjectName("vS_threshold")
            sT.setMinimum(0)
            sT.setMaximum(255)
            sT.setSingleStep(1)
            sT.setPageStep(1)
            sT.cid = channel_name
            threshold_func = partial(self.m.threshold_changed, sT, index)
            #sT.valueChanged.connect(self.threshold_func)
            sT.sliderPressed.connect(partial(self.block_signal, sT, threshold_func))
            sT.sliderReleased.connect(partial(self.unblock_signal, sT, threshold_func))

            # Sliders Noise
            sN = QSlider(self.centralwidget)
            sN.setEnabled(False)
            sN.setOrientation(QtCore.Qt.Vertical)
            sN.setObjectName("vS_noise")
            sN.setMinimum(0)
            sN.setMaximum(20)
            sN.setSingleStep(1)
            sN.setPageStep(1)
            sN.cid = channel_name
            self.noise_func = partial(self.m.noise_changed, sN, index)
            sN.valueChanged.connect(self.noise_func)
            sN.sliderPressed.connect(partial(self.block_signal, sN, self.noise_func))
            sN.sliderReleased.connect(partial(self.unblock_signal, sN, self.noise_func))

            self.sliders_threshold.append(sT)
            self.sliders_noise.append(sN)

            self.Level4_horizontalLayout_noiseL.addWidget(vL1)
            self.Level4_horizontalLayout_noise.addWidget(sN)
            self.Level4_horizontalLayout_thresL.addWidget(vL2)
            self.Level4_horizontalLayout_thres.addWidget(sT)

            # Part 2
            # Chromosome Zoomwindows
            self.select_chromosome_cb = QComboBox()
            self.select_chromosome_cb.setFixedWidth(50)
            self.select_chromosome_cb.currentIndexChanged.connect(partial(self.m.combo_box_changed, self.select_chromosome_cb))

            if index == 0:
                ZW = ZoomWindow(image_path, self.centralwidget, (100, 150),
                                channel_name, zoom_slider=True, track_mouse_move=True)
            else:
                ZW = ZoomWindow(image_path, self.centralwidget, (100, 150),
                                channel_name, zoom_slider=False, track_mouse_move=True)

                for zw in self.chr_ZWs:
                    zw.add_sync(ZW)

            ZW.setEnabled(False)

            self.chr_ZWs.append(ZW)

        # Build Layout together
        self.Level2_horizontalLayout_top.addWidget(self.ZW1)
        self.Level2_horizontalLayout_top.addLayout(self.Level3_verticalLayout_checkboxes)
        self.Level2_horizontalLayout_top.addWidget(self.ZW2)
        self.Level2_horizontalLayout_top.addLayout(self.Level3_verticalLayout_sliders)
        self.Level2_horizontalLayout_top.addWidget(self.ZW3)
        self.Level2_horizontalLayout_top.addLayout(self.Level3_verticalLayout_count)

        self.Level3_verticalLayout_count.addWidget(self.label_chr_count)
        self.Level3_verticalLayout_count.addWidget(self.label_count)
        self.Level3_verticalLayout_count.addStretch(1)
        self.Level3_verticalLayout_count.addWidget(self.pb_next)

        self.Level3_verticalLayout_checkboxes.addStretch(1)
        self.Level3_verticalLayout_checkboxes.addWidget(self.pb_clear_mask)

        # Sliders Threshold Part2
        sT0 = QSlider(self.middleWg)
        sT0.setEnabled(False)
        sT0.setOrientation(QtCore.Qt.Horizontal)
        sT0.setObjectName("c0_hS_threshold0")
        sT0.setMinimum(0)
        sT0.setMaximum(255)
        sT0.setSingleStep(1)
        sT0.setPageStep(1)
        sT0.cid = "c0_hS_threshold0"
        sL = QLabel(_t("MainGui", "Threshold"))
        threshold_func = partial(self.m.chr_threshold_changed, sT0, 0)
        # sT0.valueChanged.connect(self.threshold_func)
        sT0.sliderPressed.connect(partial(self.block_signal, sT0, threshold_func))
        sT0.sliderReleased.connect(partial(self.unblock_signal, sT0, threshold_func))

        self.Level3_verticalLayout_chrom_left.addWidget(self.select_chromosome_cb)
        self.Level3_verticalLayout_chrom_left.addWidget(self.chr_ZWs[0])
        self.Level3_verticalLayout_chrom_left.addWidget(sL)
        self.Level3_verticalLayout_chrom_left.addWidget(sT0)

        # Add Scroll Area Layer
        self.Level3_verticalLayout_chrom_right.addWidget(self.scrollArea)

        self.ZW_karyotype = ZoomWindow(image_path, self.centralwidget, (500, 150),
                                _t("MainGui", "Karyotype"), zoom_slider=False, track_mouse_move=True)
        self.Level4_horizontalLayout_chrom_right.addWidget(self.ZW_karyotype)
        self.Level4_horizontalLayout_chrom_right.addStretch()
        self.Level4_horizontalLayout_chrom_right.addWidget(self.label_logo)

        self.Level3_verticalLayout_chrom_right.addLayout(self.Level4_horizontalLayout_chrom_right)

        self.button_flip = QPushButton(_t("MainGui", "Flip Chromosome"))
        self.button_flip.clicked.connect(self.m.flip_clicked)

        self.button_mv_left = QPushButton("<")
        self.button_mv_left.setMaximumWidth(20)
        self.button_mv_left.clicked.connect(self.m.move_left_clicked)

        self.button_mv_right = QPushButton(">")
        self.button_mv_right.setMaximumWidth(20)
        self.button_mv_right.clicked.connect(self.m.move_right_clicked)

        self.Level4_horizontalLayout_chrom_buttons.addWidget(self.button_flip)
        self.Level4_horizontalLayout_chrom_buttons.addWidget(self.button_mv_left)
        self.Level4_horizontalLayout_chrom_buttons.addWidget(self.button_mv_right)

        # Clear manual mask button channel 0 (DAPI)
        self.button_clear_mask = QPushButton(_t("MainGui", "Clear manual Mask"))
        self.button_clear_mask.clicked.connect(partial(self.m.clear_mask_clicked, self.chr_ZWs[0], 0))

        self.button_flip.setEnabled(False)
        self.button_clear_mask.setEnabled(False)
        self.button_mv_left.setEnabled(False)
        self.button_mv_right.setEnabled(False)

        # Remove DAPI channel from karyotype
        self.checkBox_rmDAPI = QCheckBox(_t("MainGui", "Remove DAPI channel"))

        self.Level3_verticalLayout_chrom_left.addWidget(self.button_clear_mask)
        self.Level3_verticalLayout_chrom_left.addLayout(self.Level4_horizontalLayout_chrom_buttons)
        self.Level3_verticalLayout_chrom_left.addWidget(self.checkBox_rmDAPI)

        self.Level3_verticalLayout_chrom_left.addStretch()
        self.Level3_verticalLayout_chrom_left.addWidget(self.label_logo2)

        self.chr_widgets = [sT0, sL, self.button_clear_mask]

        for index, ZW in enumerate(self.chr_ZWs[1:]):
            threshold_func = partial(self.m.chr_threshold_changed, sT, index + 1)
            sT = QSlider(self.scrollArea)
            sT.setEnabled(False)
            sT.setOrientation(QtCore.Qt.Horizontal)
            sT.setObjectName("c{}_hS_threshold".format(index + 1))
            sT.setMinimum(0)
            sT.setMaximum(255)
            sT.setSingleStep(1)
            sT.setPageStep(1)
            sT.cid = "c{}_hS_threshold".format(index + 1)
            sT.setMaximumWidth(170)
            sT.sliderPressed.connect(partial(self.block_signal, sT, threshold_func))
            sT.sliderReleased.connect(partial(self.unblock_signal, sT, threshold_func))

            sL = QLabel(_t("MainGui", "Threshold"))

            # Clear manual mask button channel 1-5
            bT = QPushButton(_t("MainGui", "Clear manual Mask"))
            bT.clicked.connect(partial(self.m.clear_mask_clicked, ZW, index + 1))

            self.chr_widgets.extend([sT, sL, bT])

            self.Level5_verticalLayout_c = QVBoxLayout()
            self.Level5_verticalLayout_c.addWidget(ZW)
            self.Level5_verticalLayout_c.addWidget(sL)
            self.Level5_verticalLayout_c.addWidget(sT)
            self.Level5_verticalLayout_c.addWidget(bT)
            self.Level5_verticalLayout_c.addStretch()

            self.Level4_horizontalLayout_scroll.addLayout(self.Level5_verticalLayout_c)

        for widget in self.chr_widgets:
            widget.setEnabled(False)

        self.Level2_horizontalLayout_middle.addLayout(self.Level3_verticalLayout_chrom_right)


    def initMenubar(self):
        # Menu.File
        self.newAction = QAction(QIcon(os.path.join(self.m.app_path, "icons", "window-new.svg")), _t("MainGui", '&New Project'), self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip(_t("MainGui", 'Restart application'))
        self.newAction.triggered.connect(self.restart)

        self.exitAction = QAction(QIcon(os.path.join(self.m.app_path,"icons","window-close.svg")), _t("MainGui", '&Exit'), self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip(_t("MainGui", 'Exit application'))
        self.exitAction.triggered.connect(self.close)

        self.addAction = QAction(QIcon(os.path.join(self.m.app_path,"icons", "list-add.svg")), _t("MainGui", 'Add &Channel'), self)
        self.addAction.setShortcut('Ctrl+C')
        self.addAction.setStatusTip(_t("MainGui", 'Add next channel'))
        self.addAction.triggered.connect(self.m.load_next_channel)

        self.saveAction = QAction(QIcon(os.path.join(self.m.app_path, "icons", "document-save.svg")), _t("MainGui", '&Save Project'), self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip(_t("MainGui", 'Save project'))
        self.saveAction.triggered.connect(self.m.save_project)

        self.saveAsAction = QAction(QIcon(os.path.join(self.m.app_path, "icons", "document-save-as.svg")), _t("MainGui", 'Save &Project as'), self)
        self.saveAsAction.setStatusTip(_t("MainGui", 'Save project as'))
        self.saveAsAction.triggered.connect(self.m.save_as_project)

        self.openAction = QAction(QIcon(os.path.join(self.m.app_path, "icons", "document-open.svg")), _t("MainGui", '&Open Project'), self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip(_t("MainGui", 'Open project'))
        self.openAction.triggered.connect(self.m.open_project)

        # Menu.Karyotype
        self.saveKaryoAction = QAction(QIcon(os.path.join(self.m.app_path, "icons", "karyotype.svg")), _t("MainGui", 'Save &Karyotype'), self)
        self.saveKaryoAction.setShortcut('Ctrl+K')
        self.saveKaryoAction.setStatusTip(_t("MainGui", 'Save karyotype to image'))
        self.saveKaryoAction.triggered.connect(self.m.save_karyotype)
        self.saveKaryoAction.setEnabled(False)

        # Menu.Legend
        self.legendAction = QAction(QIcon(os.path.join(self.m.app_path, "icons", "legend.svg")),
                                       _t("MainGui", 'Open &Legend'), self)
        self.legendAction.setShortcut('Ctrl+L')
        self.legendAction.setStatusTip(_t("MainGui", 'Open Chromosome Color Legend'))
        self.legendAction.triggered.connect(self.m.open_legend)

        self.aboutAction = QAction(_t("MainGui", '&About'), self)
        self.aboutAction.setShortcut('Ctrl+A')
        self.aboutAction.setStatusTip(_t("MainGui", 'Open About Dialog'))
        self.aboutAction.triggered.connect(self.m.about)
        # Get menu bar
        menubar = self.menuBar()

        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.addAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)

        self.karyoMenu = menubar.addMenu('&Karyotype')
        self.karyoMenu.addAction(self.saveKaryoAction)
        self.dialogMenu = menubar.addMenu('&Dialogs')
        self.dialogMenu.addAction(self.legendAction)
        self.aboutMenu = menubar.addMenu('&Help')
        self.aboutMenu.addAction(self.aboutAction)

        self.toolbar = self.addToolBar('ToolBar')
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.addAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.saveAsAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.saveKaryoAction)
        self.fileMenu.addSeparator()
        self.toolbar.addAction(self.legendAction)

        self.statusBar().showMessage(_t("MainGui", "Ready"))

    # These two functions speed up slider actions enormously
    # TODO: Find a better way to simply block the signal (blocking does not work now)
    def block_signal(self, slider, func):
        """
        Disconnect valueChanged signal while moving the slider
        :param slider:
        :param func:
        :return:
        """
        # Check if slider is already connected
        if slider.receivers(slider.valueChanged) > 0:
            # Disconnect signal to slot
            slider.valueChanged.disconnect()

    def unblock_signal(self, slider, func):
        """
        Connects signal again after slider is released
        :param slider:
        :param func:
        :return:
        """
        slider.valueChanged.connect(func)
        slider.valueChanged.emit(slider.value())

    def keyPressEvent(self, QKeyEvent):
        self.m.keyIsPressed(QKeyEvent)


    def restart(self):
        self.m.exit_code = self.m.EXIT_CODE_REBOOT
        self.close()

    def closeEvent(self, event):
        if self.m.exit_code == self.m.EXIT_CODE_REBOOT:
            reply = QMessageBox.question(self, 'Message', _t("MainGui", "Are you sure to restart?"),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.m.logger.info(_t("MainGui", "Restart application"))
                event.accept()

                # Re-init Manager
                self.m.__init__(self.m.args)

                # Create main objects
                self.m.gui = MainGui(self.m)
                self.m.chroma = Chroma(self.m)

                # Show Gui again
                self.m.gui.show()
            else:
                event.ignore()
        else:
            reply = QMessageBox.question(self, 'Message', _t("MainGui", "Are you sure to quit?"),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


