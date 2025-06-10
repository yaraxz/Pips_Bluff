import tkinter as tk
from PIL import Image, ImageTk


class AboutUI:
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard

        self.create_main_frame()
        self.add_title()
        self.add_about_text()
        self.add_logo_image()

    def create_main_frame(self):
        self.frame = tk.Frame(
            self.parent,
            bg=self.dashboard.colors['content']
        )
        self.frame.pack(
            fill='both',
            expand=True,
            padx=20,
            pady=20
        )

    def add_title(self):
        tk.Label(
            self.frame,
            text="About Pip's Bluff",
            font=self.dashboard.header_font,
            bg=self.dashboard.colors['content'],
            fg='#552CB7'
        ).pack(
            pady=(0, 20)
        )

    def add_about_text(self):
        about_text = """
"An ordinary Balatro kid is building her own poker game from scrap parts 
and stolen rulebooks, piecing together the perfect deck so she can win big
without ever gambling a single chip. 
because she doesn't believe in luck, She believes in systems."

Features:
- Play hands card and got high points
- Customize game settings
- Beautiful and intuitive interface

Version: 1.0
Developed by: Yara:)
"""
        tk.Label(
            self.frame,
            text=about_text,
            font=self.dashboard.base_font,
            bg=self.dashboard.colors['content'],
            justify='left'
        ).pack(
            anchor='w',
            padx=20
        )

    def add_logo_image(self):
        try:
            about_img = Image.open("assets/images/logo.png").resize(
                (200, 200),
                Image.LANCZOS
            )
            self.about_photo = ImageTk.PhotoImage(about_img)

            tk.Label(
                self.frame,
                image=self.about_photo,
                bg=self.dashboard.colors['content']
            ).pack(
                pady=20
            )

        except Exception as e:
            print(f"Error loading about image: {e}")