from PyQt5.QtWidgets import QMainWindow, QDialog, QFrame
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
# import datetime
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

        self.items_combobox.currentIndexChanged[str].connect(self.add_to_checkout)
        self.done_button.clicked.connect(self.get_product_list)


    def logout(self):
        self.loginwindow = LoginWindow(self.context)
        self.loginwindow.show()
        self.hide()

    def checkout(self):
        pass

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
        self.get_product_list()
        for product in self.product_list:
            if str(product) == product_name and str(product) not in self.products_in_checkout:
                product.is_active = True                
                self.products_in_checkout.add(str(product))
                item = CheckoutFrame(product)
                item.no_label.setText(str(0))
                self.checkout_layout.addWidget(item)
                print(product_name)

# TODO: FIX Widgets positioning in checkout

    def perform_transaction(self):
        pass

    def clear_screen(self):
        pass

    def get_product_list(self):
        with DBHandler(self.context.get_database) as cursor:
            cursor.execute("SELECT * FROM products")
            results = cursor.fetchall()

            self.product_list = (self._Product(*value) for _, value in enumerate(results))


    class _Product:

        def __init__(self, name, price, remaining_stock):
            self.name = name
            self.qty = 0
            self.price = price
            self.remaining_stock = remaining_stock
            self.is_active = False
            # self.subtotal = self.subtotal

        @property
        def subtotal(self):
            return str(self.price * self.qty)

        def __repr__(self):
            return self.__str__()

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
    
    # number = 0

    def __init__(self, product, *args, **kwargs):
        super(CheckoutFrame, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # self.number += 1
        self.name = product.name
        self.price = product.price
        self.qty = product.qty
        self.total = product.subtotal

        # self.no_label.setText(str(self.number))
        self.name_label.setText(self.name)
        self.price_label.setText(str(self.price))
        self.qty_line_edit.setText(str(self.qty))
        self.subtotal_label.setText(str(self.total))
