import random
from typing import List
from .card import Card


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []

    def create_standard_deck(self, assets_path: str):
        suits = ["hearts", "diamonds", "clubs", "spades"]
        values = ["A", "02", "03", "04", "05", "06", "07", "08", "09", "10", "J", "Q", "K"]

        for suit in suits:
            for value in values:
                # Match your actual image naming pattern: card_hearts_A.png, card_diamonds_02.png, etc.
                image_path = f"{assets_path}/cards_large/card_{suit}_{value}.png"
                self.cards.append(Card(suit, value, image_path))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> List[Card]:
        dealt = []
        for _ in range(min(num_cards, len(self.cards))):
            dealt.append(self.cards.pop())
        return dealt

    def discard(self, card: Card):
        self.discard_pile.append(card)

    def reset(self):
        self.cards.extend(self.discard_pile)
        self.discard_pile = []
        self.shuffle()