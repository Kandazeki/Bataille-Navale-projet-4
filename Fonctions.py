from data import*
#import sys
#from PyQt5.QtCore import Qt
#from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLabel, QLineEdit

win = int

def bateau_allie():
    for bateau in data: 
        bateau.append(bateau_alliee)
    print(bateau_alliee)   

def bateau_ennemi() :
    for bateau in data :
        bateau.append(bateau_ennemie)
    print (bateau_ennemie)

def mouvement():
    pass


def Level() :
    level_text = input ("Stp marche")
    if level_text == 1:
        PiratesLevel()
    if level_text == 2:
        WarLevel()
    if level_text == 3:
        FuturLevel()

def PiratesLevel ():
    #import design1#phto pirate
    Round()

def WarLevel():
    #import design2#photo war
    Round()

def FuturLevel():
    #import design3#photo futur
    Round()
    
def Round():
    bateau_allie()
    bateau_ennemi()


def touché():
    bateau = True
    if bateau : False
    print ("touché")


def NewWeapons() :
    if win == 3:
        print("You won a new weapons")
        weapons.append(gamer)