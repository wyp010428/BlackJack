import json
from time import sleep


class Player:
    '''玩家的类'''

    def __init__(self) -> None:
        self.name = '玩家'
        self.ccards = []
        self.cards = []
        self.active = 1

    def load_inf(self):
        '''加载玩家信息'''
        self.user = input('请输入用户名：')
        try:
            with open(f'./data/{self.user}.json') as f:
                inf = json.load(f)
                while True:
                    password = input('请输入密码：')
                    if inf[0] == password:
                        self.ccapital = [inf[1]]
                        self.capital = inf[1]
                        self.password = password
                        print('登陆成功！')
                        print(f'账户余额{self.capital}元')
                        sleep(1)
                        break
                    else:
                        print('密码错误')
                        sleep(1)
        except:
            with open(f'./data/{self.user}.json', 'w') as f:
                print('欢迎新用户！')
                self.password = input('创建密码：')
                print('初始账号余额100,000元')
                self.ccapital = [100_000]
                self.capital = 100_000
                json.dump([self.password, self.capital], f)
                sleep(1)

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

    def update_capital(self, bet):
        '''更新本金'''
        if self.active == 10:
            self.capital += bet
            print(f'您获得了{2*bet}元奖金！！！')
        elif self.active == 0:
            self.capital -= bet
            print(f'您失去了{bet}元下注')
        elif self.active == 21:
            self.capital += 1.5 * bet
            print(f'您获得了{bet*2.5}元奖金！！！')

        self.ccapital.append(self.capital)
        self.r = self.capital - self.ccapital[0]
        if self.capital == 0:
            self.capital += 1000
            sleep(1)
            print('获得救济1000元')
            self.r -= 1000
            sleep(1)
        with open(f'./data/{self.user}.json', 'w') as f:
            json.dump([self.password, self.capital], f)
