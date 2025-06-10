import os
import json
import uuid
import customtkinter as ctk
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def generate_uuid(search=None, replace=None, capitalize=False):
    if capitalize:
        return str(uuid.uuid4()).upper()
    if search and replace is not None:
        return str(uuid.uuid4()).replace(search, replace)
    return str(uuid.uuid4())

def reset_windsurf():
    home = os.path.expanduser("~")
    windsurf = os.path.join(home, r'AppData\Roaming\Windsurf\User\globalStorage\storage.json')

    try:
        with open(windsurf, 'r', encoding="UTF-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Error: Windsurf not found."
    
    data["telemetry.machineId"] = os.urandom(32).hex()
    data["telemetry.macMachineId"] = os.urandom(32).hex()
    # data["telemetry.sqmId"] = "{" + generate_uuid(capitalize=True) + "}"
    data["telemetry.devDeviceId"] = os.urandom(32).hex()

    try:
        with open(windsurf, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return True, "Windsurf has been reset successfully!"
    except Exception as e:
        return False, f"Error: Reset interrupted."
    
def reset_cursor():
    home = os.path.expanduser("~")
    cursor = os.path.join(home, r'AppData\Roaming\Cursor\User\globalStorage\storage.json')

    try:
        with open(cursor, 'r', encoding="UTF-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Error: Cursor not found."

    data["telemetry.macMachineId"] = generate_uuid(search="-", replace="") + generate_uuid(search="-", replace="")
    data["telemetry.machineId"] = generate_uuid(search="-", replace="") + generate_uuid(search="-", replace="")
    data["telemetry.sqmId"] = "{" + generate_uuid(capitalize=True) + "}"
    data["telemetry.devDeviceId"] = generate_uuid()

    try:
        with open(cursor, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return True, "Cursor has been reset successfully!"
    except Exception as e:
        return False, f"Error: Reset interrupted."

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Resetter")
        self.geometry("370x370")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.iconbitmap(resource_path("reset.ico"))
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Resetter",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 5))
        
        self.author_label = ctk.CTkLabel(
            self.main_frame, 
            text="by OwPor",
            font=ctk.CTkFont(size=14)
        )
        self.author_label.grid(row=1, column=0, padx=20, pady=(0, 25))
        
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color=("#e3e3e3", "#2a2a2a"), corner_radius=10)
        self.info_frame.grid(row=2, column=0, padx=30, pady=10, sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)
        
        self.description = ctk.CTkLabel(
            self.info_frame,
            text="This application resets IDs of Cursor and Windsurf.",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.description.grid(row=0, column=0, padx=20, pady=15)
        
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.status_frame.grid(row=3, column=0, padx=20, pady=(15, 5), sticky="ew")
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready to reset",
            font=ctk.CTkFont(size=14),
            text_color=("#8a8a8a", "#b0b0b0")
        )
        self.status_label.grid(row=0, column=0)
        
        self.reset_option = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Windsurf", "Cursor"],
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10
        )
        self.reset_option.grid(row=4, column=0, padx=30, pady=(15, 10))
        
        self.reset_button = ctk.CTkButton(
            self.main_frame,
            text="Reset ID",
            command=self.confirm_reset,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            hover_color=("#3a7ebf", "#1f538d")
        )
        self.reset_button.grid(row=5, column=0, padx=30, pady=(10, 30))
    
    def confirm_reset(self):
        """Show confirmation dialog before resetting"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmation")
        dialog.geometry("300x180")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.after(201, lambda :dialog.iconbitmap(resource_path("reset.ico")))
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_columnconfigure(1, weight=1)
        
        message_label = ctk.CTkLabel(
            dialog,
            text=f"Do you want to reset the {self.reset_option.get()} IDs?",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=350
        )
        message_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(25, 20))
        
        note_label = ctk.CTkLabel(
            dialog,
            text="This will reset IDs and cannot be undone.",
            font=ctk.CTkFont(size=12),
            text_color=("#8a8a8a", "#b0b0b0")
        )
        note_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20))
        
        def on_yes():
            dialog.destroy()
            self.perform_reset()
        
        def on_no():
            dialog.destroy()
        
        no_button = ctk.CTkButton(
            dialog,
            text="No",
            command=on_no,
            fg_color=("#e3e3e3", "#2a2a2a"),
            text_color=("black", "white"),
            hover_color=("#d5d5d5", "#3a3a3a"),
            width=100
        )
        no_button.grid(row=2, column=0, padx=(20, 10), pady=20)
        
        yes_button = ctk.CTkButton(
            dialog,
            text="Yes",
            command=on_yes,
            width=100
        )
        yes_button.grid(row=2, column=1, padx=(10, 20), pady=20)
    
    def perform_reset(self):
        """Execute the reset operation and show result"""
        if self.reset_option.get() == "Windsurf":
            success, message = reset_windsurf()
        else:
            success, message = reset_cursor()
        
        if success:
            self.status_label.configure(text=message, text_color=("#4CAF50", "#4CAF50"))
            self.show_success_dialog(message)
        else:
            self.status_label.configure(text=message, text_color=("#F44336", "#F44336"))
            self.show_error_dialog(message)
    
    def show_success_dialog(self, message):
        """Display success confirmation dialog"""
        success_dialog = ctk.CTkToplevel(self)
        success_dialog.title("Success")
        success_dialog.geometry("300x180")
        success_dialog.transient(self)
        success_dialog.grab_set()
        success_dialog.grid_columnconfigure(0, weight=1)
        success_dialog.resizable(False, False)
        success_dialog.after(201, lambda :success_dialog.iconbitmap(resource_path("reset.ico")))
        success_dialog.update_idletasks()
        width = success_dialog.winfo_width()
        height = success_dialog.winfo_height()
        x = (success_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (success_dialog.winfo_screenheight() // 2) - (height // 2)
        success_dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        success_icon = ctk.CTkLabel(
            success_dialog,
            text="✓",
            font=ctk.CTkFont(size=40),
            text_color="#4CAF50"
        )
        success_icon.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        success_message = ctk.CTkLabel(
            success_dialog,
            text=message,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=300
        )
        success_message.grid(row=1, column=0, padx=20, pady=10)
        
        ok_button = ctk.CTkButton(
            success_dialog,
            text="OK",
            command=success_dialog.destroy,
            width=100
        )
        ok_button.grid(row=2, column=0, padx=20, pady=20)
    
    def show_error_dialog(self, message):
        """Display error dialog"""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x180")
        error_dialog.transient(self)
        error_dialog.grab_set()
        error_dialog.grid_columnconfigure(0, weight=1)
        error_dialog.resizable(False, False)
        error_dialog.after(201, lambda :error_dialog.iconbitmap(resource_path("reset.ico")))
        error_dialog.update_idletasks()
        width = error_dialog.winfo_width()
        height = error_dialog.winfo_height()
        x = (error_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (error_dialog.winfo_screenheight() // 2) - (height // 2)
        error_dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        error_icon = ctk.CTkLabel(
            error_dialog,
            text="✗",
            font=ctk.CTkFont(size=40),
            text_color="#F44336"
        )
        error_icon.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        error_message = ctk.CTkLabel(
            error_dialog,
            text=message,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=350
        )
        error_message.grid(row=1, column=0, padx=20, pady=10)
        
        ok_button = ctk.CTkButton(
            error_dialog,
            text="OK",
            command=error_dialog.destroy,
            width=100
        )
        ok_button.grid(row=2, column=0, padx=20, pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()