import os
import logging
import time
import markdown
from notion_client import Client, APIResponseError
from notion_page_service import PageBlockProcessor
import uuid

# DATABASE_ID = "dc8f63b3bc874a93818676af32fbad0e"
notion = Client(auth=os.environ["NOTION_API_KEY"])

class NotionService:
    def __init__(self, database_id, files_to_create) -> None:
        self.database_id = database_id
        self.files_to_create = files_to_create
        
    def create_pages(self):
        i = 0
        for file in self.files_to_create:
            if (i == 1):
                break
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
                                "name": "Location"
                            }
                        }
                    },
                    children=child_contents
                    # Add the other database properties for the page
                    
                )
                self.process_response(page_create_response)
                # time.sleep(5)
            except APIResponseError as error:
                logging.error(error)  
            i += 1
 
    def process_response(self, response):
        page_id = response.get("id")
        if (page_id):
            file_name = response["properties"]["Name"]["title"][0]["text"]["content"]
            print(f"*** Successfully created page: {file_name} - {page_id} ***")