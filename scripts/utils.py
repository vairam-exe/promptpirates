# scripts/utils.py
import os

def get_entire_codebase(start_path='src'):
    """Reads all code files into a single string for LLM context."""
    code_context = ""
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(('.py', '.js', '.html', '.css', '.java')): # Add your relevant extensions
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code_context += f"\n\n--- START FILE: {file_path} ---\n"
                    code_context += f.read()
                    code_context += f"\n--- END FILE: {file_path} ---\n"
    return code_context

def get_latest_brs(brs_folder='requirements'):
    """Finds the most recently modified file in the requirements folder."""
    files = [os.path.join(brs_folder, f) for f in os.listdir(brs_folder) if os.path.isfile(os.path.join(brs_folder, f))]
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, 'r') as f:
        return f.read()
