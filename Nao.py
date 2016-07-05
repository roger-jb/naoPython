# -*- coding: utf-8 -*-


class Nao:
    def __init__(self):
        self.isReal = True
        # self.isReal = False

        if self.isReal:
            self.ip = "lyonao.local"
            self.port = 9559
        else:
            self.ip = "127.0.0.1"
            self.port = 44338
