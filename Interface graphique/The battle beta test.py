import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QTextEdit, QRadioButton, QFrame, QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QTextCursor, QPixmap, QIcon
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
        self.inputs = QHBoxLayout()
        self.premierradiobutton = QVBoxLayout()
        self.deuxiemecheckbox = QVBoxLayout ()

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
        #self.abordage.setObjectName ('3')
        #self.dechhomme = QRadioButton(f"La déchéance d'un Homme.\n {Moby_Dick.NumberOfUse}/{Moby_Dick_enemy.NumberofUse}")
        #self.dechhomme.setToolTip ('Un redoutable détecteur d'ennemi')
        #self.dechhomme.setObjectName ('4')
        self.normal.setChecked(True)
        self.button_center.clicked.connect(self.startBattle)
        title_computer = QLabel("La flotte ennemie prête au combat")
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.grid_center.addWidget(self.text_edit)
        self.grid_center.addWidget(self.button_center)
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

    def fight(self, x, y, playingOnEnemyGrid = True):
        button = self.buttons_enemy[x][y] if playingOnEnemyGrid == True else self.buttons[x][y]
        button.isPlayed = True

        if playingOnEnemyGrid == False and self.isSinkingBoat == False:
            self.activeWeapon = random.randint(0, 2)
            if self.activeWeapon == 1 and Thousand_Sunny_enemy.IsAbleToUseWeapon() == False:
                self.activeWeapon = 0
            if self.activeWeapon == 2 and Vogue_Merry_enemy.IsAbleToUseWeapon() == False:
                self.activeWeapon = 0

        if self.isBattleStarted:
            # torpille
            if self.activeWeapon == 1: 
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
                
                if hasTouched == True :
                    if modeVerical:
                        self.fight(xy, y)
                    else:
                        self.fight(x, xy)
                    return
            
            # bombe
            if self.activeWeapon == 2:
                hasTouched = False
                xMax = x + 2 if x + 2 <= self.gridSize else self.gridSize
                yMax = y + 2 if y + 2 <= self.gridSize else self.gridSize
                for xx in range(x-1, xMax):
                    if playingOnEnemyGrid == True:
                        targetedButtons = self.buttons_enemy
                    else:
                        targetedButtons = self.buttons
                    refButton = targetedButtons [xx][y]
                    if refButton.state == False:
                        refButton.setStyleSheet("background-color: blue")
                    else:
                        hasTouched = True
                        self.boatIsTouched(xx, y, refButton, playingOnEnemyGrid)

                for yy in range(y-1, yMax):
                    if playingOnEnemyGrid == True:
                        targetedButtons = self.buttons_enemy
                    else:
                        targetedButtons = self.buttons
                    refButton = targetedButtons [x][yy]
                    if refButton.state == False:
                        refButton.setStyleSheet("background-color: blue")
                    else:
                        hasTouched = True
                        self.boatIsTouched(x, yy, refButton, playingOnEnemyGrid)

                if playingOnEnemyGrid == True:
                    Vogue_Merry.useWeapon()
                else:
                    Vogue_Merry_enemy.useWeapon()

                if Vogue_Merry.IsAbleToUseWeapon() == False:
                    self.barrel.setDisabled(True)

                self.barrel.setText(f"Barrel.\n {Vogue_Merry.NumberOfUse} / {Vogue_Merry_enemy.NumberOfUse}")
                self.activeWeapon = 0
                self.normal.setChecked(True)
            
            #Le bateau est touché (colorier en rouge et affiche)
            elif button.state == True :
                self.boatIsTouched(x, y, button, playingOnEnemyGrid)
                
            else :
                self.log ("A l'eau")
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
            self.log('Placez vos bateaux !!!')
    
    def boatIsTouched(self, x, y, button, playingOnEnemyGrid):
        self.log ("touché ")
        if playingOnEnemyGrid == False:
            self.isSinkingBoat = True
            if self.memoX == 100:
                self.memoX = x
                self.memoY = y
        button.setStyleSheet("background-color: red")

        # on teste si on a gagné ou perdu
        if playingOnEnemyGrid == True :
            for ship_enemy in Ships_enemy :
                if ship_enemy['id'] == button.ship :
                    ship_enemy_name = globals()[ship_enemy['name']]
            ship_enemy_name.touched ()
            if ship_enemy_name.isShipDestroyed () == True :
                    self.log ("vous avez détruit le "+ str(ship_enemy_name.name) + " !")
                    self.IsGameWon ()
        if playingOnEnemyGrid == False :
            for ship in Ships :
                if ship['id'] == button.ship :
                    ship_name = globals()[ship['name']]
            ship_name.touched()
            if ship_name.isShipDestroyed () == True :
                    self.log ("votre " + str(ship_name.name) + " a été détruit")
                    self.IsGameLost ()
                
        if playingOnEnemyGrid == False and ship_name.isShipDestroyed () == True:
            self.isSinkingBoat = False 
            self.memoX = 100
            self.memoY = 100
            self.direction = 1
            self.iteration = 1
            self.isXactive = True

    def startBattle(self):
        if self.isReadyToPlay:
            self.isBattleStarted = True
            self.grid_center.addWidget(self.weaponTitle)
            self.grid_center.addWidget(self.normal)
            self.grid_center.addLayout(self.coupdeburstGroup, 2)   
            self.grid_center.addWidget(self.barrel)
            self.normal.toggled.connect(self.changeWeapon)
            self.coupdeburst.toggled.connect(self.changeWeapon)
            self.barrel.toggled.connect(self.changeWeapon)
            self.TransformIntoLabel()  

    def TransformIntoLabel(self):
           # Parcourir les éléments du layout parent et remplacer chaque QRadioButton par un QLabel
        for i in range(self.premierradiobutton.count()):
            item = self.premierradiobutton.itemAt(i)
            if item.widget() is not None and isinstance(item.widget(), QRadioButton):
                radio_button = item.widget()
                texte = radio_button.text()
                label = QLabel(texte)
                index = self.premierradiobutton.indexOf(radio_button)
                self.premierradiobutton.takeAt(index)
                self.premierradiobutton.insertWidget(index, label)
                radio_button.deleteLater()
        # Mettre à jour le layout
        self.premierradiobutton.update()
        self.button1.setEnabled(False)

    def changeWeapon(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.activeWeapon = int(radioButton.objectName())

    def displayShipPlayer(self, Ship, line, isSelected = False):
        selector = QRadioButton(f"{Ship.name} ({Ship.size})")
        selector.setStyleSheet(f"background-color: {Ship.image}; padding: 3px;")
        selector.setAccessibleName(str(Ship.id))
        selector.setChecked(isSelected)
        check_box = QCheckBox("Vertical")
        selector.toggled.connect(partial(self.bouton_toggle, selector))
        check_box.stateChanged.connect(partial(self.check_toggle, check_box, Ship))
        self.premierradiobutton.addWidget(selector)
        self.deuxiemecheckbox.addWidget(check_box)
        self.grid_player.addLayout(self.inputs, line, 0, 1, 10)
        self.inputs.addLayout(self.premierradiobutton)
        self.inputs.addLayout(self.deuxiemecheckbox)
        if isSelected:
            self.defineActiveShip(Ship.id)
    
    def displayShipEnemy(self, Ship, line):
        shipSelector = "selector", Ship.id
        selector = ""
        globals()[selector] = shipSelector
        selector = QLabel(f"{Ship.name} ({Ship.size})")
        selector.setStyleSheet(f"background-color: {Ship.image}; padding: 3px;")
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
            button.setStyleSheet(f"background-color: {Ship.image}; padding: 3px;")

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
        numberOfShipEnnemyDestroyed = 0
        for shipEnnemy in Ships_enemy :
            ship_ennemy_name = globals()[shipEnnemy['name']]
            if ship_ennemy_name.isShipDestroyed () == True :
                numberOfShipEnnemyDestroyed = numberOfShipEnnemyDestroyed + 1
        print ("nombre de bateaux détruits : ", numberOfShipEnnemyDestroyed)
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

def make_ships ():
    # les gentils
    Moby_Dick = Ship (1, "Moby Dick", 5, "Mobydick.jpg", None)
    Vogue_Merry = Ship (2, "Merry", 2, "Vogue_Merry.jpg", "barrel", 2)
    Thousand_Sunny = Ship (3, "Thousand Sunny", 3, "Thousandsunny.jpg", "coup de burst", 3)
    Toto = Ship(4, "Toto le bateau", 7, "hollandaisvolant.jpg", None)

    # les méchants
    Moby_Dick_enemy = Ship (1, "Moby Dick", 5, "Mobydick.jpg" , None, 0)
    Vogue_Merry_enemy = Ship (2, "Merry", 2, "Vogue_Merry.jpg ", "barrel", 2)
    Thousand_Sunny_enemy = Ship (3, "Thousand Sunny", 3,  "Thousandsunny.jpg", "coup de burst", 3)
    Toto_enemy = Ship(4, "Toto le bateau", 7, "hollandaisvolant.jpg", None)

    ships = [
        {'id': 1, 'name': 'Moby_Dick'}, 
        {'id': 2, 'name': 'Vogue_Merry'},
        {'id': 3, 'name': 'Thousand_Sunny'},
        {'id': 4, 'name': 'Toto'}
    ]

    ships_enemy= [
        {'id': 1, 'name': 'Moby_Dick_enemy'}, 
        {'id': 2, 'name': 'Vogue_Merry_enemy'},
        {'id': 3, 'name': 'Thousand_Sunny_enemy'},
        {'id': 4, 'name': 'Toto_enemy'}
    ]
    return ships, ships_enemy, Moby_Dick, Moby_Dick_enemy, Vogue_Merry, Vogue_Merry_enemy, Thousand_Sunny,Thousand_Sunny_enemy,Toto, Toto_enemy

app = QApplication(sys.argv)
window = Window()
window.show()
Ships, Ships_enemy, Moby_Dick, Moby_Dick_enemy, Vogue_Merry, Vogue_Merry_enemy,Thousand_Sunny,Thousand_Sunny_enemy,Toto, Toto_enemy= make_ships ()
sys.exit(app.exec_())