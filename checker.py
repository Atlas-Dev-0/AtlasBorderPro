from PIL import Image, ExifTags
import os

def check_image_orientation(image_path):
    im = Image.open(image_path)
    orientation_tag = None
    for tag, value in im._getexif().items():
        if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'Orientation':
            orientation_tag = tag
            break
    if orientation_tag is None:
        print(f"{image_path}: Orientation tag not found in EXIF data.")
    else:
        orientation = im._getexif().get(orientation_tag)
        if orientation == 8:
            print(f"{image_path}: Orientation value = {orientation} (Portrait)")
        elif orientation == 1:
            print(f"{image_path}: Orientation value = {orientation} (Landscape)")
        else:
            print(f"{image_path}: Orientation value = {orientation} (Unknown)")

def check_orientation_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):  # Add other image extensions if needed
            image_path = os.path.join(folder_path, filename)
            check_image_orientation(image_path)

# Usage example
folder_path = "Photos_Here"
check_orientation_in_folder(folder_path)
