import random
import sys


class MakeDecision:
    '''计算双方概率'''

    def __init__(self, deller_card, player_card, other_player) -> None:
        '''初始化'''
        self.all_cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, ]
        self.deller = [deller_card]
        self.dellerf_ = self.deller[:]
        self.player = player_card
        self.player_f = player_card[:]
        self.other = other_player
        self.update_cards(self.deller)
        self.update_cards(self.player)
        self.update_cards(self.other)
        self.all_cards_f = self.all_cards[:]
        self.deller_history = []
        self.player_history = []

    def update_cards(self, cards):
        '''删除已抽卡片'''
        for i in cards:
            if i == 1:
                i = 11
            self.all_cards.remove(i)

    def deller_draw(self):
        '''计算庄家抽牌情况'''
        while sum(self.deller) < 17:
            self.deller.append(self.all_cards.pop(random.randint(0, len(self.all_cards)-1)))
            if sum(self.deller) > 21 and 11 in self.deller:
                self.deller.remove(11)
                self.deller.append(1)
        if sum(self.deller) > 21:
            return 0
        return sum(self.deller)

    def player_hit(self):
        '''玩家抽牌'''
        self.player.append(self.all_cards.pop(random.randint(0, len(self.all_cards)-1)))
        # self.debug(0)
        while sum(self.player) > 21:
            # self.debug(1)
            if self.player[-1] == 11:
                self.player[-1] = 1
            if 11 in self.player:
                self.player.remove(11)
                self.player.append(1)
            else:
                return 0
        return sum(self.player)

    def run(self, n=10000):
        '''计算概率'''
        while True:
            for i in range(n):
                self.deller_history.append(self.deller_draw())
                self.all_cards = self.all_cards_f[:]
                self.deller = self.dellerf_[:]
                self.player_history.append(self.player_hit())
                self.player = self.player_f[:]
                self.all_cards = self.all_cards_f[:]
            # self.debug(2)
            self.deller_bomb = self.deller_history.count(0) / n
            self.player_bomb = self.player_history.count(0) / n

            print(f'庄家爆牌率: {self.deller_bomb*100:.2f}%  手牌和: {sum(self.deller):2d} ')
            print(f'玩家爆牌率: {self.player_bomb*100:.2f}%  手牌和: {sum(self.player):2d} ')

            w, t, l, hw, ht, hl = 0, 0, 0, 0, 0, 0
            for i in range(n):
                if sum(self.player) > self.deller_history[i]:
                    w += 1
                elif sum(self.player) == self.deller_history[i]:
                    t += 1
                else:
                    l += 1
                if self.player_history[i] > self.deller_history[i]:
                    hw += 1
                elif self.player_history[i] == self.deller_history[i]:
                    if self.player_history[i] == 0:
                        hl += 1
                    else:
                        ht += 1
                else:
                    hl += 1

            print(f'若抽牌 胜: {hw/n*100:.2f}% 平: {ht/n*100:.2f}% 输: {hl/n*100:.2f}%')
            print(f'若停牌 胜: {w/n*100:.2f}% 平: {t/n*100:.2f}% 输: {l/n*100:.2f}%')
            print('所以应该：\n')
            if hw/n > w/n:
                print(f'    抽牌！你有 {hw/n*100:.2f}% 的胜率')
            else:
                print(f'    停牌！你有 {w/n*100:.2f}% 的胜率')

            a = input('\n输入抽到的卡:')
            print()
            if a:
                T = {'A': 11, 'J': 10, 'Q': 10, 'K': 10}
                a = T[a.upper()] if a.upper() in T.keys() else int(a)
                self.drew(a)
                self.deller_history = []
                self.player_history = []
                continue
            break

    def drew(self, a):
        '''玩家抽了一张卡'''
        self.all_cards.remove(a)
        self.all_cards_f.remove(a)
        if a == 11 and sum(self.player) > 10:
            a = 1
        self.player.append(a)
        self.player_f.append(a)
        if sum(self.player) > 21:
            print('你都炸了！')
            sys.exit()
    
    def debug(self, n):
        print(n, self.deller)
        print(n, self.player)


while(True):
    T = {'A': 11, 'J': 10, 'Q': 10, 'K': 10}
    d = input('请输入庄家手牌: ').upper()
    deller = T[d.upper()] if d.upper() in T.keys() else int(d)
    player = []
    for i in input('请输入玩家手牌: ').split():
        if i.upper() in T.keys():
            player.append(T[i.upper()])
        else:
            player.append(int(i))
    if player == [11, 11]:
        player = [11, 1]
    other = []
    for i in input('请输入其他玩家手牌: ').split():
        if i.upper() in T.keys():
            other.append(T[i.upper()])
        else:
            other.append(int(i))
    
    md = MakeDecision(deller, player, other)

    md.run(10000)
