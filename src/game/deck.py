import random
from typing import List
from .card import Card  # Mengimpor kelas Card dari file card.py


class Deck:
    """Mewakili satu dek kartu remi (52 kartu)."""

    def __init__(self):
        """Inisialisasi dek kosong dan tumpukan buangan."""
        self.cards: List[Card] = []  # Daftar kartu yang tersedia dalam dek
        self.discard_pile: List[Card] = []  # Tumpukan kartu yang telah dibuang

    def create_standard_deck(self, assets_path: str):
        """
        Membuat satu dek standar berisi 52 kartu menggunakan gambar dari direktori aset.

        Args:
            assets_path: Path folder tempat gambar kartu disimpan.
        """
        suits = ["hearts", "diamonds", "clubs", "spades"]  # Jenis kartu
        values = ["A", "02", "03", "04", "05", "06", "07", "08", "09", "10", "J", "Q", "K"]  # Nilai kartu

        # Kombinasi suit dan value untuk membentuk 52 kartu
        for suit in suits:
            for value in values:
                image_path = f"{assets_path}/cards_large/card_{suit}_{value}.png"
                self.cards.append(Card(suit, value, image_path))  # Buat objek Card dan tambahkan ke dek

    def shuffle(self):
        """Mengacak (shuffle) urutan kartu dalam dek."""
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> List[Card]:
        """
        Membagikan sejumlah kartu dari atas dek.

        Args:
            num_cards: Jumlah kartu yang ingin dibagikan.

        Returns:
            List dari objek Card yang telah dibagikan.
        """
        dealt = []

        for _ in range(min(num_cards, len(self.cards))):  # Pastikan tidak membagikan lebih dari jumlah kartu yang tersedia
            dealt.append(self.cards.pop())  # Ambil dari belakang (atas dek)

        return dealt

    def discard(self, card: Card):
        """
        Menambahkan satu kartu ke tumpukan buangan.

        Args:
            card: Objek Card yang ingin dibuang.
        """
        self.discard_pile.append(card)

    def reset(self):
        """
        Menggabungkan kembali kartu buangan ke dek, lalu mengocok ulang.
        """
        self.cards.extend(self.discard_pile)  # Tambahkan semua kartu buangan ke dek
        self.discard_pile = []  # Kosongkan tumpukan buangan
        self.shuffle()  # Kocok dek
