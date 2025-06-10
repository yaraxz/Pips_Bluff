import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from auth.register import Register
import tkinter.font as tkFont


class RegisterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("600x500")
        self.center_window(600, 500)

        # Font selection based on system availability
        available_fonts = tkFont.families()
        if 'Verdana' in available_fonts:
            font_family = 'Verdana'
        elif 'Arial' in available_fonts:
            font_family = 'Arial'
        else:
            font_family = 'Helvetica'

        # Define fonts
        self.base_font = tkFont.Font(family=font_family, size=12)
        self.bold_font = tkFont.Font(family=font_family, size=14, weight='bold')
        self.title_font = tkFont.Font(family=font_family, size=24, weight='bold')

        # Background theme
        self.root.configure(bg='#552CB7')

        # Register handler
        self.register_handler = Register()

        # Build UI
        self.create_widgets()

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def create_widgets(self):
        """Construct all UI components."""

        # Header with logo or fallback
        header_frame = tk.Frame(self.root, bg='#FD5A46', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        try:
            logo_path = os.path.join(os.getcwd(), "assets", "images", "logo.png")
            image = Image.open(logo_path)
            image = image.resize((175, 120), Image.Resampling.LANCZOS)
            logo = ImageTk.PhotoImage(image)

            self.logo_label = tk.Label(header_frame, image=logo, bg='#FD5A46')
            self.logo_label.image = logo  # Prevent GC
            self.logo_label.pack(pady=10)
        except Exception as e:
            print("Error loading logo image:", e)
            tk.Label(
                header_frame,
                text="Logo Not Found",
                font=self.title_font,
                bg='#552CB7',
                fg='white'
            ).pack(pady=0)

        # Container for content
        container = tk.Frame(self.root, bg='#552CB7')
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Center white panel
        center_frame = tk.Frame(container, bg='white', bd=3, relief='ridge')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Form wrapper
        form_frame = tk.Frame(center_frame, bg='white', padx=40, pady=30)
        form_frame.pack()

        # Title
        tk.Label(
            form_frame,
            text="Join Us Today!",
            font=self.bold_font,
            bg='white',
            fg='#552CB7',
            pady=10
        ).pack()

        # Form fields: label text, attribute name, optional mask
        fields = [
            ("Username:", "username_entry"),
            ("Email:", "email_entry"),
            ("Password:", "password_entry", "*"),
            ("Confirm Password:", "confirm_password_entry", "*")
        ]

        for label_text, attr_name, *show in fields:
            field_frame = tk.Frame(form_frame, bg='white')
            field_frame.pack(pady=12, fill='x')

            tk.Label(
                field_frame,
                text=label_text,
                bg='white',
                fg='#FD5A46',
                font=self.base_font,
                width=18,
                anchor='e'
            ).pack(side='left', padx=5)

            entry = tk.Entry(
                field_frame,
                font=self.base_font,
                bg='white',
                fg='#333333',
                insertbackground='#552CB7',
                relief='sunken',
                bd=2,
                width=25,
                show=show[0] if show else None
            )
            entry.pack(side='left')
            setattr(self, attr_name, entry)

        # Buttons section
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(pady=25)

        # Register button
        register_btn = tk.Button(
            button_frame,
            text="Register",
            width=15,
            bg='#FFC567',
            fg='#333333',
            font=self.bold_font,
            activebackground='#FFC567',
            activeforeground='#333333',
            bd=2,
            relief='raised',
            command=self.register,
            cursor="hand2",
            pady=6,
        )
        register_btn.pack(side='left', padx=10)

        # Login button
        login_btn = tk.Button(
            button_frame,
            text="Login",
            width=15,
            bg='#058CD7',
            fg='white',
            font=self.bold_font,
            activebackground='#058CD7',
            activeforeground='white',
            bd=2,
            relief='raised',
            command=self.show_login,
            cursor="hand2",
            pady=6,
        )
        login_btn.pack(side='left', padx=10)

    def register(self):
        """Handle registration logic."""
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        success, message = self.register_handler.register(
            username, email, password, confirm_password
        )

        if success:
            self.show_login()
        else:
            messagebox.showerror("Registration Error", message)

    def show_login(self):
        """Open login UI and close registration window."""
        self.root.destroy()
        from ui.login_ui import LoginUI
        login_root = tk.Tk()
        LoginUI(login_root)
        login_root.mainloop()
