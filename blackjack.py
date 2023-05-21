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
    def __init__(self, name, balance=100):
        self.name = name
        self.hands = [Hand()]
        self.balance = balance
        self.bets = [0]

    def make_bet(self, hand_index=0):
        if self.balance >= 10:
            self.bets[hand_index] = random.randint(10, min(50, self.balance))  # Bets a random amount between 10 and 50 (or remaining balance if it's less than 50)
        else:
            self.bets[hand_index] = self.balance  # If balance is less than 10, bet the remaining balance
        self.balance -= self.bets[hand_index]
        print(f"{self.name} bets {self.bets[hand_index]} on hand {hand_index+1}. Remaining balance: {self.balance}")

    def add_card(self, card, hand_index=0):
        self.hands[hand_index].add_card(card)
        print(f"{self.name} hits a card.")
        if self.hands[hand_index].value > 21:
            self.hands[hand_index].adjust_for_ace()

    def can_split(self, hand_index=0):
        return len(self.hands[hand_index].cards) == 2 and self.hands[hand_index].cards[0].rank == self.hands[hand_index].cards[1].rank and self.balance >= self.bets[hand_index]

    def split_hand(self, hand_index=0):
        self.hands.append(Hand())
        self.bets.append(self.bets[hand_index])
        self.balance -= self.bets[hand_index]
        self.hands[-1].add_card(self.hands[hand_index].cards.pop())
        print(f"{self.name} splits hand {hand_index+1}. New bet of {self.bets[-1]} placed on new hand.")

    def can_double(self, hand_index=0):
        return len(self.hands[hand_index].cards) == 2 and self.balance >= self.bets[hand_index]

    def double_bet(self, hand_index=0):
        self.balance -= self.bets[hand_index]
        self.bets[hand_index] *= 2
        print(f"{self.name} doubles bet on hand {hand_index+1} to {self.bets[hand_index]}. Remaining balance: {self.balance}")

    def make_decision(self, hand_index):
        value = self.hands[hand_index].value
        # Check for split
        if len(self.hands[hand_index].cards) == 2 and self.hands[hand_index].cards[0].rank == self.hands[hand_index].cards[1].rank and self.balance >= self.bets[hand_index]:
           # Bot will split if it can and if the cards have a value of 8 or more, or the value is 4 (meaning two twos or two threes)
           if values[self.hands[hand_index].cards[0].rank] >= 8 or values[self.hands[hand_index].cards[0].rank] == 4:
              return 'p'
        #Check for double
        if value >= 9 and value <= 11 and self.balance >= self.bets[hand_index]:
           return 'd'
         # Check for hit or stand
        return 'h' if value < 17 else 's'


    def show_hand(self, hand_index=0, hide_first_card=False):
        print(f"\n{self.name}'s Hand {hand_index+1}:")
        if hide_first_card and hand_index == 0:
            print(' <card hidden>')
            print('', self.hands[hand_index].cards[1])
        else:
            print(self.hands[hand_index])
        print(f"{self.name}'s Hand Value: {self.hands[hand_index].value}")

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

            for bot in bots:
                bot.make_bet()

            for _ in range(2):
                for bot in bots:
                    bot.add_card(self.deck.deal())
                dealer.add_card(self.deck.deal())

            dealer.show_hand(hide_first_card=True)
            for bot in bots:
                bot.show_hand()

            for bot in bots:
                for i in range(len(bot.hands)):
                    print(f"\n{bot.name}'s turn for hand {i+1}:")
                    while True:
                        decision = bot.make_decision(i)
                        if decision == 'p':
                            bot.split_hand(i)
                            bot.add_card(self.deck.deal(), i)
                            bot.add_card(self.deck.deal(), -1)
                            bot.show_hand(i)
                            bot.show_hand(-1)
                        elif decision == 'd':
                            bot.double_bet(i)
                            bot.add_card(self.deck.deal(), i)
                            bot.show_hand(i)
                            break
                        elif decision == 'h':
                            bot.add_card(self.deck.deal(), i)
                            bot.show_hand(i)
                            if bot.hands[i].value > 21:
                                print("Bust!")
                                break
                        else:
                            print("Stand!")
                            break

            print("\nDealer's turn:")
            while dealer.hands[0].value < 17:
                dealer.add_card(self.deck.deal())
                dealer.hands[0].adjust_for_ace()
            dealer.show_hand()

            dealer_score = dealer.hands[0].value
            print("\nDealer's Final Hand:")
            print(dealer.hands[0])

            print("\n--- Results ---")

            for bot in bots:
                for i, hand in enumerate(bot.hands):
                    bot_score = hand.value
                    print(f"\nResults for {bot.name}'s hand {i+1}:")
                    if dealer_score > 21:
                        print("Dealer busts! Bot wins!")
                        bot.balance += bot.bets[i] * 2
                    elif bot_score > 21:
                        print(f"{bot.name} busts!")
                    elif bot_score > dealer_score:
                        print(f"{bot.name} wins!")
                        bot.balance += bot.bets[i] * 2
                    elif bot_score == dealer_score:
                        print("Push! It's a tie.")
                        bot.balance += bot.bets[i]
                    else:
                        print(f"{bot.name} loses.")
                bot.hands = [Hand()]
                bot.bets = [0]

            print("\n--- End of round ---")
            print("\n--- Balances ---")
            for bot in bots:
                print(f"{bot.name}'s balance: {bot.balance}")

            self.deck = Deck()  # Refresh the deck for the next round

# Start the game
game = Game()
game.play_game()
