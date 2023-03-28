import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QTextEdit, QRadioButton, QFrame, QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QTextCursor
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

        self.gridSize = 10
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
        self.activeWeapon = 0 # default = 0, torpille = 1, bombe = 2  

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
        self.winBattle = QLabel ('Vous avez gagné félicitation !')
        self.looseBattle = QLabel ("Vous avez perdu dommage...")
        self.PlayAgain = QPushButton ("rejouer :)")
        self.PlayAgain.clicked.connect (self.DoANewGame)
        self.weaponTitle = QLabel("Vos armes")
        self.normal = QRadioButton('Normal')
        self.normal.setObjectName('0')
        self.coupdeburst = QRadioButton(f"Coup de Burst.\n {Thousand_Sunny.NumberOfUse} / {Thousand_Sunny_enemy.NumberOfUse}")
        self.coupdeburst.setObjectName('1')
        self.coupdeburst.setToolTip("L'arme du Thousand Sunny,\n un réel coup de torpille")
        self.coupdeburstMode = QCheckBox("V")
        self.coupdeburstGroup = QHBoxLayout()
        self.coupdeburstGroup.addWidget(self.coupdeburst)
        self.coupdeburstGroup.addWidget(self.coupdeburstMode)
        self.barrel = QRadioButton(f"Barrel\n {Vogue_Merry.NumberOfUse} / {Vogue_Merry_enemy.NumberOfUse}")
        self.barrel.setToolTip("L'arme du Vogue Merry,\n une explosion terrifiante")
        self.barrel.setObjectName('2')
        #self.abordage = QRadioButton(f"L'Abordage.\n  {Toto.NumberOfUse}/ {Toto_enemy.NumberOfUse}")
        #self.abordage.setToolTip ('Les pirates du bateau Toto\n envahissent les autres')
        #self.dechhomme = QRadioButton(f"La déchéance d'un Homme.\n {Moby_Dick.NumberOfUse}/{Moby_Dick_enemy.NumberofUse}")
        #self.dechhomme.setToolTip ('Un redoutable détecteur d'ennemi')
        self.normal.setChecked(True)
        self.button_center.clicked.connect(self.startBattle)
        title_computer = QLabel("La flotte ennemie prête au combat")
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.grid_center.addWidget(self.text_edit)
        self.grid_center.addWidget(self.button_center)

        self.log('Bonjour')
        self.log('Placez vos bateaux')
        
        # PLAYER
        frame_player = QFrame()
        frame_player.setFixedSize(400, 500)
        frame_player.setLayout(self.grid_player)
        frame_player.setLayout(self.grid_player)
        title = QHBoxLayout()
        title.addWidget(title_player)
        self.grid_player.addLayout(title, self.gridSize+1, 0, 1, 10)

        # CENTER
        frame_center = QFrame()
        frame_center.setFixedSize(220, 500)
        frame_center.setLayout(self.grid_center)

        # COMPUTER
        frame_computer = QFrame()
        frame_computer.setFixedSize(400, 500)
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

        i = 2
        for ship in Ships_enemy:
            self.isPositionned = False
            shipName = ship['name']
            object = globals()[shipName]
            self.displayShipEnemy(object, self.gridSize+i)
            while (self.isPositionned == False):
                x = random.randint(1, self.gridSize-1)
                y = random.randint(1, self.gridSize-1)
                alignement = 'H' if (random.randint(1, 2) == 1) else 'V'
                myShip = globals()[ship['name']]
                myShip.position = [x, y]
                myShip.alignement = alignement
                self.btnGridSelected(x, y, myShip, True)
            i = i + 1
            
    def log(self, message):
        message = str(message)
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertPlainText(message + '\n')
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def choosePlaceToFight(self):
        if self.isSinkingBoat == True:
            self.precisionFight()
        else:    
            x = random.randint(0, self.gridSize-1)
            y = random.randint(0, self.gridSize-1)

            if self.buttons[x][y].isPlayed != True:
                self.fight(x, y, False)
            else:
                self.log('déjà touché ' + str(x) + ',' + str(y))
                self.choosePlaceToFight()

    def precisionFight(self):
        self.log("tir de précision")
        if self.isXactive == True:
            self.log('isXactive ' + str(self.isXactive))
            self.log(str(self.memoX) + str(self.iteration) + str(self.direction))
            x = self.calcNewPosition(self.memoX)
            y = self.memoY
        else:
            x = self.memoX
            y = self.calcNewPosition(self.memoY)

        self.log('nouvelles coordonnées : ' + str(x) + str(y) + str(self.iteration))
        self.iteration = self.iteration + 1
        self.fight(x, y, False)

    def calcNewPosition(self, memo):
        xy = memo + (self.iteration * self.direction)
        self.log('new xy = ' + str(xy))
        self.log('gridSize = ' + str(self.gridSize))
        if xy >= self.gridSize:
            self.direction = -1
            self.iteration = 1
            self.log('attention on risque de quitter la grille')
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
            if self.activeWeapon == 1: # torpille
                modeVerical = self.coupdeburstMode.isChecked()
                self.log('Coupdeburst ...')
                ref = x if modeVerical else y
                hasTouched = False
                for xy in range(ref, self.gridSize):
                    if playingOnEnemyGrid == True:
                        targetedButtons = self.buttons_enemy
                    else:
                        targetedButtons = self.buttons
                    refButton = targetedButtons[xy][y] if modeVerical else targetedButtons[x][xy]
                    if refButton.state == False:
                        refButton.setStyleSheet("background-color: blue")
                    else:
                        hasTouched = True
                        break

                if playingOnEnemyGrid == True:
                    Thousand_Sunny.useWeapon()
                else:
                    Thousand_Sunny_enemy.useWeapon()

                if Thousand_Sunny.IsAbleToUseWeapon() == False:
                    self.coupdeburst.setDisabled(True)

                self.coupdeburst.setText(f"Coup de Burst.\n {Thousand_Sunny.NumberOfUse} / {Thousand_Sunny_enemy.NumberOfUse}")
                self.activeWeapon = 0
                self.normal.setChecked(True)
                
                if hasTouched == True:
                    self.log ('La torpille a touché un truc')
                    if modeVerical:
                        self.fight(xy, y)
                    else:
                        self.fight(x, xy)
                    return
                else:
                    self.log('Echec de la torpille')

            elif button.state == True :
                self.log ("touché " + str(button.ship))
                activeListShip = Ships if playingOnEnemyGrid == True else Ships_enemy
                if playingOnEnemyGrid == False:
                    self.isSinkingBoat = True
                    if self.memoX == 100:
                        self.memoX = x
                        self.memoY = y
                button.setStyleSheet("background-color: red")
                
                if playingOnEnemyGrid == True:
                    for ship in Ships_enemy :
                        if ship['id'] == button.ship :
                            ship_name = globals()[ship['name']]
                    ship_name.touched ()
                    self.IsGameWon ()
                else:
                    for ship in Ships :
                        if ship['id'] == button.ship :
                            ship_name = globals()[ship['name']]
                    ship_name.touched ()
                    self.IsGameLost () 

                if playingOnEnemyGrid == False and ship_name.isShipDestroyed () == True:
                   self.isSinkingBoat = False 
                   self.memoX = 100
                   self.memoY = 100
                   self.direction = 1
                   self.iteration = 1
                   self.isXactive = True
                
            else :
                self.log ("à l'eau")
                button.setStyleSheet("background-color: blue")
                if playingOnEnemyGrid == False and self.isSinkingBoat == True:
                    if self.direction == 1:
                        self.iteration = 1
                        self.direction = -1
                    else:
                        self.isXactive = False
                        self.iteration = 1
                        self.direction = 1
                    
            if (playingOnEnemyGrid == True):
                self.choosePlaceToFight()
        else:
            self.log('placez vos bateaux !!!')

    def startBattle(self):
        self.log ('isReadyToPlay ' + str(self.isReadyToPlay))
        if self.isReadyToPlay:
            self.isBattleStarted = True
            self.grid_center.addWidget(self.weaponTitle)
            self.grid_center.addWidget(self.normal)
            self.grid_center.addLayout(self.coupdeburstGroup, 2)   
            self.grid_center.addWidget(self.barrel)
            self.normal.toggled.connect(self.changeWeapon)
            self.coupdeburst.toggled.connect(self.changeWeapon)
            self.barrel.toggled.connect(self.changeWeapon)
        self.log('isBattleStarted ' + str(self.isBattleStarted))

    def changeWeapon(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.activeWeapon = int(radioButton.objectName())
            self.log('Option sélectionnée :' +  str(radioButton.text()) + ' / ' + str(self.activeWeapon))

    def displayShipPlayer(self, Ship, line, isSelected = False):
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
    
    def displayShipEnemy(self, Ship, line):
        shipSelector = "selector", Ship.id
        selector = ""
        globals()[selector] = shipSelector
        selector = QLabel(f"{Ship.name} ({Ship.size})")
        selector.setStyleSheet(f"background-color: {Ship.color}; color: {Ship.textColor}; padding: 3px;")
        inputs = QHBoxLayout()
        inputs.addWidget(selector)
        self.grid_computer.addLayout(inputs, line, 0, 1, 10)

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

    def DoANewGame (self):
        self.close()
        if not QCoreApplication.instance():
            new_app = QApplication(sys.argv)
        else :
            new_app = QCoreApplication.instance()
        new_main_window = Window()
        new_main_window.show()
        new_app.exec_()
    
    def IsGameWon (self) :
        self.log ('isGameWon ? ')
        if self.areAllShipsDestroyed(Ships_enemy):
            self.log ("Vous avez gagné !")
            self.grid_center.addWidget(self.winBattle)
            self.grid_center.addWidget(self.PlayAgain)
    
    def IsGameLost (self) :
        if self.areAllShipsDestroyed(Ships) :
                self.log ("Vous avez perdu")
                self.isEndOfTheBattle = True
                self.grid_center.addWidget(self.looseBattle)
                self.grid_center.addWidget(self.PlayAgain)
    
    def areAllShipsDestroyed(self, ships):
        numbreOfShipsDestroyed = 0
        for ship in ships:
            ship_name = globals()[ship['name']]
            if ship_name.isShipDestroyed () == True :
                numbreOfShipsDestroyed = numbreOfShipsDestroyed + 1
            if numbreOfShipsDestroyed == len(ships):
                return True
            else:
                return False
        
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

#Ships = [
#    {'id': 1, 'name': 'Moby_Dick'}, 
#]

Ships_enemy= [
    {'id': 1, 'name': 'Moby_Dick_enemy'}, 
    {'id': 2, 'name': 'Vogue_Merry_enemy'},
    {'id': 3, 'name': 'Thousand_Sunny_enemy'},
    {'id': 4, 'name': 'Toto_enemy'}
]

app = QApplication(sys.argv)
window = Window()
window.show()

toto = Window()
toto.show()
toto.log('Bonjour Toto')

sys.exit(app.exec_())