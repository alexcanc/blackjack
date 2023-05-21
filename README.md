# Blackjack Game

This is a simple simulation of the blackjack card game, written in Python. The game involves one dealer and four bot players.

## How the Game Works

When the game starts, the dealer and the bots are each dealt two cards. The bots then take turns deciding whether to "hit" (take another card) or "stand" (take no more cards). Bots may also "double" (double their initial bet and receive only one more card) or "split" (if they have two cards of the same rank, divide them into two hands and continue playing each hand separately).

The goal for each bot is to have the sum of their cards be higher than the dealer's without exceeding 21. The dealer must hit until their cards total 17 or more, at which point they must stand.

## How the Bots Make Decisions

Bots make decisions based on simple logic:

- If the total value of a bot's hand is less than 17, the bot will always hit.
- If the total value of a bot's hand is 17 or higher, the bot will always stand.
- If a bot has two cards of the same rank, it will always choose to split.
- A bot will choose to double if its hand value is 11.

## Running the Game

To run the game, simply execute the Python script `blackjack.py`:

```bash
python blackjack.py
