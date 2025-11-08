import google.generativeai as genai
import os
from utils import get_entire_codebase, get_latest_brs

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.5-flash')

brs_content = get_latest_brs()
codebase = get_entire_codebase('src') # Assumes your code is in a 'src' folder

prompt = f"""
You are a Principal Software Architect.
Existing Codebase:
{codebase}

New Business Requirement Specification (BRS):
{brs_content}

Task: Create a detailed Solution Design Specification (SDS) in Markdown format.
It must include:
1. System Architecture changes.
2. Detailed API specifications (if needed).
3. Database schema changes (if needed).
4. Step-by-step implementation plan for a developer.
"""

response = model.generate_content(prompt)

os.makedirs('docs', exist_ok=True)
with open('docs/SDS.md', 'w') as f:
    f.write(response.text)
print("SDS generated at docs/SDS.md")
