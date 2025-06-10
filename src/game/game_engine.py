from typing import Dict, Optional, List
from collections import Counter
from enum import IntEnum
from .card import Card
from .deck import Deck
from .hand import Hand


# Defines the ranking of poker hands as an integer enumeration.
# This makes comparing hand strengths straightforward and less error-prone.
class HandRank(IntEnum):
    """
    Enumeration for poker hand ranks, ordered from weakest to strongest.
    The integer values represent the score for each hand type.
    """
    HIGH_CARD = 10
    ONE_PAIR = 20
    TWO_PAIR = 30
    THREE_OF_A_KIND = 40
    STRAIGHT = 50
    FLUSH = 60
    FULL_HOUSE = 70
    FOUR_OF_A_KIND = 80
    STRAIGHT_FLUSH = 90
    ROYAL_FLUSH = 100


# The main class that orchestrates the card game logic.
class GameEngine:
    """
    Manages the game state, including the deck, player's hand, scoring,
    and the overall flow of a card game.
    """
    # A string representing the card ranks in ascending order.
    # 'T' is used for 10 to maintain a single character representation.
    RANKS = "23456789TJQKA"

    def __init__(self):
        """
        Initializes the game engine, setting up the deck, hand, scores,
        and discard pile for a new game session.
        """
        self.deck = Deck()  # The deck of cards for the game.
        self.hand: Optional[Hand] = None  # The player's current hand.
        self.score = 0  # Total accumulated score across all rounds.
        self.discard_pile: List[Card] = []  # Cards discarded by the player.
        self.current_hand_points = 0  # Score obtained from the current hand only.

    def initialize_game(self, assets_path: str):
        """
        Sets up a new game round. It creates and shuffles a new deck,
        resets the current hand and discard pile, but keeps the total score.
        Args:
            assets_path: The file path to the directory containing card images.
        """
        self.deck = Deck()  # Create a new Deck instance.
        self.deck.create_standard_deck(assets_path)  # Populate with 52 standard cards.
        self.deck.shuffle()  # Randomize the order of cards.
        self.hand = None  # Clear the player's hand.
        self.current_hand_points = 0  # Reset points for the new hand.
        self.discard_pile = []  # Empty the discard pile.
        # The total score (self.score) is intentionally not reset to accumulate over sessions.

    def deal_hand(self, num_cards=5) -> Hand:
        """
        Deals a specified number of cards to the player.
        If the deck is low on cards, it recycles the discard pile.
        Args:
            num_cards: The number of cards to deal for the hand (default is 5).
        Returns:
            A new Hand object containing the dealt cards.
        """
        # Check if the deck has enough cards to deal.
        if len(self.deck.cards) < num_cards:
            # If not, add the discarded cards back into the deck.
            self.deck.cards.extend(self.discard_pile)
            self.discard_pile = []  # Clear the discard pile.
            self.deck.shuffle()  # Re-shuffle the deck.

        # Deal the requested number of cards from the deck.
        cards = self.deck.deal(num_cards)
        self.hand = Hand(cards)  # Create a new Hand with these cards.
        self.current_hand_points = 0  # Reset the score for this new hand.
        return self.hand

    def discard_cards(self, card_indices: List[int]) -> List[Card]:
        """
        Removes cards from the player's hand based on their indices and
        moves them to the discard pile.
        Args:
            card_indices: A list of integer indices for the cards to be discarded.
        Returns:
            A list of the Card objects that were discarded.
        """
        # Ensure there is a hand to discard from.
        if not self.hand:
            return []

        discarded = []
        # Sort indices in reverse to avoid issues with list re-indexing after popping items.
        for i in sorted(card_indices, reverse=True):
            # Check if the index is valid.
            if 0 <= i < len(self.hand.cards):
                # Remove the card from the hand and add it to the 'discarded' list.
                discarded.append(self.hand.cards.pop(i))

        # Add all discarded cards to the game's discard pile.
        self.discard_pile.extend(discarded)
        return discarded

    def draw_cards(self, num_cards: int) -> List[Card]:
        """
        Draws a specified number of new cards from the top of the deck.
        Args:
            num_cards: The integer number of cards to draw.
        Returns:
            A list of new Card objects drawn from the deck.
        """
        return self.deck.deal(num_cards)

    def evaluate_hand(self) -> Dict:
        """
        Evaluates the player's current 5-card hand to determine its poker rank and score.
        It updates both the current hand's score and the total accumulated score.
        Returns:
            A dictionary containing the hand's type (e.g., "Full House") and its score.
        """
        # The hand must exist and contain exactly 5 cards to be evaluated.
        if not self.hand or len(self.hand.cards) != 5:
            return {"type": "Invalid Hand", "score": 0}

        # Normalize card values and suits for easier processing.
        normalized_values = []
        normalized_suits = []

        for card in self.hand.cards:
            # Standardize card value representation (e.g., '0' stripping, '10' to 'T').
            value = card.value.lstrip('0') if card.value[0] == '0' else card.value
            value = 'T' if value == '10' else value
            normalized_values.append(value)
            # Standardize suit representation to the first letter, uppercase.
            normalized_suits.append(card.suit[0].upper())

        # Count occurrences of each rank and suit.
        rank_counts = Counter(normalized_values)
        suit_counts = Counter(normalized_suits)
        # Get a sorted list of how many times each rank appears (e.g., [3, 1, 1] for a three of a kind).
        counts = sorted(rank_counts.values(), reverse=True)

        # Check for a flush (all cards of the same suit).
        is_flush = len(suit_counts) == 1

        # Check for a straight (five cards in sequence).
        indices = [self.RANKS.index(val) for val in normalized_values]
        indices = sorted(set(indices)) # Use set to handle pairs correctly
        is_straight = len(indices) == 5 and (indices[-1] - indices[0] == 4)
        # Special case for the Ace-low straight (A, 2, 3, 4, 5).
        if set(normalized_values) == {'A', '2', '3', '4', '5'}:
            is_straight = True
            # Reorder indices for Ace-low to correctly evaluate as a straight.
            indices = [0, 1, 2, 3, 12]

        # Determine hand rank based on the checks above, from best to worst.
        if is_flush and set(normalized_values) == {'A', 'K', 'Q', 'J', 'T'}:
            result = {"type": "Royal Flush", "score": HandRank.ROYAL_FLUSH}
        elif is_flush and is_straight:
            result = {"type": "Straight Flush", "score": HandRank.STRAIGHT_FLUSH}
        elif 4 in counts:
            result = {"type": "Four of a Kind", "score": HandRank.FOUR_OF_A_KIND}
        elif 3 in counts and 2 in counts:
            result = {"type": "Full House", "score": HandRank.FULL_HOUSE}
        elif is_flush:
            result = {"type": "Flush", "score": HandRank.FLUSH}
        elif is_straight:
            result = {"type": "Straight", "score": HandRank.STRAIGHT}
        elif 3 in counts:
            result = {"type": "Three of a Kind", "score": HandRank.THREE_OF_A_KIND}
        elif counts.count(2) == 2:
            result = {"type": "Two Pair", "score": HandRank.TWO_PAIR}
        elif 2 in counts:
            result = {"type": "One Pair", "score": HandRank.ONE_PAIR}
        else:
            result = {"type": "High Card", "score": HandRank.HIGH_CARD}

        # Update the game's scores with the result of this hand.
        self.current_hand_points = result['score']
        self.score += self.current_hand_points

        return result

    def reset_score(self):
        """
        Manually resets the total accumulated score to zero.
        Useful for starting a new game session from scratch.
        """
        self.score = 0