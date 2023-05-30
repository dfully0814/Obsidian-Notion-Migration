from obsidian import VaultService
from notion import NotionService
import sys
import os

_obsidian_vault_path = input("Enter the full path to your Obsidian vault: ")
while not os.path.exists(_obsidian_vault_path):
    print("Invalid path. Please try again. On some platforms, this error may return occur if the user does not have read and execute permissions on the file, even if the path physically exists.")

print("Gathering vault metadata...")
_vault_service = VaultService("Aerilon_Vault")

_notion_database_id = input("Enter Notion database id")
while not _notion_database_id:
    print("Database id cannot be empty. Please try again.")

print("Creating notion pages...")
_notion_service = NotionService("dc8f63b3bc874a93818676af32fbad0e", _vault_service.get_files_to_create())

_notion_service.create_pages()