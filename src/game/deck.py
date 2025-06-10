import random
from typing import List
from .card import Card  # Assuming card.py is in the same directory


class Deck:
    # Represents a deck of playing cards.
    def __init__(self):
        # Initializes the deck and discard pile.
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []

    def create_standard_deck(self, assets_path: str):
        # Creates a standard 52-card deck.
        suits = ["hearts", "diamonds", "clubs", "spades"]
        values = ["A", "02", "03", "04", "05", "06", "07", "08", "09", "10", "J", "Q", "K"]

        for suit in suits:
            for value in values:
                image_path = f"{assets_path}/cards_large/card_{suit}_{value}.png"
                self.cards.append(Card(suit, value, image_path))

    def shuffle(self):
        # Shuffles the cards in the deck.
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> List[Card]:
        # Deals a specified number of cards from the deck.
        dealt = []
        for _ in range(min(num_cards, len(self.cards))):
            dealt.append(self.cards.pop())
        return dealt

    def discard(self, card: Card):
        # Adds a card to the discard pile.
        self.discard_pile.append(card)

    def reset(self):
        # Resets the deck by combining it with the discard pile and shuffling.
        self.cards.extend(self.discard_pile)
        self.discard_pile = []
        self.shuffle()