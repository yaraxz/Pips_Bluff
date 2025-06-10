import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class InfoUI:
    def __init__(self, root, _):
        self.root = root
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a6fa5"
        self.text_color = "#333333"
        self.cards_path = "assets/images/cards_small"
        self.card_size = (50, 75)
        self.card_tk_images = []

        # Define hand rankings: (name, score, card images, description)
        self.hand_rankings = [
            ("Royal Flush", 100,
             ["card_hearts_A.png", "card_hearts_K.png", "card_hearts_Q.png", "card_hearts_J.png", "card_hearts_10.png"],
             "A, K, Q, J, 10 all of the same suit"),
            ("Straight Flush", 90,
             ["card_spades_05.png", "card_spades_06.png", "card_spades_07.png", "card_spades_08.png",
              "card_spades_09.png"], "Five consecutive cards of the same suit"),
            ("Four of a Kind", 80,
             ["card_diamonds_09.png", "card_hearts_09.png", "card_clubs_09.png", "card_spades_09.png",
              "card_hearts_K.png"], "Four cards of the same rank"),
            ("Full House", 70,
             ["card_spades_07.png", "card_hearts_07.png", "card_clubs_07.png", "card_diamonds_Q.png",
              "card_hearts_Q.png"], "Three of a kind and a pair"),
            ("Flush", 60,
             ["card_hearts_02.png", "card_hearts_05.png", "card_hearts_08.png", "card_hearts_J.png",
              "card_hearts_K.png"], "Five cards of the same suit"),
            ("Straight", 50,
             ["card_spades_04.png", "card_hearts_05.png", "card_diamonds_06.png", "card_clubs_07.png",
              "card_spades_08.png"], "Five consecutive cards of mixed suits"),
            ("Three of a Kind", 40,
             ["card_hearts_06.png", "card_clubs_06.png", "card_spades_06.png", "card_diamonds_K.png",
              "card_hearts_09.png"], "Three cards of the same rank"),
            ("Two Pair", 30,
             ["card_hearts_08.png", "card_spades_08.png", "card_clubs_J.png", "card_diamonds_J.png",
              "card_spades_03.png"], "Two pairs of cards"),
            ("One Pair", 20,
             ["card_spades_Q.png", "card_hearts_Q.png", "card_diamonds_07.png", "card_clubs_04.png",
              "card_spades_02.png"], "Two cards of the same rank"),
            ("High Card", 10,
             ["card_hearts_02.png", "card_spades_05.png", "card_diamonds_07.png", "card_clubs_09.png",
              "card_hearts_K.png"], "Highest value card"),
        ]

        # --- Set up scrollable canvas layout ---
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack canvas and scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame inside canvas that holds the content
        self.content_container = tk.Frame(self.canvas, bg=self.bg_color)
        self.content_window_id = self.canvas.create_window((0, 0), window=self.content_container, anchor="nw")

        # Actual content frame centered inside container
        self.content_frame = tk.Frame(self.content_container, bg=self.bg_color)
        self.content_frame.pack(anchor="center", pady=20)

        # Scroll bindings for all platforms
        self.content_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)          # Windows/macOS
        self.canvas.bind_all("<Button-4>", self.on_mousewheel_linux)      # Linux scroll up
        self.canvas.bind_all("<Button-5>", self.on_mousewheel_linux)      # Linux scroll down

        # Render UI components
        self.render()

    def on_frame_configure(self, event):
        # Update scrollable area size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Ensure content container matches canvas width
        self.canvas.itemconfig(self.content_window_id, width=event.width)

    def on_mousewheel(self, event):
        # Scroll content vertically (Windows/macOS)
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_mousewheel_linux(self, event):
        # Scroll content vertically (Linux)
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def render(self):
        # Add main title
        title_label = tk.Label(
            self.content_frame, text="Poker Hand Rankings", font=("Arial", 20, "bold"),
            fg=self.accent_color, bg=self.bg_color
        )
        title_label.pack(pady=(0, 20))

        # Add hand ranking sections
        for i, (name, points, images, desc) in enumerate(self.hand_rankings):
            self.add_hand_info(self.content_frame, name, points, images, desc)

            # Add separator between sections (except last one)
            if i < len(self.hand_rankings) - 1:
                separator = ttk.Separator(self.content_frame, orient='horizontal')
                separator.pack(fill='x', padx=20, pady=15)

    def add_hand_info(self, parent, name, points, card_files, desc):
        # Create frame for each hand entry
        entry_frame = tk.Frame(parent, bg=self.bg_color)
        entry_frame.pack()

        # Hand title and points
        title = f"{name} ({points} points)"
        tk.Label(
            entry_frame, text=title, font=("Arial", 16, "bold"),
            fg=self.text_color, bg=self.bg_color
        ).pack(pady=(0, 10))

        # Card image display
        card_frame = tk.Frame(entry_frame, bg=self.bg_color)
        card_frame.pack()

        for file_name in card_files:
            path = os.path.join(self.cards_path, file_name)
            try:
                # Load and display card image
                img = Image.open(path).resize(self.card_size, Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                self.card_tk_images.append(tk_img)
                label = tk.Label(card_frame, image=tk_img, bg=self.bg_color, borderwidth=1, relief="solid")
                label.image = tk_img
                label.pack(side="left", padx=15)
            except FileNotFoundError:
                # Show placeholder if image is missing
                placeholder = tk.Label(card_frame, text="?", font=("Arial", 20, "bold"),
                                       width=3, height=1, bg="white", borderwidth=1, relief="solid")
                placeholder.pack(side="left", padx=15)

        # Description text
        tk.Label(
            entry_frame, text=desc, font=("Arial", 12),
            bg=self.bg_color, fg=self.text_color,
            wraplength=550, justify="center"
        ).pack(pady=(10, 0))