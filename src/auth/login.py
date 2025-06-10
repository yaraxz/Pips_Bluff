from tkinter import messagebox
import tkinter as tk
from database.db_operations import DBOperations
from security import verify_password


class Login:
    def __init__(self):
        self.db = DBOperations()

    def authenticate(self, username, password):
        if not username or not password:
            return False, "Username and password are required"  # Always return tuple

        # Get user including the hashed password
        user = self.db.get_user_by_username(username)

        if not user:
            return False, "Invalid username or password"  # Return tuple

        # Verify the password against the hash
        if verify_password(password, user['password_hash']):
            return True, "Login successful"  # Success tuple
        return False, "Invalid username or password"  # Failure tuple

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, message = self.login_handler.authenticate(username, password)

        if success:
            messagebox.showinfo("Success", message)
            self.show_dashboard(username)
        else:
            messagebox.showerror("Error", message)

    def show_dashboard(self, username):
        from ui.dashboard_ui import DashboardUI
        self.root.destroy()
        root = tk.Tk()
        DashboardUI(root, username)
        root.mainloop()