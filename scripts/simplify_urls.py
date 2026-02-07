import os
import re
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, "blog", "src", "content", "posts")
IMAGES_DIR = os.path.join(BASE_DIR, "blog", "public", "images", "posts")

def simplify_urls():
    if not os.path.exists(POSTS_DIR):
        print(f"Directory not found: {POSTS_DIR}")
        return

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md"):
            continue

        # Check if filename has date prefix
        match = re.match(r"^(\d{4}-\d{2}-\d{2})-(.*)\.md$", filename)
        if not match:
            print(f"Skipping {filename} (no date prefix match)")
            continue

        date_prefix = match.group(1)
        original_slug_base = match.group(2)
        
        # Sanitize slug: remove double hyphens
        clean_slug_base = re.sub(r'-+', '-', original_slug_base)
        
        # New simplified filename
        new_filename = f"{clean_slug_base}.md"
        old_filepath = os.path.join(POSTS_DIR, filename)
        new_filepath = os.path.join(POSTS_DIR, new_filename)
        
        # Rename Markdown File
        os.rename(old_filepath, new_filepath)
        print(f"Renamed Post: {filename} -> {new_filename}")

        # Update Frontmatter
        with open(new_filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Update slug in frontmatter
        content = re.sub(r'^slug:.*$', f'slug: "{clean_slug_base}"', content, flags=re.MULTILINE)
        
        # Handle Image Directory
        # Image dir likely matches the ORIGINAL slug base (or maybe with date?)
        # Let's check common patterns
        
        full_slug_with_date = f"{date_prefix}-{original_slug_base}"
        possible_old_dirs = [
            full_slug_with_date,          # 2026-02-07-slug--with--double
            original_slug_base,           # slug--with--double
            clean_slug_base               # slug-clean (unlikely if we just created it)
        ]
        
        found_img_dir = None
        for old_dir_name in possible_old_dirs:
            path_to_check = os.path.join(IMAGES_DIR, old_dir_name)
            if os.path.exists(path_to_check):
                found_img_dir = path_to_check
                print(f"Found image dir: {old_dir_name}")
                break
        
        final_img_slug = clean_slug_base
        target_img_dir = os.path.join(IMAGES_DIR, clean_slug_base)
        
        if found_img_dir:
            if found_img_dir != target_img_dir:
                 if os.path.exists(target_img_dir):
                     print(f"Warning: Target image dir {clean_slug_base} already exists. Merging/Overwriting?")
                 else:
                     os.rename(found_img_dir, target_img_dir)
                     print(f"Renamed Image Dir to: {clean_slug_base}")
        else:
            print(f"Warning: No image directory found for {original_slug_base}")

        # Update image path in frontmatter
        content = re.sub(r'^image:.*$', f'image: "/images/posts/{final_img_slug}/image-1.jpg"', content, flags=re.MULTILINE)
        
        with open(new_filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        # Handle JSON Metadata Files (data/posts)
        DATA_POSTS_DIR = os.path.join(BASE_DIR, "data", "posts")
        json_filename_old = f"{date_prefix}-{original_slug_base}.json"
        json_filename_new = f"{clean_slug_base}.json"
        
        old_json_path = os.path.join(DATA_POSTS_DIR, json_filename_old)
        new_json_path = os.path.join(DATA_POSTS_DIR, json_filename_new)
        
        if os.path.exists(old_json_path):
            os.rename(old_json_path, new_json_path)
            print(f"Renamed JSON: {json_filename_old} -> {json_filename_new}")
        elif os.path.exists(new_json_path):
             print(f"JSON already correct: {json_filename_new}")
        else:
             print(f"Warning: JSON metadata not found for {original_slug_base}")

if __name__ == "__main__":
    simplify_urls()
