from time import sleep


class Deller:
    '''庄家的类'''

    def __init__(self) -> None:
        self.name = '庄家'
        self.ccards = []
        self.cards = []
        self.active = 1

    def add(self, card):
        '''转换牌上的数字，并添加到列表'''
        self.ccards.append(card)
        if card == 'A':
            self.cards.append(11)
        elif card in ['J', 'Q', 'K']:
            self.cards.append(10)
        else:
            self.cards.append(card)

    def new_game(self):
        '''初始化手牌'''
        self.cards = []
        self.ccards = []
        self.active = 1