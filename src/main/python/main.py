import sys

from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtGui import QIcon, QPixmap

# from loginwindow import LoginWindow
from loginwindow import LoginWindow

# from PyQt5.QtWidgets import QApplication



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


if __name__ == '__main__':
    
    appctxt = MyApplicationContext()     # 1. Instantiate ApplicationContext

    window = LoginWindow(appctxt)
    window.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
