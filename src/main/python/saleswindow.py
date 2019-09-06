from ui_designs.Ui_salewindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow


class SalesWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username, *args, **kwargs):
        super(SalesWindow, self).__init__(*args, **kwargs)

        self.username = username
        self.setupUi(self)
