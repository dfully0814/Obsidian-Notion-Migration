import requests
import json

DATABASE_ID = "dc8f63b3bc874a93818676af32fbad0e"
APIKEY = "secret_iYKxuQGT0MZ9Y0XCJPf5GL7NKrb0a0NoewxMkjPUEao"

url = "https://api.notion.com/v1/pages"


def get_request_headers():
    return {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer " + APIKEY
    }

def get_request_body():
    return {
        "parent": {
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

response = requests.post(url, json=get_request_body(), headers=get_request_headers())
print(response.text)