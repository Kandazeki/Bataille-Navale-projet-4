import sys
from functools import partial
from PyQt5.QtWidgets import QRadioButton, QFrame, QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QWidget
from classes import Ship
import random

DEBUG = True

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.buttons = []
        self.buttons_enemy = []

        self.grid_player = QGridLayout()
        self.grid_computer = QGridLayout()
        grid_center = QHBoxLayout()

        self.gridSize = 15
        self.activeShip = ''
        self.styleBlocks = "background-color: #f4f4f4;"

        for x in range(self.gridSize):
            row = []
            for y in range(self.gridSize):
                button = QPushButton("")
                button.setStyleSheet(self.styleBlocks)
                button.clicked.connect(lambda checked, x=x, y=y: self.button_clicked(x, y))
                button.state = False
                button.ship = 0
                self.grid_player.addWidget(button, x, y)
                row.append(button)
            self.buttons.append(row)

        for x in range(self.gridSize):
            row = []
            for y in range(self.gridSize):
                button = QPushButton("")
                button.setStyleSheet(self.styleBlocks)
                # on va écouter le clic ici sur les boutons pour lancer les attaques
                #button.clicked.connect(lambda checked, x=x, y=y: self.button_clicked(x, y))
                button.state = False
                button.ship = 0
                self.grid_computer.addWidget(button, x, y)
                row.append(button)
            self.buttons_enemy.append(row)
        
        title_player = QLabel("Votre flotte :")
        title_center = QLabel("        Placez vos bateaux")
        title_center.setStyleSheet("background-color: lightGrey;")
        title_computer = QLabel("La flotte ennemie")
        grid_center.addWidget(title_center)
        
        # PLAYER
        frame_player = QFrame()
        frame_player.setFixedSize(600, 600)
        frame_player.setLayout(self.grid_player)
        frame_player.setLayout(self.grid_player)
        title = QHBoxLayout()
        title.addWidget(title_player)
        self.grid_player.addLayout(title, self.gridSize+1, 0, 1, 10)

        # CENTER
        frame_center = QFrame()
        frame_center.setFixedSize(200, 600)
        frame_center.setLayout(grid_center)

        # COMPUTER
        frame_computer = QFrame()
        frame_computer.setFixedSize(600, 600)
        frame_computer.setLayout(self.grid_computer)
        title = QHBoxLayout()
        title.addWidget(title_computer)
        self.grid_computer.addLayout(title, self.gridSize+1, 0, 1, 10)

        # MAIN LAYOUT
        central_widget = QWidget()
        h_box_layout = QHBoxLayout()
        h_box_layout.addWidget(frame_player)
        h_box_layout.addWidget(frame_center)
        h_box_layout.addWidget(frame_computer)
        central_widget.setLayout(h_box_layout)
        self.setCentralWidget(central_widget)


        # On affiche la liste des bateaux du gentil
        i = 2
        for ship in Ships:
            shipName = ship['name']
            object = globals()[shipName]
            selected = True if i == 2 else False
            self.displayShipPlayer(object, self.gridSize+i, selected)
            i = i + 1 

        # les bateaux ennemis
        for ship in Ships_enemy:
            self.isPositionned = False
            while (self.isPositionned == False):
                x = random.randint(1, self.gridSize-1)
                y = random.randint(1, self.gridSize-1)
                alignement = 'H' if (random.randint(1, 2) == 1) else 'V'
                myShip = globals()[ship['name']]
                myShip.position = [x, y]
                myShip.alignement = alignement
                self.btnGridSelected(x, y, myShip, True)
    
    def displayShipPlayer(self, Ship, line, isSelected = False):
        shipSelector = "selector", Ship.id
        selector = ""
        globals()[selector] = shipSelector
        selector = QRadioButton(f"{Ship.name} ({Ship.size})")
        selector.setStyleSheet(f"background-color: {Ship.color}; color: {Ship.textColor}; padding: 3px;")
        selector.setAccessibleName(str(Ship.id))
        selector.setChecked(isSelected)
        check_box = QCheckBox("Vertical")
        selector.toggled.connect(partial(self.bouton_toggle, selector))
        check_box.stateChanged.connect(partial(self.check_toggle, check_box, Ship))
        inputs = QHBoxLayout()
        inputs.addWidget(selector)
        inputs.addWidget(check_box)
        self.grid_player.addLayout(inputs, line, 0, 1, 10)
        if (isSelected):
                self.defineActiveShip(Ship.id)

    def bouton_toggle(self, radioBtn):
        if (radioBtn.isChecked()):
            self.defineActiveShip(int(radioBtn.accessibleName()))
    
    def check_toggle(self, check, Ship):
        Ship.alignement = "V" if check.isChecked() else "H"
    
    def defineActiveShip(self, id):
        for x in Ships:
                if x['id'] == id:
                    self.activeShip = x['name']

    def btnGridSelected(self, x, y, Ship, isEnemy = False):
        errorPosition = False
        Ship.position = [x, y]
        buttons = self.buttons if isEnemy == False else self.buttons_enemy
        # si on positionne le bateau à la verticale, on fait la boucle de positionnement sur x
        # en se référant à Ship.position[x,y]  ref = 0 pour x, et ref = 1 pour y
        ref = 0 if Ship.alignement == "V" else 1
        startPosition = Ship.position[ref]
        endPosition = Ship.position[ref] + Ship.size

        if (endPosition <= self.gridSize) and (startPosition >= 0):
                for i in range(startPosition, endPosition):
                    if (Ship.alignement == "V") and (buttons[i][y].state == True):
                        errorPosition = True
                    if (Ship.alignement == "H") and (buttons[x][i].state == True):
                        errorPosition = True

        if (endPosition <= self.gridSize) and (startPosition >= 0) and (errorPosition == False):
                for i in range(startPosition, endPosition):
                    self.isPositionned = True
                    self.displayShipOnGrid(i, y, Ship, isEnemy) if Ship.alignement == "V" else self.displayShipOnGrid(x, i, Ship, isEnemy)
    
    def displayShipOnGrid(self, x, y, Ship, isEnemy = False):
        buttons = self.buttons if isEnemy == False else self.buttons_enemy
        button = buttons[x][y]
        button.state = True
        button.ship = Ship.id
        if (isEnemy == False) or (DEBUG == True ):
            button.setText(Ship.symbol)
            button.setStyleSheet(f"background-color: {Ship.color}; color: {Ship.textColor}; padding: 3px;")
        
    
    def removeShipFromGrid(self, id):
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                button = self.buttons[x][y]
                if button.ship == id:
                    button.ship = 0
                    button.state = False
                    button.setText('')
                    button.setStyleSheet(self.styleBlocks)

    def button_clicked(self, x, y):
        ship = globals()[self.activeShip]
        self.removeShipFromGrid(ship.id)
        self.btnGridSelected(x, y, ship)
        
Moby_Dick = Ship (1, "Moby Dick", 5, "red", "white", "X", None)
Vogue_Merry = Ship (2, "Merry", 2, "blue", "white", "O", "barrel", 2)
Thousand_Sunny = Ship (3, "Thousand Sunny", 3, "yellow", "black", "#", "coup de burst", 3)
Toto = Ship(4, "Toto le bateau", 7, "brown", "white", "T", None)

# les méchants
Moby_Dick_enemy = Ship (1, "Moby Dick", 5, "red", "white", "X", None)
Vogue_Merry_enemy = Ship (2, "Merry", 2, "blue", "white", "O", "barrel", 2)
Thousand_Sunny_enemy = Ship (3, "Thousand Sunny", 3, "yellow", "black", "#", "coup de burst", 3)
Toto_enemy = Ship(4, "Toto le bateau", 7, "brown", "white", "T", None)

Ships = [
    {'id': 1, 'name': 'Moby_Dick'}, 
    {'id': 2, 'name': 'Vogue_Merry'},
    {'id': 3, 'name': 'Thousand_Sunny'},
    {'id': 4, 'name': 'Toto'}
]

Ships_enemy= [
    {'id': 1, 'name': 'Moby_Dick_enemy'}, 
    {'id': 2, 'name': 'Vogue_Merry_enemy'},
    {'id': 3, 'name': 'Thousand_Sunny_enemy'},
    {'id': 4, 'name': 'Toto_enemy'}
]

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())