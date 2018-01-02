#!/usr/bin/env python3

"""Module that redirect module logging output to QPlainTextEdit
"""

from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import queue
import logging


class LoggingHandler(logging.Handler):
    def __init__(self, stream):
        super(LoggingHandler, self).__init__()
        self.stream = stream

    def emit(self, record):
        msg = self.format(record)
        if record.levelno == logging.DEBUG:
            self.stream.write('<font color="blue">' + msg + '</font>')
        elif record.levelno == logging.INFO:
            self.stream.write('<font color="orange">' + msg + '</font>')
        elif record.levelno == logging.WARNING:
            self.stream.write('<font color="blue">' + msg + '</font>')
        elif record.levelno == logging.ERROR:
            self.stream.write('<font color="red">' + msg + '</font>')
        else:  # logging.CRITICAL
            self.stream.write('<font color="magenta">' + msg + '</font>')


class WriteStream(object):
    """ The new Stream Object which replaces the default stream associated with
    sys.stdout and sys.stderr. This object just puts data in a queue!

    Arguments:
        queue (queue.Queue) : thread safe queue created for the stream
    """

    def __init__(self, queue):
        self.queue = queue

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, text):
        self.queue.put(text)


class LogReceiver(QObject):
    """ Receives log messages from Logging and sys.stdout.

    A QObject (to be run in a QThread) which sits waiting for data to come
    through a queue.Queue(). It blocks until data is available, and one it
    has got something from the queue, it sends it to the "MainThread"
    by emitting a Qt Signal.
    """
    logSignal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.logSignal.emit(text)


class Log(QPlainTextEdit):

    def __init__(self, parent=None, initiate=True):
        super(Log, self).__init__(parent)

        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        if initiate:
            self.initiate()

    def initiate(self):
        self.logThread = QThread()
        logQueue = queue.Queue()
        logStream = WriteStream(logQueue)

        self.logReceiver = LogReceiver(logQueue)

        self.logReceiver.logSignal.connect(self.appendHtml)
        self.logReceiver.moveToThread(self.logThread)
        self.logThread.started.connect(self.logReceiver.run)

        self.logThread.start()

        logHandler = LoggingHandler(logStream)
        logFormat = "%(asctime)s - %(levelname)s: %(message)s"
        logHandler.setFormatter(logging.Formatter(logFormat))

        logging.getLogger().addHandler(logHandler)

        logLevel = logging.INFO
        logging.getLogger().setLevel(logLevel)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QMainWindow
    import sys

    app = QApplication(sys.argv)
    main = QMainWindow()

    w = Log()

    main.setCentralWidget(w)
    main.show()

    logging.debug('Testing debug')
    logging.warning('Testing warning')
    logging.info('Testing info')
    logging.error('Testing error')
    logging.critical('Testing critical')

    sys.exit(app.exec_())
