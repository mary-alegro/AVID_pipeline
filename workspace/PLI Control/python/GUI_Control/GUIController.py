from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import os
from PLIControl import Ui_MainWindow
from SerialUtil import SerialUtil

class GuiController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        self.btnGo.clicked.connect(self.rotate_filters)
        self.btnHome.clicked.connect(self.go_home)

    def set_serialctrl(self, ser_obj):
        self.sutil = ser_obj

    def rotate_filters(self):
        self.sutil.do_rotation()
        doRead = True
        while doRead: #ugly busy wait  T_T
            line = self.sutil.read_line()
            pf = line[0:2]
            if pf == '**':
                log = line[2:]
                self.textStatus.append(log)
            elif line == SerialUtil.ACK_ROT:
                doRead = False
                print "Rotating executed"
            elif line == SerialUtil.ACK_MAX:
                doRead = False
                print "Maximum reached"


    def go_home(self):
        self.sutil.go_home()
        doRead = True
        while doRead: #ugly busy wait  T_T
            line = self.sutil.read_line()
            pf = line[0:2]
            if pf == '**':
                log = line[2:]
                self.textStatus.append(log)
            elif line == SerialUtil.ACK_HOME:
                doRead = False
                print "Filter position reseted"



    def browse_folder(self):
        self.listWidget.clear() # In case there are any existing elements in the list
        directory = QFileDialog.getExistingDirectory(self,
                                                           "Pick a folder")
        # execute getExistingDirectory dialog and set the directory variable to be equal
        # to the user selected directory

        if directory: # if user didn't pick a directory don't continue
            for file_name in os.listdir(directory): # for all files, if any, in the directory
                self.listWidget.addItem(file_name)  # add file to the listWidget
