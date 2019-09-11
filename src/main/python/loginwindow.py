from PyQt5.QtWidgets import QMainWindow

from dbhandler import DBHandler
from ui_designs.Ui_loginwindow import Ui_MainWindow
from about_dialog import AboutDialog


class LoginWindow(QMainWindow, Ui_MainWindow):

    """
    context:    This is the Application instance responsible for running the
                whole app
    """

    def __init__(self, context, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)

        self.context = context
        self.setupUi(self)
        self.login_button.clicked.connect(self.authenticate_user)
        self.actionAbout.setIcon(self.context.about_icon)

        self.actionAbout.triggered.connect(self.show_about)

        self.setWindowIcon(self.context.window_icon)

    def show_about(self):
        dlg = AboutDialog(self.context, self)
        dlg.exec_()

    def authenticate_user(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        with DBHandler(self.context.get_database) as cursor:
            find_user_query = """
            SELECT priviledge FROM users WHERE
            username = ? AND password = ?
            """

            cursor.execute(find_user_query, [username, password])

            results = cursor.fetchone()

        try:
            if results[0] == 0:
                from saleswindow import SalesWindow
                # Create session and all activites will be recorded with `username`
                self.saleswindow = SalesWindow(username=username, context=self.context)
                self.saleswindow.show()
                self.hide()

            if results[0] == 1:
                from adminwindow import AdminWindow
                self.adminwindow = AdminWindow(context=self.context)
                self.adminwindow.show()
                self.hide()

        except TypeError as e:
            self.error_label.setText(str(e))
            # self.error_label.setText("Invalid Username / Password")
