import os
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from .game_ui import GameUI
from .info_ui import InfoUI


class DashboardUI:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Pip's Bluff - Dashboard")
        self.root.geometry("1024x700")
        self.center_window(1024, 700)

        try:
            self.logo_img = Image.open("assets/images/logo.png")
            self.logo_img = self.logo_img.resize((150, 95), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        except:
            self.logo_photo = None

        available_fonts = tkFont.families()
        font_family = 'Arial Rounded MT Bold' if 'Arial Rounded MT Bold' in available_fonts else 'Arial'

        self.base_font = tkFont.Font(family=font_family, size=12)
        self.bold_font = tkFont.Font(family=font_family, size=12, weight='bold')
        self.header_font = tkFont.Font(family=font_family, size=16, weight='bold')
        self.title_font = tkFont.Font(family=font_family, size=20, weight='bold')

        self.colors = {
            'bg': '#552CB7',
            'header': '#FD5A46',
            'nav': '#058CD7',
            'content': '#F5F5F5'
        }

        self.root.configure(bg=self.colors['bg'])
        self.create_widgets()
        self.show_profile()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def create_widgets(self):
        if hasattr(self, "widgets_created") and self.widgets_created:
            return
        self.widgets_created = True

        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        if self.logo_photo:
            logo_label = tk.Label(header_frame, image=self.logo_photo, bg=self.colors['header'])
            logo_label.pack(expand=True, pady=10)
        else:
            tk.Label(
                header_frame,
                text="PIP'S BLUFF",
                font=self.title_font,
                bg=self.colors['header'],
                fg='white'
            ).pack(expand=True, pady=20)

        content_frame = tk.Frame(self.root, bg=self.colors['content'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        nav_frame = tk.Frame(content_frame, bg=self.colors['nav'], width=220)
        nav_frame.pack(side='left', fill='y', padx=(0, 20))
        nav_frame.pack_propagate(False)

        buttons_info = [
            ("Profile", self.show_profile, '#FB7DAB', 'white'),
            ("Play", self.show_game, '#FFC567', '#333333'),
            ("Settings", self.show_settings, '#552CB7', 'white'),
        ]

        for text, command, bg_color, fg_color in buttons_info:
            btn = tk.Button(
                nav_frame,
                text=text,
                width=18,
                bg=bg_color,
                fg=fg_color,
                font=self.bold_font,
                activebackground=bg_color,
                activeforeground=fg_color,
                bd=3,
                relief='raised',
                command=command,
                cursor="hand2",
                pady=8,
                padx=10
            )
            btn.pack(pady=8, padx=10, fill='x')

            if text == "Play":
                info_btn = tk.Button(
                    nav_frame,
                    text="Hand Info",
                    width=18,
                    bg='#058CD7',
                    fg='white',
                    font=self.bold_font,
                    activebackground='#058CD7',
                    activeforeground='white',
                    bd=3,
                    relief='raised',
                    command=self.show_info,
                    cursor="hand2",
                    pady=6,
                    padx=10
                )
                info_btn.pack(pady=(0, 8), padx=10, fill='x')

        self.main_display = tk.Frame(content_frame, bg=self.colors['content'])
        self.main_display.pack(side='right', fill='both', expand=True)

    def show_profile(self):
        self.clear_main_display()
        tk.Label(
            self.main_display,
            text="User Profile",
            font=self.header_font,
            bg=self.colors['content'],
            fg='#552CB7',
            pady=10
        ).pack(fill='x')

        info_frame = tk.Frame(self.main_display, bg=self.colors['content'], padx=20, pady=10)
        info_frame.pack(fill='both', expand=True)

        tk.Label(
            info_frame,
            text="Username:",
            bg=self.colors['content'],
            fg='#FD5A46',
            font=self.bold_font,
            width=12,
            anchor='e'
        ).grid(row=0, column=0, sticky='e', pady=5)

        tk.Label(
            info_frame,
            text=self.username,
            bg=self.colors['content'],
            fg='#058CD7',
            font=self.base_font,
            anchor='w'
        ).grid(row=0, column=1, sticky='w', pady=5)

    def show_game(self):
        self.clear_main_display()
        GameUI(self.main_display, self.username, "assets/images")

    def show_settings(self):
        self.clear_main_display()
        tk.Label(
            self.main_display,
            text="Settings",
            font=self.header_font,
            bg='white',
            fg='#552CB7',
            pady=10
        ).pack(fill='x')

        settings_frame = tk.Frame(self.main_display, bg=self.colors['content'], padx=20, pady=10)
        settings_frame.pack(fill='both', expand=True)

        logout_btn = tk.Button(
            settings_frame,
            text="Logout",
            width=18,
            bg='#FD5A46',
            fg='white',
            font=self.bold_font,
            activebackground='#FD5A46',
            activeforeground='white',
            bd=3,
            relief='raised',
            command=self.logout,
            cursor="hand2",
            pady=8,
            padx=10
        )
        logout_btn.grid(row=1, column=0, columnspan=2, pady=20)

    def show_info(self):
        self.clear_main_display()
        InfoUI(self.main_display, self.show_profile)

    def logout(self):
        from .login_ui import LoginUI
        self.root.destroy()
        login_root = tk.Tk()
        LoginUI(login_root)
        login_root.mainloop()

    def clear_main_display(self):
        for widget in self.main_display.winfo_children():
            widget.destroy()
