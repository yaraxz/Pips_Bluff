import tkinter as tk
from tkinter import messagebox, Toplevel, ttk

from database.db_operations import DBOperations
from security import verify_password


class SettingsUI:
    def __init__(self, root, username, dashboard_instance):
        """
        Initialize the Settings UI.

        Args:
            root: Parent Tkinter root window.
            username: The currently logged-in user's username.
            dashboard_instance: Reference to the dashboard (for styles, logout, and updates).
        """
        self.root = root
        self.dashboard = dashboard_instance
        self.db_ops = DBOperations()

        # Inherit fonts and colors from dashboard
        self.base_font = self.dashboard.base_font
        self.bold_font = self.dashboard.bold_font
        self.header_font = self.dashboard.header_font
        self.colors = self.dashboard.colors

        self.create_settings_widgets()

    def create_settings_widgets(self):
        """Create and layout widgets for the settings page."""
        container = tk.Frame(self.root, bg=self.colors['content'])
        container.pack(fill='both', expand=True, padx=20, pady=10)

        # Title
        title_label = tk.Label(
            container,
            text="Settings",
            font=self.header_font,
            bg=self.colors['content'],
            fg='#552CB7'
        )
        title_label.pack(pady=(0, 20))

        # Account Section
        account_frame = tk.Frame(container, bg=self.colors['content'])
        account_frame.pack(fill='x', pady=10)

        account_label = tk.Label(
            account_frame,
            text="Account",
            font=self.bold_font,
            bg=self.colors['content'],
            fg=self.colors['nav']
        )
        account_label.pack(anchor='w')

        separator = ttk.Separator(account_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)

        buttons_frame = tk.Frame(account_frame, bg=self.colors['content'])
        buttons_frame.pack(fill='x')

        # Change Username Button
        change_user_btn = tk.Button(
            buttons_frame,
            text="Change Username",
            width=20,
            bg='#FFC567',
            fg='#333333',
            font=self.bold_font,
            bd=3,
            relief='raised',
            command=self.open_change_username_dialog,
            cursor="hand2",
            pady=8
        )
        change_user_btn.pack(side='left', pady=10, padx=(0, 10))

        # Logout Button
        logout_btn = tk.Button(
            buttons_frame,
            text="Logout",
            width=20,
            bg='#FD5A46',
            fg='white',
            font=self.bold_font,
            bd=3,
            relief='raised',
            command=self.dashboard.logout,
            cursor="hand2",
            pady=8
        )
        logout_btn.pack(side='left', pady=10)

    def open_change_username_dialog(self):
        """Open a modal dialog for username change with password verification."""
        dialog = Toplevel(self.root)
        dialog.title("Change Username")
        dialog_width, dialog_height = 350, 220

        # Center dialog
        x = (self.root.winfo_screenwidth() / 2) - (dialog_width / 2)
        y = (self.root.winfo_screenheight() / 2) - (dialog_height / 2)
        dialog.geometry(f'{dialog_width}x{dialog_height}+{int(x)}+{int(y)}')

        dialog.configure(bg=self.colors['content'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # New Username Input
        tk.Label(
            dialog,
            text="Enter new username:",
            font=self.base_font,
            bg=self.colors['content']
        ).pack(pady=(15, 5))

        new_username_entry = tk.Entry(dialog, font=self.base_font, width=30)
        new_username_entry.pack(pady=5, padx=20)
        new_username_entry.focus_set()

        # Password Confirmation Input
        tk.Label(
            dialog,
            text="Confirm with your password:",
            font=self.base_font,
            bg=self.colors['content']
        ).pack(pady=(10, 5))

        password_entry = tk.Entry(dialog, font=self.base_font, width=30, show="*")
        password_entry.pack(pady=5, padx=20)

        # Action Buttons
        button_frame = tk.Frame(dialog, bg=self.colors['content'])
        button_frame.pack(pady=15)

        save_btn = tk.Button(
            button_frame,
            text="Save",
            bg="#4CAF50",
            fg="white",
            font=self.bold_font,
            command=lambda: self.save_new_username(
                new_username_entry.get(),
                password_entry.get(),
                dialog
            )
        )
        save_btn.pack(side='left', padx=10)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            bg="#f44336",
            fg="white",
            font=self.bold_font,
            command=dialog.destroy
        )
        cancel_btn.pack(side='left', padx=10)

    def save_new_username(self, new_username, password, dialog):
        """
        Validate and update username in the database after verifying password.

        Args:
            new_username: New username entered by the user.
            password: Password entered to confirm identity.
            dialog: Reference to the modal dialog for cleanup.
        """
        old_username = self.dashboard.username

        # Validation checks
        if not new_username or len(new_username.strip()) < 3 or not password:
            messagebox.showerror(
                "Error",
                "All fields are required and username must be at least 3 characters.",
                parent=dialog
            )
            return

        if new_username == old_username:
            messagebox.showinfo(
                "Info",
                "The new username is the same as the old one.",
                parent=dialog
            )
            return

        try:
            # Verify user
            user_data = self.db_ops.get_user_by_username(old_username)
            if not user_data:
                messagebox.showerror("Error", "Could not find current user data.", parent=dialog)
                return

            stored_hash = user_data['password_hash']

            if not verify_password(password, stored_hash):
                messagebox.showerror("Authentication Failed", "Incorrect password.", parent=dialog)
                return

            # Check if new username is taken
            if self.db_ops.get_user_by_username(new_username):
                messagebox.showerror("Error", "This username is already taken.", parent=dialog)
                return

            # Update in DB
            success = self.db_ops.change_username(old_username, new_username)

            if success:
                self.dashboard.update_username(new_username)
                messagebox.showinfo("Success", "Username updated successfully!", parent=dialog)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to update username in the database.", parent=dialog)

        except Exception as err:
            print(f"An error occurred in SettingsUI: {err}")
            messagebox.showerror("Error", f"An unexpected error occurred: {err}", parent=dialog)
