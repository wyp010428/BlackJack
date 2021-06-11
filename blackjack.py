# from hashlib import blake2b
import random
from deller import Deller
from player import Player


class BlackJack:
    '''21点'''

    def __init__(self):
        '''初始化游戏'''
        self.all_cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, ]
        self.deller = Deller()
        self.player = Player()
    def new_game(self, deller, player):
        '''开始一局新游戏'''
        self.all_cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                          11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, ]
        deller.cards = []
        player.cards = []
        deller.active = 1
        player.active = 1

    def hit(self, dp):
        '''抽牌'''
        n = random.randint(0, len(self.all_cards)-1)
        dp.cards.append(self.all_cards.pop(n))
        #print(f'{n}!')
        #dp.cards.append(11)

    def deller_hit(self, deller):
        '''庄家抽牌直至大于等于17'''
        if sum(deller.cards) > 21 and 11 in deller.cards:
            i = 0
            while True:
                if deller.cards[i] == 11:
                    deller.cards[i] = 1
                    break
                i += 1            
        while sum(deller.cards) < 17:
            self.hit(deller)

    def stand(self, dp):
        '''停牌'''
        dp.active = 10

    def double(self, dp):
        '''双倍下注'''
        self.hit(dp)

    def show_card(self, dp):
        '''展示手牌'''
        print(f'{dp.name}的手牌：', end='')
        for i in dp.cards:
            if i == 11 or i == 1:
                print('A', end=' ')
                continue
            print(i, end=' ')
        self.check_cards(dp)

    def check_cards(self, dp):
        '''检查是否爆牌，是否凑成21点'''
        sum_cards = sum(dp.cards)
        if sum_cards > 21:
            if 11 in dp.cards:
                i = 0
                while True:
                    if dp.cards[i] == 11:
                        dp.cards[i] = 1
                        break
                    i += 1
                if sum(dp.cards) == 21:
                    print('\n21点！！！')
                    return 0
                print(f'总和：{sum(dp.cards)}')

            else:
                print(f'总和：{sum_cards}')
                print('爆牌！')
                dp.active = 0
        elif sum_cards == 21:
            print('\n21点！！！')
            dp.active = 21
        else:
            print(f'总和：{sum_cards}')

    def start_game(self):
        '''游戏初始状态'''
        self.new_game(self.deller, self.player)
        # 庄家抽一张牌并展示
        self.hit(self.deller)
        self.show_card(self.deller)
        # 玩家抽两张牌并展示
        self.hit(self.player)
        self.hit(self.player)
        self.show_card(self.player)

    def player_turn(self):
        '''玩家操作'''
        print('请开始你的表演！')
        while self.player.active == 1:
            player_choice = input('1.抽牌 2.停牌 3.加倍\n')
            if player_choice == '1':
                self.hit(self.player)
                self.show_card(self.player)
            elif player_choice == '2':
                self.stand(self.player)
            elif player_choice == '3':
                self.double(self.player)
                self.show_card(self.player)
            else:
                print('尝试重新输入')

    def run_game(self):
        '''游戏开始'''
        while True:
            self.start_game()
            self.player_turn()

            # 结算玩家操作结果
            if self.player.active == 10:
                # 玩家停牌
                print('轮到庄家了')
            elif self.player.active == 0:
                # 玩家爆牌
                print('很遗憾，要再来一局吗？(Y/N)')
                if input().upper() in ['Y', '']:
                    continue
                else:
                    print('欢迎下次光临')
                    break  
            elif self.player.active == 21:
                # 玩家凑齐21点
                while sum(self.deller.cards) < 17:
                    self.hit(self.deller)
                self.show_card(self.deller)
                if sum(self.deller.cards) == 21:
                    print('很遗憾，要再来一局吗？(Y/N)')
                else:
                    print('恭喜获胜，要再来一局吗？(Y/N)')
                if input().upper() in ['Y', '']:
                    continue
                else:
                    print('欢迎下次光临')
                    break
                    
            # 庄家抽牌
            while sum(self.deller.cards) < 17:
                self.hit(self.deller)
            self.show_card(self.deller)

            # 结算游戏
            if sum(self.deller.cards) >= sum(self.player.cards) and sum(self.deller.cards) <= 21:
                print('很遗憾，要再来一局吗？(Y/N)')
            else:
                print('恭喜获胜，要再来一局吗？(Y/N)')
            if input().upper() in ['Y', '']:
                continue
            else:
                print('欢迎下次光临')
                break                


if __name__ == '__main__':
    bj = BlackJack()
    bj.run_game()