import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageSequence

from .about_ui import AboutUI
from .game_ui import GameUI
from .info_ui import InfoUI
from .settings_ui import SettingsUI


class DashboardUI:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        self.root.title("Pip's Bluff - Dashboard")
        self.root.geometry("1024x700")

        self.current_page = None  # Track currently active page

        self.center_window(1024, 700)
        self.load_logo()
        self.setup_fonts()
        self.setup_colors()

        self.root.configure(bg=self.colors['bg'])

        self.create_widgets()
        self.show_profile()

    def center_window(self, width, height):
        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def load_logo(self):
        try:
            self.logo_img = Image.open("assets/images/logo.png").resize(
                (150, 95),
                Image.LANCZOS
            )
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo_photo = None

    def setup_fonts(self):
        font_family = 'Arial Rounded MT Bold' if 'Arial Rounded MT Bold' in tkFont.families() else 'Arial'

        self.base_font = tkFont.Font(
            family=font_family,
            size=12
        )

        self.bold_font = tkFont.Font(
            family=font_family,
            size=12,
            weight='bold'
        )

        self.header_font = tkFont.Font(
            family=font_family,
            size=16,
            weight='bold'
        )

        self.title_font = tkFont.Font(
            family=font_family,
            size=20,
            weight='bold'
        )

    def setup_colors(self):
        self.colors = {
            'bg': '#552CB7',
            'header': '#FD5A46',
            'nav': '#058CD7',
            'content': '#F5F5F5'
        }

    def create_widgets(self):
        self.create_header()
        self.create_content_area()

    def create_header(self):
        # Create header section
        header_frame = tk.Frame(
            self.root,
            bg=self.colors['header'],
            height=100
        )
        header_frame.pack(fill='x', expand=False)
        header_frame.pack_propagate(False)

        if self.logo_photo:
            tk.Label(
                header_frame,
                image=self.logo_photo,
                bg=self.colors['header']
            ).pack(expand=True, pady=10)
        else:
            tk.Label(
                header_frame,
                text="PIP'S BLUFF",
                font=self.title_font,
                bg=self.colors['header'],
                fg='white'
            ).pack(expand=True, pady=20)

    def create_content_area(self):
        # Create main content area
        content_frame = tk.Frame(
            self.root,
            bg=self.colors['content']
        )
        content_frame.pack(
            fill='both',
            expand=True,
            padx=20,
            pady=20
        )

        self.create_navigation_sidebar(content_frame)
        self.create_main_display(content_frame)

    def create_navigation_sidebar(self, parent_frame):
        # Navigation sidebar
        nav_frame = tk.Frame(
            parent_frame,
            bg=self.colors['nav'],
            width=220
        )
        nav_frame.pack(
            side='left',
            fill='y',
            padx=(0, 20)
        )
        nav_frame.pack_propagate(False)

        self.create_navigation_buttons(nav_frame)

    def create_navigation_buttons(self, nav_frame):
        buttons_info = [
            ("Profile", self.show_profile),
            ("Play", self.show_game),
            ("Settings", self.show_settings)
        ]

        colors = ['#FB7DAB', '#FFC567', '#552CB7']

        for (text, command), color in zip(buttons_info, colors):
            btn = tk.Button(
                nav_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=self.bold_font,
                bd=3,
                relief='raised',
                cursor="hand2",
                pady=8
            )
            btn.pack(
                pady=8,
                padx=10,
                fill='x'
            )

            # Add extra button under "Play"
            if text == "Play":
                self.create_info_button(nav_frame)

            # Add About Pip's Bluff button under Settings
            if text == "Settings":
                self.create_about_button(nav_frame)

    def create_info_button(self, nav_frame):
        info_btn = tk.Button(
            nav_frame,
            text="Hand Info",
            command=self.show_info,
            bg='#058CD7',
            fg='white',
            font=self.bold_font,
            bd=3,
            relief='raised',
            cursor="hand2",
            pady=6
        )
        info_btn.pack(
            pady=(0, 8),
            padx=10,
            fill='x'
        )

    def create_about_button(self, nav_frame):
        about_btn = tk.Button(
            nav_frame,
            text="About Pip's Bluff",
            command=self.show_about,
            bg='#3BB273',
            fg='white',
            font=self.bold_font,
            bd=3,
            relief='raised',
            cursor="hand2",
            pady=6
        )
        about_btn.pack(
            pady=(0, 8),
            padx=10,
            fill='x'
        )

    def create_main_display(self, content_frame):
        # Main content display area
        self.main_display = tk.Frame(
            content_frame,
            bg=self.colors['content']
        )
        self.main_display.pack(
            side='right',
            fill='both',
            expand=True
        )

    def show_profile(self):
        self.clear_main_display()
        self.current_page = None

        # Main profile layout
        profile_frame = tk.Frame(
            self.main_display,
            bg=self.colors['content']
        )
        profile_frame.pack(
            fill='both',
            expand=True,
            padx=20,
            pady=20
        )

        self.create_profile_top_section(profile_frame)
        self.create_user_info_section(profile_frame)
        self.create_gif_section(profile_frame)

    def create_profile_top_section(self, parent_frame):
        # Top section (title & username)
        top_frame = tk.Frame(
            parent_frame,
            bg=self.colors['content']
        )
        top_frame.pack(
            anchor='nw',
            fill='x'
        )

        tk.Label(
            top_frame,
            text="User Profile",
            font=self.header_font,
            bg=self.colors['content'],
            fg='#552CB7'
        ).pack(
            anchor='center',
            pady=(0, 10)
        )

    def create_user_info_section(self, parent_frame):
        user_info_frame = tk.Frame(
            parent_frame,
            bg=self.colors['content']
        )
        user_info_frame.pack(
            anchor='nw',
            padx=10,
            pady=(0, 20)
        )

        tk.Label(
            user_info_frame,
            text="Username:",
            bg=self.colors['content'],
            fg='#FD5A46',
            font=self.bold_font
        ).grid(
            row=0,
            column=0,
            sticky='w'
        )

        tk.Label(
            user_info_frame,
            text=self.username,
            bg=self.colors['content'],
            fg='#058CD7',
            font=self.base_font
        ).grid(
            row=0,
            column=1,
            sticky='w'
        )

    def create_gif_section(self, parent_frame):
        # Centered GIF frame
        gif_holder = tk.Frame(
            parent_frame,
            bg=self.colors['content']
        )
        gif_holder.pack(expand=True)

        try:
            gif_path = "assets/gif/gif1.gif"
            gif = Image.open(gif_path)

            self.gif_frames = [
                ImageTk.PhotoImage(
                    frame.copy().convert('RGBA').resize(
                        (400, 300),
                        Image.LANCZOS
                    )
                )
                for frame in ImageSequence.Iterator(gif)
            ]

            self.gif_index = 0

            self.gif_label = tk.Label(
                gif_holder,
                bg=self.colors['content']
            )
            self.gif_label.pack()

            self.animate_gif()

        except Exception as e:
            print(f"Error loading animated gif: {e}")

    def show_game(self):
        # Show game UI
        self.clear_main_display()
        self.current_page = GameUI(
            self.main_display,
            self.username,
            "assets/images"
        )

    def show_settings(self):
        # Show settings UI
        self.clear_main_display()
        self.current_page = SettingsUI(
            self.main_display,
            self.username,
            self
        )

    def show_about(self):
        # Show about UI
        self.clear_main_display()
        self.current_page = AboutUI(
            self.main_display,
            self
        )

    def show_info(self):
        # Show hand info UI
        self.clear_main_display()
        self.current_page = InfoUI(
            self.main_display,
            self
        )

    def animate_gif(self):
        if hasattr(self, 'gif_label') and self.gif_label.winfo_exists():  # Check if the widget exists
            if hasattr(self, 'gif_frames') and self.gif_frames:
                self.gif_label.configure(
                    image=self.gif_frames[self.gif_index]
                )

                self.gif_index = (self.gif_index + 1) % len(self.gif_frames)

                # Adjust delay to control animation speed
                self.root.after(100, self.animate_gif)

    def update_username(self, new_username):
        # Update username variable
        self.username = new_username

    def logout(self):
        # Destroy current window and return to login
        from .login_ui import LoginUI

        self.root.destroy()

        login_root = tk.Tk()
        LoginUI(login_root)
        login_root.mainloop()

    def clear_main_display(self):
        # Clear the content display area
        self.current_page = None

        for widget in self.main_display.winfo_children():
            widget.destroy()