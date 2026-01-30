"""
Content Writer Agent
Responsible for writing comprehensive, SEO-optimized blog posts with media
"""
from typing import Dict, Any, List, Optional
import re
from datetime import datetime

from agents.base_agent import BaseAgent
from services.image_service import get_image_service
from services.youtube_service import get_youtube_service
from config.settings import BLOG_NICHE, MIN_WORD_COUNT, MAX_WORD_COUNT, IMAGES_PER_POST, VIDEOS_PER_POST


class WriterAgent(BaseAgent):
    """Agent that writes viral, SEO-optimized blog posts"""
    
    def __init__(self):
        super().__init__(
            name="Content Writer Agent",
            description="Writing viral blog posts optimized for search engines"
        )
        self.image_service = get_image_service()
        self.youtube_service = get_youtube_service()
    
    async def run(
        self,
        topic: str,
        keywords: Dict[str, Any],
        niche: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Write a comprehensive blog post optimized for viral potential
        
        Args:
            topic: Blog topic
            keywords: SEO keywords and meta data from KeywordAgent
            niche: Blog niche
            
        Returns:
            Complete blog post with media
        """
        self.log_start()
        niche = niche or BLOG_NICHE
        
        try:
            # Step 1: Write the blog post with SEO keywords
            self.log("Writing SEO-optimized blog post...")
            content = await self._write_viral_blog_post(topic, keywords)
            
            # Step 2: Get images for the post
            self.log("Fetching relevant images...")
            images = await self._get_images(topic, keywords)
            
            # Step 3: Get videos for the post
            self.log("Finding relevant videos...")
            videos = await self._get_videos(topic, keywords)
            
            # Step 4: Integrate media into content
            self.log("Integrating media into content...")
            final_content = await self._integrate_media(content, images, videos)
            
            # Step 5: Generate optimized frontmatter with featured image
            self.log("Generating SEO-optimized metadata...")
            frontmatter = self._generate_viral_frontmatter(topic, keywords)
            
            # Add featured image to frontmatter if available
            if images and len(images) > 0:
                frontmatter["image"] = images[0].get("url", "")
            
            # Combine everything
            full_post = f"""---
{self._format_frontmatter(frontmatter)}
---

{final_content}
"""
            
            result = {
                "topic": topic,
                "title": keywords.get("title", topic),
                "content": final_content,
                "full_post": full_post,
                "frontmatter": frontmatter,
                "images": images,
                "videos": videos,
                "word_count": len(final_content.split()),
                "keywords": keywords
            }
            
            self.log(f"Blog post complete: {result['word_count']} words, {len(images)} images, {len(videos)} videos")
            self.log_complete()
            return result
            
        except Exception as e:
            self.log(f"Error: {e}", "error")
            raise
    
    async def _write_viral_blog_post(self, topic: str, keywords: Dict[str, Any]) -> str:
        """Write a viral, SEO-optimized blog post using trending keywords"""
        
        system_prompt = """You are an expert viral content writer who creates engaging, SEO-optimized blog posts that RANK and get SHARED.

Your writing style is:
- Engaging with hooks that keep readers scrolling
- SEO optimized using trending keywords naturally
- Well-structured with scannable formatting
- Packed with value and actionable insights
- Written to encourage social sharing"""

        # Get all keyword data
        primary_keyword = keywords.get("primary_keyword", topic)
        secondary_keywords = keywords.get("secondary_keywords", [])
        long_tail = keywords.get("long_tail_keywords", [])
        hashtags = keywords.get("hashtags", [])
        suggested_headings = keywords.get("suggested_headings", [])
        viral_hooks = keywords.get("viral_hooks", [])
        google_suggestions = keywords.get("google_suggestions", [])
        
        headings_str = "\n".join([f"- {h}" for h in suggested_headings]) if suggested_headings else "Create SEO-optimized headings"
        hooks_str = "\n".join([f"- {h}" for h in viral_hooks]) if viral_hooks else ""

        prompt = f"""Write a VIRAL blog post about: {topic}

===== CRITICAL SEO KEYWORDS (USE THESE THROUGHOUT) =====
Primary Keyword: {primary_keyword}
Secondary Keywords (from Google Trends - MUST use at least 5): {', '.join(secondary_keywords[:10])}
Long-tail Keywords (use 3-5 naturally): {', '.join(long_tail[:8])}
Google Search Suggestions (people are searching these!): {', '.join(google_suggestions[:10])}

===== VIRAL TITLE =====
{keywords.get('title', topic)}

===== SUGGESTED HEADINGS =====
{headings_str}

===== OPENING HOOKS (use one) =====
{hooks_str}

===== HASHTAGS FOR POST =====
{' '.join(hashtags[:10])}

===== WRITING REQUIREMENTS =====

1. WORD COUNT: {MIN_WORD_COUNT}-{MAX_WORD_COUNT} words

2. SEO STRUCTURE:
   - Use the PRIMARY KEYWORD in the first 100 words
   - Use SECONDARY KEYWORDS in H2/H3 headings
   - Naturally weave LONG-TAIL KEYWORDS throughout
   - Use GOOGLE SUGGESTIONS as subheadings or in content
   
3. VIRAL FORMATTING:
   - Hook readers in the first sentence (curiosity, shock, or promise)
   - Use short paragraphs (2-3 sentences max)
   - Add bullet points and numbered lists
   - Include "Key Takeaway" boxes after sections
   - Add a "Quick Summary" or "TL;DR" at the start
   
4. CONTENT STRUCTURE:
   ## Quick Summary (TL;DR)
   - 3-4 bullet points summarizing the article
   
   ## Introduction (hook + what they'll learn)
   
   ## [Main Section 1 - Use keyword in heading]
   
   ## [Main Section 2 - Use keyword in heading]
   
   ## [Main Section 3 - Use keyword in heading]
   
   ## Key Statistics & Facts
   - Include 3-5 statistics or facts with sources
   
   ## Expert Tips & Recommendations
   
   ## Conclusion (summarize + strong CTA)
   
   ## Frequently Asked Questions
   - 5 questions using long-tail keywords
   
5. MEDIA PLACEHOLDERS:
   - Add [IMAGE: description] where images should go (5-6 throughout)
   - Add [VIDEO: topic] for video placement (1-2)

6. ENGAGEMENT ELEMENTS:
   - Ask questions to engage readers
   - Include quotable snippets for social sharing
   - Add actionable steps readers can take

Write the complete SEO-optimized blog post now:"""

        return self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )
    
    async def _get_images(self, topic: str, keywords: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch relevant images for the blog post"""
        
        search_terms = [topic]
        if keywords.get("secondary_keywords"):
            search_terms.extend(keywords["secondary_keywords"][:2])
        
        images = self.image_service.get_images_for_blog(
            topic=topic,
            keywords=keywords.get("secondary_keywords", []),
            count=IMAGES_PER_POST
        )
        
        return images
    
    async def _get_videos(self, topic: str, keywords: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find relevant YouTube videos"""
        
        videos = self.youtube_service.get_videos_for_blog(
            topic=topic,
            keywords=keywords.get("secondary_keywords", []),
            count=VIDEOS_PER_POST
        )
        
        return videos
    
    async def _integrate_media(
        self,
        content: str,
        images: List[Dict[str, Any]],
        videos: List[Dict[str, Any]]
    ) -> str:
        """Replace media placeholders with actual media"""
        
        # Replace image placeholders
        image_pattern = r'\[IMAGE:\s*([^\]]+)\]'
        image_matches = re.findall(image_pattern, content)
        
        for i, match in enumerate(image_matches):
            if i < len(images):
                img = images[i]
                img_markdown = f'''
![{img.get("alt", match)}]({img.get("url", "")})
*Photo by [{img.get("photographer", "Unknown")}]({img.get("photographer_url", "#")}) on Pexels*
'''
                content = content.replace(f"[IMAGE: {match}]", img_markdown, 1)
            else:
                content = content.replace(f"[IMAGE: {match}]", "", 1)
        
        # Replace video placeholders
        video_pattern = r'\[VIDEO:\s*([^\]]+)\]'
        video_matches = re.findall(video_pattern, content)
        
        for i, match in enumerate(video_matches):
            if i < len(videos):
                vid = videos[i]
                vid_markdown = vid.get("markdown", "")
                content = content.replace(f"[VIDEO: {match}]", vid_markdown, 1)
            else:
                content = content.replace(f"[VIDEO: {match}]", "", 1)
        
        return content
    
    def _generate_viral_frontmatter(self, topic: str, keywords: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SEO-optimized post frontmatter"""
        
        # Get all keywords for maximum SEO
        all_hashtags = keywords.get("hashtags", [])
        secondary_keywords = keywords.get("secondary_keywords", [])
        google_suggestions = keywords.get("google_suggestions", [])
        
        # Combine keywords for tags
        combined_tags = []
        for h in all_hashtags[:5]:
            clean = h.replace("#", "") if isinstance(h, str) else str(h)
            combined_tags.append(clean)
        
        # Use Google suggestions as additional keywords
        all_keywords = list(dict.fromkeys(secondary_keywords + google_suggestions))[:10]
        
        # Choose a realistic author name
        import random
        author_names = ['James Wilson', 'Sarah Mitchell', 'Michael Chen', 'Emily Parker', 'David Brooks', 'Jessica Adams', 'Robert Taylor', 'Amanda Collins', 'Christopher Lee', 'Rachel Green']
        author = random.choice(author_names)
        
        return {
            "title": keywords.get("title", topic),
            "description": keywords.get("meta_description", ""),
            "slug": keywords.get("slug", topic.lower().replace(" ", "-")),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "author": author,
            "tags": combined_tags,
            "keywords": all_keywords,
            "category": keywords.get("niche", BLOG_NICHE) or "trending",
            "featured": True,
            "draft": False
        }
    
    def _format_frontmatter(self, frontmatter: Dict[str, Any]) -> str:
        """Format frontmatter as YAML"""
        
        lines = []
        for key, value in frontmatter.items():
            if isinstance(value, list):
                if value:
                    lines.append(f"{key}:")
                    for item in value:
                        clean_item = item.replace("#", "") if isinstance(item, str) else item
                        lines.append(f"  - {clean_item}")
                else:
                    lines.append(f"{key}: []")
            elif isinstance(value, bool):
                lines.append(f"{key}: {str(value).lower()}")
            elif isinstance(value, str):
                escaped = value.replace('"', '\\"')
                lines.append(f'{key}: "{escaped}"')
            else:
                lines.append(f"{key}: {value}")
        
        return "\n".join(lines)
