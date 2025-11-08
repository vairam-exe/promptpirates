import google.generativeai as genai
import pandas as pd
import os
from io import StringIO
from utils import get_latest_brs

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash-latest') # Flash is enough for this

brs_content = get_latest_brs()
with open('docs/SDS.md', 'r') as f:
    sds_content = f.read()

prompt = f"""
You are a QA Engineer.
Based on this BRS: {brs_content}
And this SDS: {sds_content}

Generate a CSV of manual test cases.
Columns MUST be: TestID, Description, Preconditions, Steps, ExpectedResult.
Do NOT add any markdown formatting like ```csv, just raw CSV data.
"""

response = model.generate_content(prompt)

# Use pandas to read the CSV string and save as Excel
try:
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    df.to_excel("docs/test_cases.xlsx", index=False)
    print("Test cases saved to docs/test_cases.xlsx")
except Exception as e:
    print(f"Error generating Excel: {e}")
    # Fallback: save raw CSV if Excel fails
    with open("docs/test_cases.csv", "w") as f:
        f.write(response.text)
