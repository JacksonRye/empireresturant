from Ui_loginwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from dbhandler import DBHandler
from adminwindow import AdminWindow


class LoginWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.login_button.clicked.connect(self.authenticate_user)

    def authenticate_user(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        with DBHandler() as cursor:
            find_user_query = """
            SELECT priviledge FROM users WHERE
            username = ? AND password = ?
            """

            cursor.execute(find_user_query, [username, password])

            results = cursor.fetchone()

        try:
            if results[0] == 0:
                print('cashier')

            if results[0] == 1:
                self.adminwindow = AdminWindow()
                self.adminwindow.show()
                self.hide()

        except TypeError:
            print('User Not Found')
