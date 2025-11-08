import google.generativeai as genai
import os
import re
from utils import get_entire_codebase

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

with open("docs/SDS.md", "r") as f:
    sds_content = f.read()

codebase = get_entire_codebase("src")

prompt = f"""
You are a Senior Developer. Implement the changes required by this SDS.
SDS: {sds_content}

Current Codebase: {codebase}

IMPORTANT OUTPUT FORMAT:
You must output the FULL content of ANY file you strictly need to create or modify.
Use these exact tags so my automated parser can save them:
<FILE path="src/main.py">
print("full new content of file here")
</FILE>

Only output files that need changes.
"""

response = model.generate_content(prompt)
response_text = response.text

# --- simplistic parser to extract files and save them ---
# Finds all content between <FILE path="..."> and </FILE>
file_matches = re.findall(r'<FILE path="(.*?)">\n(.*?)\n</FILE>', response_text, re.DOTALL)

for file_path, file_content in file_matches:
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Write the new content, overwriting the old file
    with open(file_path, "w") as f:
        f.write(file_content)
    print(f"Updated/Created: {file_path}")
