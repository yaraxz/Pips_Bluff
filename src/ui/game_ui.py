import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from game.game_engine import GameEngine


class GameUI:
    def __init__(self, parent, username: str, assets_path: str):
        self.parent = parent
        self.username = username
        self.assets_path = Path(assets_path)
        self.engine = GameEngine()
        self.card_widgets = []
        self.card_images = []
        self.selected_for_discard = set()
        self._processing = False
        self.hands_played = 0

        self.setup_ui()
        self.start_new_hand()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.parent, bg='#F5F5F5')
        self.main_frame.pack(fill='both', expand=True)

        # Header
        self.header = tk.Frame(self.main_frame, bg='#F5F5F5', height=50)
        self.header.pack(fill='x')

        tk.Label(
            self.header,
            text=f"{self.username} - Bind",
            font=('Arial', 16, 'bold'),
            fg='#552CB7',
            bg='#F5F5F5'
        ).pack(side='left', padx=20, pady=10)

        # Stats + Notification at top-right
        self.top_right = tk.Frame(self.header, bg='#F5F5F5')
        self.top_right.pack(side='right', padx=20)

        self.hands_played_label = tk.Label(
            self.top_right,
            text="Hands: 0",
            bg='#F5F5F5',
            font=('Arial', 10)
        )
        self.hands_played_label.pack(anchor='e')

        self.total_score_label = tk.Label(
            self.top_right,
            text="Total: 0",
            bg='#F5F5F5',
            font=('Arial', 12, 'bold')
        )
        self.total_score_label.pack(anchor='e')

        self.result_label = tk.Label(
            self.top_right,
            text="",
            bg='#F5F5F5',
            font=('Arial', 11, 'italic'),
            fg='#2E7D32'
        )
        self.result_label.pack(anchor='e', pady=(5, 0))

        # Cards display
        self.cards_frame = tk.Frame(self.main_frame, bg='#F5F5F5')
        self.cards_frame.pack(pady=20)

        # Controls below cards
        self.controls = tk.Frame(self.main_frame, bg='#F5F5F5')
        self.controls.pack(pady=10)

        self.new_hand_btn = tk.Button(
            self.controls,
            text="New Hand",
            command=self.start_new_hand,
            bg='#4CAF50',
            fg='white',
            width=14,
            font=('Arial', 11)
        )
        self.new_hand_btn.pack(side='left', padx=8)

        self.discard_btn = tk.Button(
            self.controls,
            text="Discard Selected",
            command=self.discard_and_replace,
            bg='#FF5722',
            fg='white',
            width=14,
            font=('Arial', 11),
            state=tk.DISABLED
        )
        self.discard_btn.pack(side='left', padx=8)

        self.play_btn = tk.Button(
            self.controls,
            text="Play Hand",
            command=self.play_hand,
            bg='#9C27B0',
            fg='white',
            width=14,
            font=('Arial', 11),
            state=tk.DISABLED
        )
        self.play_btn.pack(side='left', padx=8)

    def start_new_hand(self):
        self.engine.initialize_game(str(self.assets_path))
        self.engine.deal_hand()
        self.selected_for_discard = set()
        self._processing = False
        self.update_button_states()
        self.display_cards()
        self.update_stats()
        self.result_label.config(text="")

    def update_stats(self):
        self.hands_played_label.config(text=f"Hands: {self.hands_played}")
        self.total_score_label.config(text=f"Total: {self.engine.score}")

    def update_button_states(self):
        self.discard_btn['state'] = tk.NORMAL if self.selected_for_discard else tk.DISABLED
        self.play_btn['state'] = tk.NORMAL if self.engine.hand and not self.selected_for_discard else tk.DISABLED

    def display_cards(self):
        for widget in self.card_widgets:
            widget.destroy()
        self.card_widgets = []
        self.card_images = []

        if not self.engine.hand:
            return

        for i, card in enumerate(self.engine.hand.cards):
            bg_color = '#FF6F61' if i in self.selected_for_discard else 'white'
            frame_color = '#FF0000' if i in self.selected_for_discard else '#F5F5F5'

            card_frame = tk.Frame(
                self.cards_frame,
                bg=frame_color,
                bd=2,
                relief='ridge'
            )
            card_frame.grid(row=0, column=i, padx=10)

            try:
                img_path = self.assets_path / "cards_large" / f"card_{card.suit}_{self._format_value(card.value)}.png"
                img = Image.open(img_path).resize((100, 145))
                tk_img = ImageTk.PhotoImage(img)
                self.card_images.append(tk_img)

                lbl = tk.Label(
                    card_frame,
                    image=tk_img,
                    bg=bg_color
                )
                lbl.pack(padx=5, pady=5)
            except Exception:
                lbl = tk.Label(
                    card_frame,
                    text=str(card),
                    bg=bg_color,
                    width=10,
                    height=5
                )
                lbl.pack(padx=5, pady=5)

            lbl.bind("<Button-1>", lambda e, idx=i: self.toggle_card_selection(idx))
            self.card_widgets.append(card_frame)

    def toggle_card_selection(self, index):
        if index in self.selected_for_discard:
            self.selected_for_discard.remove(index)
        else:
            self.selected_for_discard.add(index)
        self.display_cards()
        self.update_button_states()

    def discard_and_replace(self):
        if not self.engine.hand or not self.selected_for_discard:
            return

        discarded = self.engine.discard_cards(list(self.selected_for_discard))
        new_cards = self.engine.draw_cards(len(discarded))
        self.engine.hand.cards.extend(new_cards)

        self.selected_for_discard = set()
        self.display_cards()
        self.update_button_states()

        self.result_label.config(
            text=f"Replaced {len(discarded)} cards",
            fg='#2E7D32'
        )
        self.parent.after(2000, lambda: self.result_label.config(text=""))

    def play_hand(self):
        if self._processing or not self.engine.hand or self.play_btn['state'] == tk.DISABLED:
            return

        self._processing = True
        self.disable_buttons()

        try:
            result = self.engine.evaluate_hand()
            self.hands_played += 1
            self.update_stats()
            self.result_label.config(
                text=f"{result['type']} - {result['score']} points",
                fg='#2E7D32'
            )
            self.parent.after(2000, self.start_new_hand)
        finally:
            self._processing = False

    def disable_buttons(self):
        self.discard_btn['state'] = tk.DISABLED
        self.play_btn['state'] = tk.DISABLED

    def _format_value(self, value: str) -> str:
        if value.startswith('0') and value[1:].isdigit():
            value = value[1:]
        if value in ["J", "Q", "K", "A"]:
            return value
        try:
            num = int(value)
            return f"{num:02d}"
        except ValueError:
            return value
