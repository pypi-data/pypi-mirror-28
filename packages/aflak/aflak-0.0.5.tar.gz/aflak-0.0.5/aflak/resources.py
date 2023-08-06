import os
from pyqtgraph.Qt import QtGui


class AflakPixmap(QtGui.QPixmap):
    """
    Helper method to get QPixMap from PyQt
    """
    def __init__(self, path, *args, **kwargs):
        installDir = os.path.dirname(os.path.realpath(__file__))
        absolutePath = os.path.join(installDir, path)
        # QPixmap will not raise any error if the file does not exist
        # https://doc.qt.io/qt-5/qpixmap.html#QPixmap-4
        if not os.path.isfile(absolutePath):
            raise FileNotFoundError('%s not found!' % absolutePath)
        super().__init__(absolutePath, *args, **kwargs)
