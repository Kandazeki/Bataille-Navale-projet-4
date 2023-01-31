import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*

class Fenetre (QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Bataille navale")
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Bienvenue dans notre bataille navale dernière génération\nVeuillez sélectionner un mode de difficulté")
        layout.addWidget(self.label)

        self.radiobutton = QRadioButton ("Mode facile : Pirate")
        self.radiobutton.setChecked(True)
        self.radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(self.radiobutton)

        self.radiobutton = QRadioButton ("Mode normal : présent")
        self.radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(self.radiobutton)

        self.radiobutton = QRadioButton ("Mode difficile : futur")
        self.radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(self.radiobutton)

        self.bouton = QPushButton ("Valider")
        self.bouton.clicked.connect(self.appui_bouton)
        layout.addWidget(self.bouton)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Vous avez choisi un mode ")

    def appui_bouton(self):
        print("Vous avez validé")

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre()
fen.show()

app.exec_()