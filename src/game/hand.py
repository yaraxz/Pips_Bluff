from typing import List
from .card import Card


class Hand:
    def __init__(self, cards: List[Card]):
        """
        Initializes a hand with a list of Card objects.

        Args:
            cards: A list of Card instances representing the hand.
        """
        self.cards = cards
        self.selected: List[int] = []  # Indices of selected cards

    def toggle_selection(self, index: int):
        """
        Toggles selection status of a card at a given index.

        Args:
            index: The index of the card to select or deselect.
        """
        if index in self.selected:
            self.selected.remove(index)
        else:
            self.selected.append(index)

    def get_selected_cards(self) -> List[Card]:
        """
        Returns:
            A list of selected Card objects.
        """
        return [self.cards[i] for i in self.selected]

    def remove_selected(self):
        """
        Removes all selected cards from the hand and clears selection.
        """
        for i in sorted(self.selected, reverse=True):
            if 0 <= i < len(self.cards):
                self.cards.pop(i)

        self.selected = []