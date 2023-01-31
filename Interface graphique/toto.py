import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLabel, QLineEdit

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Ma fenetre")
        self.n = 0
        # activation du suivi du mouvement de la souris
        self.setMouseTracking(True) 
    
        self.btn1 = QPushButton("Bouton Toto")
        self.btn2 = QPushButton("Bouton Tata")
        self.case = QCheckBox("Voici ma premiere case a cocher")
        self.label = QLabel("Voici mon premier texte avec un QLabel, les licornes sont magiques et elles font du caca paillette :)")
        self.label2 = QLabel("vous avez appuer " + str(self.n) + " fois.")
        self.champ = QLineEdit("Voici mon premier champ de texte")
        self.bouton = QPushButton ("COPIE")
        self.label3 = QLabel()

        # on connecte le signal "clicked" a la methode appui_bouton
        self.btn1.clicked.connect(self.appui_bouton)
        self.btn2.clicked.connect(self.appuiBouton)
        self.bouton.clicked.connect(self.appui_bouton_copie)

        # on connecte le signal "stateChanged" à la fonction "etat_change"
        self.case.stateChanged.connect(self.etat_change)

        layout = QVBoxLayout()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.case)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.champ)
        layout.addWidget(self.bouton)
        layout.addWidget(self.label3)

        self.setLayout(layout)
        self.setWindowTitle("TOTO est dans la place")

    # on définit une fonction à connecter au signal envoyé
    def etat_change(self):
        print("action sur la case")
        if self.case.checkState() == Qt.Checked:
            print("coche")
        else:
            print("decoche")

    def mousePressEvent(self, event):
        print("appui souris avec : ", event.button())
        print("Position : ", str(event.x()) + " " + str(event.y()))
    
    def mouseMoveEvent(self,event):
        print("position = " + str(event.x()) + " " + str(event.y()))
    
    def appui_bouton(self):
        print("Appui sur le bouton :)")

    def appuiBouton(self):
        # on incrémente l'attribut "n" de 1
        self.n = self.n + 1 
        # on utilise la méthode "setText" de QLabel pour fixer le texte
        self.label2.setText("vous avez appuer " + str(self.n) + " fois.")

    # on définit une méthode à connecter au signal envoyé
    def appui_bouton_copie(self):
        # la méthode "text" de QLineEdit permet d'obtenir le texte à copier
        texte_a_copier = self.champ.text()
        # la méthode "setText" de QLabel permet de changer le texte de l'étiquette
        self.label3.setText(texte_a_copier)

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre()
fen.show()

app.exec_()