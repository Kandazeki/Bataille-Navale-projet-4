#je teste la programmation objet sur python

# je crée une classe 'Ship'
class Ship :
    # j'initialise le bateau en donnant son nom, sa taille, 
    # son arme, le nombre de fois qu'on peut l'utiliser et ses points de vie
    def __init__(self, name, size, weapon, number_of_use = 0):
        self.name = name
        self.size = size
        self.weapon = weapon
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

# Je crée 3 objets grâce à la classe ship
Thousand_Sunny = Ship ("Sunny", 3, "coup de burst", 3)
Vogue_Merry = Ship ("Merry", 2, "barrel", 2)
Moby_Dick = Ship ("Moby Dick", 5, None)
Thousand_Sunny_ennemi = Ship ("Sunny", 3, "coup de burst", 3)
Vogue_Merry_ennemi = Ship ("Merry", 2, "barrel", 2)
Moby_Dick_ennemi = Ship ("Moby Dick", 5, None)

#je teste la fonction 'touched'
Thousand_Sunny.touched ()
print (Thousand_Sunny.life)

# J'enlève les 2 vies du voque merry pour tester la fonction 'isShipDestroyed'
Vogue_Merry.touched ()
Vogue_Merry.touched ()
Vogue_Merry.isShipDestroyed()
Moby_Dick.isShipDestroyed()

# je teste la fonction qui enlève une munition si le bateau n'est pas détruit et qu'il lui reste des munitions
print ("\nVous avzez", Thousand_Sunny.NumberOfUse, "munitions")
Thousand_Sunny.useWeapon()
print ("il vous reste", Thousand_Sunny.NumberOfUse, 'munitions')
Thousand_Sunny.useWeapon()
print ("il vous reste", Thousand_Sunny.NumberOfUse, 'munition')
Thousand_Sunny.useWeapon()
print ("il vous reste", Thousand_Sunny.NumberOfUse, 'munition')
Thousand_Sunny.useWeapon()
print ("il vous reste", Thousand_Sunny.NumberOfUse, 'munition')

# je teste si une des équipes a gagné ou pas encore
def IsGameOver():
        if Thousand_Sunny.life == 0 and Vogue_Merry.life == 0 and Moby_Dick.life == 0 :
            print ("\nvous avez perdu l'équipe ennemie vous a anéanti")
            print ('------------------------------------------------------------------------------------------------------------')
            return True
        elif Thousand_Sunny_ennemi.life == 0 and Vogue_Merry_ennemi.life == 0 and Moby_Dick_ennemi.life == 0 :
            print ("\nVous avez gagné l'équipe ennemie a été défaite !")
            print ('-----------------------------------------------------------------------------------------------------')
            return True
        else :
            return False

# je teste si ma fonction 'isgameover' marche
while Moby_Dick.isShipDestroyed() == False :
    Moby_Dick.touched ()
while Thousand_Sunny.isShipDestroyed () == False :
    Thousand_Sunny.touched ()
IsGameOver ()

print("\n\nBonjour comme tu l'as vu j'ai un peu avancé cependant mon code n'est pas vraiment utilisable pour le moment"\
      +" il faudrait en effet avancer dans l'interface graphique avant d'aller plus loin "\
        + "j'ai essayé de créer une grille dans le fichier grilleinterface mais on ne peut pas faire grand chose avec pour le moment"\
            +" c'est pourquoi si tu vois ce message il faudrait qu'on s'organise pour voir comment on avance et surtout comment on fait cette putain de grille "\
                +" \ntrès cordialement,\nta camarade de NSI.")