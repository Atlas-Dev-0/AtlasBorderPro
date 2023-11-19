import os
import sys
import shutil
import ctypes
from PIL import Image, ImageOps

def Instructions():
    print("")
    print("Folders are Now Created and are now ready!")
    print("")
    print("Instructions on Images:")
    print("     1.) Add images in their respective folders, if the image's ortientation is landscape put it in the Landscape folder")
    print("     2.) If the image's orientation is in portrait, put it in the Portrait folder")
    print("     3.) Make sure the image is .jpg")
    print("")
    print("Instructions on Borders:")
    print("     1.) Add the Border in their respective folder, either landscape or portrait")
    print("     2.) Make sure to only put one border per folder")
    print("     3.) Make sure the Border is PNG!")
    print("")
    print("")
    print("")
    input("Press Enter and Restart the program after you added the images..")
    sys.exit()

def add_border(folder_path, png_folder, output_folder):
    try:
        # Get the PNG file from the folder
        png_files = [file for file in os.listdir(png_folder) if file.endswith(".png")]

        # Check if there is only one PNG file
        if len(png_files) != 1:
            raise ValueError("PNG folder must contain only one PNG file.")

        # Set the PNG path to the full path of the PNG file
        png_path = os.path.join(png_folder, png_files[0])

        print(f"Using Border: {png_path}")

        # Load the PNG image
        png_image = Image.open(png_path).convert("RGBA")

        print(f"Loaded Border: {str(png_image)}")

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Loop through each image file in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG')):
                image_path = os.path.join(folder_path, filename)

                # Open the image
                image = Image.open(image_path).convert("RGBA")

                # Resize the PNG image to match the dimensions of the loaded image
                png_resized = png_image.resize(image.size)

                # Create a composite image by overlaying the PNG image on top of the loaded image
                overlay_image = Image.alpha_composite(image, png_resized)

                # Save the composite image as JPEG to the output folder
                output_filename = os.path.splitext(filename)[0] + ".jpg"
                output_path = os.path.join(output_folder, output_filename)
                overlay_image.convert("RGB").save(output_path, "JPEG")

                print(f"Overlay applied: {output_path}")

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

            
def resize_Borders(base_dir):
    # Loop through all files in the base directory
    for filename in os.listdir(base_dir):
        # Check if the file is a PNG image
        if filename.endswith(".png"):
            file_path = os.path.join(base_dir, filename)
            
            # Determine the image dimensions and DPI based on the folder name
            folder_name = os.path.basename(base_dir)
            if folder_name.lower() == "landscape":
                width, height = 36, 24
                dpi = 240
            elif folder_name.lower() == "portrait":
                width, height = 24, 36
                dpi = 240
            else:
                # Skip processing if the folder name doesn't match
                continue
            
            # Open the image using PIL
            image = Image.open(file_path)
            
            # Resize the image
            resized_image = image.resize((width, height))
            
            # Set the DPI
            resized_image.info['dpi'] = (dpi, dpi)
            
            # Save the resized image with the same filename
            resized_image.save(file_path)

def convert(input_folder, output_folder):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Get a list of all files in the input folder
        files = os.listdir(input_folder)
        
        # Loop through each file in the input folder
        for file in files:
            # Check if the file is a JPG image
            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                input_path = os.path.join(input_folder, file)
                output_path = os.path.join(output_folder, file)
                
                # Open the image and apply EXIF rotation correction
                image = Image.open(input_path)
                image = ImageOps.exif_transpose(image)
                
                # Convert the image to regular JPG format
                if image.mode != "RGB":
                    image = image.convert("RGB")
                
                # Save the converted image
                image.save(output_path, "JPEG")
                
                print(f"Image {file} converted successfully! at {output_path}")
        
        print("All images converted successfully!")
        
    except IOError:
        print(f"Failed to convert images in {input_folder}.")

def resize_image(input_path, output_folder, height, width, dpi):
    # Open the image
    image = Image.open(input_path)
    # Calculate the new size in pixels
    desired_width = int(width * dpi)
    desired_height = int(height * dpi)

    try:
        # Resize the image to the desired dimensions
        resized_image = image.resize((desired_width, desired_height), resample=Image.LANCZOS)

        resized_image.info['dpi'] = (dpi, dpi)

        # Save the resized image with the desired resolution inside the output folder
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_folder, filename)
        resized_image.save(output_path, dpi=(dpi, dpi))

        print("[imageResizer] Saved:", output_path)
    except Exception as e:
        print(f"Error saving image {output_path}: {str(e)}")
        
def Resize_Image_Folder(input_folder, output_folder, height, width, dpi): 
    # Convert the images and resize them
    convert(output_folder, input_folder)
     
    # Resize images in the input folder
    image_files = os.listdir(input_folder)
     
    for file in image_files:
        file_path = os.path.join(input_folder, file)
        resize_image(file_path, output_folder, height, width, dpi)
        print(f"[imageResizer] Resized {file} and saved at {output_folder}")      
    
def Run_ABP():
    main_folder = "Files_Here"
    subfolders = ["Borders", "Landscape", "Portrait"]
    Border_path = "Files_Here/Borders"
    border_Subfolders = ["Landscape_Border", "Portrait_Border"]
    print("Checking if Folders needed are present")
    
        
    L_Border = os.path.join(Border_path, border_Subfolders[0])
    P_Border = os.path.join(Border_path, border_Subfolders[1])

    try:
        # Check if the main folder exists
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)
            print(f"Created folder: {main_folder}")
            # Check and create subfolders
            for subfolder in subfolders:
                subfolder_path = os.path.join(main_folder, subfolder)
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                    print(f"Created folder: {subfolder_path}")
                else:
                    print(f"{subfolder_path} Folders Exist")

            for border_subfolder in border_Subfolders:
                subfolder_path = os.path.join(Border_path, border_subfolder)
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                    print(f"Created folder: {subfolder_path}")
                else:
                    print(f"{subfolder_path} Folders Exist")
            Instructions()

        else: 
            print(f"Main Folder Exists")

        # Check and create subfolders
        for subfolder in subfolders:
            subfolder_path = os.path.join(main_folder, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
                print(f"Created folder: {subfolder_path}")
            else:
                print(f"{subfolder_path} Folders Exist")

        for border_subfolder in border_Subfolders:
            subfolder_path = os.path.join(Border_path, border_subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
                print(f"Created folder: {subfolder_path}")
            else:
                print(f"{subfolder_path} Folders Exist")

        for subfolder in subfolders:
            processed_folder_path = os.path.join(main_folder, subfolder, "converted")
            if os.path.exists(processed_folder_path):
                shutil.rmtree(processed_folder_path)
                print("Deleted 'converted' folder")

        # landscape = 36w x 24h
        # portrait = 24w x 36h
        print("Converting Borders")
        resize_Borders("Files_Here/Borders/Landscape_Border")   
        resize_Borders("Files_Here/Borders/Portrait_Border")

        Landscape_Folder_Path = r"Files_Here/Landscape"
        Landscape_Folder_Path_converted = r"Files_Here/Landscape/converted"
        Portrait_Folder_Path = r"Files_Here/Portrait"
        Portrait_Folder_Path_converted = r"Files_Here/Portrait/converted"

        print("Resizing Landscape")
        user_dpi = input("Enter DPI: ")
    
        # Resize Images in Landscape 
        Resize_Image_Folder(Landscape_Folder_Path_converted, Landscape_Folder_Path, 24, 36, user_dpi)

        # Resize Images in Portrait 
        print("Resizing Portrait")
        Resize_Image_Folder(Portrait_Folder_Path_converted, Portrait_Folder_Path, 36, 24, user_dpi)

        for subfolder in subfolders:
            processed_folder_path = os.path.join(main_folder, subfolder, "converted")
            if os.path.exists(processed_folder_path):
                shutil.rmtree(processed_folder_path)
                print("Deleted 'converted' folder")

        try: 
            # Add The Borders to Landscape
            Landscape_Folder_Path_Bordered = os.path.join(Landscape_Folder_Path, "Images_With_Border")
            add_border(Landscape_Folder_Path, L_Border, Landscape_Folder_Path_Bordered)

            # Add The Borders to Portrait
            Portrait_Folder_Path_Bordered = os.path.join(Portrait_Folder_Path, "Images_With_Border")
            add_border(Portrait_Folder_Path, P_Border, Portrait_Folder_Path_Bordered)

        except FileNotFoundError:
            print("Error: Border file not found.")
        except Exception as e:
            print(f"Error occurred while adding borders: {str(e)}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    
# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    
    print("           _    _             _____                    _              ____")
    print("   / \\   | |_ | |  __ _  ___ | __ )   ___   _ __   __| |  ___  _ __ |  _ \\  _ __   ___")
    print("  / _ \\  | __|| | / _` |/ __||  _ \\  / _ \\ | '__| / _` | / _ \\| '__|| |_) || '__| / _ \\")
    print(" / ___ \\ | |_ | || (_| |\\__ \\| |_) || (_) || |   | (_| ||  __/| |   |  __/ | |   | (_) |")
    print("/_/   \\_\\ \\__||_| \\__,_||___/|____/  \\___/ |_|    \\__,_| \\___||_|   |_|    |_|    \\___/")
    print("By Kenneth Gonzales")
    print("")
    print("")
    Run_ABP()
    input("Press enter to close the program")
