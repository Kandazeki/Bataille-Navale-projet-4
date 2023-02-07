#je teste la programmation objet sur python

# je crée une classe 'Ship'
class Ship :
    # j'initialise le bateau en donnant son nom, sa taille et son arme
    def __init__(self, name, size, weapon):
        self.name = name
        self.size = size
        self.weapon = weapon

    # je diminue de 1 la taille du bateau donc sa vie
    def touched (self, size):
        self.size = self.size - 1

# Je crée 2 objets grâce à la classe ship
Thousand_Sunny = Ship ("Sunny", 3, "coup de burst")
Vogue_Merry = Ship ("Merry", 2, "barrel")

print (Thousand_Sunny.name, Thousand_Sunny.weapon)
print (Vogue_Merry.name, Vogue_Merry.weapon)

#je teste la fonction 'touched'
Thousand_Sunny.touched (Thousand_Sunny.size)

print (Thousand_Sunny.size)

# fonction pour vérifier si un bateau est détruit
def ShipDestroyed (ship):
    if ship.size == 0 :
        print ("votre ", ship, " a été détruit !")
    else :
        pass