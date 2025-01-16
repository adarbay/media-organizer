import os
import shutil
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image
import cv2

def organize_media():
    # Open folder selection dialog
    folder = filedialog.askdirectory(title="Select Folder to Organize Media")
    if not folder:
        return

    # Define folder structure
    pictures_folder = os.path.join(folder, "pictures")
    vertical_pics_folder = os.path.join(pictures_folder, "vertical pics")
    horizontal_pics_folder = os.path.join(pictures_folder, "horizontal pics")

    videos_folder = os.path.join(folder, "videos")
    vertical_videos_folder = os.path.join(videos_folder, "vertical videos")
    horizontal_videos_folder = os.path.join(videos_folder, "horizontal videos")

    # Create folders if they don't exist
    os.makedirs(vertical_pics_folder, exist_ok=True)
    os.makedirs(horizontal_pics_folder, exist_ok=True)
    os.makedirs(vertical_videos_folder, exist_ok=True)
    os.makedirs(horizontal_videos_folder, exist_ok=True)

    # Define valid extensions
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".heic", ".heif"}  # Added iPhone image extensions
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".webm", ".3gp", ".m4v"}  # Added iPhone and camera video extensions

    # Organize media
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)

            # Skip files already in the target folders
            if pictures_folder in file_path or videos_folder in file_path:
                continue

            # Get file extension
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            # Handle images
            if ext in image_extensions:
                try:
                    img = Image.open(file_path)
                    width, height = img.size
                    img.close()
                    if width > height:
                        shutil.move(file_path, os.path.join(horizontal_pics_folder, file))
                    else:
                        shutil.move(file_path, os.path.join(vertical_pics_folder, file))
                except Exception:
                    pass  # Skip if not a valid image file

            # Handle videos
            elif ext in video_extensions:
                try:
                    cap = cv2.VideoCapture(file_path)
                    if not cap.isOpened():
                        continue
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cap.release()
                    if width > height:
                        shutil.move(file_path, os.path.join(horizontal_videos_folder, file))
                    else:
                        shutil.move(file_path, os.path.join(vertical_videos_folder, file))
                except Exception:
                    pass  # Skip if not a valid video file

    messagebox.showinfo("Success", "Media files organized successfully!")

# Create the GUI
root = Tk()
root.title("Media Organizer")
root.geometry("400x200")

label = Label(root, text="Click the button below to organize media files.")
label.pack(pady=20)

button = Button(root, text="Choose Folder and Organize", command=organize_media)
button.pack(pady=20)

root.mainloop()
