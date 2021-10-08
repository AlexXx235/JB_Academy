from DataBase import DataBase
from BankCard import BankCard


def show_main_menu():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')


def show_account_menu():
    print('1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
    print('0. Exit')


def check_if_number_is_valid(number):
    current_check_sum = number[-1]
    temp = number[:-1]
    counted_check_sum = BankCard.check_sum(temp)
    if counted_check_sum == current_check_sum:
        return True
    else:
        return False


def find_card(cards, number):
    founded_card = next((card for card in cards
                if card.number == number), None)
    return founded_card


def log_into_account(cards, number, pin):
    founded_card = find_card(cards, number)
    if founded_card is not None:
        if founded_card.pin_code == pin:
            return founded_card
    return None




if __name__ == '__main__':
    db = DataBase()
    cards = db.get_cards()

    # for card in cards:
        # print(card.get_account_info())
        # print(card.get_balance_info())
    # quit()

    last_id = 0
    if len(cards) > 0:
        last_card = cards[-1]
        last_id = last_card.id + 1
    BankCard.current_account_id = last_id

    while True:
        show_main_menu()
        choice = int(input())
        if choice == 1:
            new_card = BankCard.create()
            print('Your card has been created')
            print(new_card.get_account_info())
            cards.append(new_card)
            db.add_card(new_card)
        elif choice == 2:
            number = input('Enter your card number: ')
            pin_code = input('Enter your PIN: ')
            card = log_into_account(cards, number, pin_code)
            if card is None:
                print('Wrong card number or PIN!')
                continue
            print('You have successfully logged in!')
            while True:
                show_account_menu()
                choice = int(input())
                if choice == 1:
                    print(card.get_balance_info())
                elif choice == 2:
                    income = int(input('Enter income: '))
                    new_balance = card.balance + income
                    card.balance = new_balance
                    db.change_balance(card.number, new_balance)
                    print('Income was added!')
                elif choice == 3:
                    print('Transfer')
                    t_number = input('Enter card number: ')
                    check_result = check_if_number_is_valid(t_number)
                    if check_result is False:
                        print('Probably you made a mistake in the card number. '
                              'Please Try again!')
                        continue
                    card_recipient = find_card(cards, t_number)
                    if card_recipient is None:
                        print('Such a card does not exist.')
                        continue
                    amount = int(input('Enter how much money '
                                       'you want to transfer: '))
                    if amount > card.balance:
                        print('Not enough money!')
                        continue
                    db.transfer(card, card_recipient, amount)
                    card.balance -= amount
                    card_recipient.balance += amount
                    print('Success!')
                elif choice == 4:
                    cards.remove(card)
                    db.delete_account(card.number)
                    print('The account has been closed!')
                    break
                elif choice == 5:
                    print('You have successfully logged out!')
                    break
                elif choice == 0:
                    print('Bye!')
                    db.connection.close()
                    quit()
        elif choice == 0:
            print('Bye!')
            db.connection.close()
            break

