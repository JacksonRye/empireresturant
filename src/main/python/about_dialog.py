from PyQt5.QtWidgets import QDialog

from ui_designs.Ui_about_dialog import Ui_Dialog


class AboutDialog(QDialog, Ui_Dialog):
    
    def __init__(self, context, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.context= context

        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.logo_label.setPixmap(self.context.about_logo)


    def show_about(self):
        self.exec_()
