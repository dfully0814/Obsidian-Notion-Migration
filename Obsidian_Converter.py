import os
import sys

directories = [
    "Characters",
    "Locations",
    "Lore",
    "NPCs",
    "Organizations",
    "Vessels",
    "Session Recaps",
    "Uncharted North"
]

def find_dir_name(file_path):
    head, tail = os.path.split(file_path)
    file_name, file_extension = os.path.splitext(tail)
    return file_name

def find_files(parentDirectory, directories):
    totalFiles = 0
    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Error: missing parent directory path argument.")
            print("Usage: python script.py <parent_directory_path>")
            sys.exit(1)

    for dir_name in directories:
        dir_path = os.path.join(parentDirectory, dir_name)
        for dir_path, dir_names, file_names in os.walk(dir_path):
            for file_name in file_names:
                if file_name.endswith(".md"):
                    totalFiles += 1
    print(totalFiles)            

parent_directory = sys.argv[1]
find_files(parent_directory, directories)
