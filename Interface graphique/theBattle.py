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
        self.grid_center = QVBoxLayout()

        self.gridSize = 15
        self.activeShip = ''
        self.styleBlocks = "background-color: #f4f4f4;"

        # game parameters
        self.isReadyToPlay = False
        self.isBattleStarted = False
        self.isSinkingBoat = False
        self.memoX = 100
        self.memoY = 100
        self.isXactive = True
        self.iteration = 1
        self.direction = 1
        self.activeWeapon = 0

        for x in range(self.gridSize):
            row = []
            for y in range(self.gridSize):
                button = QPushButton("")
                button.setStyleSheet(self.styleBlocks)
                button.clicked.connect(lambda checked, x=x, y=y: self.button_clicked(x, y))
                button.state = False
                button.ship = 0
                button.isPlayed = False
                self.grid_player.addWidget(button, x, y)
                row.append(button)
            self.buttons.append(row)

        for x in range(self.gridSize):
            row = []
            for y in range(self.gridSize):
                button = QPushButton("")
                button.setStyleSheet(self.styleBlocks)
                # on va écouter le clic ici sur les boutons pour lancer les attaques
                button.clicked.connect(lambda checked, x=x, y=y: self.fight(x, y, True))
                button.state = False
                button.ship = 0
                button.isPlayed = False
                self.grid_computer.addWidget(button, x, y)
                row.append(button)
            self.buttons_enemy.append(row)
        
        title_player = QLabel("Votre flotte :")
        self.button_center = QPushButton("Embarquement ...", self)
        spacer=QLabel('')
        self.weaponTitle = QLabel("Vos armes")
        self.normal = QRadioButton('Normal')
        self.torpille = QRadioButton('Torpille')
        self.normal.setChecked(True)
        self.button_center.clicked.connect(self.startBattle)
        title_computer = QLabel("La flotte ennemie prête au combat")
        self.grid_center.addWidget(self.button_center)
        
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
        frame_center.setLayout(self.grid_center)

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

    def choosePlaceToFight(self):
        if self.isSinkingBoat == True:
            self.precisionFight()
        else:    
            x = random.randint(0, self.gridSize-1)
            y = random.randint(0, self.gridSize-1)

            if self.buttons[x][y].isPlayed != True:
                self.fight(x, y, False)
            else:
                print('déjà touché ',x, y)
                self.choosePlaceToFight()

    def precisionFight(self):
        print("tir de précision")
        if self.isXactive == True:
            print('isXactive ', self.isXactive)
            print(self.memoX, self.iteration, self.direction)
            x = self.calcNewPosition(self.memoX)
            y = self.memoY
        else:
            x = self.memoX
            y = self.calcNewPosition(self.memoY)

        print('nouvelles coordonnées : ', x, y, self.iteration)
        self.iteration = self.iteration + 1
        self.fight(x, y, False)

    def calcNewPosition(self, memo):
        xy = memo + (self.iteration * self.direction)
        print('new xy = ', xy)
        print('gridSize = ', self.gridSize)
        if xy >= self.gridSize:
            self.direction = -1
            self.iteration = 1
            print('attention on risque de quitter la grille')
            xy = self.calcNewPosition(memo)
        if xy < 0:
            self.direction = 1
            self.iteration = 1
            self.isXactive = False
            xy = self.calcNewPosition(memo)
        return xy

    def fight(self, x, y, playingOnEnemyGrid = True):
        button = self.buttons_enemy[x][y] if playingOnEnemyGrid == True else self.buttons[x][y]
        button.isPlayed = True

        if self.isBattleStarted:
            if button.state == True :
                print ("touché ", button.ship)
                if playingOnEnemyGrid == False:
                    print('bateau ami touché : ', self.iteration)
                    self.isSinkingBoat = True
                    if self.memoX == 100:
                        self.memoX = x
                        self.memoY = y
                button.setStyleSheet("background-color: red")
                for ship in Ships_enemy :
                    if ship['id'] == button.ship :
                        ship_name = globals()[ship['name']]
                ship_name.touched ()
                ship_name.isShipDestroyed ()
                if playingOnEnemyGrid == False and ship_name.isShipDestroyed () == True:
                   self.isSinkingBoat = False 
                   self.memoX = 100
                   self.memoY = 100
                   self.direction = 1
                   self.iteration = 1
                   self.isXactive = True
            else :
                print ("à l'eau")
                button.setStyleSheet("background-color: blue")
                if playingOnEnemyGrid == False and self.isSinkingBoat == True:
                    if self.direction == 1:
                        self.iteration = 1
                        self.direction = -1
                    else:
                        self.isXactive = False
                        self.iteration = 1
                        self.direction = 1
                    
            print('attaque ', x, y)
            if (playingOnEnemyGrid == True):
                self.choosePlaceToFight()
        else:
            print('placez vos bateaux !!!')

    def startBattle(self):
        print ('isReadyToPlay ', self.isReadyToPlay)
        if self.isReadyToPlay:
            self.isBattleStarted = True
            self.grid_center.addWidget(self.weaponTitle)
            self.grid_center.addWidget(self.normal)
            self.grid_center.addWidget(self.torpille)   
        print('isBattleStarted ', self.isBattleStarted)

    
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
                        print('erreur de position')
                        errorPosition = True
                    
                    if (Ship.alignement == "H") and (buttons[x][i].state == True):
                        print ('erreur 2 de position')
                        errorPosition = True

        if (endPosition <= self.gridSize) and (startPosition >= 0) and (errorPosition == False):
                for i in range(startPosition, endPosition):
                    self.isPositionned = True
                    self.displayShipOnGrid(i, y, Ship, isEnemy) if Ship.alignement == "V" else self.displayShipOnGrid(x, i, Ship, isEnemy)
                self.updateIsReadyToPlay()
        else:
            self.button_center.setText('Embarquement ...')  
   
    def updateIsReadyToPlay(self):
        # on vérifie si tous les bateaux amis sont placés
        ready = True
        for x in Ships:
            ship = globals()[x['name']]
            print (ship.position)
            if not ship.position: 
                ready = False 
        if ready == True:
            self.isReadyToPlay = True
        if self.isReadyToPlay == True:
            self.button_center.setText("A l'attaque")
        else:
            self.button_center.setText('Embarquement ...')       
    
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
        
# les gentils
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

'''
    def IsGameOver (self):
        numberOfShipDestroyed = 0
        for ship in Ships :
            ship_name = globals()[ship['name']]
            if ship_name.isShipDestroyed () == True :
                numberOfShipDestroyed = numberOfShipDestroyed + 1

                print ('HELLO')
        if numberOfShipDestroyed == len (Ships) :
                print ("Vous avez perdu")
        numberOfShipEnnemyDestroyed = 0
        for shipEnnemy in Ships_enemy :
            ship_ennemy_name = globals()[shipEnnemy['name']]
            if ship_ennemy_name.isShipDestroyed () == True :
                numberOfShipEnnemyDestroyed = numberOfShipEnnemyDestroyed + 1
        if numberOfShipEnnemyDestroyed == len (Ships_enemy) :
            print ("Vous avez gagné !")
'''







