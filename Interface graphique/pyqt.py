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
        
        self.label = QLabel("Bienvenue dans notre bataille navale dernière génération\nVeuillez sélectionner un mode de difficulté")
        
        self.radiobutton1 = QRadioButton ("Mode facile : Pirate")
        self.radiobutton1.setChecked(True)
        self.radiobutton1.setAccessibleName("pirate")
        self.radiobutton2 = QRadioButton ("Mode normal : présent")
        self.radiobutton2.setAccessibleName("présent")
        self.radiobutton3 = QRadioButton ("Mode difficile : futur")
        self.radiobutton3.setAccessibleName("futur")
        
        self.bouton = QPushButton ("Valider")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.radiobutton1)
        layout.addWidget(self.radiobutton2)
        layout.addWidget(self.radiobutton3)
        layout.addWidget(self.bouton)
        self.setLayout(layout)

        self.radiobutton1.toggled.connect(self.onClicked)
        self.radiobutton2.toggled.connect(self.onClicked)
        self.radiobutton3.toggled.connect(self.onClicked)
        self.bouton.clicked.connect(self.appui_bouton)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Vous avez choisi le mode", radioButton.accessibleName())

    def appui_bouton(self):
        if self.radiobutton1.isChecked():
            print("Vous avez validé le mode ", self.radiobutton1.accessibleName())
        elif self.radiobutton2.isChecked():
            print("Vous avez validé le mode ", self.radiobutton2.accessibleName())
        elif self.radiobutton3.isChecked():
            print("Vous avez validé le mode ", self.radiobutton3.accessibleName())

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre()
fen.show()

app.exec_()