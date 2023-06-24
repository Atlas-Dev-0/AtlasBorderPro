from PIL import Image
import os

def print_image_orientation(image_path):
    try:
        # Open the image
        image = Image.open(image_path)

        # Get the orientation (if available)
        if "exif" in image.info:
            exif_data = image._getexif()
            if exif_data is not None:
                orientation = exif_data.get(274)
                if orientation is not None:
                    width, height = image.size
                    if orientation == 1:
                        if width > height:
                            print("Image orientation: Landscape")
                        else:
                            print("Image orientation: Portrait")
                    elif orientation == 6:
                        print("Image orientation: Portrait")
                    else:
                        print("Image orientation: Unknown")
                    return

        print("Image orientation: Not available")

    except IOError:
        print("Unable to open image.")

# Provide the folder path containing the images
folder_path = "Photos_Here"

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Construct the full path to the image
        image_path = os.path.join(folder_path, filename)

        # Print the orientation of the image
        print("Image path: ", image_path)
        print_image_orientation(image_path)
        print("-----------------------------------")
