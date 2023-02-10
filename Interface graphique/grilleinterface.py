import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication)

class basicWindow(QWidget):

    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for x in range(10):
            for y in range(10):
                self.button = QPushButton(" ")
                self.button.setGeometry(11,11,11,11)
                grid_layout.addWidget(self.button, x, y)
                self.button.clicked.connect(self.isButtonclicked)
            grid_layout.setColumnStretch(x,1)
                
        self.setWindowTitle('grille bataille navale')

    def isButtonclicked (self):
        print ("vous avez cliqué")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())