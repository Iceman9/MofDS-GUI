from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot

import logging
import parser
import numpy as np
from scipy.misc import imresize

TRIFUNC = ['sin', 'cos']


class Map(QObject):
    """Base class for map.

    Attributes:
        name (str): Name of map for representation or short description
        description (str): Longer description about the map
        mod (float): Modulus number
        steps (int): Number of iterations to perform. Default 1000
        variables (list): A list of variables to calculate
        constants (list): A list of constants the user can change
        values (dict): A dictionary of values corresponding to the variables
            and constants
        functions (dict): A dictionary of compiled functions that calculate the
            next values
    """

    def __init__(self, parent=None):
        super(Map, self).__init__(parent)
        self.mod = 0.0
        self.name = ''
        self.description = ''
        self.steps = 1000
        self.variables = []
        self.constants = []
        self.values = {}
        self.functions = {}

    @pyqtSlot(str)
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    NAME = pyqtProperty(str, getName, setName)

    @pyqtSlot(str)
    def setDescription(self, desc):
        self.description = desc

    def getDescription(self):
        return self.description

    DESCRIPTION = pyqtProperty(str, getDescription, setDescription)

    @pyqtSlot(float)
    def setMod(self, mod):
        self.mod = mod

    def getMod(self):
        return self.mod

    MOD = pyqtProperty(float, getMod, setMod)

    def processFunctions(self, funcs):
        """Process the functions string in order that the variables are
        first replaced with self.variables['name_of_variable']. The name
        for variables should be unique, i.e., avoid using c,o,s,i,n, as these
        are used in other mathematical functions.
        """
        logging.info('Parsing functions.')
        for function in funcs:
            funcStr = funcs[function]
            logging.info('Function for variable %s: %s', function, funcStr)

            # Replacing variables, i.e, q -> self.values['q']
            # Also replacing sin as np.sin, and other trigonometry functions

            for V in self.variables:
                funcStr = funcStr.replace(V, 'self.values["' + V + '"]')
            for V in self.constants:
                funcStr = funcStr.replace(V, 'self.values["' + V + '"]')

            # Basic trigonometry functions
            for F in TRIFUNC:
                funcStr = funcStr.replace(F, 'np.' + F)

            # Parsing the function string as an expression
            eq = parser.expr(funcStr)

            # Check if the function string is REALLY an expression and not
            # some strange import os; os.system("rm -rf /home")
            # ... hopefully
            if not eq.isexpr():
                logging.error('String %s is not an expression!', funcStr)
                return

            # Compile into python object
            obj = eq.compile()
            logging.info('Successfully compiled %s for %s', funcStr, function)
            self.functions[function] = obj

    def map(self):
        """Virtual function to calculate the next frame of the map. Hardcoded
        to return two arrays, i.e., X and Y.
        """
        return None


class StandardMap(Map):
    """Standard map as in the usual maps in q, p.
    """

    def __init__(self, parent=None):
        super(StandardMap, self).__init__(parent)
        self.type = 'standard'

    def setVariables(self, list):
        self.variables = list
        for var in self.variables:
            self.values[var] = 0.0

    def setConstants(self, list):
        self.constants = list
        for var in self.constants:
            self.values[var] = 0.0

    def map(self):
        """Calculating the next points and values.

        The current values are stored in :attr:`self.values`
        """

        # Create arrays
        logging.info('Calculating the next frame for "%s"', self.name)
        q = np.zeros(self.steps, dtype=np.float64)
        p = np.zeros(self.steps, dtype=np.float64)

        q[0] = self.values['q']
        p[0] = self.values['p']

        for i in range(1, self.steps):

            self.values['q'] = eval(self.functions['q']) % self.mod
            self.values['p'] = eval(self.functions['p']) % self.mod

            q[i] = self.values['q']
            p[i] = self.values['p']

        return q, p


class ImageMap(Map):
    """Maps that play with positional indexes in a NxN (square) image.

    Attributes:
        baseImage (ndarray): Original image (Matrix with shape (N, N, 3))
        image (ndarray): Image of current state (map iterations, resizes...)
    """

    def __init__(self, parent=None):
        super(ImageMap, self).__init__(parent)
        self.type = 'image'
        self.baseImage = None
        self.image = None
        self.shape = (0)

    def setBaseImage(self, img):
        """Sets the original image or matrix.
        """
        self.baseImage = img

        self.setImage(self.baseImage)


    def setImage(self, img):
        """Sets a new image to the :attr:`image`. There are two copies of the
        image or matrix. An original one and the one on which we perform
        transformations.

        Also the modulus value is set to the new size of the image.
        """
        self.image = np.array(img, copy=True)
        self.shape = self.image.shape
        self.setMod(self.shape[0]) # Setting mod to the size or matrix.

    def map(self):
        """Perform the mapping on the current image. This means "shifting" the
        indexes of each pixel around as set in the json file.
        The attribute :attr:`image` is being changed.

        Returns nothing as changes are done to the :attr:`image`.
        """
        newImage = np.zeros(self.shape, dtype=np.uint8)
        for i in range(self.mod):
            for j in range(self.mod):
                x, y = i, j
                new_X = eval(self.functions['x']) % self.mod
                new_Y = eval(self.functions['y']) % self.mod
                newImage[i][j] = self.image[new_X][new_Y]

        self.image = newImage

    def resize(self, newSize):
        """Change the dimension of the image. In this case the argument is the
        new size of the image matrix.

        The resize is done on the original image, so as to not lose pixel
        information.

        Arguments:
            newSize (int): New size for resizing the image.
        """

        size = int((newSize / self.baseImage.shape[0]) * 100)

        self.setImage(imresize(self.baseImage, size))

    def reset(self):
        """Resets the attribute :attr:`image` to the original image.
        """
        self.setImage(self.baseImage)
