from typing import List
from .card import Card  # Mengimpor kelas Card dari file card.py


class Hand:
    def __init__(self, cards: List[Card]):
        """
        Inisialisasi tangan pemain dengan daftar objek kartu.

        Args:
            cards: Daftar objek Card yang membentuk tangan.
        """
        self.cards = cards  # Semua kartu yang sedang dipegang
        self.selected: List[int] = []  # Menyimpan index kartu yang sedang dipilih

    def toggle_selection(self, index: int):
        """
        Mengubah status pilihan kartu di posisi tertentu.

        Jika kartu sudah dipilih, maka akan dibatalkan (diseleksi ulang),
        jika belum dipilih, maka akan ditambahkan ke daftar pilihan.

        Args:
            index: Index kartu dalam tangan (0-based).
        """
        if index in self.selected:
            self.selected.remove(index)  # Batalkan pilihan
        else:
            self.selected.append(index)  # Pilih kartu

    def get_selected_cards(self) -> List[Card]:
        """
        Mengambil daftar kartu yang saat ini dipilih.

        Returns:
            List objek Card yang sedang dipilih.
        """
        return [self.cards[i] for i in self.selected]

    def remove_selected(self):
        """
        Menghapus semua kartu yang dipilih dari tangan.

        Proses dilakukan dari index terbesar ke terkecil
        untuk menghindari error index saat melakukan pop.
        Setelah itu, daftar pilihan dikosongkan.
        """
        for i in sorted(self.selected, reverse=True):
            if 0 <= i < len(self.cards):
                self.cards.pop(i)  # Hapus kartu berdasarkan index

        self.selected = []  # Kosongkan daftar pilihan
