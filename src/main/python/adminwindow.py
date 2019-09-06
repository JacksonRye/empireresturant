from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow

from loginwindow import LoginWindow
from ui_designs.Ui_adminwindow import Ui_MainWindow


class AdminWindow(QMainWindow, Ui_MainWindow):

    """
    Ui_MainWindow: Class containing widgets and their respective settings
    """
    def __init__(self, *args, **kwargs):
        super(AdminWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)      # create widgets from Ui_MainWindow
        self.load_tables()      # create tables from database
        self.actionLog_Out.triggered.connect(self.logout)

    def load_tables(self):
        self.connect_database()
        self.load_products_table()
        self.load_users_table()
        self.load_orders_table()

    def connect_database(self):
        # connection to database and open connection
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('resturant_database.db')
        db.open()

    def load_products_table(self):
        self.product_model = QSqlTableModel()
        self.product_model.setTable('products')
        self.product_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.product_model.select()

        self.product_table_view.setModel(self.product_model)

    def load_users_table(self):
        self.users_model = QSqlTableModel()
        self.users_model.setTable('users')
        self.users_model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.users_model.select()

        self.user_table_view.setModel(self.users_model)

    def load_orders_table(self):
        self.orders_model = QSqlTableModel()
        self.orders_model.setTable('orders')

        self.orders_model.select()

        self.orders_table_view.setModel(self.orders_model)

    def logout(self):
        self.loginwindow = LoginWindow()
        self.loginwindow.show()
        self.hide()
