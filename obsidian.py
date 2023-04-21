"""
Process all files in the Obsidian vault for sending to Notion.

Author: Daniel Fuller
Returns:
    dict: A dictionary of the fileName, notion_folder, and file contents
"""

from pathlib import PurePath
import io
import obsidiantools.api as otools

vault = otools.Vault("Aerilon_Vault").connect().gather()

# dictionary of files to send to the notion service with the .md suffixes stripped out
files_to_create = {}

for fileName, path in vault.md_file_index.items():
    # Get the lowest directory in the path after getting the parent of the file
    notion_folder = PurePath(path).parent.parts[-1]
    files_to_create.update({
        "fileName" : fileName,
        "notion_folder" : notion_folder,
        "contents" : io.BytesIO(vault.get_readable_text(fileName))
    })
