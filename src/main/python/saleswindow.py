from ui_designs.Ui_salewindow import Ui_MainWindow
from loginwindow import LoginWindow
from PyQt5.QtWidgets import QMainWindow


class SalesWindow(QMainWindow, Ui_MainWindow):
    """
    username:   current user login, whose name transactions
                will be carried on with
    """
    def __init__(self, username, *args, **kwargs):
        super(SalesWindow, self).__init__(*args, **kwargs)

        self.username = username
        self.setupUi(self)
        self.actionLog_Out.triggered.connect(self.logout)

    def logout(self):
        self.loginwindow = LoginWindow()
        self.loginwindow.show()
        self.hide()
