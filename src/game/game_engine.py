from typing import Dict, Optional, List
from collections import Counter
from enum import IntEnum
from .card import Card
from .deck import Deck
from .hand import Hand


class HandRank(IntEnum):
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


class GameEngine:
    RANKS = "23456789TJQKA"

    def __init__(self):
        self.deck = Deck()
        self.hand: Optional[Hand] = None
        self.score = 0  # Total accumulated score
        self.discard_pile: List[Card] = []
        self.current_hand_points = 0  # Points from current hand only

    def initialize_game(self, assets_path: str):
        """Initialize a new game without resetting the total score"""
        self.deck = Deck()
        self.deck.create_standard_deck(assets_path)
        self.deck.shuffle()
        self.hand = None
        self.current_hand_points = 0  # Reset current hand points
        self.discard_pile = []
        # Note: Don't reset self.score here to maintain accumulation

    def deal_hand(self, num_cards=5) -> Hand:
        """Deal a new hand, recycling discard pile if needed"""
        if len(self.deck.cards) < num_cards:
            self.deck.cards.extend(self.discard_pile)
            self.discard_pile = []
            self.deck.shuffle()

        cards = self.deck.deal(num_cards)
        self.hand = Hand(cards)
        self.current_hand_points = 0  # Reset current hand points
        return self.hand

    def discard_cards(self, card_indices: List[int]) -> List[Card]:
        """Discard selected cards and return them"""
        if not self.hand:
            return []

        discarded = []
        for i in sorted(card_indices, reverse=True):
            if 0 <= i < len(self.hand.cards):
                discarded.append(self.hand.cards.pop(i))

        self.discard_pile.extend(discarded)
        return discarded

    def draw_cards(self, num_cards: int) -> List[Card]:
        """Draw new cards from the deck"""
        return self.deck.deal(num_cards)

    def evaluate_hand(self) -> Dict:
        """Evaluate the current hand and update scores"""
        if not self.hand or len(self.hand.cards) != 5:
            return {"type": "Invalid Hand", "score": 0}

        normalized_values = []
        normalized_suits = []

        for card in self.hand.cards:
            value = card.value.lstrip('0') if card.value[0] == '0' else card.value
            value = 'T' if value == '10' else value
            normalized_values.append(value)
            normalized_suits.append(card.suit[0].upper())

        rank_counts = Counter(normalized_values)
        suit_counts = Counter(normalized_suits)
        counts = sorted(rank_counts.values(), reverse=True)

        is_flush = len(suit_counts) == 1

        indices = [self.RANKS.index(val) for val in normalized_values]
        indices = sorted(set(indices))
        is_straight = len(indices) == 5 and (indices[-1] - indices[0] == 4)
        if set(normalized_values) == {'A', '2', '3', '4', '5'}:
            is_straight = True
            indices = [0, 1, 2, 3, 12]

        # Evaluate hand type and get points
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

        # Update scores
        self.current_hand_points = result['score']
        self.score += self.current_hand_points

        return result

    def reset_score(self):
        """Optional method to manually reset the total score"""
        self.score = 0