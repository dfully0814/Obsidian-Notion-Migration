import json
import os
from pprint import pprint
from notion_client import Client


DATABASE_ID = "dc8f63b3bc874a93818676af32fbad0e"

notion = Client(auth=os.environ["NOTION_API_KEY"])
page_create_response = notion.pages.create(
    parent={"database_id": DATABASE_ID},
    properties={
        "Name": {"title": [{"text": {"content": "Obsidian/Notion Test"}}]}
    }
)

pprint(page_create_response)