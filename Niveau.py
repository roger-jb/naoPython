

class Niveau:
    def __init__(self, id_niveau, nb_chance, nb_car):
        self.id_niveau = id_niveau
        self.nb_chance = nb_chance
        self.nb_car = nb_car

    def getIdNiveau(self):
        return self.id_niveau

    def getNbChance(self):
        return self.nb_chance

    def getNbCar(self):
        return self.nb_car