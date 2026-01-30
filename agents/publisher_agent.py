"""
Publisher Agent
Responsible for publishing blog posts to the website
"""
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json
import shutil

from agents.base_agent import BaseAgent
from config.settings import BLOG_DIR, POSTS_DIR, IMAGES_DIR, AUTO_PUBLISH, REVIEW_BEFORE_PUBLISH
from services.image_service import get_image_service


class PublisherAgent(BaseAgent):
    """Agent that publishes blog posts to the website"""
    
    def __init__(self):
        super().__init__(
            name="Publisher Agent",
            description="Publishing blog posts to the website"
        )
        self.image_service = get_image_service()
        
        # Blog content directory (for Next.js)
        self.blog_posts_dir = BLOG_DIR / "src" / "content" / "posts"
        self.blog_images_dir = BLOG_DIR / "public" / "images" / "posts"
    
    async def run(
        self,
        blog_post: Dict[str, Any],
        auto_publish: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Publish a blog post to the website
        
        Args:
            blog_post: Complete blog post from WriterAgent
            auto_publish: Override auto-publish setting
            
        Returns:
            Publication result with file paths and URLs
        """
        self.log_start()
        
        should_publish = auto_publish if auto_publish is not None else AUTO_PUBLISH
        
        try:
            # Step 1: Save to drafts/data folder first
            self.log("Saving post to data folder...")
            draft_path = await self._save_to_data(blog_post)
            
            # Step 2: Download and save images locally
            self.log("Processing images...")
            local_images = await self._process_images(blog_post)
            
            # Step 3: Update content with local image paths
            self.log("Updating image paths...")
            updated_content = self._update_image_paths(blog_post["full_post"], local_images)
            
            # Step 4: Publish to blog if auto-publish is enabled
            published_path = None
            if should_publish:
                self.log("Publishing to blog...")
                published_path = await self._publish_to_blog(blog_post, updated_content)
            elif REVIEW_BEFORE_PUBLISH:
                self.log("Post saved for review. Set AUTO_PUBLISH=true to publish automatically.", "warning")
            
            result = {
                "success": True,
                "draft_path": str(draft_path),
                "published_path": str(published_path) if published_path else None,
                "images_processed": len(local_images),
                "auto_published": should_publish,
                "post_url": self._generate_post_url(blog_post) if published_path else None,
                "frontmatter": blog_post.get("frontmatter", {}),
                "word_count": blog_post.get("word_count", 0)
            }
            
            self.log_complete()
            return result
            
        except Exception as e:
            self.log(f"Error: {e}", "error")
            raise
    
    async def _save_to_data(self, blog_post: Dict[str, Any]) -> Path:
        """Save the blog post to the data folder"""
        
        # Create filename from slug or title
        slug = blog_post.get("frontmatter", {}).get("slug", "")
        if not slug:
            slug = blog_post.get("title", "post").lower().replace(" ", "-")
        
        # Clean slug
        slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug)
        
        # Add date prefix
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_prefix}-{slug}.md"
        
        # Save to posts directory
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        post_path = POSTS_DIR / filename
        
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(blog_post.get("full_post", ""))
        
        # Also save metadata as JSON
        meta_path = POSTS_DIR / f"{date_prefix}-{slug}.json"
        meta_data = {
            "title": blog_post.get("title", ""),
            "date": date_prefix,
            "word_count": blog_post.get("word_count", 0),
            "images": [img.get("url", "") for img in blog_post.get("images", [])],
            "videos": [vid.get("link", "") for vid in blog_post.get("videos", [])],
            "frontmatter": blog_post.get("frontmatter", {}),
            "keywords": blog_post.get("keywords", {})
        }
        
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2)
        
        self.log(f"Saved draft to: {post_path}")
        return post_path
    
    async def _process_images(self, blog_post: Dict[str, Any]) -> Dict[str, str]:
        """Download images and return mapping of URL to local path"""
        
        local_images = {}
        images = blog_post.get("images", [])
        
        # Create images directory
        slug = blog_post.get("frontmatter", {}).get("slug", "post")
        post_images_dir = IMAGES_DIR / slug
        post_images_dir.mkdir(parents=True, exist_ok=True)
        
        for i, img in enumerate(images):
            url = img.get("url", "")
            if not url:
                continue
            
            # Download image
            filename = f"image-{i + 1}.jpg"
            local_path = self.image_service.download_image(
                url=url,
                filename=filename,
                folder=post_images_dir
            )
            
            if local_path:
                # Store relative path for web
                relative_path = f"/images/posts/{slug}/{filename}"
                local_images[url] = relative_path
        
        return local_images
    
    def _update_image_paths(self, content: str, local_images: Dict[str, str]) -> str:
        """Replace remote image URLs with local paths"""
        
        updated_content = content
        for remote_url, local_path in local_images.items():
            updated_content = updated_content.replace(remote_url, local_path)
        
        return updated_content
    
    async def _publish_to_blog(self, blog_post: Dict[str, Any], content: str) -> Path:
        """Publish the post to the blog website"""
        
        # Create blog posts directory if it doesn't exist
        self.blog_posts_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        slug = blog_post.get("frontmatter", {}).get("slug", "post")
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_prefix}-{slug}.md"
        
        post_path = self.blog_posts_dir / filename
        
        # Write the post
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Copy images to blog public folder
        slug = blog_post.get("frontmatter", {}).get("slug", "post")
        source_images = IMAGES_DIR / slug
        target_images = self.blog_images_dir / slug
        
        if source_images.exists():
            target_images.mkdir(parents=True, exist_ok=True)
            for img_file in source_images.glob("*"):
                shutil.copy2(img_file, target_images / img_file.name)
        
        self.log(f"Published to: {post_path}")
        return post_path
    
    def _generate_post_url(self, blog_post: Dict[str, Any]) -> str:
        """Generate the URL for the published post"""
        
        slug = blog_post.get("frontmatter", {}).get("slug", "post")
        date = datetime.now().strftime("%Y/%m/%d")
        
        from config.settings import BLOG_URL
        return f"{BLOG_URL}/blog/{date}/{slug}"
    
    async def publish_manually(self, post_path: Path) -> Dict[str, Any]:
        """Manually publish a saved draft"""
        
        self.log(f"Publishing draft: {post_path}")
        
        if not post_path.exists():
            raise FileNotFoundError(f"Draft not found: {post_path}")
        
        # Read the draft
        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Copy to blog posts directory
        self.blog_posts_dir.mkdir(parents=True, exist_ok=True)
        published_path = self.blog_posts_dir / post_path.name
        
        with open(published_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.log(f"Published to: {published_path}")
        
        return {
            "success": True,
            "published_path": str(published_path)
        }
