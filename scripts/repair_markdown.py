import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, "blog", "src", "content", "posts")
DATA_POSTS_DIR = os.path.join(BASE_DIR, "data", "posts")

def sanitize_slug(slug):
    """Sanitize slug: lowercase, remove specials, collapse hyphens."""
    slug = slug.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = slug.replace(" ", "-")
    slug = re.sub(r'-+', '-', slug)
    return slug.strip("-")

def repair_markdown_files():
    if not os.path.exists(POSTS_DIR):
        print(f"Directory not found: {POSTS_DIR}")
        return

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(POSTS_DIR, filename)
        
        # 1. Read the content
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 2. Check and fix wrapper blocks
        content_stripped = content.strip()
        cleaned_content = content
        
        if content_stripped.startswith("```markdown"):
            cleaned_content = re.sub(r"^```markdown\s*", "", content_stripped, flags=re.IGNORECASE)
            cleaned_content = re.sub(r"\s*```$", "", cleaned_content)
        elif content_stripped.startswith("```"):
             cleaned_content = re.sub(r"^```\s*", "", content_stripped)
             cleaned_content = re.sub(r"\s*```$", "", cleaned_content)
        
        cleaned_content = cleaned_content.strip()

        # 3. Check/Update Frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", cleaned_content, re.DOTALL)
        
        existing_fm = {}
        body_content = cleaned_content
        
        if frontmatter_match:
            fm_str = frontmatter_match.group(1)
            body_content = cleaned_content[frontmatter_match.end():]
            
            # Simple parsing of existing frontmatter
            for line in fm_str.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    existing_fm[key.strip()] = val.strip().strip('"')
        
        # Check source JSON for data (Note: JSON filename might still have date prefix if not renamed)
        # We try both
        json_filename = filename.replace(".md", ".json")
        json_path = os.path.join(DATA_POSTS_DIR, json_filename)
        
        # Also try date-prefixed version if current filename has no date
        if not os.path.exists(json_path):
             # Try finding a pattern matching the slug
             pass 

        json_data = {}
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as jf:
                    json_data = json.load(jf)
            except Exception as e:
                print(f"Error reading JSON for {filename}: {e}")

        # Derive slug from filename for consistency
        filename_slug = filename.replace(".md", "")
        # Remove date prefix if present (for logic robustnes)
        if re.match(r"\d{4}-\d{2}-\d{2}-", filename_slug):
             filename_slug = filename_slug[11:]
             print(f"Warning: File {filename} still has date prefix.")
             
        sanitized_slug = sanitize_slug(filename_slug) # Ensure it's clean
        
        # Merge metadata
        fm = json_data.get("frontmatter", {})
        if not fm and "title" in json_data:
             fm = {
                 "title": json_data.get("title"),
                 "date": json_data.get("date"),
                 "slug": sanitized_slug,
             }
        
        # Override with existing frontmatter 
        fm.update(existing_fm)
        
        # FORCE slug to match filename slug
        fm["slug"] = sanitized_slug 
        
        # Fix image path using SANITIZED slug
        # Check if we should add image
        has_image = "image" in fm
        json_images = json_data.get("images", [])
        
        # Always re-construct image path if images exist to ensure it uses sanitized slug
        if json_images or has_image:
             fm["image"] = f"/images/posts/{sanitized_slug}/image-1.jpg"

        # Clean excerpt if present
        if "excerpt" in fm:
            excerpt = fm["excerpt"]
            # remove wrapping quotes
            if excerpt.startswith('"') and excerpt.endswith('"'):
                excerpt = excerpt[1:-1]
            # remove markdown blocks
            if excerpt.strip().startswith("```"):
                 excerpt = re.sub(r"^```\w*\s*", "", excerpt.strip())
                 excerpt = re.sub(r"\s*```$", "", excerpt)
            fm["excerpt"] = excerpt.strip()

        # Re-construct YAML
        frontmatter_str = "---\n"
        for k, v in fm.items():
            if v is None: continue
            if isinstance(v, str):
                safe_val = v.replace('"', '\\"')
                frontmatter_str += f'{k}: "{safe_val}"\n'
            else:
                frontmatter_str += f'{k}: {v}\n'
        frontmatter_str += "---\n\n"
        
        new_full_content = frontmatter_str + body_content.strip() + "\n"

        # 4. Write back if changed
        if new_full_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_full_content)
            print(f"Fixed {filename} (Slug: {sanitized_slug})")
        else:
            print(f"No changes needed for {filename}")

if __name__ == "__main__":
    repair_markdown_files()
