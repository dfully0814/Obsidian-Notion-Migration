import os
import logging
import time
import markdown
from notion_client import Client, APIResponseError
from notion_page_service import PageBlockProcessor
import uuid
import sys

# DATABASE_ID = "dc8f63b3bc874a93818676af32fbad0e"

class NotionService:
    def __init__(self, database_id, files_to_create) -> None:
        self.database_id = database_id
        self.files_to_create = files_to_create
        self.notion = Client(auth=os.environ["NOTION_API_KEY"])
        
    def create_pages(self):
        int_test = 0
        for file in self.files_to_create:
            if (int_test == 5):
                break
            try:
                child_contents = PageBlockProcessor(
                        file["contents"].getvalue().decode("utf-8")
                    ).convert_to_pageblocks()
                
                child_contents_with_image = self.createPreviewImageBlock(child_contents, file)
                
                page_create_response = self.notion.pages.create(
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
                    children=child_contents_with_image
                )
                self.process_response(page_create_response)
                time.sleep(2)
                int_test += 1
            except APIResponseError as error:
                file_name = file["file_name"]
                with self.safe_open_a("logs/output.log") as f:
                    f.write(f"Error creating {file_name} == " + str(error) + "\n")
                    f.close()
                
    def createPreviewImageBlock(self, child_contents, file):
        if (len(child_contents) > 1 and any([c["type"] for c in child_contents[:3] if "type" in c and c["type"] == "image"])):
            return child_contents
        # Insert image block for imgur image at the top of the page
        child_contents.insert(0,
            {
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": file["imageUrl"] if file["imageUrl"] else "https://i.imgur.com/86WDQNk.jpg"
                    }
                }
            })
        return child_contents
    
    def process_response(self, response):
        page_id = response.get("id")
        if (page_id):
            file_name = response["properties"]["Name"]["title"][0]["text"]["content"]
            print(f"*** Successfully created page: {file_name} - {page_id} ***")
    
    def safe_open_a(self, path):
        """Open 'path' for appending, creating any parent directories as needed

        Args:
            path (string): The fully qualified path for the file to be opened
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return open(path, "a", encoding="utf-8")
    
    def create_mentions(self):
        """ Create page mentions on each newly created notion page
        """
        
        notion_pages = self.notion.databases.query(
            database_id=self.database_id
        )
        
        int_test = 0
        for page in notion_pages["results"]:
            if (int_test == 10):
                break
            child_blocks = self.notion.blocks.children.list(
                block_id=page["id"]
            )
            for block in child_blocks.get("results"):
                block_type = block["type"]
                rich_text_blocks = block.get(block_type).get("rich_text")
                if (rich_text_blocks):
                    for text_block in rich_text_blocks:
                        text = text_block.get("text").get("content")
                        self.process_mentions(text)
            int_test += 1

    def process_mentions(self, text): 
        start_bracket = "[["
        end_bracket = "]]"
        exclude_start_bracket = "![["
        
        start_index = 0
        print("::: text string ::: ")
        print(text)
        while start_index < len(text):
            exclude_start_index = text.find(exclude_start_bracket, start_index)
            if (exclude_start_index != -1):
                break

            mention_start_index = text.find(start_bracket, start_index)
            if (mention_start_index == -1):
                break

            mention_end_index = text.find(end_bracket, mention_start_index + len(start_bracket))
            if (mention_end_index == -1):
                break

            mention_word = text[mention_start_index + len(start_bracket):mention_end_index]
            print("-- mention word -- " + mention_word)
                # API call
            start_index = mention_end_index + len(end_bracket)