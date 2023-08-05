from PyQt5.QtWidgets import (QWidget) #, QGraphicsScene, QToolTip, QPushButton, QApplication, QAction, qApp, QMessageBox)

import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QTransform, QFont
import math
import os

class QScene(QtWidgets.QGraphicsScene):
    # Create events for left and right click
    mouseLeftClicked = pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent, name='mouseLeftClicked')
    mouseRightClicked = pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent, name='mouseRightClicked')
    mouseWheelClicked = pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent, name='mouseWheelClicked')
    mouseLeftReleased = pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent, name='mouseLeftReleased')
    mouseRightReleased = pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent, name='mouseRightReleased')
    mouseWheelReleased = pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent, name='mouseWheelReleased')
    mouseMoved = pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent, name='mouseMoved')
    mouseWheel = pyqtSignal(QtWidgets.QGraphicsSceneWheelEvent, name='mouseWheel')

    def __init__(self, *args, **kwds):
        QtWidgets.QGraphicsScene.__init__(self, *args, **kwds)

    def mousePressEvent(self, ev):
        # Send left click signal
        if ev.button() == QtCore.Qt.LeftButton:
            self.mouseLeftClicked.emit(ev)

        # Send right click signal
        elif ev.button() == QtCore.Qt.RightButton:
            self.mouseRightClicked.emit(ev)

        elif ev.button() == QtCore.Qt.MidButton:
            self.mouseWheelClicked.emit(ev)

    def mouseReleaseEvent(self, ev):
        # Send left click signal
        if ev.button() == QtCore.Qt.LeftButton:
            self.mouseLeftReleased.emit(ev)

        # Send right click signal
        elif ev.button() == QtCore.Qt.RightButton:
            self.mouseRightReleased.emit(ev)

        elif ev.button() == QtCore.Qt.MidButton:
            self.mouseWheelReleased.emit(ev)

    def mouseMoveEvent(self, ev):
        self.mouseMoved.emit(ev)

    def wheelEvent(self, ev):
        self.mouseWheel.emit(ev)

        # Avoid scrolling
        ev.accept() # Event will not be propagte to parent

class ZoomWindow(QWidget):
    keyIsPressed = pyqtSignal(QtGui.QKeyEvent, name='keyIsPressed')
    keyIsReleased = pyqtSignal(QtGui.QKeyEvent, name='keyIsReleased')
    mouseEnter = pyqtSignal(QtGui.QEnterEvent, name='mouseEnter')
    mouseLeave = pyqtSignal(QtCore.QEvent, name='mouseLeave')

    def keyReleaseEvent(self, event):
        self.keyIsReleased.emit(event)

    def keyPressEvent(self, event):
        self.keyIsPressed.emit(event)

    def enterEvent(self, ev):
        self.mouseEnter.emit(ev)

    def leaveEvent(self, ev):
        self.mouseLeave.emit(ev)

    def __init__(self, image_path, parent=None, view_shape=(300, 300), label="Image", zoom_slider=True, zoom_slider_enabled=True, track_mouse_move=False):
        super().__init__(parent)

        self.app_path = os.path.dirname(os.path.realpath(__file__))
        self.view_shape = view_shape
        self.label = label
        self._sync = [self]
        self.zoom_slider = zoom_slider
        self._zooming = False
        self.f_scrollHValue = 0.0
        self.f_scrollVValue = 0.0

        # Run setup for qt5 designer widget
        self.setupUi(self)

        self.pix = None

        # Initiate ZoomWindow
        self.init(image_path)

        self.setEnabledZooming(zoom_slider_enabled)
        self.zoom = 1
        self.zoomView.setMouseTracking(track_mouse_move)

        # Aspect ratio between view and orig. image - tuple(y, x)
        self.scale_factor = None

    def init(self, image_path):
        if not self.zoom_slider:
            spacerItem = QtWidgets.QSpacerItem(self.l_zoom.geometry().width(), 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
            self.zoomSlider.setVisible(False)
            self.l_zoom.setVisible(False)
            self.verticalLayout_4.addItem(spacerItem)

        boldFont = QFont()
        boldFont.setBold(True)

        # Set size
        self.resize(self.view_shape[0] + 74, self.view_shape[1] + 42)

        self.setMinimumSize(QtCore.QSize(self.view_shape[0] + 79, self.view_shape[1] + 42))
        self.setMaximumSize(QtCore.QSize(self.view_shape[0] + 79, self.view_shape[1] + 42))

        # Set Title
        self.title.setText(self.label)
        self.title.setFont(boldFont)

        # Create transform matrix
        self.matrix = QTransform()

        # Create scene object
        self.scene = QScene(self)


        # Connect zoom slider to zooming function
        self.zoomSlider.valueChanged.connect(self.zooming)
        self.zoomView.verticalScrollBar().valueChanged.connect(self.sync_scrolling)
        self.zoomView.horizontalScrollBar().valueChanged.connect(self.sync_scrolling)

        self.updateImage(file=image_path)

        # Set scene in graphicsView
        self.zoomView.setScene(self.scene)

    def zooming(self, value):
        zoom = (value / 10) * min(self.scale_factor)  # Convert to float

        # Set new matrix for all synced ZoomWindows
        for ZW in self._sync:
            # Avoid multiple scrolling before zooming
            ZW._zooming = True

            # Reset and create scaling matrix
            ZW.matrix.setMatrix(zoom, 0, 0, 0, zoom, 0, 0, 0, 1)

            # Set updated matrix
            ZW.zoomView.setTransform(ZW.matrix)

            # Set zoom slider
            ZW.zoomSlider.valueChanged.disconnect(ZW.zooming)
            ZW.zoomSlider.setValue(value)
            ZW.zoomSlider.valueChanged.connect(ZW.zooming)

            ZW.zoom = value/10
            ZW._zooming = False

    def zoomingTo(self, rect):
        zoom = abs(min(self.view_shape[0] / rect.width(), self.view_shape[1] / rect.height())) / min(self.scale_factor)

        self.zoom = math.ceil(10 if zoom > 10 else zoom)

        self.zoomSlider.setValue(self.zoom * 10)

        self.scrollToHorizontral(int(rect.left() * (self.zoom * min(self.scale_factor))))
        self.scrollToVertical(int(rect.top() * (self.zoom * min(self.scale_factor))))

    def sync_scrolling(self, value):
        # Run only if not zooming
        if not self._zooming:
            # Scroll Iimage in all synced ZoomWindows
            for ZW in self._sync:
                # Only synced windows
                if ZW is not self:
                    vS = ZW.zoomView.verticalScrollBar()
                    hS = ZW.zoomView.horizontalScrollBar()

                    # Disconnect signal to avoid multi signal dispatching
                    hS.valueChanged.disconnect(ZW.sync_scrolling)
                    vS.valueChanged.disconnect(ZW.sync_scrolling)

                    vS.setValue(self.zoomView.verticalScrollBar().value())
                    hS.setValue(self.zoomView.horizontalScrollBar().value())

                    # Connect signal again
                    hS.valueChanged.connect(ZW.sync_scrolling)
                    vS.valueChanged.connect(ZW.sync_scrolling)

    def scrollHorizontral(self, value):
        hS = self.zoomView.horizontalScrollBar()
        hS.setValue(hS.value() - value)

    def scrollVertical(self, value):
        vS = self.zoomView.verticalScrollBar()
        vS.setValue(vS.value() - value)

    def scrollToHorizontral(self, value):
        self.zoomView.horizontalScrollBar().setValue(value)

    def scrollToVertical(self, value):
        self.zoomView.verticalScrollBar().setValue(value)

    def add_sync(self, zoomWindow):
        if zoomWindow not in self._sync:
            self._sync.append(zoomWindow)

            for ZW in self._sync:
                if self not in ZW._sync:
                    ZW.add_sync(self)

    def setEnabledZooming(self, enabled):
            self.zoomSlider.setEnabled(enabled)

    def loadImage(self, *, numpy=None, file=None):
        """Load new image and reset scene to fit to new size."""
        if file:
            self.img_orig = cv2.imread(file, 0)
        else:
            self.img_orig = numpy

        # Create image from numpy array
        if len(self.img_orig.shape) == 2:
            self.image = QtGui.QImage(self.img_orig, self.img_orig.shape[1], self.img_orig.shape[0],
                                      self.img_orig.strides[0], QtGui.QImage.Format_Grayscale8)  # Format_RGB888
        elif len(self.img_orig.shape) == 3:
            self.image = QtGui.QImage(self.img_orig, self.img_orig.shape[1], self.img_orig.shape[0],
                                      self.img_orig.strides[0],
                                      QtGui.QImage.Format_RGB888)  # QtGui.QImage.Format_RGB888)  # Format_RGB888

        # Remove old pixmap from scene
        self.scene.clear()

        # Create scene object
        #self.scene = QScene(self)

        self.zoomView.setSceneRect(0, 0, self.img_orig.shape[1], self.img_orig.shape[0])

        # Set scene in graphicsView
        #self.zoomView.setScene(self.scene)

        # Create Qpixmap from Qimage
        self.pix = QtGui.QPixmap(self.image)

        # Add QPixmap to scene
        self.scene.addPixmap(self.pix)

        # Get scale factor for image
        self.scale_factor = (self.view_shape[1] / self.img_orig.shape[0],
                             self.view_shape[0] / self.img_orig.shape[1])

        self.zooming(self.zoomSlider.value())

        return True

    def updateImage(self, *, numpy=None, file=None):
            if file is not None:
                self.img_orig = cv2.imread(file, 0)
            else:
                self.img_orig = numpy

            # Create image from numpy array
            if len(self.img_orig.shape) == 2:
                self.image = QtGui.QImage(self.img_orig, self.img_orig.shape[1], self.img_orig.shape[0],
                                          self.img_orig.strides[0], QtGui.QImage.Format_Grayscale8) # Format_RGB888
            elif len(self.img_orig.shape) == 3:
                self.image = QtGui.QImage(self.img_orig, self.img_orig.shape[1], self.img_orig.shape[0],
                                          self.img_orig.strides[0], QtGui.QImage.Format_RGB888)#QtGui.QImage.Format_RGB888)  # Format_RGB888

            # Create Qpixmap from Qimage
            self.pix = QtGui.QPixmap(self.image)

            # Add QPixmap to scene
            self.scene.addPixmap(self.pix)

            # Get scale factor for image
            self.scale_factor = (self.view_shape[1] / self.img_orig.shape[0],
                                 self.view_shape[0] / self.img_orig.shape[1])

            self.zooming(self.zoomSlider.value())

            return True

    def getImage(self, numpy=True):
        if numpy:
            return self.img_orig.copy()
        else:
            return self.pix.copy()

    def isMouseLeftClicked(self):
        return self.scene.isLeftMouseButtonDown

    def isMouseRigthClicked(self):
        return self.scene.isRightMouseButtonDown

    def isMouseWheelClicked(self):
        return self.scene.isWheelMouseButtonDown

    # Send keypress to keyIsPressed slot
    #def keyPressEvent(self, ev):
    #    self.keyIsPressed.emit(ev)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(330, 298)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(Form)
        self.title.setMinimumSize(QtCore.QSize(0, 18))
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.zoomView = QtWidgets.QGraphicsView(Form)
        self.zoomView.setObjectName("zoomView")
        self.horizontalLayout.addWidget(self.zoomView)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.l_zoom = QtWidgets.QLabel(Form)
        self.l_zoom.setMinimumSize(QtCore.QSize(50, 0))
        self.l_zoom.setMaximumSize(QtCore.QSize(50, 16777215))
        self.l_zoom.setObjectName("label")
        self.verticalLayout_4.addWidget(self.l_zoom)
        self.zoomSlider = QtWidgets.QSlider(Form)
        self.zoomSlider.setMinimumSize(QtCore.QSize(30, 0))
        self.zoomSlider.setMinimum(10)
        self.zoomSlider.setMaximum(100)
        self.zoomSlider.setSingleStep(1)
        self.zoomSlider.setPageStep(1)
        self.zoomSlider.setOrientation(QtCore.Qt.Vertical)
        self.zoomSlider.setObjectName("zoomSlider")
        self.verticalLayout_4.addWidget(self.zoomSlider)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.title.setText(_translate("Form", "TextLabel"))
        self.l_zoom.setText(_translate("Form", "Zoom"))





