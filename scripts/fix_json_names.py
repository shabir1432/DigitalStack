import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_POSTS_DIR = os.path.join(BASE_DIR, "data", "posts")

def fix_json_names():
    if not os.path.exists(DATA_POSTS_DIR):
        print(f"Directory not found: {DATA_POSTS_DIR}")
        return

    for filename in os.listdir(DATA_POSTS_DIR):
        if not filename.endswith(".json"):
            continue

        # Check if filename has date prefix
        match = re.match(r"^(\d{4}-\d{2}-\d{2})-(.*)\.json$", filename)
        if not match:
            continue

        date_prefix = match.group(1)
        original_slug_base = match.group(2)
        
        # Sanitize slug (same logic as simplify_urls.py)
        clean_slug_base = re.sub(r'-+', '-', original_slug_base)
        
        new_filename = f"{clean_slug_base}.json"
        
        old_filepath = os.path.join(DATA_POSTS_DIR, filename)
        new_filepath = os.path.join(DATA_POSTS_DIR, new_filename)
        
        if old_filepath != new_filepath:
            os.rename(old_filepath, new_filepath)
            print(f"Renamed JSON: {filename} -> {new_filename}")

if __name__ == "__main__":
    fix_json_names()
