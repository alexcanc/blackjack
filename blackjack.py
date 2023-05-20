import random

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return ''.join('\n ' + str(card) for card in self.cards)

class Bot:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def make_decision(self):
        return 'h' if self.hand.value < 17 else 's'

    def add_card(self, card):
        self.hand.add_card(card)
        print(f"{self.name} hits a card.")
        if self.hand.value > 21:
            self.hand.adjust_for_ace()

    def show_hand(self, hide_first_card=False):
        print(f"\n{self.name}'s Hand:")
        if hide_first_card:
            print(' <card hidden>')
            print('', self.hand.cards[1])
        else:
            print(self.hand)
        print(f"{self.name}'s Hand Value: {self.hand.value}")

    def __str__(self):
        return self.name

class Game:
    def __init__(self, num_rounds=1):
        self.deck = Deck()
        self.num_rounds = num_rounds

    def play_game(self):
        for _ in range(self.num_rounds):
            self.deck.shuffle()

            bots = [Bot(f"Bot {i+1}") for i in range(4)]
            dealer = Bot("Dealer")

            for _ in range(2):
                for bot in bots:
                    bot.add_card(self.deck.deal())
                dealer.add_card(self.deck.deal())

            dealer.show_hand(hide_first_card=True)
            for bot in bots:
                bot.show_hand()

            for bot in bots:
                print(f"\n{bot.name}'s turn:")
                while bot.make_decision() == 'h':
                    bot.add_card(self.deck.deal())
                    bot.show_hand()
                    if bot.hand.value > 21:
                        print("Bust!")
                        break
                else:
                    print("Stand!")
            print("\nDealer's turn:")
            while dealer.hand.value < 17:
                dealer.add_card(self.deck.deal())
                dealer.hand.adjust_for_ace()
            dealer.show_hand()

            dealer_score = dealer.hand.value
            print("\nDealer's Final Hand:")
            print(dealer.hand)

            print("\n--- Results ---")

            if dealer_score > 21:
                print("Dealer busts! All bots win!")
            else:
                winners = []
                for bot in bots:
                    bot_score = bot.hand.value
                    if bot_score > 21:
                        print(f"{bot.name} busts!")
                    elif bot_score > dealer_score:
                        winners.append(bot.name)

                if not winners:
                    print("Dealer wins! All bots lose.")
                else:
                    print("Bots that beat the dealer:")
                    for winner in winners:
                        print(winner)

            print("\n--- End of round ---")

            self.deck = Deck()  # Refresh the deck for the next round

# Start the game
game = Game()
game.play_game()
