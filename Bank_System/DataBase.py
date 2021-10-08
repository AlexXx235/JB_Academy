import sqlite3
from BankCard import BankCard


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('card.s3db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS card(
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0 
        );''')

    def get_data(self):
        self.cursor.execute('''
        SELECT * FROM card 
        ''')
        return self.cursor.fetchall()

    def get_cards(self):
        data = self.get_data()
        cards = [BankCard(card[0], card[1], card[2], card[3]) for card in data]
        return cards

    def add_card(self, card):
        self.cursor.execute(f'''
            INSERT INTO 
                card
            VALUES
                (
                {card.id},
                "{card.number}",
                "{card.pin_code}",
                {card.balance}
                )
            ;''')
        self.connection.commit()

    def change_balance(self, number, new_balance):
        self.cursor.execute(f'''
            UPDATE 
                card
            SET
                balance = {new_balance}
            WHERE
                number = {number}
        ''')
        self.connection.commit()

    def transfer(self, card, card_recipient, amount):
        new_card_balance = card.balance - amount
        new_card_recipient_balance = card_recipient.balance + amount
        self.change_balance(card.number, new_card_balance)
        self.change_balance(card_recipient.number, new_card_recipient_balance)

    def delete_account(self, number):
        self.cursor.execute(f'''
            DELETE FROM
                card
            WHERE
                number = {number}
        ''')
        self.connection.commit()
