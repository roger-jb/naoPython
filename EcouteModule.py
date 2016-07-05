# -*- coding: utf-8 -*-
from naoqi import ALModule, ALProxy


class EcouteModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        try:
            self.__sr = ALProxy("ALSpeechRecognition")
            self.__sr.setLanguage("French")
        except Exception, e:
            print("Impossible de définir la restriction de vocabulaire")
            print("Probable utilisation d'un robot virtuel, on continue")
            self.__sr = None

        global memory
        memory = ALProxy("ALMemory")
        self.__callback = None
        self.motReconnu = None
        self.precision = 0.3

    def onWordRecognized(self, eventName, value, subIdent):
        """ méthode qui récupère les mots dits et lance la méthode callback associée """
        vocabulaire = self.vocabulaire
        self.stopReco()
        if len(value) > 1 and value[1] > self.precision:  # 0.3 : seuil de 30%
            self.__callback(str(value[0]))
        else:
            self.startReco(self.__callback, vocabulaire)

    def startRecoYN(self, callback):
        """
        ecoute avec retour attendu OUI/NON
        :param callback: méthode traitant le retour
        """
        vocabulaire = ['oui', 'non']
        EcouteModule.startReco(self, callback, vocabulaire)

    def startRecoNiveau(self, callback):
        """
        ecoute pour le niveau de difficulté (facile/normal/difficile)
        :param callback: methode traitant le retour
        """
        vocabulaire = ["facile", "normal", "difficile"]
        EcouteModule.startReco(self, callback, vocabulaire)

    def startRecoLettre(self, callback):
        """
        ecoute pour la récupération des lettres
        :param callback: methode traitant le retour
        """
        vocabulaire = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                       "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                       "ALPHA", "BRAVO", "CHARLIE", "DELTA", "EQUO", "FOXTROTE", "GOLF",
                       "HOTEL", "INDIA", "JULIETTE", "KILO", "LIMA", "MIKE", "NOVEMBEURRE",
                       "OSCAR", "PAPA", "QUEBEC", "ROMEO", "SIERRA", "TANGO", "UNIFORME",
                       "VICTOR", "WHISKY", "XYLOPHONE", "YAOURT", "ZOULOU"]
        EcouteModule.startReco(self, callback, vocabulaire)

    def startReco(self, callback, vocabulaire):
        """

        :param callback: la méthode traitant le retour
        :param vocabulaire: la liste des mots attendus
        """
        self.vocabulaire = vocabulaire
        print "startReco"
        if self.__sr is not None:
            self.__sr.setVocabulary(vocabulaire, False)
        self.__callback = callback
        memory.subscribeToEvent("WordRecognized", "Ecoute", "onWordRecognized")

    def stopReco(self):
        """
        arrete l'écoute
        """
        print "stopReco"
        self.vocabulaire = None
        memory.unsubscribeToEvent("WordRecognized", "Ecoute")
