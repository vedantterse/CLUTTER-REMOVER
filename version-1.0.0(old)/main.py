import os
import shutil
import zipfile

def clutter_remover(source_folder):
    try:
        # Check if source folder exists
        if not os.path.exists(source_folder):
            raise FileNotFoundError("Source folder does not exist.")

        # Check if source folder is empty
        if not os.listdir(source_folder):
            raise ValueError("Source folder is empty.")

        # Dictionary to store file extensions and their corresponding folder names
        file_types = {
            'png': 'PNG',
            'jpg': 'JPG',
            'pdf': 'PDF',
            'txt': 'Text',
            # Add more file types as needed
        }

        # Walk through the source folder and move files to their respective folders
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                if file_extension.lower()[1:] in file_types:
                    destination_folder = file_types[file_extension.lower()[1:]]
                else:
                    destination_folder = file_extension.lower()[1:]  # Use the extension name as folder name
                destination_path = os.path.join(source_folder, destination_folder)
                os.makedirs(destination_path, exist_ok=True)
                destination_file = os.path.join(destination_path, file)

                # Check if destination file already exists
                if os.path.exists(destination_file):
                    new_file_name = file_name + "_duplicate" + file_extension
                    destination_file = os.path.join(destination_path, new_file_name)

                shutil.move(os.path.join(root, file), destination_file)

        print("\033[32mClutter removed successfully!\033[0m")
    except (FileNotFoundError, OSError) as e:
        print(f"\033[91mError: {e}\033[0m")
    except ValueError as e:
        print(f"\033[91mError: {e}\033[0m")

def folder_zip(source_folder):
    try:
        # Check if source folder exists
        if not os.path.exists(source_folder):
            raise FileNotFoundError("Source folder does not exist.")

        # Create a zip file containing the entire source folder and its contents
        zip_file_path = os.path.join(os.path.dirname(source_folder), 'organized_files.zip')
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    zip_file.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_folder))

        print("\033[32mSource folder compressed into organized_files.zip!\033[0m")
    except (FileNotFoundError, OSError) as e:
        print(f"\033[91mError: {e}\033[0m")


def rename_pngs(source_folder):
    try:
        # Check if source folder exists
        if not os.path.exists(source_folder):
            raise FileNotFoundError("Source folder does not exist.")

        # Get list of PNG files in the source folder
        png_files = [file for file in os.listdir(source_folder) if file.lower().endswith('.png')]

        # Sort PNG files based on modification time
        png_files.sort(key=lambda x: os.stat(os.path.join(source_folder, x)).st_mtime)

        # Rename PNG files sequentially
        for i, png_file in enumerate(png_files):
            new_name = str(i + 1) + '.png'
            os.rename(os.path.join(source_folder, png_file), os.path.join(source_folder, new_name))

        print("\033[32mPNG files renamed successfully!\033[0m")
    except (FileNotFoundError, OSError) as e:
        print(f"\033[91mError: {e}\033[0m")


while True:
    print("\033[33m!!! CLUTTER MANAGER TOOL !!!\033[0m")
    print("\033[36mSELECT FROM THE OPTIONS \033[0m")
    print("1. All files clutter manager (makes folder for each file type) ")
    print("2. Folder to zip")
    print("3. Rename the cluttered PNGs in order")
    print("Type \033[91m'exit'\033[0m to quit")

    choice = input("Enter the Option: ").strip().lower()

    if choice == 'exit':
        print("Exiting the program...")
        break

    try:
        choice = int(choice)
        if choice not in (1, 2, 3):
            print("\033[91mPlease select from the options list\033[0m")
            continue  # Go back to the start of the loop
        source_folder = input("Enter the path of the folder: ")
        if choice == 1:
            clutter_remover(source_folder)
        elif choice == 2:
            folder_zip(source_folder)
        elif choice == 3:
            rename_pngs(source_folder)
    except ValueError:
        print("\033[91mInvalid input. Please enter a number corresponding to the options.\033[0m")
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
