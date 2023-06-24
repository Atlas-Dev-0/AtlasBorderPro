import os
import sys
import shutil
from PIL import Image, ExifTags, ImageOps

# Code Written and Compiled by Kenneth Gonzales

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS    
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class Landscape:
    def __init__(self, width, height, resolution, folder_path, border_path, processed_path, Border_Complete_Path):
        if None in (width, height, resolution, folder_path, border_path, processed_path, Border_Complete_Path):
            raise ValueError("One or more parameters are missing in Landscape.")
        
        self.width = width
        self.height = height
        self.resolution = resolution
        self.folder_path = folder_path
        self.AYFO_BORDER = border_path
        self.processed_path = processed_path
        self.Border_Complete_Path = Border_Complete_Path


class Portrait:
    def __init__(self, width, height, resolution, folder_path, border_path, processed_path, Border_Complete_Path):
        if None in (width, height, resolution, folder_path, border_path, processed_path, Border_Complete_Path):
            raise ValueError("One or more parameters are missing in Portrait.")
        
        self.width = width
        self.height = height
        self.resolution = resolution
        self.folder_path = folder_path
        self.AYFO_BORDER = border_path
        self.processed_path = processed_path
        self.Border_Complete_Path = Border_Complete_Path

Dim_Landscape = Landscape(36, 24, 240, r'Photos_Here/Seperated/Landscape',resource_path('AYFO_BORDERS/AYFP-WATERMARK-LANDSCAPE.png'), r'Photos_Here/Seperated/Landscape/processed', r'Photos_Here/Seperated/Landscape/Border_Done')
Dim_Portrait = Portrait(24, 36, 240, r'Photos_Here/Seperated/Portrait',resource_path('AYFO_BORDERS/AYFP-WATERMARK-PORTRAIT.png'), r'Photos_Here/Seperated/Portrait/processed', r'Photos_Here/Seperated/Portrait/Border_Done')


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
                resize(image_path, output_path, width, height, resolution)
                print(f"Resizing Image that has {width} x {height} ")
            except FileNotFoundError as e:
                print(f"Error: File not found {image_path}: {str(e)}")
            except Exception as e:
                print(f"Error processing image {filename}: {str(e)}")


def resize(image_path, output_path, width, height, resolution):
    print("[imageResizer] Processing:", image_path)

    try:
        image = Image.open(image_path)
    except Image.UnidentifiedImageError as e:
        print(f"Error opening image {image_path}: {str(e)}")
        return

    # Check the image path for orientation information
    if "Landscape" in image_path:
        orientation = "Landscape"
    elif "Portrait" in image_path:
        orientation = "Portrait"
    else:
        # Check the EXIF metadata for the orientation tag
        if hasattr(image, '_getexif') and image._getexif() is not None:
            exif_data = image._getexif()
            orientation = exif_data.get(0x0112)

            # Rotate the image based on the orientation tag
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(-90, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)

    # Force the image to be in the correct orientation (if it's not a landscape image)
    if not ("Landscape" in image_path):
        if image.width > image.height:
            image = image.transpose(Image.ROTATE_90)

    desired_width = int(width * resolution)
    desired_height = int(height * resolution)

    # Determine the aspect ratio of the desired dimensions and the original image
    desired_ratio = desired_width / desired_height
    original_ratio = image.width / image.height

    if desired_ratio > original_ratio:
        # Crop horizontally
        new_width = int(image.height * desired_ratio)
        left = (image.width - new_width) // 2
        right = left + new_width
        image = image.crop((left, 0, right, image.height))
    elif desired_ratio < original_ratio:
        # Crop vertically
        new_height = int(image.width / desired_ratio)
        top = (image.height - new_height) // 2
        bottom = top + new_height
        image = image.crop((0, top, image.width, bottom))

    try:
        # Resize the image to the desired dimensions
        resized_image = image.resize((desired_width, desired_height), resample=Image.LANCZOS)

        resized_image.info['dpi'] = (resolution, resolution)
        # Save the resized image with the desired resolution
        resized_image.save(output_path, dpi=(resolution, resolution))
        print("[imageResizer] Saved:", output_path)
    except Exception as e:
        print(f"Error saving image {output_path}: {str(e)}")

def Image_Seperation(source_photo_folder):
    source_folder = source_photo_folder
    destination_folder = os.path.join(os.getcwd(), "Photos_Here", "Seperated")
    image_path = source_photo_folder

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Get the list of files in the source folder
    files = os.listdir(source_folder)

    # Iterate through each file
    for file_name in files:
        # Get the full path of the file
        file_path = os.path.join(source_folder, file_name)

        # Check if the file is a directory or not an image
        if not os.path.isfile(file_path) or not file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG')):
            continue

        try:
            # Open the image using PIL
            image = Image.open(file_path)
            orientation_tag = None
            for tag, value in image._getexif().items():
                if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'Orientation':
                    orientation_tag = tag
                    break
            if orientation_tag is None:
                print(f"{image_path}: Orientation tag not found in EXIF data.")
            else:
                orientation_number = image._getexif().get(orientation_tag)
                if orientation_number == 8:
                    print(f"{image_path}: Orientation value = {orientation_number} (Portrait)")
                    orientation = "Portrait";
                elif orientation_number == 1:
                    print(f"{image_path}: Orientation value = {orientation_number} (Landscape)")
                    orientation = "Landscape";
                else:
                    print(f"{image_path}: Orientation value = {orientation_number} (Unknown)")
            

            # Create the destination folder for the image orientation if it doesn't exist
            orientation_folder = os.path.join(destination_folder, orientation)
            os.makedirs(orientation_folder, exist_ok=True)

            # Copy the image to the appropriate folder
            destination_path = os.path.join(orientation_folder, file_name)
            shutil.copy2(file_path, destination_path)

            print(f"Image '{file_name}' copied to '{orientation}' folder.")

        except FileNotFoundError:
            print(f"File not found: '{file_name}'")
        except Exception as e:
            print(f"Error processing '{file_name}': {e}")

    print("Image Seperation completed.")


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
    
    try:            
        # Variables
        source_photo_folder = os.path.join(os.getcwd(), "Photos_Here")

        # Main code of your program goes here
        print("AYFO - Image Border Applier and Resizer")
        print("[IBAR] - Process Starting")

        # Check if any parameter is None or empty for Landscape object
        missing_parameters_landscape = [name for name, value in vars(Dim_Landscape).items() if value is None or value == ""]
        if missing_parameters_landscape:
            print("Missing parameters in the Landscape object:")
            for parameter in missing_parameters_landscape:
                print(parameter)
            sys.exit()

        # Check if any parameter is None or empty for Portrait object
        missing_parameters_portrait = [name for name, value in vars(Dim_Portrait).items() if value is None or value == ""]
        if missing_parameters_portrait:
            print("Missing parameters in the Portrait object:")
            for parameter in missing_parameters_portrait:
                print(parameter)
            sys.exit()

        # Image Seperation
        print("[IBAR] - Image Seperation beginning")
        try:
            Image_Seperation(source_photo_folder)
        except Exception as e:
            print("[IBAR] - Error occurred during Image Seperation:", str(e))

        try:
            print("[IBAR - RESIZING] - Resizing Images in process.")
            if os.path.exists(Dim_Landscape.folder_path):
                # Process Landscape
                try:
                    resize_images_in_folder(Dim_Landscape.folder_path, Dim_Landscape.width, Dim_Landscape.height,
                                            Dim_Landscape.resolution)
                except Exception as e:
                    print("[IBAR] - Error occurred during resizing images in the Landscape folder:", str(e))

                try:
                    delete_images_in_folder(Dim_Landscape.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during deletion of images in the Landscape folder:", str(e))

                try:
                    copy_processed_images(Dim_Landscape.processed_path, Dim_Landscape.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during copying processed images to the Landscape folder:", str(e))

                try:
                    Add_Border_To_Images(Dim_Landscape.folder_path, Dim_Landscape.AYFO_BORDER)
                except Exception as e:
                    print("[IBAR] - Error occurred during adding border to images in the Landscape folder:", str(e))

                try:
                    delete_images_in_folder(Dim_Landscape.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during deletion of images in the Landscape folder:", str(e))

                try:
                    copy_processed_images(Dim_Landscape.Border_Complete_Path, Dim_Landscape.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during copying processed border images to the Landscape folder:", str(e))

                try:
                    delete_all_folders(Dim_Landscape.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during deletion of folders in the Landscape folder:", str(e))
            else:
                print(f"[IBAR] - NO LANDSCAPE FOLDER EXISTS!: {Dim_Landscape.folder_path}")
                os.makedirs(Dim_Landscape.folder_path)
                print(f"[IBAR] - Created the folder: {Dim_Landscape.folder_path}")
                print("[IBAR] - Add the files to the folder.")

            if os.path.exists(Dim_Portrait.folder_path):
                # Process Portrait
                try:
                    resize_images_in_folder(Dim_Portrait.folder_path, Dim_Portrait.width, Dim_Portrait.height,
                                            Dim_Portrait.resolution)
                except Exception as e:
                    print("[IBAR] - Error occurred during resizing images in the Portrait folder:", str(e))

                try:
                    delete_images_in_folder(Dim_Portrait.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during deletion of images in the Portrait folder:", str(e))

                try:
                    copy_processed_images(Dim_Portrait.processed_path, Dim_Portrait.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during copying processed images to the Portrait folder:", str(e))

                try:
                    Add_Border_To_Images(Dim_Portrait.folder_path, Dim_Portrait.AYFO_BORDER)
                except Exception as e:
                    print("[IBAR] - Error occurred during adding border to images in the Portrait folder:", str(e))

                try:
                    delete_images_in_folder(Dim_Portrait.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during deletion of images in the Portrait folder:", str(e))

                try:
                    copy_processed_images(Dim_Portrait.Border_Complete_Path, Dim_Portrait.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during copying processed border images to the Portrait folder:", str(e))


                try:
                    delete_all_folders(Dim_Portrait.folder_path)
                except Exception as e:
                    print("[IBAR] - Error occurred during deletion of folders in the Portrait folder:", str(e))
            else:
                print("[IBAR] - NO PORTRAIT FOLDER EXISTS!:")
                os.makedirs(Dim_Portrait.folder_path)
                print(f"[IBAR] - Created the folder: {Dim_Portrait.folder_path}")
                print("[IBAR] - Add the files to the folder.")

        except Exception as e:
            print("[IBAR - RESIZING] - An unexpected error occurred:", str(e))

    except Exception as e:
        print("[IBAR] - An unexpected error occurred:", str(e))
    else:
        print("[IBAR] - Image processing completed.")
        # Add pauses using os
        os.system("pause")
    

# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    Run_IBAR()
    input("Press enter to close program")
    