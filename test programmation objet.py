#je teste la programmation objet sur python

# je crée une classe 'Ship'
class Ship :
    # j'initialise le bateau en donnant son nom, sa taille, 
    # son arme (et le nombre de fois qu'on peut l'utiliser) et son état
    def __init__(self, name, size, weapon, number_of_use = 0):
        self.name = name
        self.size = size
        self.weapon = weapon
        self.NumberOfUse = number_of_use
        self.life = self.size

    # je diminue de 1 la taille du bateau donc sa vie
    def touched (self):
        self.life = self.life - 1

    # j'augmente de 1 le nombre d'utilisation
    def useWeapon (self):
        if self.IsAbleToUseWeapon() == True :
            self.NumberOfUse = self.NumberOfUse - 1
        else :
            print ("Vous ne pouvez pas utiliser votre arme")

    # je teste si le bateau est détruit
    def isShipDestroyed(self):
        if self.life == 0 :
            print ("votre", self.name, "a été détruit !")
            return True
        else :
            return False
    
    #on teste si le bateai peut utiliser son arme
    def IsAbleToUseWeapon (self):
        if self.NumberOfUse <= 0 or self.life == 0 :
            return False
        else :
            return True

# Je crée 3 objets grâce à la classe ship
Thousand_Sunny = Ship ("Sunny", 3, "coup de burst", 3)
Vogue_Merry = Ship ("Merry", 2, "barrel", 2)
Moby_Dick = Ship ("Moby Dick", 5, None)

print (Thousand_Sunny.name, Thousand_Sunny.weapon)
print (Vogue_Merry.name, Vogue_Merry.weapon)
print (Moby_Dick.name)

#je teste la fonction 'touched'
Thousand_Sunny.touched ()

print (Thousand_Sunny.life)

# J'enlève les 2 vies du voque merry pour tester la fonction
Vogue_Merry.touched ()
Vogue_Merry.touched ()

Vogue_Merry.isShipDestroyed()
Moby_Dick.isShipDestroyed()

Thousand_Sunny.useWeapon()
print ("il vous reste", Thousand_Sunny.NumberOfUse, 'munitions')
Thousand_Sunny.useWeapon()
Thousand_Sunny.useWeapon()
print (Thousand_Sunny.NumberOfUse)
Thousand_Sunny.useWeapon
print (Thousand_Sunny.NumberOfUse)
print(Thousand_Sunny.useWeapon)