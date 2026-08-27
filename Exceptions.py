
class TributError(Exception):

    def __init__(self, tribut):


        self.tribut = tribut

        print(f'{tribut} Inválido')

    def __repr__(self):
        return f'{self.tribut} Inválido'

    pass

class pastaExistenteError(Exception):

    def __init__(self, pasta):


        self.pasta = pasta
        self.msg = self.__str__()

        print(f'{pasta} Já Existe no servidor')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.pasta} Já Existe no servidor'
