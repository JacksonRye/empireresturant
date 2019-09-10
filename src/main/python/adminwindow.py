from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow

from loginwindow import LoginWindow
from ui_designs.Ui_adminwindow import Ui_MainWindow


class AdminWindow(QMainWindow, Ui_MainWindow):

    """
    Ui_MainWindow:  Class containing widgets and their respective settings
    context:        This is the overall application context, containing
                    resources used through out the app.

    Seriously aren't the variable names and function names intuitive enough?
    """

    def __init__(self, context, *args, **kwargs):
        super(AdminWindow, self).__init__(*args, **kwargs)
        
        self.context = context
        self.setupUi(self)      # create widgets from Ui_MainWindow
        self.load_tables()      # create tables from database

        self.actionAbout.setIcon(self.context.about_icon)
        self.actionLog_Out.setIcon(self.context.logout_icon)
        self.actionLog_Out.triggered.connect(self.logout)

        self.add_product_button.clicked.connect(self.add_product)
        
        self.delete_product_button.clicked.connect(lambda: self.product_model.removeRow(
            self.product_table_view.currentIndex().row()))

        self.add_user_button.clicked.connect(self.add_user)

        self.delete_user_button.clicked.connect(
            lambda: self.users_model.removeRow(
                self.user_table_view.currentIndex().row()
        ))

    def load_tables(self):
        self.connect_database()
        self.load_products_table()
        self.load_users_table()
        self.load_orders_table()

    def connect_database(self):
        # connection to database and open connection
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(self.context.get_database)
        db.open()

    def load_products_table(self):
        # The model used by the view
        self.product_model = QSqlTableModel()
        self.product_model.setTable('products')
        self.product_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.product_model.select()

        # Use the product model as the model. MV programming
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
        # Go to login window
        self.loginwindow = LoginWindow(context=self.context)
        self.loginwindow.show()
        self.hide()

    def add_product(self):
        self.product_model.insertRows(self.product_model.rowCount(), 1)

    def add_user(self):
        self.users_model.insertRows(self.users_model.rowCount(), 1)