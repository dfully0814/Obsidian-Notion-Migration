"""
Process all files in the Obsidian vault for sending to Notion.

Author: Daniel Fuller
Returns:
    dict: A dictionary of the fileName, notion_folder, and file contents
"""

from pathlib import PurePath
import io
import obsidiantools.api as otools


class VaultService:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.vault = otools.Vault(self.vault_path).connect().gather()
        self.front_matter_index = self.get_front_matter_index()
        
    def get_files_to_create(self):
        """
        Get the files to send to Notion from Obsidian vault

        Author:
            Daniel Fuller
            
        Returns:
            tuple: A tuple of {file_name: <text>, notion_folder: <notion_folder>, contents: <bytes>}
        """
        # Gather Obsidian vault metadata
        # dictionary of files to send to the notion service with the .md suffixes stripped out
        files_to_create = []
        for file_name, path in self.vault.md_file_index.items():
            # Get the lowest directory in the path after getting the parent of the file
            parent_folder = PurePath(path).parent.parts[-1]
            files_to_create.append({
                "file_name" : file_name,
                "parent_folder" : parent_folder,
                "contents" : io.BytesIO(self.vault.get_source_text(file_name).encode("utf-8")),
                "imageUrl": self.front_matter_index.get(file_name).get("thumbnail")
            })
        return tuple(files_to_create)

    def get_front_matter_index(self):
        return self.vault.front_matter_index
    
