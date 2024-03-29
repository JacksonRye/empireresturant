from PyQt5.QtWidgets import QMainWindow, QDialog, QFrame, QTextEdit
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5 import QtPrintSupport
from PyQt5.QtCore import QDateTime

import datetime
# import tempfile

from loginwindow import LoginWindow
from ui_designs.Ui_salewindow import Ui_MainWindow
from ui_designs.Ui_closingsalesdialog import Ui_Dialog
from ui_designs.Ui_product_frame import Ui_product_frame
from ui_designs.Ui_checkout_dialog import Ui_checkout_dialog
from about_dialog import AboutDialog

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
        self.setWindowIcon(self.context.window_icon)
        self.get_product_list()

        self.username_label.setText(self.username.title())
        self.actionLog_Out.setIcon(self.context.logout_icon)
        self.actionAbout.setIcon(self.context.about_icon)
        self.actionAbout.triggered.connect(self.show_about)
        
        self.actionLog_Out.triggered.connect(self.logout)
        self.closing_sales_button.clicked.connect(self.select_duration)
        self.populate_combobox()

        self.items_combobox.currentTextChanged.connect(self.add_to_checkout)
        self.done_button.clicked.connect(self.checkout)

    
    def show_about(self):
        dlg = AboutDialog(self.context, self)
        dlg.exec_()

    def logout(self):
        self.loginwindow = LoginWindow(self.context)
        self.loginwindow.show()
        self.hide()

    def checkout(self):
        dlg = CheckoutConfirmationDialog(self)

        if dlg.exec_():
            self.perform_transaction()
            self.clear_screen()
            print('Success')
        else:
            print('Cancel')

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
        item = ProductFrame(product, self.context, self)
        item.no_label.setText(str(0))
        self.checkout_layout.addWidget(item)

    def calculate_total(self):
        self.total_label.setText(
            str(
                sum(product.subtotal for product in self.products_in_checkout)
                )
            )
        

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
                            product.name, product.quantity, product.subtotal])

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
        self.set_date()
        self.editor = QTextEdit()

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def set_date(self):
        now = QDateTime.currentDateTime()

        # If you press 'Ok' button I'll run.

        self.from_datetime_edit.setDateTime(now)
        self.to_datetime_edit.setDateTime(now)

    def get_results(self):

        from_ = self.from_datetime_edit
        to = self.to_datetime_edit


        # from_.setDateTime(now)

        # to = to.dateTimeFromText(now)



        from_date = from_.textFromDateTime(from_.dateTime())    # Starting date
        to_date = to.textFromDateTime(to.dateTime())            # Ending date

        with DBHandler(self.context.get_database) as cursor:

            cursor.execute("""SELECT product_name, sum(quantity_sold), sum(price)
                            FROM `orders` WHERE username= ? AND
                            `date` BETWEEN ? AND ?
                            GROUP BY product_name;""",

                            [self.username, from_date, to_date])

            products_result = cursor.fetchall()


            cursor.execute("""SELECT sum(price)
                            FROM `orders` WHERE username = ? 
                            AND `date` BETWEEN ? AND ?""",
                            
                            [self.username, from_date, to_date])        

            total_result = cursor.fetchone()


            # print(products_result)

            return products_result, total_result

            # cursor.execute()

            # for _, values in enumerate(result):
            #     print(values)



    def accept(self):
        super().accept()
        products_result, total_result = self.get_results()

        for values in products_result:
            name, quantity, total = values

            line = f"{name[:8]:-<10}{quantity:-^5}{total:->5}"
            self.editor.append(line)

        self.editor.append('Total:{:->25}'.format(str(total_result)))

        self.handle_preview()


    def handle_preview(self):
        dlg = QtPrintSupport.QPrintPreviewDialog()
        dlg.paintRequested.connect(self.editor.print_)
        dlg.exec_()



class ProductFrame(QFrame, Ui_product_frame):
    """
        Widget to hold each product in the checkout

        product:    Instance of _Product class,
                    contains product metadata.
    """

    def __init__(self, product, context, root, *args, **kwargs):
        super(ProductFrame, self).__init__(*args, **kwargs)
        self.product = product
        self.context = context
        self.saleswindow = root

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
        self.saleswindow.calculate_total()

    def remove_product(self):
        reset(self.product)
        self.deleteLater()
        self.setParent(None)
        self.update_price_label()


def reset(product):
    product.in_checkout = False
    product.quantity = 0


class CheckoutConfirmationDialog(QDialog, Ui_checkout_dialog):

    def __init__(self, *args, **kwargs):
        super(CheckoutConfirmationDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.editor = QTextEdit()

    def accept(self):
        super().accept()
        # self.editor.append("{:<10}|{:^2}|{:>4}".format("Product", "Qty", "Total"))
        
        for product in SalesWindow.products_in_checkout:
            if product.quantity >= 1:
                Header = f"{product.name[:8]:-<10}{product.quantity:-^2}{product.subtotal:->4}"
                self.editor.append(Header)


        self.editor.append("\nTotal:{:->22}".format(str(
                sum(
                    product.subtotal for product in SalesWindow.products_in_checkout
                )
            )))
        
        
        self.handle_preview()
        
    def create_checkout_receipt(self):
        pass

    def handle_print(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.editor.document().print_(dialog.printer())
    
    def handle_preview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()