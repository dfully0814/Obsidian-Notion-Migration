from obsidian import VaultService
from notion import NotionService
import sys
import os

_obsidian_vault_path = input("Enter the full path to your Obsidian vault: ")
while not os.path.exists(_obsidian_vault_path):
    print("Invalid path. Please try again. On some platforms, this error may occur if you do not have read and execute permissions on the file, even if the path physically exists.")
    _obsidian_vault_path = input("Enter the full path to your Obsidian vault: ")

print("Gathering vault metadata...")
_vault_service = VaultService(_obsidian_vault_path)

os.environ["NOTION_DATABASE_ID"] = input("Enter Notion database id: ")
while not os.environ["NOTION_DATABASE_ID"]:
    print("Database id cannot be empty. Please try again.")
    os.environ["NOTION_DATABASE_ID"] = input("Enter Notion database id")
    
os.environ["NOTION_API_KEY"] = input("Enter your Notion API Key: ")
while not os.environ["NOTION_API_KEY"]:
    print("Notion API Key cannot be empty. Please try again.")
    os.environ["NOTION_API_KEY"] = input("Enter your Notion API Key: ")

print("Creating notion pages...")
_notion_service = NotionService(os.environ["NOTION_DATABASE_ID"], _vault_service.get_files_to_create())

_notion_service.create_pages()