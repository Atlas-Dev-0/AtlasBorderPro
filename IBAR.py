import os
import shutil
from PIL import Image


class Landscape:
    def __init__(self, width, height, resolution, folder_path, border_path, processed_path, Border_Complete_Path):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.folder_path = folder_path
        self.AYFO_BORDER = border_path
        self.processed_path = processed_path
        self.Border_Complete_Path = Border_Complete_Path


class Portrait:
    def __init__(self, width, height, resolution, folder_path, border_path, processed_path, Border_Complete_Path):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.folder_path = folder_path
        self.AYFO_BORDER = border_path
        self.processed_path = processed_path
        self.Border_Complete_Path = Border_Complete_Path


Dim_Landscape = Landscape(36, 24, 240, r'Photos_Here\Seperated\landscape',
                          r'AYFO_BORDER\AYFP-WATERMARK-LANDSCAPE.png', r'Photos_Here\Seperated\landscape\processed', r'Photos_Here\Seperated\Landscape\Border_Done')
Dim_Portrait = Portrait(24, 36, 240, r'Photos_Here\Seperated\portrait',
                        r'AYFO_BORDER\AYFP-WATERMARK-PORTRAIT.png', r'Photos_Here\Seperated\portrait\processed', r'Photos_Here\Seperated\portrait\Border_Done')


def resize_images_in_folder(folder_path, width, height, resolution):
    # Create the output folder if it doesn't exist
    output_folder = os.path.join(folder_path, 'processed')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.JPEG') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                resize_image(image_path, output_path,
                             width, height, resolution)
            except Exception as e:
                print(f"Error processing image {filename}: {str(e)}")


def resize_image(image_path, output_path, width, height, resolution):
    print("[imageResizer] Processing:", image_path)
    try:
        image = Image.open(image_path)
    except Image.UnidentifiedImageError as e:
        print(f"Error opening image {image_path}: {str(e)}")
        return

    image_width, image_height = image.size

    # Calculate the desired width and height in pixels
    desired_width = int(width * resolution)
    desired_height = int(height * resolution)

    # Calculate the aspect ratios
    image_aspect_ratio = image_width / image_height
    desired_aspect_ratio = desired_width / desired_height

    if image_aspect_ratio > desired_aspect_ratio:
        # The image is wider than desired, crop the sides
        new_width = int(image_aspect_ratio * desired_height)
        resized_image = image.resize(
            (new_width, desired_height), Image.LANCZOS)
        left = (new_width - desired_width) / 2
        right = new_width - left
        cropped_image = resized_image.crop((left, 0, right, desired_height))
    else:
        # The image is taller than desired, crop the top and bottom
        new_height = int(desired_width / image_aspect_ratio)
        resized_image = image.resize(
            (desired_width, new_height), Image.LANCZOS)
        top = (new_height - desired_height) / 2
        bottom = new_height - top
        cropped_image = resized_image.crop((0, top, desired_width, bottom))

    try:
        # Save the resized and cropped image with the desired resolution
        cropped_image.save(output_path, dpi=(resolution, resolution))
        print("[imageResizer] Saved:", output_path)
    except Exception as e:
        print(f"Error saving image {output_path}: {str(e)}")


def Image_Seperation(source_photo_folder):
    source_folder = source_photo_folder
    destination_folder = os.path.join(os.getcwd(), "Photos_Here", "Seperated")

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Get the list of files in the source folder
    files = os.listdir(source_folder)

    # Iterate through each file
    for file_name in files:
        # Get the full path of the file
        file_path = os.path.join(source_folder, file_name)

        # Check if the file is a directory or not an image
        if not os.path.isfile(file_path) or not file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            # Open the image using PIL
            image = Image.open(file_path)

            # Determine the orientation of the image based on pixel sizes
            # Get the orientation (if available)
            if "exif" in image.info:
                exif_data = image._getexif()
                if exif_data is not None:
                    image_orientation = exif_data.get(274)
                    if orientation is not None:
                        width, height = image.size
                        if image_orientation == 1:
                            if width > height:
                                print("Image orientation: Landscape")
                                orientation = landscape
                            else:
                                print("Image orientation: Portrait")
                                orientation = portrait
                        elif image_orientation == 6:
                            orientation = portrait
                            print("Image orientation: Portrait")
                        else:
                            print("Image orientation: Unknown")

            # Create the destination folder for the image orientation if it doesn't exist
            orientation_folder = os.path.join(destination_folder, orientation)
            os.makedirs(orientation_folder, exist_ok=True)

            # Copy the image to the appropriate folder
            destination_path = os.path.join(orientation_folder, file_name)
            shutil.copy2(file_path, destination_path)

            print(f"Image '{file_name}' copied to '{orientation}' folder.")

        except FileNotFoundError:
            print(f"File not found: '{file_name}'")
        except PIL.UnidentifiedImageError:
            print(f"Unidentified image: '{file_name}'")
        except Exception as e:
            print(f"Error processing '{file_name}': {e}")

    print("Image separation completed.")


def delete_images_in_folder(folder_path):
    if os.path.exists(folder_path):
        print("Path: " + folder_path + " exists")
        # Iterate over the files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.JPEG') or filename.endswith('.png'):
                file_path = os.path.join(folder_path, filename)
                try:
                    # Delete the file
                    os.remove(file_path)
                    print("Deleted:", file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {str(e)}")
    else:
        print("Path: " + folder_path + " Doesn't exists")
        pass


def copy_processed_images(processed_folder_path, destination_folder_path):
    # Get the list of files in the processed folder
    files = os.listdir(processed_folder_path)

    # Iterate over each file in the processed folder
    for filename in files:
        file_path = os.path.join(processed_folder_path, filename)
        destination_path = os.path.join(destination_folder_path, filename)

        try:
            # Move the processed image file to the destination folder
            shutil.move(file_path, destination_path)
            print("Moved:", destination_path)
        except Exception as e:
            print(
                f"Error moving file {file_path} to {destination_path}: {str(e)}")


# OverLay Border
def Add_Border_To_Images(image_folder, border_file):
    # Path to the folder where modified images will be saved
    output_folder = os.path.join(image_folder, "Border_Done")
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each image file in the folder
    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG')):
            # Load the image
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)

            # Load the border and resize it to match the image dimensions
            border = Image.open(border_file)
            border = border.resize(image.size)

            # Create a new image with the border
            bordered_image = Image.new("RGB", image.size)
            bordered_image.paste(image, (0, 0))
            bordered_image.paste(border, (0, 0), mask=border)

            # Save the modified image in the output folder
            output_path = os.path.join(output_folder, filename)
            bordered_image.save(output_path)
            print(f"Added border to: {filename}")

    print("Border addition complete!")


def delete_all_folders(folder_path):
    if os.path.exists(folder_path):
        try:
            # Iterate over the contents of the folder
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    try:
                        # Delete the directory and its contents recursively
                        shutil.rmtree(item_path)
                        print("Deleted folder:", item_path)
                    except Exception as e:
                        print(f"Error deleting folder {item_path}: {str(e)}")
                else:
                    pass
        except Exception as e:
            print(f"Error deleting folder: {str(e)}")
    else:
        pass


def Run_IBAR():
    # Variables
    source_photo_folder = os.path.join(os.getcwd(), "Photos_Here")

    # Main code of your program goes here
    print("AYFO - Image Border Applier and Resizer")
    print("[IBAR] - Proccess Starting")
    print("[IBAR] - Image Seperation begining")
    Image_Seperation(source_photo_folder)

    print("[IBAR] RESIZING IMAGES ON PROCESS.")

    if os.path.exists(Dim_Landscape.folder_path):
        # Process Landscape
        resize_images_in_folder(
            Dim_Landscape.folder_path, Dim_Landscape.width, Dim_Landscape.height, Dim_Landscape.resolution)
        delete_images_in_folder(Dim_Landscape.folder_path)
        copy_processed_images(Dim_Landscape.processed_path,
                              Dim_Landscape.folder_path)
        Add_Border_To_Images(Dim_Landscape.folder_path,
                             Dim_Landscape.AYFO_BORDER)
        delete_images_in_folder(Dim_Landscape.folder_path)
        copy_processed_images(Dim_Landscape.Border_Complete_Path,
                              Dim_Landscape.folder_path)
        delete_all_folders(Dim_Landscape.folder_path)

    else:
        pass

    if os.path.exists(Dim_Portrait.folder_path):
        # Process Portrait
        resize_images_in_folder(Dim_Portrait.folder_path, Dim_Portrait.width,
                                Dim_Portrait.height, Dim_Portrait.resolution)
        delete_images_in_folder(Dim_Portrait.folder_path)
        copy_processed_images(Dim_Portrait.processed_path,
                              Dim_Portrait.folder_path)
        Add_Border_To_Images(Dim_Portrait.folder_path,
                             Dim_Portrait.AYFO_BORDER)
        delete_images_in_folder(Dim_Portrait.folder_path)
        copy_processed_images(Dim_Portrait.Border_Complete_Path,
                              Dim_Portrait.folder_path)
        delete_all_folders(Dim_Portrait.folder_path)

    else:
        pass


# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    Run_IBAR()