class Ship :
    # j'initialise le bateau en donnant son nom, sa taille, 
    # son arme, le nombre de fois qu'on peut l'utiliser et ses points de vie
    def __init__(self, id, name, size, color, symbol, weapon, number_of_use = 0):
        self.id = id
        self.name = name
        self.size = size
        self.color = color
        self.symbol = symbol
        self.weapon = weapon
        self.position = []
        self.alignement = 'H'
        self.NumberOfUse = number_of_use
        self.life = self.size

    # je diminue de 1 la vie du bateau si il est touché
    def touched (self):
        self.life = self.life - 1

    # je diminue de 1 le nombre de munition si le bateau peut attaquer
    def useWeapon (self):
        if self.IsAbleToUseWeapon() == True :
            self.NumberOfUse = self.NumberOfUse - 1
        elif self.IsAbleToUseWeapon() == False : 
            print ("Vous ne pouvez pas utiliser votre arme")

    # je teste si le bateau est détruit
    def isShipDestroyed(self):
        if self.life == 0 :
            print ("votre", self.name, "a été détruit !")
            return True
        else :
            return False
    
    # on teste si le bateau peut utiliser son arme (si il n'est pas détruit et qu'il lui reste des munitions)
    def IsAbleToUseWeapon (self):
        if self.NumberOfUse <= 0 or self.life == 0 :
            return False
        else :
            return True