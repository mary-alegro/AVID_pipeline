from GUIController import GuiController
from PyQt5.QtWidgets import QApplication
import sys
from SerialUtil import SerialUtil


def main():

    sutil = SerialUtil()
    ports = sutil.get_devices()
    sutil.connect(ports[1].device)

    app = QApplication(sys.argv)  # A new instance of QApplication
    form = GuiController()  # We set the form to be our ExampleApp (design)
    form.set_serialctrl(sutil)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function