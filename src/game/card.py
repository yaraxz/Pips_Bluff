from dataclasses import dataclass
from typing import Optional
from PIL import Image, ImageTk


@dataclass
class Card:
    suit: str
    value: str
    image_path: str
    tk_image: Optional[ImageTk.PhotoImage] = None

    def load_image(self, size=(100, 145)) -> bool:
        """
        Loads the card image from disk and stores it as a Tkinter-compatible image.

        Args:
            size (tuple): Desired (width, height) of the image.

        Returns:
            bool: True if image is loaded successfully, False if file not found.
        """
        try:
            img = Image.open(self.image_path).resize(size)
            self.tk_image = ImageTk.PhotoImage(img)
            return True

        except FileNotFoundError:
            return False

    def __str__(self) -> str:
        """
        Returns a human-readable string for the card (e.g., '10 of Hearts').

        Returns:
            str: String representation of the card.
        """
        value_map = {
            "02": "2", "03": "3", "04": "4", "05": "5",
            "06": "6", "07": "7", "08": "8", "09": "9",
            "10": "10", "J": "J", "Q": "Q", "K": "K", "A": "A"
        }

        display_value = value_map.get(self.value, self.value)

        return f"{display_value} of {self.suit}"