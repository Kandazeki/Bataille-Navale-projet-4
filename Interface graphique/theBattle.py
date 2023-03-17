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
        self.isEndOfTheBattle = False

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
        self.winBattle = QLabel ('Vous avez gagné félicitation !')
        self.looseBattle = QLabel ("Vous avez perdu dommage...")
        self.PlayAgain = QPushButton ("Voulez vous rejouer ?")
        self.weaponTitle = QLabel("Vos armes")
        self.coupdeburst = QRadioButton(f"Coup de Burst.\n L'arme du Thousand Sunny,\n un réel coup de torpille{Thousand_Sunny.NumberOfUse}")
        self.Barrel = QRadioButton(f"Barrel.\n L'arme du Vogue Merry,\n une explosion terrifiante {Vogue_Merry.NumberOfUse}")
        self.abordage = QRadioButton(f"L'Abordage.\n Les pirates du bateau Toto\n envahissent les autres {Toto.NumberOfUse}")
        self.dechhomme = QRadioButton(f"La déchéance d'un Homme.\n Un redoutable détecteur \n d'ennemi {Moby_Dick.NumberOfUse}")
        self.coupdeburst.setChecked(True)
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
                self.choosePlaceToFight()

    def precisionFight(self):
        if self.isXactive == True:
            x = self.calcNewPosition(self.memoX)
            y = self.memoY
        else:
            x = self.memoX
            y = self.calcNewPosition(self.memoY)
        self.iteration = self.iteration + 1
        self.fight(x, y, False)

    def calcNewPosition(self, memo):
        xy = memo + (self.iteration * self.direction)
        if xy >= self.gridSize:
            self.direction = -1
            self.iteration = 1
            xy = self.calcNewPosition(memo)
        if xy < 0:
            self.direction = 1
            self.iteration = 1
            self.isXactive = False
            xy = self.calcNewPosition(memo)
        return xy

    def fight (self, x, y, playingOnEnemyGrid = True):
        button = self.buttons_enemy[x][y] if playingOnEnemyGrid == True else self.buttons[x][y]
        button.isPlayed = True
        if self.isBattleStarted:
            if button.state == True :
                print ("touché ", button.ship)
                if playingOnEnemyGrid == False:
                    self.isSinkingBoat = True
                    if self.memoX == 100:
                        self.memoX = x
                        self.memoY = y
                button.setStyleSheet("background-color: red")
                if playingOnEnemyGrid == True :
                    for ship_enemy in Ships_enemy :
                        if ship_enemy['id'] == button.ship :
                            ship_enemy_name = globals()[ship_enemy['name']]
                    ship_enemy_name.touched ()
                    if ship_enemy_name.isShipDestroyed () == True :
                        print ("le", ship_enemy_name.name, "a été détruit")
                        self.IsGameWon ()
                if playingOnEnemyGrid == False :
                    for ship in Ships :
                        if ship['id'] == button.ship :
                            ship_name = globals()[ship['name']]
                    ship_name.touched()
                    if ship_name.isShipDestroyed () == True :
                        print ("le", ship_name.name, "a été détruit")
                        self.IsGameLost ()
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
            if playingOnEnemyGrid == True:
                self.choosePlaceToFight()
        else:
            print('placez vos bateaux !!!')

    def IsGameWon (self) :
        numberOfShipEnnemyDestroyed = 0
        for shipEnnemy in Ships_enemy :
            ship_ennemy_name = globals()[shipEnnemy['name']]
            if ship_ennemy_name.isShipDestroyed () == True :
                numberOfShipEnnemyDestroyed = numberOfShipEnnemyDestroyed + 1
        if numberOfShipEnnemyDestroyed == len (Ships_enemy) :
            print ("Vous avez gagné !")
            self.isEndOfTheBattle = True
            self.grid_center.addWidget(self.winBattle)
            self.grid_center.addWidget(self.PlayAgain)

    def IsGameLost (self) :
        numberOfShipDestroyed = 0
        for ship in Ships :
            ship_name = globals()[ship['name']]
            if ship_name.isShipDestroyed () == True :
                numberOfShipDestroyed = numberOfShipDestroyed + 1
        if numberOfShipDestroyed == len (Ships) :
                print ("Vous avez perdu")
                self.isEndOfTheBattle = True
                self.grid_center.addWidget(self.looseBattle)
                self.grid_center.addWidget(self.PlayAgain)

    def startBattle(self):
        if self.isReadyToPlay:
            self.isBattleStarted = True
            self.grid_center.addWidget(self.weaponTitle)
            self.grid_center.addWidget(self.coupdeburst)
            self.grid_center.addWidget(self.dechhomme)   
            self.grid_center.addWidget(self.abordage)
            self.grid_center.addWidget(self.Barrel)
        print('isBattleStarted ', self.isBattleStarted)

<<<<<<< Updated upstream
=======
        def weapons (self):
            if QRadioButton.setChecked(True) in self.grid_center:
                frame_weapon = QFrame
                frame_weapon.setFixedSize(400, 400)
                self.grid_weapon = QVBoxLayout()
                frame_weapon.setLayout(self.grid_weapon)
                self.choice = QLabel (f"Voulez-vous utilisez l'arme {QRadioButton.setChecked(True)}")
                self.grid_weapon.addWidget(self.choice)


    
>>>>>>> Stashed changes
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
                self.updateIsReadyToPlay()
        else:
            self.button_center.setText('Embarquement ...')  
   
    def updateIsReadyToPlay(self):
        # on vérifie si tous les bateaux amis sont placés
        ready = True
        for x in Ships:
            ship = globals()[x['name']]
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
Moby_Dick = Ship (1, "Moby Dick", 5, "red", "white", "X", "La déchéance d'un Homme", 1)
Vogue_Merry = Ship (2, "Merry", 2, "blue", "white", "O", "barrel", 2)
Thousand_Sunny = Ship (3, "Thousand Sunny", 3, "yellow", "black", "#", "coup de burst", 1)
Toto = Ship(4, "Toto le bateau", 7, "brown", "white", "T", "L'Abordage", 1)

# les méchants
Moby_Dick_enemy = Ship (1, "Moby Dick", 5, "red", "white", "X", "La déchéance d'un Homme", 1)
Vogue_Merry_enemy = Ship (2, "Merry", 2, "blue", "white", "O", "barrel", 2)
Thousand_Sunny_enemy = Ship (3, "Thousand Sunny", 3, "yellow", "black", "#", "coup de burst", 1)
Toto_enemy = Ship(4, "Toto le bateau", 7, "brown", "white", "T", "L'Abordage")

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





