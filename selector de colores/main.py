import sys
import pyperclip as clipboard
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Selector de color")
        self.setWindowIcon(QIcon("color_select.png"))
        
        self.value = 0
        self.BG_rojo_hex = "0x00"
        self.BG_verde_hex = "0x00"
        self.BG_azul_hex = "0x00"
        self.BG_color = "#000000"
        self.FG_rojo_hex = "0xFF"
        self.FG_verde_hex = "0xFF"
        self.FG_azul_hex = "0xFF"
        self.FG_color = "#FFFFFF"

        self.SB_BG_Rojo.valueChanged.connect(lambda: self.__value_bg_sb_changed("R"))
        self.SB_BG_Verde.valueChanged.connect(lambda: self.__value_bg_sb_changed("G"))
        self.SB_BG_Azul.valueChanged.connect(lambda: self.__value_bg_sb_changed("B"))
        self.SL_BG_Rojo.valueChanged.connect(lambda: self.__value_bg_sl_changed("R"))
        self.SL_BG_Verde.valueChanged.connect(lambda: self.__value_bg_sl_changed("G"))
        self.SL_BG_Azul.valueChanged.connect(lambda: self.__value_bg_sl_changed("B"))
        
        self.SB_FG_Rojo.valueChanged.connect(lambda: self.__value_fg_sb_changed("R"))
        self.SB_FG_Verde.valueChanged.connect(lambda: self.__value_fg_sb_changed("G"))
        self.SB_FG_Azul.valueChanged.connect(lambda: self.__value_fg_sb_changed("B"))
        self.SL_FG_Rojo.valueChanged.connect(lambda: self.__value_fg_sl_changed("R"))
        self.SL_FG_Verde.valueChanged.connect(lambda: self.__value_fg_sl_changed("G"))
        self.SL_FG_Azul.valueChanged.connect(lambda: self.__value_fg_sl_changed("B"))
        
        self.BTN_Copiar_Fondo.clicked.connect(self.__copiar_fondo)
        self.BTN_Copiar_Texto.clicked.connect(self.__copiar_texto)
        
    def __value_bg_sb_changed(self, color):
        if color == "R":
            self.value = self.SB_BG_Rojo.value()
            self.SL_BG_Rojo.setValue(self.value)
        elif color == "G":
            self.value = self.SB_BG_Verde.value()
            self.SL_BG_Verde.setValue(self.value)
        else: # color == "B"
            self.value = self.SB_BG_Azul.value()
            self.SL_BG_Azul.setValue(self.value)
        self.__calculate_bg_value()

    def __value_bg_sl_changed(self, color):
        if color == "R":
            self.value = self.SL_BG_Rojo.value()
            self.SB_BG_Rojo.setValue(self.value)
        elif color == "G":
            self.value = self.SL_BG_Verde.value()
            self.SB_BG_Verde.setValue(self.value)
        else: # color == "B"
            self.value = self.SL_BG_Azul.value()
            self.SB_BG_Azul.setValue(self.value)
        self.__calculate_bg_value()
    
    def __calculate_bg_value(self):
        self.BG_rojo_hex = hex(self.SB_BG_Rojo.value())
        self.BG_verde_hex = hex(self.SB_BG_Verde.value())
        self.BG_azul_hex = hex(self.SB_BG_Azul.value())
        self.__construir_bg_valor()
    
    def __construir_bg_valor(self):
        self.BG_rojo_hex = self.BG_rojo_hex[2:]
        self.BG_verde_hex = self.BG_verde_hex[2:]
        self.BG_azul_hex = self.BG_azul_hex[2:]
        self.BG_rojo_hex = "".join(('0', self.BG_rojo_hex)) if len(self.BG_rojo_hex) < 2 else self.BG_rojo_hex
        self.BG_verde_hex = "".join(('0', self.BG_verde_hex)) if len(self.BG_verde_hex) < 2 else self.BG_verde_hex
        self.BG_azul_hex = "".join(('0', self.BG_azul_hex)) if len(self.BG_azul_hex) < 2 else self. BG_azul_hex
        self.BG_color = "".join(("#", self.BG_rojo_hex, self.BG_verde_hex, self.BG_azul_hex))
        self.__pintar_color()
        

    def __value_fg_sb_changed(self, color):
        if color == "R":
            self.value = self.SB_FG_Rojo.value()
            self.SL_FG_Rojo.setValue(self.value)
        elif color == "G":
            self.value = self.SB_FG_Verde.value()
            self.SL_FG_Verde.setValue(self.value)
        else: # color == "B"
            self.value = self.SB_FG_Azul.value()
            self.SL_FG_Azul.setValue(self.value)
        self.__calculate_fg_value()

    def __value_fg_sl_changed(self, color):
        if color == "R":
            self.value = self.SL_FG_Rojo.value()
            self.SB_FG_Rojo.setValue(self.value)
        elif color == "G":
            self.value = self.SL_FG_Verde.value()
            self.SB_FG_Verde.setValue(self.value)
        else: # color == "B"
            self.value = self.SL_FG_Azul.value()
            self.SB_FG_Azul.setValue(self.value)
        self.__calculate_fg_value()
    
    def __calculate_fg_value(self):
        self.FG_rojo_hex = hex(self.SB_FG_Rojo.value())
        self.FG_verde_hex = hex(self.SB_FG_Verde.value())
        self.FG_azul_hex = hex(self.SB_FG_Azul.value())
        self.__construir_fg_valor()
    
    def __construir_fg_valor(self):
        self.FG_rojo_hex = self.FG_rojo_hex[2:]
        self.FG_verde_hex = self.FG_verde_hex[2:]
        self.FG_azul_hex = self.FG_azul_hex[2:]
        self.FG_rojo_hex = "".join(('0', self.FG_rojo_hex)) if len(self.FG_rojo_hex) < 2 else self.FG_rojo_hex
        self.FG_verde_hex = "".join(('0', self.FG_verde_hex)) if len(self.FG_verde_hex) < 2 else self.FG_verde_hex
        self.FG_azul_hex = "".join(('0', self.FG_azul_hex)) if len(self.FG_azul_hex) < 2 else self. FG_azul_hex
        self.FG_color = "".join(("#", self.FG_rojo_hex, self.FG_verde_hex, self.FG_azul_hex))
        self.__pintar_color()
        
    def __pintar_color(self):
        self.LB_Muestra.setStyleSheet(f"background-color: {self.BG_color};\
                                      color: {self.FG_color};\
                                      font-family: Arial;\
                                      font-size: 48px;")
        self.RES_Fondo.setText(self.BG_color)
        self.RES_Texto.setText(self.FG_color)
        
    def __copiar_fondo(self):
        clipboard.copy(self.BG_color)

    def __copiar_texto(self):
        clipboard.copy(self.FG_color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
