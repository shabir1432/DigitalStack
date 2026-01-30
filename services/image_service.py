"""
Image Service
Multi-source image service: Pexels stock photos + StabilityAI generation
"""
import os
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import base64
from rich.console import Console

from config.settings import PEXELS_API_KEY, STABILITY_API_KEY, IMAGES_DIR, IMAGE_SOURCE

console = Console()


class PexelsService:
    """Pexels stock photo service"""
    
    BASE_URL = "https://api.pexels.com/v1"
    
    def __init__(self):
        self.api_key = PEXELS_API_KEY
        self.headers = {"Authorization": self.api_key}
    
    def search_images(self, query: str, per_page: int = 10,
                      orientation: str = "landscape") -> List[Dict[str, Any]]:
        """Search for stock photos"""
        if not self.api_key:
            return []
        
        try:
            console.print(f"[blue]Searching Pexels for '{query}'...[/blue]")
            
            response = requests.get(
                f"{self.BASE_URL}/search",
                headers=self.headers,
                params={"query": query, "per_page": per_page, "orientation": orientation}
            )
            response.raise_for_status()
            
            photos = response.json().get("photos", [])
            console.print(f"[green]Found {len(photos)} images[/green]")
            
            return [
                {
                    "id": photo["id"],
                    "url": photo["src"]["large"],
                    "original": photo["src"]["original"],
                    "alt": photo.get("alt", query),
                    "photographer": photo["photographer"],
                    "photographer_url": photo["photographer_url"],
                    "source": "pexels"
                }
                for photo in photos
            ]
        except Exception as e:
            console.print(f"[red]Pexels error: {e}[/red]")
            return []


class StabilityAIService:
    """StabilityAI image generation service"""
    
    BASE_URL = "https://api.stability.ai/v2beta"
    
    def __init__(self):
        self.api_key = STABILITY_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }
    
    def generate_image(self, prompt: str, style: str = "photographic",
                       aspect_ratio: str = "16:9") -> Optional[Dict[str, Any]]:
        """Generate an AI image"""
        if not self.api_key:
            console.print("[yellow]StabilityAI not configured[/yellow]")
            return None
        
        try:
            console.print(f"[blue]Generating image: '{prompt[:50]}...'[/blue]")
            
            response = requests.post(
                f"{self.BASE_URL}/stable-image/generate/sd3",
                headers=self.headers,
                files={"none": ""},
                data={
                    "prompt": prompt,
                    "style_preset": style,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "png",
                }
            )
            
            if response.status_code == 200:
                # Save the image
                image_hash = hashlib.md5(prompt.encode()).hexdigest()[:10]
                filename = f"ai_generated_{image_hash}.png"
                filepath = IMAGES_DIR / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                console.print(f"[green]Generated: {filename}[/green]")
                
                return {
                    "id": image_hash,
                    "url": str(filepath),
                    "alt": prompt,
                    "photographer": "AI Generated",
                    "photographer_url": "https://stability.ai",
                    "source": "stability",
                    "local_path": str(filepath)
                }
            else:
                console.print(f"[red]StabilityAI error: {response.text}[/red]")
                return None
                
        except Exception as e:
            console.print(f"[red]StabilityAI error: {e}[/red]")
            return None
    
    def generate_blog_images(self, topic: str, descriptions: List[str]) -> List[Dict[str, Any]]:
        """Generate multiple images for a blog post"""
        images = []
        for desc in descriptions:
            full_prompt = f"Professional blog header image: {desc}. Topic: {topic}. High quality, sharp focus, editorial style."
            image = self.generate_image(full_prompt)
            if image:
                images.append(image)
        return images


class ImageService:
    """
    Unified image service that uses:
    1. StabilityAI for AI-generated images (if configured)
    2. Pexels as fallback for stock photos
    """
    
    def __init__(self):
        self.pexels = PexelsService()
        self.stability = StabilityAIService()
        self.preferred_source = IMAGE_SOURCE
    
    def get_images_for_blog(self, topic: str, keywords: List[str],
                            count: int = 5) -> List[Dict[str, Any]]:
        """Get images for a blog post from configured source"""
        
        if self.preferred_source == "stability" and STABILITY_API_KEY:
            return self._get_stability_images(topic, count)
        else:
            return self._get_pexels_images(topic, keywords, count)
    
    def _get_stability_images(self, topic: str, count: int) -> List[Dict[str, Any]]:
        """Generate AI images"""
        descriptions = [
            f"Hero image representing {topic}",
            f"Concept illustration of {topic}",
            f"Infographic style visualization of {topic}",
            f"Abstract representation of {topic}",
            f"Modern design related to {topic}",
        ][:count]
        
        images = self.stability.generate_blog_images(topic, descriptions)
        
        # Fall back to Pexels if not enough images
        if len(images) < count:
            console.print("[yellow]Supplementing with Pexels images...[/yellow]")
            pexels_images = self._get_pexels_images(topic, [], count - len(images))
            images.extend(pexels_images)
        
        return images[:count]
    
    def _get_pexels_images(self, topic: str, keywords: List[str],
                           count: int) -> List[Dict[str, Any]]:
        """Get stock photos from Pexels"""
        images = []
        
        # Search by main topic
        topic_images = self.pexels.search_images(topic, per_page=count)
        images.extend(topic_images)
        
        # If not enough, search by keywords
        if len(images) < count and keywords:
            for keyword in keywords[:3]:
                if len(images) >= count:
                    break
                keyword_images = self.pexels.search_images(keyword, per_page=2)
                for img in keyword_images:
                    if img["id"] not in [i["id"] for i in images]:
                        images.append(img)
        
        return images[:count]
    
    def download_image(self, url: str, filename: Optional[str] = None,
                       folder: Optional[Path] = None) -> Optional[Path]:
        """Download an image to local storage"""
        try:
            folder = folder or IMAGES_DIR
            folder.mkdir(parents=True, exist_ok=True)
            
            if not filename:
                url_hash = hashlib.md5(url.encode()).hexdigest()[:10]
                ext = url.split(".")[-1].split("?")[0]
                if ext not in ["jpg", "jpeg", "png", "webp", "gif"]:
                    ext = "jpg"
                filename = f"image_{url_hash}.{ext}"
            
            filepath = folder / filename
            
            console.print(f"[blue]Downloading: {filename}[/blue]")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filepath
            
        except Exception as e:
            console.print(f"[red]Download error: {e}[/red]")
            return None


# Singleton
_image_instance = None

def get_image_service() -> ImageService:
    """Get or create the image service instance"""
    global _image_instance
    if _image_instance is None:
        _image_instance = ImageService()
    return _image_instance
