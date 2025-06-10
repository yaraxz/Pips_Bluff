from typing import List
from .card import Card


class Hand:
    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.selected: List[int] = []

    def toggle_selection(self, index: int):
        if index in self.selected:
            self.selected.remove(index)
        else:
            self.selected.append(index)

    def get_selected_cards(self) -> List[Card]:
        return [self.cards[i] for i in self.selected]

    def remove_selected(self):
        # Remove in reverse order to avoid index shifting
        for i in sorted(self.selected, reverse=True):
            if 0 <= i < len(self.cards):
                self.cards.pop(i)
        self.selected = []