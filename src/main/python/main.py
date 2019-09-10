import sys

from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                                                   cached_property)
from PyQt5.QtGui import QIcon

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


appctxt = MyApplicationContext()     # 1. Instantiate ApplicationContext
window = LoginWindow(appctxt)
window.show()
exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
sys.exit(exit_code)
