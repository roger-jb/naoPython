import threading
from random import choice

from naoqi import ALProxy
from Niveau import *


class Pendu:
    def __init__(self, le_broker, l_ecoute):
        """

        :param le_broker:
        :param l_ecoute:
        """
        self.__broker = le_broker
        self.__ecoute = l_ecoute
        self.__parle = ALProxy("ALTextToSpeech")
        self.__parle.setLanguage("French")

        self.nouvelle_partie = True
        self.niveau = None
        self.mot_recherche = None
        self.mot_trouve = None
        self.lettres_trouvees = []
        self.erreure = 0
        self.liste_mot_complet = None

        self.load_dictionnaire()

        self.conditional_object = threading.Condition()

    def debut_partie(self):
        self.reset_info()
        self.veut_jouer()

    def reset_info(self):
        self.niveau = None
        self.mot_recherche = None
        self.mot_trouve = None
        self.lettres_trouvees = []
        self.erreure = 0

    def quitter(self):
        self.conditional_object.acquire()
        self.nouvelle_partie = False
        self.conditional_object.notify_all()
        self.conditional_object.release()
        self.dire("Au revoir.")
        print "pendu.quitter"

    def attendre(self):
        self.conditional_object.acquire()
        while self.nouvelle_partie:
            self.conditional_object.wait()
        self.conditional_object.release()

    def dire(self, texte):
        self.__parle.say(texte)

    def selectionne_mot(self):
        liste_mot_du_niveau = []
        for mot in self.liste_mot_complet:
            if len(mot) <= self.niveau.getNbCar():
                liste_mot_du_niveau.append(mot)
            else:
                pass
        self.mot_recherche = choice(liste_mot_du_niveau)
        print ("spoil : " + str(self.mot_recherche))
        self.masque_mot()
        self.tour_de_jeu()

    def veut_jouer(self):
        self.dire("Veux-tu jouer au pendu ?")
        self.__ecoute.startRecoYN(self.rep_veut_jouer)

    def rep_veut_jouer(self, reponse):
        print "reponse CB : " + reponse

        if reponse == 'non':
            self.quitter()
        else:
            self.choix_niveau()

        # self.quitter()

    def choix_niveau(self):
        self.dire("Quel niveau souhaites tu ?")
        self.dire("facile, normal, difficile")
        self.__ecoute.startRecoNiveau(self.rep_choix_niveau)

    def rep_choix_niveau(self, reponse):
        compris = False
        if reponse == 'facile':
            self.niveau = Niveau(1, 12, 6)
            compris = True
        elif reponse == 'normal':
            self.niveau = Niveau(2, 8, 10)
            compris = True
        elif reponse == 'difficile':
            self.niveau = Niveau(3, 6, 15)
            compris = True
        else:
            self.dire("Je n'ai pas compris")

        if compris:
            self.selectionne_mot()
        else:
            self.choix_niveau()

    def tour_de_jeu(self):
        if self.mot_recherche != self.mot_trouve and self.erreure < self.niveau.getNbChance():
            self.dire("Il te reste " + str(self.niveau.getNbChance() - self.erreure) + " chance")
            self.epeler_mot()
            self.recuperer_lettre()
        else:
            self.fin_partie()

    def load_dictionnaire(self):
        fichier = open("Dictionnaire.txt", 'r')
        contenu = fichier.read()
        fichier.close()
        self.liste_mot_complet = contenu.split("\n")

    def masque_mot(self):
        self.mot_trouve = ""
        for lettre in self.mot_recherche:
            if lettre in self.lettres_trouvees:
                self.mot_trouve += lettre
            else:
                self.mot_trouve += "_"

    def fin_partie(self):
        if self.mot_trouve == self.mot_recherche:
            self.dire("Bravo, le mot est bien")
        else:
            self.dire("PENDU !!! le mot est")
        self.dire(self.mot_recherche)
        self.debut_partie()

    def epeler_mot(self):
        if len(self.lettres_trouvees) == 0:
            self.dire("le mot est de " + str(len(self.mot_recherche)) + " lettre")
        else:
            for lettre in self.mot_recherche:
                if lettre not in self.lettres_trouvees:
                    self.dire("inconnu")
                else:
                    self.dire(lettre.lower())

    def recuperer_lettre(self):
        self.dire("proposes une lettre")
        self.__ecoute.startRecoLettre(self.rep_recuperer_lettre)

    def rep_recuperer_lettre(self, reponse):
        lettre = reponse[0]
        print "la lettre est : " + str(lettre)
        if self.niveau.getIdNiveau() < 3 and lettre in self.lettres_trouvees:
            self.dire("tu as deja dit cette lettre")
        elif str(lettre) in self.mot_recherche:
            self.lettres_trouvees.append(lettre)
            self.dire("Bravo")
        else:
            self.erreure += 1
            self.dire("dommage, la lettre n'est pas presente")
        self.masque_mot()
        self.tour_de_jeu()
