from PyQt5.QtWidgets import QMainWindow, QDialog, QFrame
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
import datetime
# import tempfile

from loginwindow import LoginWindow
from ui_designs.Ui_salewindow import Ui_MainWindow
from ui_designs.Ui_closingsalesdialog import Ui_Dialog
from ui_designs.Ui_product_frame import Ui_product_frame
from ui_designs.Ui_checkout_dialog import Ui_checkout_dialog

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
        self.get_product_list()
        
        self.actionLog_Out.triggered.connect(self.logout)
        self.closing_sales_button.clicked.connect(self.select_duration)
        self.populate_combobox()

        self.items_combobox.currentTextChanged.connect(self.add_to_checkout)
        self.done_button.clicked.connect(self.checkout)
        self.decorator_button.clicked.connect(self.calculate_total)



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

    def add_to_checkout(self, currenttext):
        # check if product already in checkout
        for product in self.product_list:
            if product.name == currenttext: 
                break
            
        self.process_product(product)

    def process_product(self, product):
        if not product.in_checkout:
            product.in_checkout = True
            self.products_in_checkout.add(product)
            self.add_create_product_layout(product)
   
    
    def add_create_product_layout(self, product):
        item = ProductFrame(product, self.context)
        item.no_label.setText(str(0))
        self.checkout_layout.addWidget(item)

    def calculate_total(self):
        self.total_label.setText(
            str(
                sum(product.subtotal for product in self.products_in_checkout)
                )
            )
        

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

        for i in reversed(range(self.checkout_layout.count())):
            self.checkout_layout.itemAt(i).widget().setParent(None)

        for product in self.products_in_checkout:
            reset(product)
        
        self.products_in_checkout.clear()
        self.total_label.setText(str('0'))
        


    def get_product_list(self):
        with DBHandler(self.context.get_database) as cursor:
            cursor.execute("SELECT * FROM products")
            results = cursor.fetchall()

            # Genexpr to get all items from database
            self.product_list = [self._Product(*value) for _, value in enumerate(results)]

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
            return self.price * self.quantity

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

    def get_results(self):

        # If you press 'Ok' button I'll run.
        from_ = self.from_datetime_edit
        to = self.to_datetime_edit

        from_date = from_.textFromDateTime(from_.dateTime())    # Starting date
        to_date = to.textFromDateTime(to.dateTime())            # Ending date

        with DBHandler(self.context.get_database) as cursor:

            cursor.execute("""SELECT product_name, sum(quantity_sold), sum(price)
                            FROM `orders` WHERE username= ? AND
                            `date` BETWEEN ? AND ?
                            GROUP BY product_name;""",

                            [self.username, from_date, to_date])

            result = cursor.fetchall()

            print(result)

            # for _, values in enumerate(result):
            #     print(values)



    def accept(self):
        super().accept()
        self.get_results()

class ProductFrame(QFrame, Ui_product_frame):
    """
        Widget to hold each product in the checkout

        product:    Instance of _Product class,
                    contains product metadata.
    """

    def __init__(self, product, context, *args, **kwargs):
        super(ProductFrame, self).__init__(*args, **kwargs)
        self.product = product
        self.context = context

        self.setupUi(self)
        self.delete_button.setIcon(self.context.cancel_icon)



        # self.no_label.setText(str(self.number))
        self.name_label.setText(self.product.name)
        self.price_label.setText(str(self.product.price))
        self.qty_line_edit.setText(str(self.product.quantity))
        self.subtotal_label.setText(str(self.product.subtotal))
        

        self.add_qty_btn.clicked.connect(self.add_quantity)
        self.sub_qty_btn.clicked.connect(self.sub_quantity)
        self.delete_button.clicked.connect(self.remove_product)

    def add_quantity(self):
        self.product.quantity += 1
        self.update_price_label()

    def sub_quantity(self):
        if self.product.quantity > 0:
            self.product.quantity -= 1
            self.update_price_label()

    def update_price_label(self):
        self.qty_line_edit.setText(str(self.product.quantity))
        self.subtotal_label.setText(str(self.product.subtotal))

    def remove_product(self):
        reset(self.product)
        self.deleteLater()
        self.setParent(None)


def reset(product):
    product.in_checkout = False
    product.quantity = 0


class CheckoutConfirmationDialog(QDialog, Ui_checkout_dialog):

    def __init__(self, *args, **kwargs):
        super(CheckoutConfirmationDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)