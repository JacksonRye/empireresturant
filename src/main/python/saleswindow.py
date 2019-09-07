from PyQt5.QtWidgets import QMainWindow, QDialog

from loginwindow import LoginWindow
from ui_designs.Ui_salewindow import Ui_MainWindow
from ui_designs.Ui_closingsalesdialog import Ui_Dialog


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
        self.closing_sales_button.clicked.connect(self.select_duration)

    def logout(self):
        self.loginwindow = LoginWindow()
        self.loginwindow.show()
        self.hide()

    def select_duration(self):
        dlg = ClosingSalesDialog(self)
        
        from_ = dlg.from_datetime_edit        
        to = dlg.to_datetime_edit

        if dlg.exec_():
            from_date = from_.textFromDateTime(from_.dateTime())
            to_date = to.textFromDateTime(to.dateTime())

            print('{} to {}'.format(from_date, to_date))

        else:
            print("Cancel!")

class ClosingSalesDialog(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(ClosingSalesDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
