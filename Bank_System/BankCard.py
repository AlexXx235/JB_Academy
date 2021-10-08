import random


class BankCard:
    current_account_id = 0
    BIN = '400000'  # Bank Identification Number

    def __init__(self, card_id=0, number='', pin_code='', balance=0):
        self.id = card_id
        self.number = number
        self.pin_code = pin_code
        self.balance = balance

    def get_account_info(self):
        info = 'Your card number:\n' + self.number
        info += '\nYour card PIN:\n' + self.pin_code
        return info

    def get_balance_info(self):
        return 'Balance: ' + str(self.balance)

    @staticmethod
    def create():
        # create id with length 9
        account_id = '{:0>9}'.format(str(BankCard.current_account_id))
        # make id for next card
        card_id = BankCard.current_account_id
        BankCard.current_account_id += 1

        number = BankCard.BIN + account_id
        check_sum = BankCard.check_sum(number)
        number += check_sum

        pin_int = random.randint(0, 9000)
        # create pin with length 4
        pin_code = '{:0>4}'.format(str(pin_int))
        card_pin_code = pin_code
        card_number = number
        card_balance = 0
        card = BankCard(card_id, card_number, card_pin_code, card_balance)
        return card

    @staticmethod
    def check_sum(str_account_id):
        account_id = list(map(int, str_account_id))
        for i in range(len(account_id)):
            if (i + 1) % 2 == 1:
                temp = account_id[i] * 2
                if temp > 9:
                    account_id[i] = temp - 9
                else:
                    account_id[i] = temp
        s = sum(account_id)
        result = str(10 - s % 10) if s % 10 != 0 else '0'
        return result
