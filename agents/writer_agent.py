"""
Writer Agent
Generates high-authority, SEO-optimized blog posts using Ranking Blueprints
"""
from typing import Dict, Any, List, Optional
import random
from agents.base_agent import BaseAgent
from config.settings import BLOG_NICHE, MIN_WORD_COUNT, MAX_WORD_COUNT, IMAGES_PER_POST, VIDEOS_PER_POST
from services.image_service import get_image_service
from services.seo_service import get_seo_service

class WriterAgent(BaseAgent):
    """Agent that writes high-authority blog posts"""
    
    def __init__(self):
        super().__init__(
            name="Writer Agent",
            description="Writing high-authority, SEO-optimized content"
        )
        self.image_service = get_image_service()
        self.seo_service = get_seo_service()
    
    async def run(
        self,
        topic: str,
        keywords: Dict[str, Any],
        niche: str,
        blueprint: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Write a complete blog post
        """
        self.log_start()
        
        # 1. Generate Blueprint if not provided
        if not blueprint:
            self.log("Generating Ranking Blueprint...")
            blueprint = self.seo_service.generate_ranking_blueprint(topic)
            
        self.log(f"Writing article based on blueprint: {blueprint.get('h1')}")

        # 2. Write Content
        system_prompt = self._get_authority_system_prompt(niche)
        
        prompt = f"""
        Write a comprehensive, high-authority blog post about: "{topic}"
        
        # Ranking Blueprint (Strictly Follow This Structure)
        Title (H1): {blueprint.get('h1')}
        Target Word Count: {blueprint.get('target_word_count')} words
        
        # Competitor Gaps to Fill (Make sure to cover these!)
        {blueprint.get('gaps', 'Detailed analysis and expert examples')}
        
        # Outline
        {self._format_outline(blueprint.get('outline', []))}
        
        # SEO Instructions
        - Primary Keyword: {keywords.get('primary', topic)}
        - LSI Keywords to use naturally: {", ".join(blueprint.get('lsi_keywords', []) or keywords.get('lsi', []))}
        - Featured Snippet: Write a clear, direct answer (40-60 words) for the question "{topic}" immediately after the first H2.
        
        # Formatting Rules
        - Use H2 for main sections, H3 for subsections.
        - NO fluff introductions ("In this digital age..."). Start with a "Hook" -> "Problem" -> "Solution".
        - EVERY section must have at least one list, table, or bolded key takeaway.
        - Cite (invented but realistic) data points where appropriate to demonstrate expertise.
        
        Return the Full Blog Post in Markdown format.
        """
        
        full_post = self.llm.generate(prompt, system_prompt=system_prompt, max_tokens=MAX_WORD_COUNT)
        
        # Strip markdown code blocks if present
        full_post = full_post.strip()
        if full_post.startswith("```markdown"):
            full_post = full_post.replace("```markdown", "", 1)
            if full_post.endswith("```"):
                full_post = full_post[:-3]
        elif full_post.startswith("```"):
            full_post = full_post.replace("```", "", 1)
            if full_post.endswith("```"):
                full_post = full_post[:-3]
        
        full_post = full_post.strip()
        
        # 3. Add Media (Images/Videos)
        self.log("Finding media assets...")
        images = await self._get_relevant_images(topic, niche)
        videos = [] 
        
        # 4. Final Polish (Insert Images)
        final_post = self._insert_media(full_post, images, videos)
        
        result = {
            "title": blueprint.get('h1') or topic,
            "full_post": final_post,
            "word_count": len(final_post.split()),
            "images": images,
            "videos": videos,
            "keywords": keywords,
            "frontmatter": {
                "title": blueprint.get('h1') or topic,
                "date": "2025-01-01", 
                "excerpt": self._generate_excerpt(full_post),
                "slug": self._generate_slug(blueprint.get('h1') or topic),
                "niche": niche,
                "author": self._get_author_persona(niche)
            }
        }
        
        self.log_complete()
        return result

    def _get_authority_system_prompt(self, niche: str) -> str:
        return f"""
        You are the Editor-in-Chief of a high-authority industry publication in the "{niche}" space.
        
        Your Goal: Write the single best, most detailed resource on the internet for the given topic.
        
        Tone & Style:
        - Expert, Authoritative, yet Accessible.
        - Data-driven and specific (avoid vague advice).
        - ZERO FLUFF. Do not use phrases like "Let's dive in", "In conclusion", "As we all know".
        - Use professional terminology appropriate for {niche}.
        
        Layout:
        - Short paragraphs (2-3 sentences max).
        - Frequent use of Bullet Points, Numbered Lists, and Comparison Tables.
        - **Bold** key concepts for skim-readers.
        """

    def _format_outline(self, outline: List[Dict]) -> str:
        text = ""
        for section in outline:
            text += f"- H2: {section.get('heading')}\n"
            for sub in section.get('subsections', []):
                text += f"  - H3: {sub}\n"
        return text

    def _generate_excerpt(self, text: str) -> str:
        # Simple extraction of first paragraph or meta description
        lines = text.split("\n")
        for line in lines:
            if line.strip() and not line.startswith("#"):
                return line[:160] + "..."
        return "Read this in-depth guide."

    def _generate_slug(self, title: str) -> str:
        import re
        # Lowercase
        slug = title.lower()
        # Remove special chars (keep only alphanumeric and spaces/hyphens)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        # Replace spaces with hyphens
        slug = slug.replace(" ", "-")
        # Collapse multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        # Strip leading/trailing hyphens
        return slug.strip("-")

    async def _get_relevant_images(self, topic: str, niche: str) -> List[Dict]:
        """Fetch high-quality images"""
        query = f"{niche} {topic}"
        return self.image_service.get_images_for_blog(topic=query, keywords=[], count=IMAGES_PER_POST)

    def _insert_media(self, content: str, images: List[Dict], videos: List[Dict]) -> str:
        """Insert images/videos into the markdown content"""
        paragraphs = content.split("\n\n")
        total_p = len(paragraphs)
        if not images:
            return content
            
        # Insert image every N paragraphs
        stride = max(2, total_p // (len(images) + 1))
        
        img_idx = 0
        new_content = []
        
        for i, p in enumerate(paragraphs):
            new_content.append(p)
            if i > 0 and i % stride == 0 and img_idx < len(images):
                img = images[img_idx]
                caption = img.get('alt', 'Image')
                md_image = f"\n![{caption}]({img['url']})\n*Image: {caption}*\n"
                new_content.append(md_image)
                img_idx += 1
                
        return "\n\n".join(new_content)

    def _get_author_persona(self, niche: str) -> str:
        personas = {
            "Digital Operations": "Dr. Alex Chen, Digital Systems Architect",
            "Professional Remote Work Setup": "Sarah Jenkins, Remote Work Consultant",
            "Sustainable Smart Home": "Marcus Green, LEED Certified Energy Auditor"
        }
        return personas.get(niche, "Editorial Team")
