import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk
from auth.login import Login


class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x500")
        self.center_window(600, 500)

        self.configure_fonts()
        self.login_handler = Login()
        self.root.configure(bg='#552CB7')

        self.create_widgets()

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configure_fonts(self):
        """Set font families and sizes."""
        available_fonts = tkFont.families()
        if 'Verdana' in available_fonts:
            font_family = 'Verdana'
        elif 'Arial' in available_fonts:
            font_family = 'Arial'
        else:
            font_family = 'Helvetica'

        self.base_font = tkFont.Font(family=font_family, size=12)
        self.bold_font = tkFont.Font(family=font_family, size=14, weight='bold')
        self.title_font = tkFont.Font(family=font_family, size=24, weight='bold')

    def create_widgets(self):
        """Build and place all UI components."""
        self.create_header()
        self.create_form()

    def create_header(self):
        """Display the logo or fallback title."""
        header_frame = tk.Frame(self.root, bg='#FD5A46', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        try:
            logo_path = os.path.join(os.getcwd(), "assets", "images", "logo.png")
            image = Image.open(logo_path)
            image = image.resize((175, 120), Image.Resampling.LANCZOS)
            logo = ImageTk.PhotoImage(image)

            self.logo_label = tk.Label(header_frame, image=logo, bg='#FD5A46')
            self.logo_label.image = logo
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

    def create_form(self):
        """Build the login form UI."""
        container = tk.Frame(self.root, bg='#552CB7')
        container.pack(fill='both', expand=True, padx=20, pady=20)

        center_frame = tk.Frame(container, bg='white', bd=3, relief='ridge')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        form_frame = tk.Frame(center_frame, bg='white', padx=40, pady=30)
        form_frame.pack()

        tk.Label(
            form_frame,
            text="Please Login",
            font=self.bold_font,
            bg='white',
            fg='#552CB7',
            pady=10
        ).pack()

        self.create_username_field(form_frame)
        self.create_password_field(form_frame)
        self.create_buttons(form_frame)

    def create_username_field(self, parent):
        username_frame = tk.Frame(parent, bg='white')
        username_frame.pack(pady=10, fill='x')

        tk.Label(
            username_frame,
            text="Username:",
            bg='white',
            fg='#FD5A46',
            font=self.base_font
        ).pack(side='left', padx=(0, 10))

        self.username_entry = tk.Entry(
            username_frame,
            font=self.base_font,
            bg='white',
            fg='#333333',
            insertbackground='#552CB7',
            relief='sunken',
            bd=2,
            width=25
        )
        self.username_entry.pack(side='left')

    def create_password_field(self, parent):
        password_frame = tk.Frame(parent, bg='white')
        password_frame.pack(pady=10, fill='x')

        tk.Label(
            password_frame,
            text="Password:",
            bg='white',
            fg='#FD5A46',
            font=self.base_font
        ).pack(side='left', padx=(0, 10))

        self.password_entry = tk.Entry(
            password_frame,
            show="*",
            font=self.base_font,
            bg='white',
            fg='#333333',
            insertbackground='#552CB7',
            relief='sunken',
            bd=2,
            width=25
        )
        self.password_entry.pack(side='left')

    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(pady=20)

        login_btn = tk.Button(
            button_frame,
            text="Login",
            width=12,
            bg='#FFC567',
            fg='#333333',
            font=self.bold_font,
            activebackground='#FFC567',
            activeforeground='#333333',
            bd=2,
            relief='raised',
            command=self.login,
            cursor="hand2",
            pady=5,
        )
        login_btn.pack(side='left', padx=10)

        register_btn = tk.Button(
            button_frame,
            text="Register",
            width=12,
            bg='#FB7DAB',
            fg='white',
            font=self.bold_font,
            activebackground='#FB7DAB',
            activeforeground='white',
            bd=2,
            relief='raised',
            command=self.show_register,
            cursor="hand2",
            pady=5,
        )
        register_btn.pack(side='left', padx=10)

    def login(self):
        """Handle login button click."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, message = self.login_handler.authenticate(username, password)

        if success:
            self.root.destroy()
            self.show_dashboard(username)
        else:
            messagebox.showerror("Login Error", message)

    def show_register(self):
        """Open register page UI."""
        from ui.register_ui import RegisterUI
        self.root.destroy()
        register_root = tk.Tk()
        RegisterUI(register_root)
        register_root.mainloop()

    def show_dashboard(self, username):
        """Open dashboard UI after successful login."""
        from ui.dashboard_ui import DashboardUI
        dashboard_root = tk.Tk()
        DashboardUI(dashboard_root, username)
        dashboard_root.mainloop()
