# on doit trouver l'antécédent de 0 dans une fonction grâce à la dichotomie

import math
# c'est la fonction qu'on va étudier
def f(x):
    y = math.cos (x) + math.sin(x)
    return y

# C'est l'intervalle des valeurs dans lequel on va chercher des valeurs
a = 2
b = 3
epsilon = 0.001

# On cherhe l'antécédent de 0
def FindAntecedentOf0 (a,b,epsilon):
    # m est la première valeur qu'on teste, c'est le milieu entre a et b
    m = (a + b)/2
    # on créée une boucle tant que l'antécédent de m ne s'approche pas de 0
    # (ca serait trop long d'essayer d'obtenir pile 0)
    while abs (f(m))> epsilon :
        m = (a+b)/2
        # On cherche le signe de la multiplication pour déterminer si m est plus proche de a ou de b
        if f(a)*f(m)<0 :
            # on place b à la nouvelle valeur de m car m est plus proche de a
            b = m
        if f(a)*f(m)>0 :
            # on place a à la nouvelle valeur de m car m est plus proche de b
            a = m
    return m
# et on print le résultat :)
print ("le resultat est", FindAntecedentOf0(a,b,epsilon))

