from obsidian import VaultService
from notion import NotionService

print("Gathering vault metadata...")
vault_service = VaultService("Aerilon_Vault")

print("Creating notion pages...")
notion_service = NotionService("dc8f63b3bc874a93818676af32fbad0e", vault_service.get_files_to_create())

notion_service.create_pages()