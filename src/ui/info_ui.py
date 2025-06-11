import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class InfoUI:
    def __init__(self, root, _):
        self.root = root
        self.setup_colors()
        self.setup_paths()
        self.define_hand_rankings()
        self.setup_scrollable_canvas()
        self.render_ui()

    def setup_colors(self):
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a6fa5"
        self.text_color = "#333333"

    def setup_paths(self):
        self.cards_path = "assets/images/cards_small"
        self.card_size = (50, 75)
        self.card_tk_images = []

    def define_hand_rankings(self):
        self.hand_rankings = [
            ("Royal Flush", 100,
             ["card_hearts_A.png", "card_hearts_K.png", "card_hearts_Q.png",
              "card_hearts_J.png", "card_hearts_10.png"],
             "A, K, Q, J, 10 all of the same suit"),

            ("Straight Flush", 90,
             ["card_spades_05.png", "card_spades_06.png", "card_spades_07.png",
              "card_spades_08.png", "card_spades_09.png"],
             "Five consecutive cards of the same suit"),

            ("Four of a Kind", 80,
             ["card_diamonds_09.png", "card_hearts_09.png", "card_clubs_09.png",
              "card_spades_09.png", "card_hearts_K.png"],
             "Four cards of the same rank"),

            ("Full House", 70,
             ["card_spades_07.png", "card_hearts_07.png", "card_clubs_07.png",
              "card_diamonds_Q.png", "card_hearts_Q.png"],
             "Three of a kind and a pair"),

            ("Flush", 60,
             ["card_hearts_02.png", "card_hearts_05.png", "card_hearts_08.png",
              "card_hearts_J.png", "card_hearts_K.png"],
             "Five cards of the same suit"),

            ("Straight", 50,
             ["card_spades_04.png", "card_hearts_05.png", "card_diamonds_06.png",
              "card_clubs_07.png", "card_spades_08.png"],
             "Five consecutive cards of mixed suits"),

            ("Three of a Kind", 40,
             ["card_hearts_06.png", "card_clubs_06.png", "card_spades_06.png",
              "card_diamonds_K.png", "card_hearts_09.png"],
             "Three cards of the same rank"),

            ("Two Pair", 30,
             ["card_hearts_08.png", "card_spades_08.png", "card_clubs_J.png",
              "card_diamonds_J.png", "card_spades_03.png"],
             "Two pairs of cards"),

            ("One Pair", 20,
             ["card_spades_Q.png", "card_hearts_Q.png", "card_diamonds_07.png",
              "card_clubs_04.png", "card_spades_02.png"],
             "Two cards of the same rank"),

            ("High Card", 10,
             ["card_hearts_02.png", "card_spades_05.png", "card_diamonds_07.png",
              "card_clubs_09.png", "card_hearts_K.png"],
             "Highest value card"),
        ]

    def setup_scrollable_canvas(self):
        # Canvas and scrollbar setup
        self.canvas = tk.Canvas(
            self.root,
            bg=self.bg_color,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack canvas and scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Content container setup
        self.content_container = tk.Frame(
            self.canvas,
            bg=self.bg_color
        )

        self.content_window_id = self.canvas.create_window(
            (0, 0),
            window=self.content_container,
            anchor="nw"
        )

        # Main content frame
        self.content_frame = tk.Frame(
            self.content_container,
            bg=self.bg_color
        )
        self.content_frame.pack(anchor="center", pady=20)

        # Scroll bindings
        self.setup_scroll_bindings()

    def setup_scroll_bindings(self):
        self.content_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # Windows/macOS
        self.canvas.bind_all("<Button-4>", self.on_mousewheel_linux)  # Linux scroll up
        self.canvas.bind_all("<Button-5>", self.on_mousewheel_linux)  # Linux scroll down

    def render_ui(self):
        self.add_title()
        self.add_hand_rankings()

    def add_title(self):
        title_label = tk.Label(
            self.content_frame,
            text="Bind Rank",
            font=("Arial", 20, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(pady=(0, 20))

    def add_hand_rankings(self):
        for i, (name, points, images, desc) in enumerate(self.hand_rankings):
            self.add_hand_info(name, points, images, desc)

            if i < len(self.hand_rankings) - 1:
                self.add_separator()

    def add_hand_info(self, name, points, card_files, desc):
        entry_frame = tk.Frame(
            self.content_frame,
            bg=self.bg_color
        )
        entry_frame.pack()

        self.add_hand_title(entry_frame, name, points)
        self.add_card_images(entry_frame, card_files)
        self.add_description(entry_frame, desc)

    def add_hand_title(self, parent, name, points):
        title = f"{name} ({points} points)"
        tk.Label(
            parent,
            text=title,
            font=("Arial", 16, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(pady=(0, 10))

    def add_card_images(self, parent, card_files):
        card_frame = tk.Frame(
            parent,
            bg=self.bg_color
        )
        card_frame.pack()

        for file_name in card_files:
            self.add_card_image(card_frame, file_name)

    def add_card_image(self, parent, file_name):
        path = os.path.join(self.cards_path, file_name)

        try:
            img = Image.open(path).resize(self.card_size, Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.card_tk_images.append(tk_img)

            label = tk.Label(
                parent,
                image=tk_img,
                bg=self.bg_color,
                borderwidth=1,
                relief="solid"
            )
            label.image = tk_img
            label.pack(side="left", padx=15)

        except FileNotFoundError:
            self.add_card_placeholder(parent)

    def add_card_placeholder(self, parent):
        placeholder = tk.Label(
            parent,
            text="?",
            font=("Arial", 20, "bold"),
            width=3,
            height=1,
            bg="white",
            borderwidth=1,
            relief="solid"
        )
        placeholder.pack(side="left", padx=15)

    def add_description(self, parent, desc):
        tk.Label(
            parent,
            text=desc,
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=550,
            justify="center"
        ).pack(pady=(10, 0))

    def add_separator(self):
        separator = ttk.Separator(
            self.content_frame,
            orient='horizontal'
        )
        separator.pack(fill='x', padx=20, pady=15)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.content_window_id, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")