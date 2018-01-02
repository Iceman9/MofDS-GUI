#!/usr/bin/env python3

"""This module visually represents maps.
"""
from PyQt5.QtWidgets import QTabWidget, QApplication, QMainWindow

import glob
import logging
import os
import json
import sys

import numpy as np
from PIL import Image

from maps import StandardMap, ImageMap
from tab_widget import StandardMapTab, ImageMapTab
from log import Log

def loadMaps():
    files = glob.glob('*.json')

    maps = []
    for f in files:
        if not os.access(f, os.F_OK | os.R_OK):
            logging.info('No reading access to %s', f)
        logging.info('Reading %s', f)
        with open(f, 'r') as f:
            jsonString = f.read()

        mapJson = json.loads(jsonString)
        TYPE = mapJson['type']
        logging.info('Creating map object of type %s', TYPE)

        if TYPE == 'standard':
            m = StandardMap()
            m.setMod(mapJson['mod'])
            m.setConstants(mapJson['constants'])
            m.setVariables(mapJson['variables'])

        elif TYPE == 'image':
            m = ImageMap()
            imageFile = mapJson['image']
            logging.info('Reading image %s', imageFile)
            img = Image.open(imageFile)
            img.load()

            imageArray = np.asarray(img, dtype="float32")
            img.close()
            dim = imageArray.shape
            if dim[0] != dim[1]:
                logging.info('Picture is NOT square!')
                continue
            logging.info('Setting image.')
            m.setImage(imageArray)

        else:
            logging.info('Unkown types: %s', TYPE)

        m.setName(mapJson['name'])
        m.setDescription(mapJson['description'])

        m.processFunctions(mapJson['functions'])

        logging.info('Loaded map of type %s and name %s', mapJson['type'],
                     mapJson['name'])
        maps.append(m)
    return maps

if __name__ == '__main__':

    app = QApplication(sys.argv)

    log = Log()  # Instancing log so every log is directed here and nothing to
                 # console.
    main = QMainWindow()
    tabWidget = QTabWidget()

    Maps = loadMaps()
    for m in Maps:
        type = m.type
        if type == 'standard':
            tab = StandardMapTab()
        else:
            tab = ImageMapTab()
        tab.setMap(m)
        tabWidget.addTab(tab, m.name)
    tabWidget.addTab(log, 'Log')

    main.setCentralWidget(tabWidget)
    main.show()

    sys.exit(app.exec_())