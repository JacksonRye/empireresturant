import sys

from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                                                   cached_property)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog

from ui_designs.Ui_about_dialog import Ui_Dialog


from loginwindow import LoginWindow


class MyApplicationContext(ApplicationContext):

    @cached_property
    def about_icon(self):
        return QIcon(self.get_resource('icons/anchor.png'))

    @cached_property
    def get_database(self):
        return self.get_resource('database/resturant_database.db')

    @cached_property
    def cancel_icon(self):
        return QIcon(self.get_resource('icons/cross-button.png'))

    @cached_property
    def logout_icon(self):
        return QIcon(self.get_resource('icons/control-power.png'))

    @cached_property
    def about_logo(self):
        return QPixmap(self.get_resource('icons/restaurant128.png'))

    @cached_property
    def window_icon(self):
        return QIcon(self.get_resource('icons/restaurant64.png'))

    @cached_property
    def get_about(self):
        return AboutDialog(self)

    def show_about(self):
        dlg = self.get_about

        if dlg.exec_():
            pass


class AboutDialog(QDialog, Ui_Dialog):

    def __init__(self, context, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.context= context

        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.logo_label.setPixmap(self.context.about_logo)


appctxt = MyApplicationContext()     # 1. Instantiate ApplicationContext

window = LoginWindow(appctxt)
window.show()

exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
sys.exit(exit_code)
