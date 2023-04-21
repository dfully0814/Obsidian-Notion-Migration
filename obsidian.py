import os
from pathlib import PurePath
import obsidiantools.api as otools
import io

vault = otools.Vault("Aerilon_Vault").connect().gather()

# dictionary of files to send to the notion service with the .md suffixes stripped out
files_to_create = {}

def remove_file_name_from_path(path):
    return PurePath()

for fileName, path in vault.md_file_index.items():
    # Get the lowest directory in the path after getting the parent of the file
    notion_folder = PurePath(path).parent.parts[-1]
    
    files_to_create.update({
        "fileName" : fileName,
        "notion_folder" : notion_folder,
        "contents" : io.BytesIO(vault.get_readable_text(fileName))
    })
    
print(files_to_create)
        
