import sys
from PyQt6.QtWidgets import QApplication, QWidget

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        
    def inicializarUI(self):
        self.setGeometry(100,100,250,250)
        self.setWindowTitle("Mi primera ventana")
        self.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventan = Ventana
    sys.exit(app.exec())
        