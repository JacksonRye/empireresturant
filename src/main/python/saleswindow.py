from PyQt5.QtWidgets import QMainWindow, QDialog, QFrame
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
import datetime
# import tempfile

from loginwindow import LoginWindow
from ui_designs.Ui_salewindow import Ui_MainWindow
from ui_designs.Ui_closingsalesdialog import Ui_Dialog
from ui_designs.Ui_checkout_widget import Ui_checkout_frame

from dbhandler import DBHandler


class SalesWindow(QMainWindow, Ui_MainWindow):
    """
    username:   current user login, whose name transactions
                will be carried on with

    context:    The Application context that controls the whole
                app and contains all resources
    """

    products_in_checkout = set()

    def __init__(self, username, context, *args, **kwargs):
        super(SalesWindow, self).__init__(*args, **kwargs)

        self.username = username
        self.context = context
        self.setupUi(self)
        self.actionLog_Out.triggered.connect(self.logout)
        self.closing_sales_button.clicked.connect(self.select_duration)
        self.populate_combobox()
        self.get_product_list()

        self.items_combobox.currentIndexChanged[str].\
            connect(self.add_to_checkout)
        self.done_button.clicked.connect(self.checkout)

    def logout(self):
        self.loginwindow = LoginWindow(self.context)
        self.loginwindow.show()
        self.hide()

    def checkout(self):
        self.perform_transaction()
        self.clear_screen()

    def select_duration(self):
        """Creates a dialog containg two datetime edit widgets"""

        dlg = ClosingSalesDialog(self.context, self.username, self)

        if dlg.exec_():
            print('Success!')
        else:
            print("Cancel!")

    def connect_database(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(self.context.get_database)
        db.open()

    def populate_combobox(self):
        self.connect_database()
        model = QSqlTableModel()
        model.setTable('products')
        column = model.fieldIndex('name')
        model.select()
        self.items_combobox.setModel(model)
        self.items_combobox.setModelColumn(column)

    def add_to_checkout(self, product_name):

        # check if product already in checkout
        for product in self.product_list:
            if not product.in_checkout:
                product.in_checkout = True
                self.products_in_checkout.add(product)
                self.add_create_product_layout(product)

                
    
    def add_create_product_layout(self, product):
        item = CheckoutFrame(product)
        item.no_label.setText(str(0))
        self.checkout_layout.addWidget(item)

# TODO: FIX Widgets positioning in checkout

    def update_database(self, product):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        with DBHandler(self.context.get_database) as cursor:
            update_SQL = """
                    UPDATE products SET 
                    quantity_in_stock = quantity_in_stock - ?
                    """

            insert_SQL = """
                            INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)
                        """
            
            cursor.execute(update_SQL, [product.quantity])
            cursor.execute(insert_SQL, [None, self.username, now, 
                            product.name, product.quantity, product.price])

            print('Success')
    
    def perform_transaction(self):
        for product in self.products_in_checkout:
            self.update_database(product)
            product.in_checkout = False
            product.quantity = 0
        

        
    def clear_screen(self):
        for product in self.products_in_checkout:
            product.in_checkout = False
        
        self.products_in_checkout.clear()
        


    def get_product_list(self):
        with DBHandler(self.context.get_database) as cursor:
            cursor.execute("SELECT * FROM products")
            results = cursor.fetchall()

            # Genexpr to get all items from database
            self.product_list = (self._Product(*value) for _, value in enumerate(results))

    class _Product:
        """
            This is a private class that holds attributes of
            each product.
            """

        def __init__(self, name, price, remaining_stock):
            self.name = name
            self.quantity = 0
            self.price = price
            self.remaining_stock = remaining_stock
            self.in_checkout = False

        @property
        def subtotal(self):
            return str(self.price * self.quantity)

        def __str__(self):
            return str(self.name)


class ClosingSalesDialog(QDialog, Ui_Dialog):

    """Dialog that show up when closing sales button is pressed.
        Allows user to selecting duration of closing and prints
        information concerning it."""

    def __init__(self, context, username, *args, **kwargs):
        super(ClosingSalesDialog, self).__init__(*args, **kwargs)

        self.context = context
        self.username = username
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        super().accept()

        # If you press 'Ok' button I'll run.
        from_ = self.from_datetime_edit
        to = self.to_datetime_edit

        from_date = from_.textFromDateTime(from_.dateTime())    # Starting date
        to_date = to.textFromDateTime(to.dateTime())            # Ending date
        print(from_date)

        # print('{} to {}'.format(from_date, to_date))

        with DBHandler(self.context.get_database) as cursor:

            cursor.execute("""SELECT product_name, sum(quantity_sold), sum(price)
                            FROM `orders` WHERE username= ? AND
                            `date` BETWEEN ? AND ?
                            GROUP BY product_name;""",

                            [self.username, from_date, to_date])

            result = cursor.fetchall()

            print(result)

            for _, values in enumerate(result):
                print(values)


class CheckoutFrame(QFrame, Ui_checkout_frame):
    """
        Widget to hold each product in the checkout

        product:    Instance of _Product class,
                    contains product metadata.
    """

    def __init__(self, product, *args, **kwargs):
        super(CheckoutFrame, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # self.number += 1
        self.name = product.name
        self.price = product.price
        self.quantity = product.quantity
        self.total = product.subtotal

        # self.no_label.setText(str(self.number))
        self.name_label.setText(self.name)
        self.price_label.setText(str(self.price))
        self.qty_line_edit.setText(str(self.quantity))
        self.subtotal_label.setText(str(self.total))
