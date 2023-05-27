import json
import subprocess

class PageBlockProcessor:
    def __init__(self, markdown) -> None:
         self.markdown = markdown
         
    def convert_to_pageblocks(self):
        try:
            output = subprocess.run(["node", 'mdPageblockConverter.js', self.markdown], capture_output=True, text=True, check=True)
            return json.loads(output.stdout)

        except subprocess.CalledProcessError as error:
            error_message = error.stderr.strip()
            print(f"Page block parsing failed; {error_message}")
