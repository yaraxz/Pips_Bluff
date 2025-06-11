from typing import Dict, Optional, List
from collections import Counter
from enum import IntEnum
from .card import Card
from .deck import Deck
from .hand import Hand


# Mendefinisikan peringkat tangan poker sebagai enumerasi integer.
class HandRank(IntEnum):
    """
    Enumerasi untuk peringkat tangan poker, diurutkan dari terlemah hingga terkuat.
    Nilai integer mewakili skor untuk setiap jenis tangan.
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


# Kelas utama yang mengatur logika permainan kartu.
class GameEngine:
    """
    Mengelola status permainan, termasuk dek, tangan pemain, penilaian,
    dan alur keseluruhan permainan kartu.
    """
    # String yang mewakili peringkat kartu dalam urutan menaik.
    RANKS = "23456789TJQKA"

    def __init__(self):
        """
        Menginisialisasi mesin permainan, menyiapkan dek, tangan, skor,
        dan tumpukan buangan untuk sesi permainan baru.
        """
        self.deck = Deck()  # Dek kartu untuk permainan.
        self.hand: Optional[Hand] = None  # Tangan pemain saat ini.
        self.score = 0  # Total skor yang terkumpul dari semua ronde.
        self.discard_pile: List[Card] = []  # Kartu yang dibuang oleh pemain.
        self.current_hand_points = 0  # Skor yang diperoleh dari tangan saat ini saja.

    def initialize_game(self, assets_path: str):
        self.deck = Deck()  # Membuat instance Deck baru.
        self.deck.create_standard_deck(assets_path)  # Mengisi dengan 52 kartu standar.
        self.deck.shuffle()  # Mengacak urutan kartu.
        self.hand = None  # Mengosongkan tangan pemain.
        self.current_hand_points = 0  # Mengatur ulang poin untuk tangan baru.
        self.discard_pile = []  # Mengosongkan tumpukan buangan.
        # Total skor (self.score) sengaja tidak direset untuk akumulasi antar sesi.

    def deal_hand(self, num_cards=5) -> Hand:
        """
        Membagikan sejumlah kartu tertentu kepada pemain.
        Jika dek kehabisan kartu, daur ulang tumpukan buangan.
        Args:
            num_cards: Jumlah kartu yang akan dibagikan untuk tangan (default adalah 5).
        Returns:
            Objek Hand baru yang berisi kartu yang dibagikan.
        """
        # Memeriksa apakah dek memiliki cukup kartu untuk dibagikan.
        if len(self.deck.cards) < num_cards:
            # Jika tidak, tambahkan kartu yang dibuang kembali ke dalam dek.
            self.deck.cards.extend(self.discard_pile)
            self.discard_pile = []  # Mengosongkan tumpukan buangan.
            self.deck.shuffle()  # Mengacak ulang dek.

        # Membagikan jumlah kartu yang diminta dari dek.
        cards = self.deck.deal(num_cards)
        self.hand = Hand(cards)  # Membuat Hand baru dengan kartu-kartu ini.
        self.current_hand_points = 0  # Mengatur ulang skor untuk tangan baru ini.
        return self.hand

    def discard_cards(self, card_indices: List[int]) -> List[Card]:
        """
        Menghapus kartu dari tangan pemain berdasarkan indeksnya dan
        memindahkannya ke tumpukan buangan.
        Args:
            card_indices: Daftar indeks integer untuk kartu yang akan dibuang.
        Returns:
            Daftar objek Card yang dibuang.
        """
        # Memastikan ada tangan untuk dibuang.
        if not self.hand:
            return []

        discarded = []
        # Mengurutkan indeks secara terbalik untuk menghindari masalah dengan pengindeksan ulang list setelah menghapus item.
        for i in sorted(card_indices, reverse=True):
            # Memeriksa apakah indeks valid.
            if 0 <= i < len(self.hand.cards):
                # Menghapus kartu dari tangan dan menambahkannya ke daftar 'discarded'.
                discarded.append(self.hand.cards.pop(i))

        # Menambahkan semua kartu yang dibuang ke tumpukan buangan permainan.
        self.discard_pile.extend(discarded)
        return discarded

    def draw_cards(self, num_cards: int) -> List[Card]:
        """
        Mengambil sejumlah kartu baru dari atas dek.
        Args:
            num_cards: Jumlah integer kartu yang akan diambil.
        Returns:
            Daftar objek Card baru yang diambil dari dek.
        """
        return self.deck.deal(num_cards)

    def evaluate_hand(self) -> Dict:
        """
        Mengevaluasi tangan pemain saat ini (5 kartu) untuk menentukan peringkat poker dan skornya.
        Memperbarui skor tangan saat ini dan total skor yang terkumpul.
        Returns:
            Kamus yang berisi jenis tangan (misalnya, "Full House") dan skornya.
        """
        # Tangan harus ada dan berisi tepat 5 kartu untuk dievaluasi.
        if not self.hand or len(self.hand.cards) != 5:
            return {"type": "Tangan Tidak Valid", "score": 0}

        # Normalisasi nilai dan suit kartu untuk mempermudah pemrosesan.
        normalized_values = []
        normalized_suits = []

        for card in self.hand.cards:
            # Standarisasi representasi nilai kartu (misalnya, menghapus '0', '10' menjadi 'T').
            value = card.value.lstrip('0') if card.value[0] == '0' else card.value
            value = 'T' if value == '10' else value
            normalized_values.append(value)
            # Standarisasi representasi suit ke huruf pertama, huruf besar.
            normalized_suits.append(card.suit[0].upper())

        # Menghitung kemunculan setiap peringkat dan suit.
        rank_counts = Counter(normalized_values)
        suit_counts = Counter(normalized_suits)
        # Mendapatkan daftar terurut berapa kali setiap peringkat muncul (misalnya, [3, 1, 1] untuk three of a kind).
        counts = sorted(rank_counts.values(), reverse=True)

        # Memeriksa flush (semua kartu memiliki suit yang sama).
        is_flush = len(suit_counts) == 1

        # Memeriksa straight (lima kartu berurutan).
        indices = [self.RANKS.index(val) for val in normalized_values]
        indices = sorted(set(indices)) # Menggunakan set untuk menangani pasangan dengan benar
        is_straight = len(indices) == 5 and (indices[-1] - indices[0] == 4)
        # Kasus khusus untuk straight Ace-rendah (A, 2, 3, 4, 5).
        if set(normalized_values) == {'A', '2', '3', '4', '5'}:
            is_straight = True
            # Mengurutkan ulang indeks untuk Ace-rendah agar dievaluasi dengan benar sebagai straight.
            indices = [0, 1, 2, 3, 12]

        # Menentukan peringkat tangan berdasarkan pemeriksaan di atas, dari terbaik hingga terburuk.
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

        # Memperbarui skor permainan dengan hasil dari tangan ini.
        self.current_hand_points = result['score']
        self.score += self.current_hand_points

        return result

    def reset_score(self):
        """
        Secara manual mengatur ulang total skor yang terkumpul menjadi nol.
        Berguna untuk memulai sesi permainan baru dari awal.
        """
        self.score = 0