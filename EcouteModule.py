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
        """ méthode qui récupère les mots dits et les répète """
        self.stopReco()
        if len(value) > 1 and value[1] > self.precision:  # 0.3 : seuil de 30%
            self.__callback(str(value[0]))
        else:
            self.startListening(self.__callback)

    def startRecoYN(self, callback):
        vocabulaire = ['oui', 'non']
        EcouteModule.startReco(self, callback, vocabulaire)

    def startRecoNiveau(self, callback):
        vocabulaire = ["facile", "normal", "difficile"]
        EcouteModule.startReco(self, callback, vocabulaire)

    def startRecoLettre(self, callback):
        vocabulaire = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                       "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                       "ALPHA", "BRAVO", "CHARLIE", "DELTA", "ECHO", "FOXTROT", "GOLF",
                       "HOTEL", "INDIA", "JULIET", "KILO", "LIMA", "MIKE", "NOVEMBER",
                       "OSCAR", "PAPA", "QUEBEC", "ROMEO", "SIERRA", "TANGO", "UNIFORM",
                       "VICTOR", "WHISKY", "XRAY", "YANKEE", "ZOULOU"]
        EcouteModule.startReco(self, callback, vocabulaire)

    def startReco(self, callback, vocabulaire):
        print "startReco"
        if self.__sr is not None:
            self.__sr.setVocaulary(vocabulaire, False)
        self.__callback = callback
        memory.subscribeToEvent("WordRecognized", "Ecoute", "onWordRecognized")

    def stopReco(self):
        print "stopReco"
        memory.unsubscribeToEvent("WordRecognized", "Ecoute")
