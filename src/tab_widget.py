from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QGroupBox, QGridLayout,
                             QLabel, QDoubleSpinBox, QSpacerItem,
                             QPushButton, QSpinBox)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as \
    FigureCanvas
from matplotlib.figure import Figure

import logging


class MplCanvas(FigureCanvas):
    """QWidget and FigureCanvasAgg.
    """

    def __init__(self):
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


class StandardMapTab(QWidget):
    """GUI class for the Standard map class.
    """

    def __init__(self, parent=None):
        super(StandardMapTab, self).__init__(parent)
        self.canvas = MplCanvas()
        self.canvas.mpl_connect('button_press_event', self.mousePress)
        layout = QGridLayout()
        layout.addWidget(self.canvas, 0, 0, 1, -1)
        self.setLayout(layout)

    def setMap(self, map):
        """Sets the map and perform UI setup.
        """
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
        self.layout().addWidget(group, 1, 0)

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
        """Update constants that are defined in the JSON file.
        """
        sender = self.sender()
        constant = sender.constant
        logging.info('Updating constant %s for map %s. New value %s',
                     constant, self.map.name, str(value))
        self.map.values[constant] = value

    def clearPlot(self):
        """Clears the plot.
        """
        self.canvas.axes.cla()
        self.canvas.draw()

    def draw(self):
        """Draws the new path from the map.
        """
        x, y = self.map.map()
        self.canvas.axes.plot(x, y, '.', ms=1.0)
        self.canvas.axes.set_xlim(0, self.map.mod)
        self.canvas.axes.set_ylim(0, self.map.mod)
        self.canvas.fig.tight_layout()
        self.canvas.draw()


class ImageMapTab(QWidget):
    """Widget that holds the plot area and other controls for maps, for which
    the inputs are matrices or images.

    Attributes:
        map (Map): Map object
    """
    def __init__(self, parent=None):
        super(ImageMapTab, self).__init__(parent)
        self.canvas = MplCanvas()
        self.canvas.mpl_connect('button_press_event', self.mousePress)
        layout = QGridLayout()
        layout.addWidget(self.canvas, 0, 0, 1, -1)
        self.setLayout(layout)
        self.AUTO_ITERATING = 0
        self.autoTimer = QTimer()
        self.autoTimer.timeout.connect(self.performIteration)
        self.iteration = 0

    def setMap(self, map):
        """Sets the map object and perform other UI setup.
        """
        logging.info('Setting map %s to ImageMapTab.', map.name)
        self.map = map
        self.updateLayout()
        self.draw(self.map.baseImage)

    def updateLayout(self):
        """Fills the user interfaces with control widgets.

        Attributes:
            timer (QPushButton): Starts the QTimer to start map iteration
            resize (QSpinBox): Holds the resize value for resizing the image
            sizeLabel (QLabel): Current image dimension
        """
        self.timer = QPushButton('Auto iterate')
        self.timer.clicked.connect(self.setAutoMap)

        reset = QPushButton('Reset')
        reset.clicked.connect(self.reset)

        self.resize = QSpinBox()
        self.resize.setMinimum(10)
        self.resize.setMaximum(1000)

        resizePush = QPushButton('Resize')
        resizePush.clicked.connect(self.resizeImage)

        sizeLabel = QLabel('Size: ')
        self.sizeLabel = QLabel()
        self.sizeLabel.setNum(self.map.image.shape[0])
        iterationLabel = QLabel('Iteration: ')
        self.iterationLabel = QLabel()
        self.iterationLabel.setNum(self.iteration)

        self.layout().addWidget(self.timer, 1, 0, 1, -1)
        self.layout().addWidget(reset, 2, 0, 1, -1)
        self.layout().addWidget(self.resize, 3, 0)
        self.layout().addWidget(resizePush, 3, 1)
        self.layout().addWidget(sizeLabel, 3, 2)
        self.layout().addWidget(self.sizeLabel, 3, 3)
        self.layout().addWidget(iterationLabel, 3, 4)
        self.layout().addWidget(self.iterationLabel, 3, 5)

    def drawImage(self):
        pass

    @pyqtSlot()
    def performIteration(self):
        logging.info('Performing iteration for %s', self.map.name)
        self.map.map()
        self.draw(self.map.image)
        self.iteration += 1
        self.iterationLabel.setNum(self.iteration)

    def draw(self, img):
        logging.info('Drawing image for %s', self.map.name)
        self.canvas.axes.cla()
        self.canvas.axes.imshow(img)
        self.canvas.axes.axis('off')
        self.canvas.fig.tight_layout()

        self.canvas.draw()

    def mousePress(self, e):
        """Manually starts the next iteration.
        """
        self.performIteration()

    def setAutoMap(self):
        """Automatically call iterations.
        """
        if self.AUTO_ITERATING:
            logging.info('Auto iteration stopped')
            self.timer.setText('Auto iterate')
            self.AUTO_ITERATING = 0
            self.autoTimer.stop()
            return
        logging.info('Auto iteration started')
        self.AUTO_ITERATING = 1
        self.autoTimer.start(1000)
        self.timer.setText('Stop iteration')

    def reset(self):
        """Reset to original figure
        """
        logging.info('Reseting to original image for map %s', self.map.name)
        self.map.reset()
        self.sizeLabel.setNum(self.map.image.shape[0])
        self.draw(self.map.image)

        self.iteration = 0
        self.iterationLabel.setNum(0)

    def resizeImage(self):
        """Resizes the original image to a new image and draws it immediately.
        The new size value is received from :attr:`resize` QSpinBox.
        """
        logging.info('Resizing image for map %s', self.map.name)

        value = self.resize.value()

        self.map.resize(value)
        self.sizeLabel.setNum(self.map.image.shape[0])
        self.draw(self.map.image)
