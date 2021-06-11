import random
from time import sleep
from deller import Deller
from player import Player


class BlackJack:
    '''21点'''

    def __init__(self):
        '''初始化游戏'''
        self.all_cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', ]
        self.deller = Deller()
        self.player = Player()

    def new_game(self):
        '''开始一局新游戏'''
        self.all_cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', ]
        self.deller.new_game()
        self.player.new_game()

    def hit(self, dp):
        '''抽牌'''
        n = random.randint(0, len(self.all_cards)-1)
        dp.add(self.all_cards.pop(n))

    def deller_hit(self, deller):
        '''庄家抽牌直至大于等于17'''
        while sum(deller.cards) < 17:
            self.hit(deller)
            if sum(deller.cards) > 21 and 11 in deller.cards:
                i = 0
                while True:
                    if deller.cards[i] == 11:
                        deller.cards[i] = 1
                        break
                    i += 1

    def stand(self, dp):
        '''停牌'''
        dp.active = 10

    def double(self, dp):
        '''双倍下注'''
        self.hit(dp)

    def show_card(self, dp):
        '''展示手牌'''
        print(f'{dp.name}的手牌：', end='')
        for i in dp.ccards:
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
                if sum_cards > 21:
                    print(f'总和：{sum_cards}\n爆牌！')
                    dp.active = 0
                    return 0
            else:
                print(f'总和：{sum_cards}\n爆牌！')
                dp.active = 0
                return 0
        elif sum_cards == 21 and len(self.player.cards) == 2:
            dp.active = 21
        else:
            pass
        print(f'总和：{sum(dp.cards)}')

    def show(self):
        '''展示双方手牌'''
        self.show_card(self.deller)
        self.show_card(self.player)
        print()
        sleep(1)

    def start_game(self):
        '''游戏初始状态'''
        print()
        print('*' * 30)
        self.new_game()
        # 庄家抽一张牌
        self.hit(self.deller)
        # 玩家抽两张牌
        self.hit(self.player)
        self.hit(self.player)
        self.show()

    def player_turn(self):
        '''玩家操作'''
        print('请开始你的表演！')
        while self.player.active == 1:
            player_choice = input('1.抽牌 2.停牌 3.加倍\n')
            print('\n', end='')
            print('*' * 30)
            if player_choice == '1' or player_choice == '':
                self.hit(self.player)
                self.show()
            elif player_choice == '2':
                self.stand(self.player)
            elif player_choice == '3':
                self.double(self.player)
                self.show()
            else:
                print('尝试重新输入')

    def run_game(self):
        '''游戏开始'''
        while True:
            self.start_game()
            self.player_turn()

            # 结算玩家操作结果
            if self.player.active == 0:
                # 玩家爆牌
                print('很遗憾，要再来一局吗？(Y/N)')
                if input().upper() in ['Y', '']:
                    continue
                else:
                    print('欢迎下次光临')
                    sleep(1)
                    break
            elif self.player.active == 21:
                print('Black Jack!!!')
                if input('再来一次？(Y/N)').upper() in ['Y', '']:
                    continue
                else:
                    print('欢迎下次光临')
                    sleep(1)
                    break
            else:
                print('轮到庄家了')
                sleep(0.5)

            # 庄家抽牌
            self.deller_hit(self.deller)
            self.show()

            # 结算游戏
            if sum(self.deller.cards) >= sum(self.player.cards) and sum(self.deller.cards) <= 21:
                print('很遗憾，要再来一局吗？(Y/N)')
            else:
                print('恭喜获胜，要再来一局吗？(Y/N)')
            if input().upper() in ['Y', '']:
                continue
            else:
                print('欢迎下次光临')
                sleep(1)
                break


if __name__ == '__main__':
    bj = BlackJack()
    bj.run_game()
