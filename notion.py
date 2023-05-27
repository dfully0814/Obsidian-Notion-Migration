import os
import logging
import time
import markdown
from notion_client import Client, APIResponseError
from notion_page_service import PageBlockProcessor

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
                        }
                    },
                    children=child_contents
                )
                self.process_response(page_create_response)
                # time.sleep(5)
            except APIResponseError as error:
                logging.error(error)  
            i += 1
    
    def _split_rich_text(self, file_contents):
        if (len(file_contents) <= 2000):
            return
        
        chunks = []
        chunk_size = 2000
        current_chunk = ""
        
        words = file_contents.split()
        chunks = []
        current_chunk = ""
        for word in words:
            if len(current_chunk) + len(word) + 1 <= chunk_size:  # +1 for the space between words
                current_chunk += " " + word if current_chunk else word
            else:
                chunks.append({
                    "type": "text",
                    "text": {
                        "content": current_chunk
                    }
                })
                current_chunk = word
        if current_chunk:
            chunks.append({
                    "type": "text",
                    "text": {
                        "content": current_chunk
                    }
            })
                
        return chunks
 
    def process_response(self, response):
        page_id = response.get("id")
        if (page_id):
            file_name = response["properties"]["Name"]["title"][0]["text"]["content"]
            print(f"*** Successfully created page: {file_name} - {page_id} ***")