# -*- coding: utf-8 -*-
from naoqi import ALBroker
from Nao import *
from EcouteModule import *
from Pendu import *


def main():
    nao = Nao()
    # création du broker
    global broker
    broker = ALBroker("broker", "0.0.0.0", 0, nao.ip, nao.port)
    # création du speachRecognition
    global Ecoute
    Ecoute = EcouteModule("Ecoute")
    # création de l'objet pendu avec le broker et le SpeachRecogn en paramètre
    pendu = Pendu(broker, Ecoute)
    # lancement du jeu
    pendu.debut_partie()
    # mise en attente du main pour permettre de jouer
    pendu.attendre()


if __name__ == "__main__":
    main()
