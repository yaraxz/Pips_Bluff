from typing import List
from .card import Card

class Hand:
    def __init__(self, cards: List[Card]):
        self.cards = cards  # List of cards in hand
        self.selected: List[int] = []  # Indices of selected cards

    def toggle_selection(self, index: int):
        # Select or deselect a card by index
        if index in self.selected:
            self.selected.remove(index)
        else:
            self.selected.append(index)

    def get_selected_cards(self) -> List[Card]:
        # Return list of selected cards
        return [self.cards[i] for i in self.selected]

    def remove_selected(self):
        # Remove selected cards (from highest index to avoid shifting)
        for i in sorted(self.selected, reverse=True):
            if 0 <= i < len(self.cards):
                self.cards.pop(i)
        self.selected = []  # Clear selection after removal