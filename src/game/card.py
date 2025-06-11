from dataclasses import dataclass
from typing import Optional
from PIL import Image, ImageTk


@dataclass
class Card:
    suit: str  # Jenis kartu: Hearts, Diamonds, Clubs, Spades
    value: str  # Nilai kartu: 02, 03, ..., 10, J, Q, K, A
    image_path: str  # Path ke file gambar kartu
    tk_image: Optional[ImageTk.PhotoImage] = None  # Objek gambar Tkinter (opsional)

    def load_image(self, size=(100, 145)) -> bool:
        """
        Memuat gambar kartu dari path dan simpan sebagai objek ImageTk untuk ditampilkan di Tkinter.

        Args:
            size (tuple): Ukuran gambar yang diinginkan dalam format (lebar, tinggi)

        Returns:
            bool: True jika berhasil dimuat, False jika file tidak ditemukan.
        """
        try:
            img = Image.open(self.image_path).resize(size)  # Buka dan ubah ukuran gambar
            self.tk_image = ImageTk.PhotoImage(img)  # Simpan sebagai objek ImageTk
            return True
        except FileNotFoundError:
            return False  # Jika file tidak ditemukan

    def __str__(self) -> str:
        """
        Mengembalikan string representasi kartu yang mudah dibaca, seperti '10 of Hearts'.

        Returns:
            str: Representasi string dari kartu
        """
        # Pemetaan nilai kartu agar lebih mudah dibaca
        value_map = {
            "02": "2", "03": "3", "04": "4", "05": "5",
            "06": "6", "07": "7", "08": "8", "09": "9",
            "10": "10", "J": "J", "Q": "Q", "K": "K", "A": "A"
        }

        display_value = value_map.get(self.value, self.value)  # Ambil nilai tampilan dari peta

        return f"{display_value} of {self.suit}"  # Gabungkan dengan jenis kartu
