from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QLabel
from PyQt5 import uic
import sys
import random

import util
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



    def debug(self, text):
        if self.checkBoxDebug.isChecked():
            print(text)

    def display_error(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Chyba")
        msg.setInformativeText(text)
        msg.setWindowTitle("Chyba")
        msg.exec_()


    def encrypt(self):
        if self.keys == None:
            self.display_error("Musíte nejprve zadat veřejný klíč")
            return
        text = self.textEditInput.toPlainText()
        normalized = u.normalize_text(text)
        text_arr = [normalized[i:i+6] for i in range(0, len(normalized), 6)]
        bin_arr = []
        for i in range(0, len(text_arr)):
            bin_num = ""
            for char in text_arr[i]:
                bin_num += format(ord(char), '08b').rjust(11, "0")
            bin_arr.append(bin_num)
        if len(bin_arr[len(bin_arr)-1]) < 66:
            bin_arr[len(bin_arr) - 1] = bin_arr[len(bin_arr) - 1].rjust(66, "0")

        print(bin_arr)


        int_arr = []
        for bin_num in bin_arr:
            int_arr.append(int(bin_num, 2))

        print(int_arr)

        n, e = self.keys.get_pub()

        cipher = []
        for int_num in int_arr:
            cipher.append(pow(int_num, e, n))

        string_cipher = []

        for cipher_num in cipher:
            string_cipher.append(str(cipher_num))
        print("Cipher text: " + ' '.join(string_cipher))
        self.textEditOutput.setPlainText(' '.join(string_cipher))

    def decrypt(self):
        print("Decrypt")
        if self.keys == None:
            self.display_error("Musíte nejprve zadat soukromý klíč")
            return

        text = self.textEditInput.toPlainText()
        cipher_arr = text.split(" ")
        print(cipher_arr)
        n, d = self.keys.get_priv()
        decrypted_nums = []
        for string_num in cipher_arr:
            if not u.is_integer(string_num):
                self.display_error(
                    "V části řetězce byl nalezen neočekávaný znak. Řetězec k rozšifrování se smí skládat pouze z číslic a mezer.")
                return
            decrypted_nums.append(pow(int(string_num), d, n))
        print("Decrypted nums: " + str(decrypted_nums))
        bin_nums = []
        for num in decrypted_nums:
            bin_nums.append(bin(num)[2:].rjust(66, "0"))

        print("Bin nums: " + str(bin_nums))



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
