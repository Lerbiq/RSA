from PyQt5.QtWidgets import *
from PyQt5 import uic

qtKeyGenFile = "ui/key_gen.ui"


class UiKeyGen(QWidget):

    def __init__(self, main):
        super().__init__()
        self.main_window = main
        uic.loadUi(qtKeyGenFile, self)
        self.buttonGenKey.clicked.connect(self.handle_gen_keys)

    def reset_and_show(self):
        self.spinBoxPrecision.setValue(self.spinBoxPrecision.minimum())
        self.show()

    def handle_gen_keys(self):
        self.main_window.gen_keys(self.spinBoxPrecision.value())



