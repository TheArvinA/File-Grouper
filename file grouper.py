import os
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext
from datetime import datetime, timedelta
from pathlib import Path

def get_creation_date(file_path):
    """Returns the creation date of a file."""
    timestamp = os.path.getctime(file_path)
    return datetime.fromtimestamp(timestamp)

def organize_files_by_type_and_date(directory, dry_run=True):
    """Scans a directory and sorts files by type and creation date. Supports dry-run mode."""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    # Define file type categories
    file_categories = {
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Videos": [".mp4", ".avi", ".mov", ".mkv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac"],
        "Code": [".py", ".java", ".cpp", ".js", ".html", ".css", ".sh"],
        "Archives": [".zip", ".tar", ".rar", ".7z"],
    }
    
    # Calculate the threshold date (6 months ago)
    six_months_ago = datetime.now() - timedelta(days=180)
    
    # Prepare results for GUI display
    folder_structure = {}
    
    # Process each file in the directory
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        
        if os.path.isfile(file_path):
            file_extension = Path(file).suffix.lower()
            creation_date = get_creation_date(file_path)
            
            # Determine file category
            category = "Other"
            for cat, extensions in file_categories.items():
                if file_extension in extensions:
                    category = cat
                    break
            
            # Determine age-based folder
            age_folder = "Recent" if creation_date >= six_months_ago else "Older"
            
            # Create directories for category and age
            category_folder = os.path.join(directory, category)
            age_folder_path = os.path.join(category_folder, age_folder)
            
            folder_name = os.path.relpath(age_folder_path, directory)
            
            if folder_name not in folder_structure:
                folder_structure[folder_name] = []
            folder_structure[folder_name].append(file)
            
            if not dry_run:
                os.makedirs(age_folder_path, exist_ok=True)
                shutil.move(file_path, os.path.join(age_folder_path, file))
    
    if dry_run:
        display_results_gui(directory, folder_structure)
    else:
        print("Sorting complete!")

def display_results_gui(directory, folder_structure):
    """Displays the dry-run results in a Tkinter GUI window with grouped folders."""
    result_window = tk.Tk()
    result_window.title("Dry Run Results")
    result_window.geometry("600x400")
    
    text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    text_area.insert(tk.INSERT, f"The following folders will be created in {directory} containing your files:\n\n")
    
    for folder, files in folder_structure.items():
        text_area.insert(tk.INSERT, f"Folder: {folder}\n")
        for file in files:
            text_area.insert(tk.INSERT, f"    - {file}\n")
        text_area.insert(tk.INSERT, "\n")
    
    text_area.config(state=tk.DISABLED)  # Make text read-only
    
    close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
    close_button.pack(pady=10)
    
    result_window.mainloop()

def select_directory():
    """Opens a file dialog to select a directory without requiring Tkinter's main loop."""
    directory = filedialog.askdirectory(title="Select a Directory to Organize")
    if directory:
        dry_run_choice = input("Run in dry-run mode? (y/n): ").strip().lower()
        dry_run = dry_run_choice == "y"
        organize_files_by_type_and_date(directory, dry_run)

# Run the directory selection
select_directory()