#je teste la programmation objet sur python

# je crée une classe 'Ship'
class Ship :
    # j'initialise le bateau en donnant son nom, sa taille, son arme (et le nombre de fois qu'on peut l'utiliser)
    # et son état
    def __init__(self, name, size, weapon, number_of_use, state):
        self.name = name
        self.size = size
        self.weapon = weapon
        self.NumberOfUse = number_of_use
        self.state = state

    # je diminue de 1 la taille du bateau donc sa vie
    def touched (self):
        self.size = self.size - 1

    # j'augmente de 1 le nombre d'utilisation
    def UseWeapon (self):
        self.NumberOfUse = self.NumberOfUse + 1
        

# Je crée 3 objets grâce à la classe ship
Thousand_Sunny = Ship ("Sunny", 3, "coup de burst", 0, "alive")
Vogue_Merry = Ship ("Merry", 2, "barrel", 0, "alive")
Moby_Dick = Ship ("Moby Dick", 5, None, 0, "alive")

print (Thousand_Sunny.name, Thousand_Sunny.weapon)
print (Vogue_Merry.name, Vogue_Merry.weapon)
print (Moby_Dick.name)

#je teste la fonction 'touched'
Thousand_Sunny.touched ()

print (Thousand_Sunny.size)

# fonction pour vérifier si un bateau est détruit
def ShipDestroyed (ship):
    if ship.size == 0 :
        print ("votre", ship.name, "a été détruit !")
        ship.state = "destroyed"
    else :
        pass

# J'enlève les 2 vies du voque merry pour tester la fonction
Vogue_Merry.touched ()
Vogue_Merry.touched ()

ShipDestroyed (Vogue_Merry)
ShipDestroyed(Moby_Dick)