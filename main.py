from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
import sys

from util.keys import Keys
import util.util as u
from windows.key_gen import UiKeyGen

qtMainFile = "ui/main.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMainFile)


class RSA(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.keys = None
        self.key_gen_window = None
        # self.radioButtonEncrypt.toggled.connect(self.handle_option_change)
        self.buttonOpenKeyGen.clicked.connect(self.open_key_gen)
        self.buttonDoStuff.clicked.connect(self.do_stuff)

        qregex = QRegExp("[0-9]*")
        self.lineEditPubN.setValidator(QRegExpValidator(qregex, self.lineEditPubN))
        self.lineEditPubE.setValidator(QRegExpValidator(qregex, self.lineEditPubE))
        self.lineEditPrivN.setValidator(QRegExpValidator(qregex, self.lineEditPrivN))
        self.lineEditPrivD.setValidator(QRegExpValidator(qregex, self.lineEditPrivD))

    def open_key_gen(self):
        if self.key_gen_window is None:
            self.key_gen_window = UiKeyGen(self)
        self.key_gen_window.reset_and_show()

    def gen_keys(self, precision):
        self.keys = Keys()
        self.keys.generate_keys(precision)
        n, e = self.keys.get_pub()
        self.lineEditPubN.setText(str(n))
        self.lineEditPubE.setText(str(e))
        n, d = self.keys.get_priv()
        self.lineEditPrivN.setText(str(n))
        self.lineEditPrivD.setText(str(d))

    def display_error(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Chyba")
        msg.setInformativeText(text)
        msg.setWindowTitle("Chyba")
        msg.exec_()

    def get_pub_from_ui(self):
        n = self.lineEditPubN.text()
        e = self.lineEditPubE.text()
        if n == "" or e == "":
            return None, None
        if not u.is_integer(n) or not u.is_integer(e):
            self.display_error("V klíči se nesmí vyskytovat jiné znaky než číslice!")
        return int(n), int(e)

    def get_priv_from_ui(self):
        n = self.lineEditPrivN.text()
        d = self.lineEditPrivD.text()
        if n == "" or d == "":
            return None, None
        if not u.is_integer(n) or not u.is_integer(d):
            self.display_error("V klíči se nesmí vyskytovat jiné znaky než číslice!")
        return int(n), int(d)

    def encrypt(self):
        n, e = 0, 0
        if self.keys is None:
            n, e = self.get_pub_from_ui()
            if n is None:
                self.display_error("Musíte nejprve zadat nebo vygenerovat veřejný klíč")
                return
        else:
            n, e = self.keys.get_pub()
        text = self.textEditInput.toPlainText()
        text_arr = [text[i:i+6] for i in range(0, len(text), 6)]
        bin_arr = []
        for i in range(0, len(text_arr)):
            bin_num = ""
            for char in text_arr[i]:
                bin_num += format(ord(char), '08b').rjust(11, "0")
            bin_arr.append(bin_num)
        if len(bin_arr[len(bin_arr)-1]) < 66:
            bin_arr[len(bin_arr) - 1] = bin_arr[len(bin_arr) - 1].rjust(66, "0")

        int_arr = []
        for bin_num in bin_arr:
            int_arr.append(int(bin_num, 2))

        cipher = []
        for int_num in int_arr:
            cipher.append(pow(int_num, e, n))

        string_cipher = []

        for cipher_num in cipher:
            string_cipher.append(str(cipher_num))
        self.textEditOutput.setPlainText(' '.join(string_cipher))

    def decrypt(self):
        n, d = 0, 0
        if self.keys is None:
            n, d = self.get_priv_from_ui()
            if n is None:
                self.display_error("Musíte nejprve zadat nebo vygenerovat veřejný klíč")
                return
        else:
            n, d = self.keys.get_priv()

        text = self.textEditInput.toPlainText()
        cipher_arr = text.split(" ")
        decrypted_nums = []
        for string_num in cipher_arr:
            if not u.is_integer(string_num):
                self.display_error(
                    "V části řetězce byl nalezen neočekávaný znak. Řetězec k rozšifrování se smí skládat pouze z "
                    "číslic a mezer.")
                return
            decrypted_nums.append(pow(int(string_num), d, n))
        bin_nums = []
        for num in decrypted_nums:
            bin_nums.append(bin(num)[2:].rjust(66, "0"))
        decrypted = ""
        for num in bin_nums:
            split = [num[i:i+11] for i in range(0, len(num), 11)]
            for char in split:
                dec = int(char, 2)
                if dec != 0:
                    decrypted += chr(dec)
        self.textEditOutput.setPlainText(decrypted)

    def do_stuff(self):
        if self.radioButtonEncrypt.isChecked():
            self.encrypt()
        elif self.radioButtonDecrypt.isChecked():
            self.decrypt()
        else:
            self.display_error("Nebyla vybrána žádná možnost!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RSA()
    window.show()
    sys.exit(app.exec_())
