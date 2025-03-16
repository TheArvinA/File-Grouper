import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog

def get_creation_date(file_path):
    """Returns the creation date of a file."""
    timestamp = os.path.getctime(file_path)
    return datetime.fromtimestamp(timestamp)

def organize_files_by_type_and_date(directory):
    """Scans a directory and sorts files by type and creation date."""
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
            
            os.makedirs(age_folder_path, exist_ok=True)
            
            # Move file to the appropriate folder
            destination = os.path.join(age_folder_path, file)
            shutil.move(file_path, destination)
            print(f"Moved: {file} -> {destination}")
    
    print("Sorting complete!")

def select_directory():
    """Opens a file dialog to select a directory without requiring Tkinter's main loop."""
    directory = filedialog.askdirectory(title="Select a Directory to Organize")
    if directory:
        organize_files_by_type_and_date(directory)

# Run the directory selection
select_directory()
