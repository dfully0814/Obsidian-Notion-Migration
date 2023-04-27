import json
import os
import requests

DATABASE_ID = "dc8f63b3bc874a93818676af32fbad0e"
API_KEY = "secret_iYKxuQGT0MZ9Y0XCJPf5GL7NKrb0a0NoewxMkjPUEao"

NOTION_PAGE_URL = "https://api.notion.com/v1/pages"


def get_request_headers():
    return {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }

def get_request_body():
    return {
        "√": {
            "type": "database_id",
            "database_id": DATABASE_ID,
        },
        "properties": {
            "Name": {
                "type": "title",
                "title": [{
                    "type": "text",
                    "text": {
                        "content": "Tomatoes"
                    }
                }]
            }
        }
    }

# response = requests.post(url, json=get_request_body(), headers=get_request_headers())
print(get_request_headers())