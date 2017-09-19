from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import sys
import os
from design import Ui_MainWindow


# from PyQt5.QtGui import QDialog
# from ui_imagedialog import Ui_ImageDialog
#
# class ImageDialog(QDialog, Ui_ImageDialog):
#     def __init__(self):
#         super(ImageDialog, self).__init__()
#
#         # Set up the user interface from Designer.
#         self.setupUi(self)
#
#         # Make some local modifications.
#         self.colorDepthCombo.addItem("2 colors (1 bit per pixel)")
#
#         # Connect up the buttons.
#         self.okButton.clicked.connect(self.accept)
#         self.cancelButton.clicked.connect(self.reject)

class ExampleApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        self.btnBrowser.clicked.connect(self.browse_folder)  # When the button is pressed
                                                            # Execute browse_folder function

    def browse_folder(self):
        self.listWidget.clear() # In case there are any existing elements in the list
        directory = QFileDialog.getExistingDirectory(self,
                                                           "Pick a folder")
        # execute getExistingDirectory dialog and set the directory variable to be equal
        # to the user selected directory

        if directory: # if user didn't pick a directory don't continue
            for file_name in os.listdir(directory): # for all files, if any, in the directory
                self.listWidget.addItem(file_name)  # add file to the listWidget


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
