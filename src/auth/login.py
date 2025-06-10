from tkinter import messagebox
import tkinter as tk
from database.db_operations import DBOperations
from security import verify_password


class Login:
    def __init__(self):
        # Initialize database operations instance
        self.db = DBOperations()

    def authenticate(self, username, password):
        # Ensure both fields are provided
        if not username or not password:
            return False, "Username and password are required"

        # Retrieve user record by username
        user = self.db.get_user_by_username(username)

        if not user:
            return False, "Invalid username or password"

        # Check entered password against stored hash
        if verify_password(password, user['password_hash']):
            return True, "Login successful"
        return False, "Invalid username or password"

    def login(self):
        # Get user input from entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Attempt authentication using provided credentials
        success, message = self.login_handler.authenticate(username, password)

        if success:
            # Show success message and navigate to dashboard
            messagebox.showinfo("Success", message)
            self.show_dashboard(username)
        else:
            # Show error message on failure
            messagebox.showerror("Error", message)

    def show_dashboard(self, username):
        # Transition to the dashboard interface
        from ui.dashboard_ui import DashboardUI
        self.root.destroy()
        root = tk.Tk()
        DashboardUI(root, username)
        root.mainloop()