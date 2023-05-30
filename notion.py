import os
import logging
import time
import markdown
from notion_client import Client, APIResponseError
from notion_page_service import PageBlockProcessor
import uuid
import sys

# DATABASE_ID = "dc8f63b3bc874a93818676af32fbad0e"
notion = Client(auth=os.environ["NOTION_API_KEY"])

class NotionService:
    def __init__(self, database_id, files_to_create) -> None:
        self.database_id = database_id
        self.files_to_create = files_to_create
        
    def create_pages(self):
        for file in self.files_to_create:
            try:
                child_contents = PageBlockProcessor(
                        file["contents"].getvalue().decode("utf-8")
                    ).convert_to_pageblocks()
                page_create_response = notion.pages.create(
                    parent={"database_id": self.database_id},
                    properties={
                        "Name": {
                            "title": [
                                {
                                    "text": {
                                            "content": file["file_name"]
                                        }
                                    }
                            ]
                        },
                        "Type": {
                            "id": str(uuid.uuid4()),
                            "select": {
                                "name": file["parent_folder"]
                            }
                        }
                    },
                    children=child_contents            
                )
                self.process_response(page_create_response)
                time.sleep(1)
            except APIResponseError as error:
                file_name = file["file_name"]
                log_file = open("output.log", "a", encoding="utf-8")
                
                log_file.write(f"Error creating {file_name} == " + str(error) + "\n")
                
                log_file.close()
                 
    def process_response(self, response):
        page_id = response.get("id")
        if (page_id):
            file_name = response["properties"]["Name"]["title"][0]["text"]["content"]
            print(f"*** Successfully created page: {file_name} - {page_id} ***")