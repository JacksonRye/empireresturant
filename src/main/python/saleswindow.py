from PyQt5.QtWidgets import QMainWindow, QDialog, QFrame
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
    def __init__(self, username, context, *args, **kwargs):
        super(SalesWindow, self).__init__(*args, **kwargs)

        self.username = username
        self.context = context
        self.setupUi(self)
        self.actionLog_Out.triggered.connect(self.logout)
        self.closing_sales_button.clicked.connect(self.select_duration)

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
    number = 0

    def __init__(self, product, *args, **kwargs):
        super(CheckoutFrame, self).__init__(*args, **kwargs)

        self.number += 1
        self.name = product.name
        self.price = product.price
        self.qty = product.qty
        self.total = product.subtotal

        self.name_label.setText(self.name)
        self.price_label.setText(self.price)
        self.qty_line_edit.setText(self.qty)
        self.subtotal_label.setText(self.total)
