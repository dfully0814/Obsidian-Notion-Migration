import os
from pathlib import PurePath
import obsidiantools.api as otools

vault = otools.Vault("C:\\Users\\Daniel\Documents\\Aerilon Vault\\Aerilon-Vault-Cloud").connect().gather()

# dictionary of files to send to the notion service with the .md suffixes stripped out
files_to_create = {}

def remove_file_name_from_path(path):
    return PurePath(os.path.dirname(path))

for fileName, path in vault.md_file_index.items():
    remove_file_name_from_path(path)
    
