import tkinter as tk
from tkinter import ttk, messagebox, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk
import requests
import os
import threading

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
            self.mac_image = Image.open("icons/mac.ico")  # Replace with your macOS icon path
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

        # Load Windows image
        try:
            self.windows_image = Image.open("icons/windows.ico")  # Replace with your Windows icon path
            self.windows_image = self.windows_image.resize((32, 32), 0)  # Resize the image
            self.windows_photo = ImageTk.PhotoImage(self.windows_image)
        except Exception as e:
            print(f"Error loading Windows image: {e}")
            self.windows_photo = None

        # Add Windows button with image
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

        # Bind mouse scroll event to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Add categories
        if os_name == "Windows":
            self.add_category("File Compressors", os_name, ["NanoZip", "WinRAR", "7-Zip"], self.scrollable_frame)
            self.add_category("Security Apps", os_name, ["Bitwarden", "Windscribe"], self.scrollable_frame)
            self.add_category("Game Launchers", os_name, ["Steam", "Epic Games", "GOG", "Wargaming Game Center"], self.scrollable_frame)
            self.add_category("Dev Tools", os_name, ["NetLimiter", "Notepad++", "PuTTY", "PowerToys", "Process Explorer", "Autoruns"], self.scrollable_frame)
            self.add_category("Social", os_name, ["TeamSpeak"], self.scrollable_frame)
            self.add_category("BAT Files", os_name, ["Restart Audio Service", "Kill Valorant Process"], self.scrollable_frame)
            self.add_category("Overclocking", os_name, [
                "TestMem5", "ZenTimings", "Cinebench R20", "CPU-Z", "HWiNFO", "HWMonitor x64",
                "NVIDIA Profile Inspector", "OCCT", "Prime95", "Timer Resolution", "Timing Configurator v4.0.4",
                "Display Driver Uninstaller (DDU)"
            ], self.scrollable_frame)
        else:
            self.add_category("Development", os_name, ["VSCode", "PyCharm", "Git"], self.scrollable_frame)
            self.add_category("Browsers", os_name, ["Brave Browser", "LibreWolf"], self.scrollable_frame)
            self.add_category("Social", os_name, ["Discord", "Telegram"], self.scrollable_frame)

    def add_category(self, category_name, os_name, apps, parent_frame):
        """Add a category with apps."""
        category_label = ttk.Label(parent_frame, text=category_name, font=("Helvetica", 12, "bold"))
        category_label.pack(pady=10, anchor="w")

        for app in apps:
            # Create a frame for each app
            app_frame = ttk.Frame(parent_frame)
            app_frame.pack(pady=5, anchor="w", fill="x")

            # Load app logo
            try:
                app_logo = Image.open(f"icons/{app.lower().replace(' ', '_')}.ico")  # Replace with your app logo path
                app_logo = app_logo.resize((32, 32), 0)
                app_logo_photo = ImageTk.PhotoImage(app_logo)
            except Exception as e:
                print(f"Error loading {app} logo: {e}")
                app_logo_photo = None

            # Add app button with logo
            app_button = ttk.Button(
                app_frame,
                text=app,
                image=app_logo_photo,
                compound="left",  # Place image to the left of the text
                command=lambda a=app: self.start_download(a, os_name)
            )
            app_button.image = app_logo_photo  # Keep a reference to avoid garbage collection
            app_button.pack(side="left", padx=5)

    def start_download(self, app_name, os_name):
        """Start the download in a separate thread."""
        download_thread = threading.Thread(target=self.download_app, args=(app_name, os_name))
        download_thread.start()

    def download_app(self, app_name, os_name):
        """Download an app dynamically based on the OS."""
        # Define the download URLs for each app
        app_urls = {
            "Brave Browser": {
                "macOS": "https://referrals.brave.com/latest/Brave-Browser.dmg",
                "Windows": "https://referrals.brave.com/latest/Brave-Browser-Setup.exe"
            },
            "Discord": {
                "macOS": "https://discord.com/api/downloads/discord-canary?platform=osx",
                "Windows": "https://discord.com/api/downloads/discord-canary?platform=win"
            },
            "VSCode": {
                "macOS": "https://code.visualstudio.com/sha/download?build=stable&os=darwin",
                "Windows": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
            },
            "PyCharm": {
                "macOS": "https://download.jetbrains.com/python/pycharm-professional-2023.2.2.dmg",
                "Windows": "https://download.jetbrains.com/python/pycharm-professional-2023.2.2.exe"
            },
            "LibreWolf": {
                "macOS": "https://gitlab.com/api/v4/projects/24386000/packages/generic/LibreWolf/117.0.1-1/LibreWolf.dmg",
                "Windows": "https://gitlab.com/api/v4/projects/24386000/packages/generic/LibreWolf/117.0.1-1/LibreWolf_Setup.exe"
            },
            "Telegram": {
                "macOS": "https://osx.telegram.org/updates/Telegram.dmg",
                "Windows": "https://telegram.org/dl/desktop/win"
            },
            "NanoZip": {
                "Windows": "https://www.nanozip.net/download/nanozip64.exe"
            },
            "WinRAR": {
                "Windows": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-623.exe"
            },
            "7-Zip": {
                "Windows": "https://www.7-zip.org/a/7z2301-x64.exe"
            },
            "Bitwarden": {
                "Windows": "https://vault.bitwarden.com/download/?app=desktop&platform=windows"
            },
            "Windscribe": {
                "Windows": "https://windscribe.com/install/desktop/Windscribe_2.6.12.exe"
            },
            "Steam": {
                "Windows": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe"
            },
            "Epic Games": {
                "Windows": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi"
            },
            "GOG": {
                "Windows": "https://www.gog.com/downloader2/galaxy_client_2.0.exe"
            },
            "Wargaming Game Center": {
                "Windows": "https://wgc.wargaming.net/WGC_World_of_Warships_NA.exe"
            },
            "NetLimiter": {
                "Windows": "https://www.netlimiter.com/download/nl5setup.exe"
            },
            "Notepad++": {
                "Windows": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.4/npp.8.5.4.Installer.x64.exe"
            },
            "PuTTY": {
                "Windows": "https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.78-installer.msi"
            },
            "PowerToys": {
                "Windows": "https://github.com/microsoft/PowerToys/releases/download/v0.68.1/PowerToysSetup-0.68.1-x64.exe"
            },
            "Process Explorer": {
                "Windows": "https://download.sysinternals.com/files/ProcessExplorer.zip"
            },
            "Autoruns": {
                "Windows": "https://download.sysinternals.com/files/Autoruns.zip"
            },
            "TeamSpeak": {
                "Windows": "https://files.teamspeak-services.com/releases/client/3.6.1/TeamSpeak3-Client-win64-3.6.1.exe"
            },
            "Restart Audio Service": {
                "Windows": "restart_audio.bat"
            },
            "Kill Valorant Process": {
                "Windows": "kill_valorant.bat"
            },
            "TestMem5": {
                "Windows": "https://testmem5.com/download/TestMem5.zip"
            },
            "ZenTimings": {
                "Windows": "https://zentimings.pro/download/ZenTimings.zip"
            },
            "Cinebench R20": {
                "Windows": "https://cinebench.com/download/CinebenchR20.zip"
            },
            "CPU-Z": {
                "Windows": "https://cpuid.com/downloads/cpu-z/cpu-z_2.00-en.exe"
            },
            "HWiNFO": {
                "Windows": "https://www.hwinfo.com/download/hwi_716.exe"
            },
            "HWMonitor x64": {
                "Windows": "https://www.cpuid.com/downloads/hwmonitor/hwmonitor_1.45.exe"
            },
            "NVIDIA Profile Inspector": {
                "Windows": "https://github.com/Orbmu2k/nvidiaProfileInspector/releases/download/2.4.0.3/nvidiaProfileInspector.zip"
            },
            "OCCT": {
                "Windows": "https://www.ocbase.com/download/OCCT.zip"
            },
            "Prime95": {
                "Windows": "https://www.mersenne.org/download/prime95.zip"
            },
            "Timer Resolution": {
                "Windows": "https://timerresolution.com/download/TimerResolution.zip"
            },
            "Timing Configurator v4.0.4": {
                "Windows": "https://timingconfigurator.com/download/TimingConfigurator_v4.0.4.zip"
            },
            "Display Driver Uninstaller (DDU)": {
                "Windows": "https://www.wagnardsoft.com/download/DDU_v18.1.0.0.exe"
            }
        }

        # Get the download URL for the selected app and OS
        if app_name in app_urls:
            url = app_urls[app_name].get(os_name)
            if url:
                try:
                    # Handle BAT files
                    if app_name in ["Restart Audio Service", "Kill Valorant Process"]:
                        self.create_bat_file(app_name, url)
                        messagebox.showinfo("BAT File Created", f"{app_name} BAT file has been created.")
                        return

                    # Start the download
                    response = requests.get(url, stream=True)
                    response.raise_for_status()  # Raise an error for bad status codes

                    # Determine the file extension
                    file_extension = ".dmg" if os_name == "macOS" else ".exe"
                    download_path = os.path.join(os.path.expanduser("~"), "Downloads", f"{app_name}{file_extension}")

                    # Save the file
                    with open(download_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)

                    messagebox.showinfo("Download Complete", f"{app_name} has been downloaded to {download_path}.")
                except Exception as e:
                    messagebox.showerror("Download Failed", f"Failed to download {app_name}: {e}")
            else:
                messagebox.showerror("Error", f"No download link found for {app_name} on {os_name}.")
        else:
            messagebox.showerror("Error", f"{app_name} is not supported for automatic download.")

    def create_bat_file(self, app_name, url):
        """Create a BAT file for Windows utilities."""
        bat_content = ""
        if app_name == "Restart Audio Service":
            bat_content = 'powershell -Command "Restart-Service -Name \'AudioSrv\' -Force"'
        elif app_name == "Kill Valorant Process":
            bat_content = '@echo off\npowershell -Command "Get-Process | Where-Object { $_.Name -eq \'VALORANT-Win64-Shipping\' } | Stop-Process -Force"'

        if bat_content:
            bat_path = os.path.join(os.path.expanduser("~"), "Downloads", f"{app_name}.bat")
            with open(bat_path, "w") as bat_file:
                bat_file.write(bat_content)

    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()