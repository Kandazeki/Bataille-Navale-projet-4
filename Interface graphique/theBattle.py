import sys
from functools import partial
from PyQt5.QtWidgets import QRadioButton, QFrame, QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QWidget
from classes import Ship

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.buttons = []

        self.grid_player = QGridLayout()
        self.grid_computer = QGridLayout()

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
                self.grid_computer.addWidget(button, x, y)
                row.append(button)
            self.buttons.append(row)

        self.title_player = QLabel("Placez vos bateaux")
        title_computer = QLabel("La grille de l'adversaire")
        
        frame_player = QFrame()
        frame_player.setFixedSize(600, 600)
        frame_player.setLayout(self.grid_player)

        frame_computer = QFrame()
        frame_computer.setFixedSize(600, 600)
        frame_computer.setLayout(self.grid_computer)

        v_box_layout_1 = QVBoxLayout()
        v_box_layout_1.addWidget(self.title_player)
        v_box_layout_1.addWidget(frame_player)
        frame_player.setLayout(self.grid_player)

        v_box_layout_2 = QVBoxLayout()
        v_box_layout_2.addWidget(title_computer)
        v_box_layout_2.addWidget(frame_computer)
        frame_computer.setLayout(self.grid_computer)

        central_widget = QWidget()
        h_box_layout = QHBoxLayout()

        h_box_layout.addWidget(frame_player)
        h_box_layout.addWidget(frame_computer)
        central_widget.setLayout(h_box_layout)
        self.setCentralWidget(central_widget)

        title = QHBoxLayout()
        title.addWidget(self.title_player)
        self.grid_player.addLayout(title, self.gridSize+1, 0, 1, 10)

        # On affiche la liste des bateaux du 
        i = 2
        for ship in Ships:
            shipName = ship['name']
            object = globals()[shipName]
            selected = True if i == 2 else False
            self.displayShipPlayer(object, self.gridSize+i, selected)
            i = i + 1

        #self.displayShipPlayer(Moby_Dick, self.gridSize+2, True)
        #self.displayShipPlayer(Vogue_Merry, self.gridSize+3)   
    
    def displayShipPlayer(self, Ship, line, isSelected = False):
        shipSelector = "selector", Ship.id
        selector = ""
        globals()[selector] = shipSelector
        shipSymbol = QPushButton("")
        shipSymbol.setStyleSheet(f"background-color: {Ship.color}; color:#fff;")
        shipSymbol.setText(Ship.symbol)
        self.selector = QRadioButton(Ship.name)
        self.selector.setAccessibleName(str(Ship.id))
        self.selector.setChecked(isSelected)
        check_box = QCheckBox("Vertical")
        self.selector.toggled.connect(partial(self.bouton_toggle, self.selector))
        check_box.stateChanged.connect(partial(self.check_toggle, check_box, Ship))
        inputs = QHBoxLayout()
        inputs.addWidget(shipSymbol)
        inputs.addWidget(self.selector)
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

    def btnGridSelected(self, x, y, Ship):
        Ship.position = [x, y]
        # si on positionne le bateau à la verticale, on fait la boucle de positionnement sur x
        # en se référant à Ship.position[x,y]  ref = 0 pour x, et ref = 1 pour y
        ref = 0 if Ship.alignement == "V" else 1
        startPosition = Ship.position[ref]
        endPosition = Ship.position[ref] + Ship.size
        if (endPosition <= self.gridSize) and (startPosition >= 0):
                for i in range(startPosition, endPosition):
                    self.checkShipCollisions(i, y, Ship)
                    self.toggleButton(i, y, Ship) if Ship.alignement == "V" else self.toggleButton(x, i, Ship)

    def toggleButton(self, x, y, Ship):
        button = self.buttons[x][y]
        if button.state == False:
            button.state = True
            button.ship = Ship.id
            button.setText(Ship.symbol)
            button.setStyleSheet(f"background-color: {Ship.color}; color:#fff;")
        else:
            button.state = False
            button.setStyleSheet(self.styleBlocks)

    def checkShipCollisions(self, x, y, Ship):
        ref = 0 if Ship.alignement == "V" else 1
        startPosition = Ship.position[ref]
        endPosition = Ship.position[ref] + Ship.size
        for i in range(startPosition-1, endPosition+1):
            for j in range(y-1, y+2):
                if i < 0 or j < 0 or i >= self.gridSize or j >= self.gridSize:
                    continue
                button = self.buttons[i][j]
                if button.ship != 0 and button.ship != Ship.id:
                    return True
        return False

    
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
        
Moby_Dick = Ship (1, "Moby Dick", 5, "red", "X", None)
Vogue_Merry = Ship (2, "Merry", 2, "blue", "O", "barrel", 2)
Thousand_Sunny = Ship (3, "Thousand Sunny", 3, "yellow", "#", "coup de burst", 3)
Toto = Ship(4, "Toto le bateau", 7, "brown", "T", None)

Ships = [
    {'id': 1, 'name': 'Moby_Dick'}, 
    {'id': 2, 'name': 'Vogue_Merry'},
    {'id': 3, 'name': 'Thousand_Sunny'},
    {'id': 4, 'name': 'Toto'}
]

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
