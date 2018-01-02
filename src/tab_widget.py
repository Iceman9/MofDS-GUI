from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QVBoxLayout, QGroupBox,
                             QGridLayout, QLabel, QDoubleSpinBox, QSpacerItem,
                             QPushButton)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as \
    FigureCanvas
from matplotlib.figure import Figure

import logging


class MplCanvas(FigureCanvas):
    """QWidget and FigureCanvasAgg.
    """

    def __init__(self, paren=None):
        # Figsize is default 4, 5
        self.fig = Figure(figsize=(4, 5), dpi=100)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()


class MyDoubleSpin(QDoubleSpinBox):
    def __init__(self, constant, parent=None):
        self.constant = constant
        super(MyDoubleSpin, self).__init__(parent)
        self.setSingleStep(0.05)


class MapTabWidget(QWidget):
    """This is a qwidget holding the matplotlib canvas widget and contains
    other interface widgets.
    """

    def __init__(self, parent=None):
        super(MapTabWidget, self).__init__(parent)

        self.canvas = MplCanvas(self)
        self.canvas.mpl_connect('button_press_event', self.mousePress)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def setMap(self, map):
        """Sets the map and do other setup.
        """
        logging.error('Empty map function')
        pass

    def draw(self):
        """Starts the drawing by first computing the next frame from Map
        object and then showing it in the matplotlib canvas area.
        """
        logging.error('Empty draw function!')
        pass


class StandardMapTab(MapTabWidget):
    def __init__(self, parent=None):
        super(StandardMapTab, self).__init__(parent)


    def setMap(self, map):
        logging.info('Setting map %s to StandardMapTab.', map.name)
        self.map = map
        self.updateLayout()

    def updateLayout(self):
        """Adds additional widgets for interactiveness
        """
        group = QGroupBox()
        group.setTitle('Controls')
        layout = QGridLayout()
        constants = self.map.constants
        i = 0
        for i, c in enumerate(constants):
            label = QLabel(c)
            doubleSpinBox = MyDoubleSpin(constant=c)
            doubleSpinBox.valueChanged.connect(self.updateConstant)
            layout.addWidget(label, i, 0)
            layout.addWidget(doubleSpinBox, i, 1)
            layout.addItem(QSpacerItem(40, 20, hPolicy=QSizePolicy.Expanding),
                           i, 2)

        clearPush = QPushButton('Clear')
        clearPush.clicked.connect(self.clearPlot)
        layout.addWidget(clearPush, i + 1, 3)

        group.setLayout(layout)
        self.layout().addWidget(group)

    def mousePress(self, event):
        """Get x,y position of the mouse in the plot. Usable only for
        standard maps
        """
        q, p = event.xdata, event.ydata
        self.updateInitValues(q, p)
        self.draw()

    def updateInitValues(self, q, p):
        """Update the initial p, q values if the map is a standard map.
        """

        logging.info('Setting initial values for next frame for map %s',
                     self.map.name)
        if q is None or p is None:
            logging.error('None values selected. You clicked on the outside'
                          ' of plot area. No updating of points')
            return
        logging.info('q: %s, p: %s', str(q), str(p))
        self.map.values['q'] = q
        self.map.values['p'] = p

    @pyqtSlot(float)
    def updateConstant(self, value):
        sender = self.sender()
        constant = sender.constant
        logging.info('Updating constant %s for map %s. New value %s',
                     constant, self.map.name, str(value))
        self.map.values[constant] = value

    def clearPlot(self):
        self.canvas.axes.cla()
        self.canvas.draw()

    def draw(self):
        x, y = self.map.map()
        self.canvas.axes.plot(x, y, '.', ms=1.0)
        self.canvas.axes.set_xlim(0, self.map.mod)
        self.canvas.axes.set_ylim(0, self.map.mod)
        self.canvas.fig.tight_layout()
        self.canvas.draw()



class ImageMapTab(MapTabWidget):
    def __init__(self, parent=None):
        super(ImageMapTab, self).__init__(parent)
        self.AUTO_ITERATING = 0
        self.autoTimer = QTimer()
        self.autoTimer.timeout.connect(self.draw)

    def setMap(self, map):
        logging.info('Setting map %s to ImageMapTab.', map.name)
        self.map = map
        self.updateLayout()

        self.canvas.axes.cla()
        self.canvas.axes.imshow(self.map.imageArray) # First show the orig img
        self.canvas.axes.axis('off')
        self.canvas.fig.tight_layout()
        self.canvas.draw()

    def updateLayout(self):
        pushTimer = QPushButton('Auto iterate')
        pushTimer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        pushTimer.clicked.connect(self.setAutoMap)

        self.layout().addWidget(pushTimer)

    def draw(self):
        logging.info('Drawing the next frame for %s', self.map.name)
        newImg = self.map.map()
        self.canvas.axes.cla()
        self.canvas.axes.imshow(newImg)
        self.canvas.axes.axis('off')
        self.canvas.fig.tight_layout()

        self.canvas.draw()

    def mousePress(self, e):
        self.draw()

    def setAutoMap(self):
        if self.AUTO_ITERATING:
            logging.info('Auto iteration stopped')
            self.AUTO_ITERATING = 0
            self.autoTimer.stop()
            return
        logging.info('Auto iteration started')
        self.AUTO_ITERATING = 1
        self.autoTimer.start(1000)
