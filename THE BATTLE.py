import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QTextEdit, QRadioButton, QFrame, QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QWidget, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtGui import QTextCursor
import random
import time
import datetime
import json
from classes import *

#Apparition des bateaux adverses pour pouvoir débuguer si besoin
DEBUG = False

#Création d'une fenetre principale
class Window(QMainWindow):
    #initialisation 
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
        self.elapsed_time = 0
        self.gridSize = 10
        self.activeShip = ''
        self.styleBlocks = "background-color: #f4f4f4;"
        
        # game parameters, initialisation du système de jeu
        self.timer_label = QLabel("00:00")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.grid_center.addWidget(self.timer_label)
        self.isReadyToPlay = False
        self.isBattleStarted = False
        self.isSinkingBoat = False
        self.memoX = 100
        self.memoY = 100
        self.isXactive = True
        self.iteration = 1
        self.direction = 1
        self.isEndOfTheBattle = False
        self.numberOfShipEnnemyDestroyed = 0
        self.numberOfShipDestroyed = 0
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
        
        # Mise en place de l'interface graphique tout les labels et bouton qui apparaissent

        self.spacer = QLabel ('')
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
        self.normal.setChecked(True)
        self.button_center.clicked.connect(self.startBattle)
        title_computer = QLabel("La flotte ennemie prête au combat")
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.grid_center.addWidget(self.text_edit)
        self.grid_center.addWidget(self.button_center)
        self.log('Placez vos bateaux')
        
        ## Frame et Widgets associés à leur utilisateur
        # PLAYER
        frame_player = QFrame()
        frame_player.setFixedSize(700, 900)
        frame_player.setLayout(self.grid_player)
        frame_player.setLayout(self.grid_player)
        title = QHBoxLayout()
        title.addWidget(title_player)
        self.grid_player.addLayout(title, self.gridSize+1, 0, 1, 10)
        
        # CENTER
        frame_center = QFrame()
        frame_center.setFixedSize(300, 600)
        frame_center.setLayout(self.grid_center)
        
        # COMPUTER
        frame_computer = QFrame()
        frame_computer.setFixedSize(700, 900)
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
    
    #Affichage de messages curseurs au centre 
    def log(self, message):
        message = str(message)
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertPlainText(message + '\n')
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    #Définition des endroits où le bateau enemi peut attaquer c'est aléatoire
    def choosePlaceToFight(self) :
        if self.isSinkingBoat == True:
            self.precisionFight()
        else:    
            x = random.randint(0, self.gridSize-1)
            y = random.randint(0, self.gridSize-1)
            if self.buttons[x][y].isPlayed != True:
                self.fight(x, y, False)
            else:
                self.choosePlaceToFight()

    #On retient les endroits où on a tiré et touché un bateau
    def precisionFight(self):
        if self.isXactive == True:
            x = self.calcNewPosition(self.memoX)
            y = self.memoY
        else:
            x = self.memoX
            y = self.calcNewPosition(self.memoY)
        self.iteration = self.iteration + 1
        self.fight(x, y, False)

    #Puis on retire à côté de l'emplacement trouvé
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

    #La fonction fight est la principale du programme, elle permet de jouer et de mettre toutes les commandes en action
    def fight(self, x, y, playingOnEnemyGrid = True):
        #On crée une variable is.Played pour déterminer si une action a été faite 
        button = self.buttons_enemy[x][y] if playingOnEnemyGrid == True else self.buttons[x][y]
        button.isPlayed = True

        #On met en place le système d'armes pour l'ordinateur qui vérifie et détermine au hasard les armes utilisées
        if playingOnEnemyGrid == False and self.isSinkingBoat == False:
            self.activeWeapon = random.randint(0, 2)
            if self.activeWeapon == 1 and Thousand_Sunny_enemy.IsAbleToUseWeapon() == False:
                self.activeWeapon = 0
            if self.activeWeapon == 2 and Vogue_Merry_enemy.IsAbleToUseWeapon() == False:
                self.activeWeapon = 0

        if self.isBattleStarted:
             # définition des effets du Coup de Burst
            if self.activeWeapon == 1: 
                #Utilisable en vertical et Horizontale (par défaut horizontale)
                modeVerical = self.coupdeburstMode.isChecked()
                ref = x if modeVerical else y
                hasTouched = False
                #on détermine la ligne ou colonne touché on vérifie si il y a des bateaux et on colore en Bleu ou rouge
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

            # définition des effets du Barrel
            if self.activeWeapon == 2:
                hasTouched = False
                #On détermine dans quel cadre on peut toucher
                xMax = x + 2 if x + 2 <= self.gridSize else self.gridSize
                yMax = y + 2 if y + 2 <= self.gridSize else self.gridSize
                #Vérification qu'on joue sur la grille ennemie
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

            #Le bateau est touché (colorier en rouge et afficher)
            elif button.state == True :
                self.boatIsTouched(x, y, button, playingOnEnemyGrid)
            
            #On précise à l'utilisateur qu'il a raté
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
            #C'est ensuite au tour de l'ennemi       
            if playingOnEnemyGrid == True:
                self.choosePlaceToFight()
        else:
            self.log('Placez vos bateaux !!!')

    #On définit les actions à faire quand un bateau est touché
    def boatIsTouched(self, x, y, button, playingOnEnemyGrid) :
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
    #On transforme l'interface pour permettre la bataille
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
    
    #Eviter de pouvoir replacer les bateaux une fois placé
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

    def changeWeapon(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.activeWeapon = int(radioButton.objectName())

    #Affichage des bateaux gentils
    def displayShipPlayer(self, Ship, line, isSelected = False):
        selector = QRadioButton(f"{Ship.name} ({Ship.size})")
        selector.setStyleSheet(f"background-color: {Ship.color}; color: {Ship.textColor}; padding: 3px;")
        selector.setAccessibleName(str(Ship.id))
        selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        selector.setChecked(isSelected)
        check_box = QCheckBox("Vertical")
        check_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        selector.toggled.connect(partial(self.bouton_toggle, selector))
        check_box.stateChanged.connect(partial(self.check_toggle, check_box, Ship))
        self.premierradiobutton.addWidget(selector)
        self.deuxiemecheckbox.addWidget(check_box)
        self.grid_player.addLayout(self.inputs, line, 0, 1, 10)
        self.inputs.addLayout(self.premierradiobutton)
        self.inputs.addLayout(self.deuxiemecheckbox)
        if isSelected:
            self.defineActiveShip(Ship.id)

    #Affichage des bateaux 
    def displayShipEnemy(self, Ship, line):
        shipSelector = "selector", Ship.id
        selector = ""
        globals()[selector] = shipSelector
        selector = QLabel(f"{Ship.name} ({Ship.size})")
        selector.setStyleSheet(f"background-color: {Ship.color}; color: {Ship.textColor}; padding: 3px;")
        inputs = QHBoxLayout()
        inputs.addWidget(selector)
        self.grid_computer.addLayout(inputs, line, 0, 1, 10)

    #Définition pour pouvoir placer les bateaux et afficher leurs noms et les placer à la verticale ou l'horizontale
    def bouton_toggle(self, radioBtn):
        if radioBtn.isChecked():
            self.defineActiveShip(int(radioBtn.accessibleName()))
    
    def check_toggle(self, check, Ship):
        Ship.alignement = "V" if check.isChecked() else "H"
    
    def defineActiveShip(self, id):
        for x in Ships:
                if x['id'] == id:
                    self.activeShip = x['name']


    #Placement des bateaux
    def btnGridSelected(self, x, y, Ship, isEnemy = False):
        errorPosition = False
        Ship.position = [x, y]
        buttons = self.buttons if isEnemy == False else self.buttons_enemy
        # si on positionne le bateau à la verticale, on fait la boucle de positionnement sur x
        # en se référant à Ship.position[x,y]  ref = 0 pour x, et ref = 1 pour y
        ref = 0 if Ship.alignement == "V" else 1
        startPosition = Ship.position[ref]
        endPosition = Ship.position[ref] + Ship.size
        if endPosition <= self.gridSize and startPosition >= 0 :
                for i in range(startPosition, endPosition):
                    if Ship.alignement == "V" and buttons[i][y].state == True :
                        errorPosition = True
                    
                    if Ship.alignement == "H" and buttons[x][i].state == True :
                        errorPosition = True
        if endPosition <= self.gridSize and startPosition >= 0 and errorPosition == False :
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
    
    #On vérifie si on affiche ou non les bateaux alliés:
    #Oui
    def displayShipOnGrid(self, x, y, Ship, isEnemy = False):
        buttons = self.buttons if isEnemy == False else self.buttons_enemy
        button = buttons[x][y]
        button.state = True
        button.ship = Ship.id
        if isEnemy == False or DEBUG == True :
            button.setText(Ship.symbol)
            button.setStyleSheet(f"background-color: {Ship.color}; color: {Ship.textColor}; padding: 3px;")
    # on déplace un bateau donc on commence par le déplacer
    def removeShipFromGrid(self, id):
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                button = self.buttons[x][y]
                if button.ship == id:
                    button.ship = 0
                    button.state = False
                    button.setText('')
                    button.setStyleSheet(self.styleBlocks)

    #savoir si un bouton a été cliqué
    def button_clicked(self, x, y):
        ship = globals()[self.activeShip]
        self.removeShipFromGrid(ship.id)
        self.btnGridSelected(x, y, ship)

    #Rejouer 
    def DoANewGame (self):
        self.close()
        if not QCoreApplication.instance():
            new_app = QApplication(sys.argv)
            
        else :
            new_app = QCoreApplication.instance()
        new_main_window = Window()
        new_main_window.show()
        new_app.exec_()
    
    #On vérifie si tous les bateaus sont détruits et chez qui
    #Partie Gagné
    def IsGameWon (self) :
        self.numberOfShipEnnemyDestroyed = self.numberOfShipEnnemyDestroyed + 1
        print ("nombre de bateaux détruits : ", self.numberOfShipEnnemyDestroyed)
        if self.numberOfShipEnnemyDestroyed == len (Ships_enemy) :
            self.log ("Vous avez gagné !")
            self.isEndOfTheBattle = True
            self.grid_center.addWidget(self.winBattle)
            self.grid_center.addWidget(self.PlayAgain)
            self.timer.stop()
            self.save_score(self.elapsed_time)
            self.get_best_score ()

    #Partie Perdu
    def IsGameLost (self) :
        self.numberOfShipDestroyed = self.numberOfShipDestroyed + 1
        if self.numberOfShipDestroyed == len (Ships) :
                print ("Vous avez perdu")
                self.isEndOfTheBattle = True
                self.grid_center.addWidget(self.looseBattle)
                self.grid_center.addWidget(self.PlayAgain)

    ##Le Chrono
    #Mise à jour 
    def update_timer(self):
        self.elapsed_time += 1
        self.timer_label.setText(time.strftime("%M:%S", time.gmtime(self.elapsed_time)))

    #Utilisation d'un fichier json pour stocker les scores
    def save_score(self, score):
        filename = "scores.json"
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"best_score": None}
        if data["best_score"] is None or score < data["best_score"]:
            data["best_score"] = score
            data["best_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

    #Définir les meilleurs scores
    def get_best_score(self):
        with open('scores.json', 'r') as f:
            scores = json.load(f)
        if not scores:
            return None
        self.log ('le meilleur score est de ' + str(scores["best_score"]))
        self.log ("vous êtes à " + str(self.elapsed_time - scores["best_score"]) + " secondes du meilleur score.")

###Les infos pour tout
       
# les gentils
Moby_Dick = Ship (1, "Moby Dick", 5, "red", "white", "X", None)
Vogue_Merry = Ship (2, "Merry", 2, "blue", "white", "O", "barrel", 2)
Thousand_Sunny = Ship (3, "Thousand Sunny", 3, "yellow", "black", "#", "coup de burst", 3)
hollandais = Ship(4, "hollandais volant", 7, "brown", "white", "T", None)
# les méchants
Moby_Dick_enemy = Ship (1, "Moby Dick", 5, "red", "white", "X", None)
Vogue_Merry_enemy = Ship (2, "Merry", 2, "blue", "white", "O", "barrel", 2)
Thousand_Sunny_enemy = Ship (3, "Thousand Sunny", 3, "yellow", "black", "#", "coup de burst", 3)
hollandais_enemy = Ship(4, "hollandais volant", 7, "brown", "white", "T", None)

#Les raccourcis pour appeler les bateaux
Ships = [
    {'id': 1, 'name': 'Moby_Dick'}, 
    {'id': 2, 'name': 'Vogue_Merry'},
    {'id': 3, 'name': 'Thousand_Sunny'},
    {'id': 4, 'name': 'hollandais'}
]

Ships_enemy= [
    {'id': 1, 'name': 'Moby_Dick_enemy'}, 
    {'id': 2, 'name': 'Vogue_Merry_enemy'},
    {'id': 3, 'name': 'Thousand_Sunny_enemy'},
    {'id': 4, 'name': 'hollandais_enemy'}
]
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
