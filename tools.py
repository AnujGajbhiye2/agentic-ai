# tools.py
import os
from google.adk.tools import FunctionTool

def save_article_to_disk(filename: str, content: str, folder: str = "output") -> dict:
    """
    Saves the final article content to a markdown file.
    
    Args:
        filename (str): The name of the file (e.g., "nvidia-gpu-news.md").
        content (str): The full markdown content of the article.
        folder (str): The target directory.
        
    Returns:
        dict: Status message indicating success or failure.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Ensure filename ends in.md
    if not filename.endswith(".md"):
        filename += ".md"
        
    filepath = os.path.join(folder, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "path": filepath}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Wrap the function for ADK consumption
save_file_tool = FunctionTool(save_article_to_disk)