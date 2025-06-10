from dataclasses import dataclass
from typing import Optional
from PIL import Image, ImageTk


@dataclass
class Card:
    suit: str
    value: str
    image_path: str
    tk_image: Optional[ImageTk.PhotoImage] = None

    def load_image(self, size=(100, 145)):
        try:
            img = Image.open(self.image_path).resize(size)
            self.tk_image = ImageTk.PhotoImage(img)
            return True
        except FileNotFoundError:
            return False

    def __str__(self):
        # Convert numeric values back to simple numbers for display
        value_map = {
            "02": "2", "03": "3", "04": "4", "05": "5",
            "06": "6", "07": "7", "08": "8", "09": "9",
            "10": "10", "J": "J", "Q": "Q", "K": "K", "A": "A"
        }
        display_value = value_map.get(self.value, self.value)
        return f"{display_value} of {self.suit}"