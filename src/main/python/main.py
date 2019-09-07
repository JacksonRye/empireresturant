import sys

from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                                                   cached_property)
from PyQt5.QtGui import QIcon

from loginwindow import LoginWindow


class MyApplicationContext(ApplicationContext):

    def __init__(self, *args, **kwargs):
        super(MyApplicationContext, self).__init__(*args, **kwargs)

    @cached_property
    def about_icon(self):
        return QIcon(self.get_resource('images/anchor.png'))


appctxt = MyApplicationContext()     # 1. Instantiate ApplicationContext
window = LoginWindow(appctxt)
window.show()
exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
sys.exit(exit_code)
