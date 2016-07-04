# -*- coding: utf-8 -*-
import time
from naoqi import ALBroker
from Nao import *
from EcouteModule import *
from Pendu import *


def main():
    nao = Nao()
    global broker
    broker = ALBroker("broker", "0.0.0.0", 0, nao.ip, nao.port)
    global Ecoute
    Ecoute = EcouteModule("Ecoute")
    pendu = Pendu(broker, Ecoute)
    pendu.debut_partie()

    pendu.attendre()
    # Ecoute.startRecoYN(Ecoute)
    # time.sleep(5)
    # print "fin sleep"
    # print str(Ecoute.motReconnu)
    # Ecoute.stopReco()

if __name__ == "__main__":
    main()
