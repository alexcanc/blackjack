Blackjack Game with Bots
Overview
This project is a simulation of a Blackjack game, written in Python, where bots play the game against the dealer. The goal of the game is to get as close to 21 as possible without going over.

The game is played with a shuffled deck of 52 cards. Bots make bets, receive cards, and make decisions based on the state of their hands. The dealer also plays, following a set of predefined rules.

Game Rules
Each bot starts with a balance of 100.
At the start of each round, each bot places a random bet between 10 and 50.
Each bot and the dealer are dealt two cards.
Bots can choose to hit (receive another card), stand (receive no more cards), double down (double their bet and receive exactly one more card), or split (if their first two cards have the same rank, they can split them into two hands and place an additional bet equal to the original on the second hand).
Bots continue to make decisions until they stand or their hand value exceeds 21 (a bust).
The dealer then plays, hitting until their hand value is 17 or more.
If a bot's hand value is closer to 21 than the dealer's, without exceeding 21, the bot wins the round and receives twice their bet. If a bot busts or has a hand value further from 21 than the dealer's, they lose their bet. In the event of a tie, the bot's bet is returned.
Bot Decision-Making
Bots make decisions based on the following rules:

If a bot has two cards of the same rank and enough balance for an additional bet, it will split if the cards have a value of 8 or more, or a value of 4 (two twos or two threes).
If a bot's hand value is between 9 and 11 (inclusive) and it has enough balance to double the bet, it will choose to double down.
If a bot's hand value is less than 17, it will choose to hit.
If a bot's hand value is 17 or more, it will choose to stand.
Bots automatically count an Ace as 11, but will count it as 1 instead if counting it as 11 would make the hand value exceed 21.
Running the Game
You can run the game by executing the Python script in your terminal with the following command:

Copy code
python blackjack.py
Enjoy the game!
