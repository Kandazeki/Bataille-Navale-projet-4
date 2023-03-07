import sys
from functools import partial
from PyQt5.QtWidgets import QFrame, QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QPushButton, QWidget
from classes import Ship

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.buttons = []

        grid = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)
        self.gridSize = 10

        for x in range(self.gridSize):
            row = []
            for y in range(self.gridSize):
                button = QPushButton(" ")
                button.setStyleSheet("background-color: #f4f4f4;")
                button.clicked.connect(lambda checked, x=x, y=y: self.button_clicked(x, y))
                button.state = False
                grid.addWidget(button, x, y)
                row.append(button)
            self.buttons.append(row)

        ship_label = QLabel(Moby_Dick.name)
        x_label = QLabel("X : ")
        y_label = QLabel("Y : ")
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.check_box = QCheckBox("Vertical")
        ok_button = QPushButton("Place ship")
        ok_button.clicked.connect(partial(self.ok_clicked, Moby_Dick, self.x_input, self.y_input, self.check_box))
        inputs = QHBoxLayout()
        inputs.addWidget(ship_label)
        inputs.addWidget(x_label)
        inputs.addWidget(self.x_input)
        inputs.addWidget(y_label)
        inputs.addWidget(self.y_input)
        inputs.addWidget(self.check_box)
        inputs.addWidget(ok_button)
        grid.addLayout(inputs, 15, 0, 1, 5)

        ship_label2 = QLabel(Vogue_Merry.name)
        x_label2 = QLabel("X : ")
        y_label2 = QLabel("Y : ")
        self.x_input2 = QLineEdit()
        self.y_input2 = QLineEdit()
        self.check_box2 = QCheckBox("Vertical")
        ok_button2 = QPushButton("Place ship")
        ok_button2.clicked.connect(partial(self.ok_clicked, Vogue_Merry, self.x_input2, self.y_input2, self.check_box2))
        inputs2 = QHBoxLayout()
        inputs2.addWidget(ship_label2)
        inputs2.addWidget(x_label2)
        inputs2.addWidget(self.x_input2)
        inputs2.addWidget(y_label2)
        inputs2.addWidget(self.y_input2)
        inputs2.addWidget(self.check_box2)
        inputs2.addWidget(ok_button2)
        grid.addLayout(inputs2, 17, 0, 1, 5)

    def ok_clicked(self, Ship, x, y, isVertical):
        x = int(x.text()) - 1
        y = int(y.text()) - 1
        button = self.buttons[x][y]
        Ship.position = [x, y]
        if isVertical.isChecked():
            Ship.alignement = 'V'
        else:
            Ship.alignement = 'H'
        print(Ship.name, Ship.position)
        self.positionShipOnGrid(Ship, x, y)
    
    def positionShipOnGrid(self, Ship, x, y):
        # si on positionne le bateau à la verticale, on faire la boucle de positionnement sur x
        # en se référant à Ship.position[x,y] 
        ref = 0 if Ship.alignement == "V" else 1
        startPosition = Ship.position[ref]
        endPosition = Ship.position[ref] + Ship.size
        if (endPosition <= self.gridSize) and (startPosition >= 0):
                for i in range(startPosition, endPosition):
                    self.toggleButton(i, y) if Ship.alignement == "V" else self.toggleButton(x, i)

    def toggleButton(self, x, y):
        button = self.buttons[x][y]
        if button.state == False:
            button.state = True
            button.setStyleSheet("background-color: yellow")
        else:
            button.state = False
            button.setStyleSheet("background-color: lightGrey")
        
    def button_clicked(self, x, y):
        button = self.buttons[x][y]
        self.toggleButton(x, y)
        button.setText('X')
        print('TEST ', Moby_Dick.name, Moby_Dick.size, self.check_box.isChecked(), 'State : ', button.state)

Moby_Dick = Ship ("Moby Dick", 5, None)
Vogue_Merry = Ship ("Merry", 2, "barrel", 2)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
