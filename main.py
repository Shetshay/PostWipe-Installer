import tkinter as tk
from tkinter import ttk, messagebox, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fresh Wipe App Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Set background image
        self.set_background()

        # OS Selection Screen
        self.show_os_selection()

    def set_background(self):
        """Set a background image for the app."""
        try:
            self.bg_image = Image.open("background.jpg")  # Replace with your background image
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.background_label = ttk.Label(self.root, image=self.bg_photo)
            self.background_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

    def show_os_selection(self):
        """Display the OS selection screen."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a label
        self.label = ttk.Label(self.root, text="Select Your Operating System", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Load macOS image
        try:
            self.mac_image = Image.open("mac.ico")  # Replace with your macOS icon path
            self.mac_image = self.mac_image.resize((32, 32), 0)  # Resize the image
            self.mac_photo = ImageTk.PhotoImage(self.mac_image)
        except Exception as e:
            print(f"Error loading macOS image: {e}")
            self.mac_photo = None

        # Add macOS button with image
        self.mac_button = ttk.Button(
            self.root,
            text="macOS",
            image=self.mac_photo,
            compound="left",  # Place image to the left of the text
            command=lambda: self.show_categories("macOS")
        )
        self.mac_button.pack(pady=10)

        # Load windows image
        try:
            self.windows_image = Image.open("windows.ico")  # Replace with your macOS icon path
            self.windows_image = self.windows_image.resize((32, 32), 0)  # Resize the image
            self.windows_photo = ImageTk.PhotoImage(self.windows_image)
        except Exception as e:
            print(f"Error loading macOS image: {e}")
            self.windows_photo = None

        # Add windows button with image
        self.windows_button = ttk.Button(
            self.root,
            text="Windows",
            image=self.windows_photo,
            compound="left",  # Place image to the left of the text
            command=lambda: self.show_categories("Windows")
        )
        self.windows_button.pack(pady=10)



    def show_categories(self, os_name):
        """Display categories for the selected OS."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add a back button
        self.back_button = ttk.Button(self.root, text="Back", command=self.show_os_selection)
        self.back_button.pack(pady=10, anchor="nw")

        # Add a label for the selected OS
        self.os_label = ttk.Label(self.root, text=f"Selected OS: {os_name}", font=("Helvetica", 14))
        self.os_label.pack(pady=10)

        # Create a scrollable frame for categories
        self.canvas = Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add categories
        self.add_category("Development", os_name, ["VSCode", "PyCharm", "Git"], self.scrollable_frame)
        self.add_category("Browsers", os_name, ["Brave Browser", "LibreWolf"], self.scrollable_frame)
        self.add_category("Social", os_name, ["Discord", "Telegram"], self.scrollable_frame)

    def add_category(self, category_name, os_name, apps, parent_frame):
        """Add a category with apps."""
        category_label = ttk.Label(parent_frame, text=category_name, font=("Helvetica", 12, "bold"))
        category_label.pack(pady=10, anchor="w")

        for app in apps:
            app_button = ttk.Button(parent_frame, text=app, command=lambda a=app: self.download_app(a, os_name))
            app_button.pack(pady=5, anchor="w")

    def download_app(self, app_name, os_name):
        """Simulate downloading an app based on the OS."""
        file_extension = ".dmg" if os_name == "macOS" else ".exe"
        messagebox.showinfo("Download", f"Downloading {app_name} for {os_name} as {app_name}{file_extension}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()