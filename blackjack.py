import random
import matplotlib.pyplot as plt
from time import sleep
from deller import Deller
from player import Player


class BlackJack:
    '''21点'''

    def __init__(self):
        '''初始化游戏'''
        self.all_cards_ = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K',
                          'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', ]
        self.all_cards = self.all_cards_[:]
        self.deller = Deller()
        self.player = Player()
        self.player.load_inf()
        self.turn = 0
        self.bet = 0
        self.game = True

    def new_game(self):
        '''开始一局新游戏'''
        self.all_cards = self.all_cards_[:]
        self.deller.new_game()
        self.player.new_game()

    def hit(self, dp):
        '''抽牌'''
        n = random.randint(0, len(self.all_cards)-1)
        dp.add(self.all_cards.pop(n))
        if sum(self.player.cards) == 21:
            self.player.active = 10

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

    def show_card(self, dp):
        '''展示手牌'''
        print(f'{dp.name}的手牌：', end='')
        for i in dp.ccards:
            print(i, end=' ')
        self.check_cards(dp)

    def check_cards(self, dp):
        '''检查是否爆牌，是否凑成21点'''
        if sum(dp.cards) > 21:
            if 11 in dp.cards:
                i = 0
                while True:
                    if dp.cards[i] == 11:
                        dp.cards[i] = 1
                        break
                    i += 1
                if sum(dp.cards) > 21:
                    print(f'总和：{sum(dp.cards)}\n爆牌！！！')
                    dp.active = 0
                    return 0
            else:
                print(f'总和：{sum(dp.cards)}\n爆牌！！！')
                dp.active = 0
                return 0
        elif sum(dp.cards) == 21 and len(self.player.cards) == 2:
            dp.active = 21
        else:
            pass
        print(f'总和：{sum(dp.cards)}')

    def show(self):
        '''展示双方手牌'''
        self.show_card(self.deller)
        self.show_card(self.player)
        print('*' * 25)
        sleep(1)

    def start_game(self):
        '''游戏初始状态'''
        self.turn += 1
        print()
        print('*' * 10, end='')
        print(f'第{self.turn}轮', end='')
        print('*' * 10)
        self.new_game()
        print(f'本金剩余：{self.player.capital}')
        while True:
            try:
                bet = int(input('请下注：'))
                break
            except:
                print('请输入正确的下注')
        self.bet = min(self.player.capital, bet)
        if self.player.capital == self.bet:
            print('All In！！！')
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
            print('*' * 10, end='')
            print(f'第{self.turn}轮', end='')
            print('*' * 10)
            if player_choice == '1' or player_choice == '':
                self.hit(self.player)
                print(f'你抽了一张：{self.player.ccards[-1]}')
                sleep(1)
                self.show()
            elif player_choice == '2':
                self.stand(self.player)
                print('你停牌了')
            elif player_choice == '3':
                if self.player.capital >= 2 * self.bet:
                    self.hit(self.player)
                    print(f'你双倍下注并抽了最后一张：{self.player.ccards[-1]}')
                    self.bet *= 2
                    self.stand(self.player)
                else:
                    print('本金不够')
                sleep(1)
                self.show()
            else:
                print('尝试重新输入')
                continue

    def end_or_continue(self):
        '''判断玩家是否继续'''
        if input().upper() in ['Y', '']:
            pass
        else:
            print(f'本金还剩{self.player.capital}元，', end='')
            if self.player.r >= 0:
                print(f'这次赚了{self.player.r}元！')
            else:
                print(f'这次亏了{-self.player.r}元')
            sleep(1)
            self.game = False
            print('保存成功，欢迎下次光临')
            sleep(1)
            self.show_pic()

    def show_pic(self):
        '''画出本金的变化图'''
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.figure(figsize=(10, 6))
        plt.title('本金变化曲线')
        plt.xlabel('轮数')
        plt.ylabel('本金')
        plt.plot(range(len(self.player.ccapital)), self.player.ccapital)
        plt.show()

    def run_game(self):
        '''游戏开始'''
        while self.game:
            self.start_game()
            self.player_turn()

            # 结算玩家操作结果
            if self.player.active == 0:
                # 玩家爆牌
                self.player.update_capital(self.bet)
                print('很遗憾，要再来一局吗？(Y/N)')
                self.end_or_continue()
                continue
            elif self.player.active == 21:
                print('Black Jack!!!')
                self.player.update_capital(self.bet)
                print('恭喜获胜，要再来一局吗？(Y/N)')
                self.end_or_continue()
                continue
            else:
                print('轮到庄家了')
                sleep(1)

            # 庄家抽牌
            self.deller_hit(self.deller)
            self.show()

            # 结算游戏
            if sum(self.deller.cards) > sum(self.player.cards) and sum(self.deller.cards) <= 21:
                self.player.active = 0
                self.player.update_capital(self.bet)
                print('很遗憾，要再来一局吗？(Y/N)')
            elif sum(self.deller.cards) == sum(self.player.cards):
                self.player.active = 11
                self.player.update_capital(self.bet)
                print('平局！要再来一局吗？(Y/N)')
            else:
                self.player.update_capital(self.bet)
                print('恭喜获胜，要再来一局吗？(Y/N)')
            self.end_or_continue()


if __name__ == '__main__':
    bj = BlackJack()
    bj.run_game()
