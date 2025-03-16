import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from datetime import datetime, timedelta

class FileGrouperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated File Grouper")
        self.root.geometry("500x350")
        self.root.configure(bg="#2C2F33")  # Dark grey background
        
        # Style Configuration
        self.style = tb.Style()
        
        # Main Frame
        self.main_frame = tb.Frame(self.root, bootstyle="dark")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.label = tb.Label(self.main_frame, text="Select a Directory to Organize", font=("Helvetica", 14), background="#2C2F33", foreground="white")
        self.label.pack(pady=10)
        
        self.select_button = tb.Button(self.main_frame, text="Choose Folder", bootstyle="primary", command=self.select_directory)
        self.select_button.pack(pady=10)
        
        self.dry_run_button = tb.Button(self.main_frame, text="Run Dry Run", bootstyle="warning", command=self.run_dry_run)
        self.dry_run_button.pack(pady=10)
        
        self.apply_button = tb.Button(self.main_frame, text="Apply Sorting", bootstyle="success", command=self.apply_sorting_direct)
        self.apply_button.pack(pady=10)
    
    def select_directory(self):
        self.selected_directory = filedialog.askdirectory()
        if self.selected_directory:
            self.label.config(text=f"Selected: {self.selected_directory}")
    
    def run_dry_run(self):
        if not hasattr(self, 'selected_directory') or not self.selected_directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return
        
        file_groups = self.simulate_sorting(self.selected_directory)
        self.show_dry_run_results(file_groups)
    
    def simulate_sorting(self, directory):
        six_months_ago = datetime.now() - timedelta(days=180)
        file_groups = {}
        
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                file_type = file.split('.')[-1] if '.' in file else "Unknown"
                created_time = datetime.fromtimestamp(os.path.getctime(file_path))
                age_group = "Recent" if created_time > six_months_ago else "Old"
                folder_name = f"{file_type}_{age_group}"
                
                if folder_name not in file_groups:
                    file_groups[folder_name] = []
                file_groups[folder_name].append(file)
        
        return file_groups
    
    def show_dry_run_results(self, file_groups):
        result_window = tk.Toplevel(self.root)
        result_window.title("Dry Run Results")
        result_window.geometry("450x400")
        result_window.configure(bg="#23272A")  # Dark grey background for dry run window
        
        result_label = tb.Label(result_window, text=f"The following folders will be created in\n{self.selected_directory}", font=("Helvetica", 12), background="#23272A", foreground="white")
        result_label.pack(pady=10)
        
        for folder, files in file_groups.items():
            folder_label = tb.Label(result_window, text=folder, font=("Helvetica", 10, "bold"), background="#23272A", foreground="lightgray")
            folder_label.pack(anchor="w", padx=10)
            
            for file in files:
                file_label = tb.Label(result_window, text=f"  - {file}", font=("Helvetica", 9), background="#23272A", foreground="white")
                file_label.pack(anchor="w", padx=20)
        
        apply_button = tb.Button(result_window, text="Apply Sorting", bootstyle="success", command=lambda: self.apply_sorting(file_groups, result_window))
        apply_button.pack(pady=10)
    
    def apply_sorting(self, file_groups, window):
        for folder, files in file_groups.items():
            folder_path = os.path.join(self.selected_directory, folder)
            os.makedirs(folder_path, exist_ok=True)
            
            for file in files:
                src_path = os.path.join(self.selected_directory, file)
                dst_path = os.path.join(folder_path, file)
                shutil.move(src_path, dst_path)
        
        messagebox.showinfo("Success", "Files have been sorted successfully.")
        window.destroy()
    
    def apply_sorting_direct(self):
        if not hasattr(self, 'selected_directory') or not self.selected_directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return
        
        file_groups = self.simulate_sorting(self.selected_directory)
        self.apply_sorting(file_groups, self.root)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = FileGrouperApp(root)
    root.mainloop()
