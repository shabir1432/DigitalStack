"""
YouTube Service
Searches for relevant videos using YouTube Data API or youtube-search-python
"""
from typing import List, Dict, Any, Optional
from youtubesearchpython import VideosSearch
from rich.console import Console

console = Console()


class YouTubeService:
    """Service for searching YouTube videos"""
    
    def __init__(self):
        pass
    
    def search_videos(
        self,
        query: str,
        limit: int = 5,
        region: str = "US",
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos
        
        Args:
            query: Search query
            limit: Number of videos to return
            region: Region code
            language: Language code
            
        Returns:
            List of video data
        """
        try:
            console.print(f"[blue]Searching YouTube videos for '{query}'...[/blue]")
            
            search = VideosSearch(query, limit=limit, region=region, language=language)
            results = search.result()
            
            videos = []
            for video in results.get("result", []):
                videos.append({
                    "id": video.get("id", ""),
                    "title": video.get("title", ""),
                    "description": video.get("descriptionSnippet", [{}])[0].get("text", "") if video.get("descriptionSnippet") else "",
                    "duration": video.get("duration", ""),
                    "views": video.get("viewCount", {}).get("text", ""),
                    "channel": video.get("channel", {}).get("name", ""),
                    "thumbnail": video.get("thumbnails", [{}])[0].get("url", "") if video.get("thumbnails") else "",
                    "link": video.get("link", ""),
                    "embed_url": f"https://www.youtube.com/embed/{video.get('id', '')}",
                    "published": video.get("publishedTime", "")
                })
            
            console.print(f"[green]Found {len(videos)} videos[/green]")
            return videos
            
        except Exception as e:
            console.print(f"[red]Error searching videos: {e}[/red]")
            return []
    
    def get_video_embed_html(
        self,
        video_id: str,
        width: int = 560,
        height: int = 315,
        title: str = "YouTube video"
    ) -> str:
        """
        Generate HTML embed code for a video
        
        Args:
            video_id: YouTube video ID
            width: Embed width
            height: Embed height
            title: Title for accessibility
            
        Returns:
            HTML embed code
        """
        return f'''<iframe 
    width="{width}" 
    height="{height}" 
    src="https://www.youtube.com/embed/{video_id}" 
    title="{title}" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
</iframe>'''
    
    def get_video_markdown(self, video_id: str, title: str = "Video") -> str:
        """
        Generate markdown for embedding a video
        
        Args:
            video_id: YouTube video ID
            title: Video title
            
        Returns:
            Markdown formatted video embed
        """
        return f'''
<div class="video-container">
<iframe width="100%" height="400" src="https://www.youtube.com/embed/{video_id}" title="{title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
'''
    
    def search_tutorial_videos(self, topic: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search for tutorial/how-to videos
        
        Args:
            topic: Topic to search tutorials for
            limit: Number of videos
            
        Returns:
            List of tutorial videos
        """
        return self.search_videos(f"{topic} tutorial how to", limit=limit)
    
    def search_explanation_videos(self, topic: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search for explanation/educational videos
        
        Args:
            topic: Topic to search
            limit: Number of videos
            
        Returns:
            List of explanation videos
        """
        return self.search_videos(f"{topic} explained", limit=limit)
    
    def get_videos_for_blog(
        self,
        topic: str,
        keywords: List[str],
        count: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Get relevant videos for a blog post
        
        Args:
            topic: Main blog topic
            keywords: Related keywords
            count: Number of videos to fetch
            
        Returns:
            List of videos with embed codes
        """
        videos = []
        
        # Search by main topic
        topic_videos = self.search_videos(topic, limit=count)
        videos.extend(topic_videos)
        
        # Add markdown embed to each video
        for video in videos:
            video["markdown"] = self.get_video_markdown(
                video["id"],
                video["title"]
            )
        
        return videos[:count]


# Singleton instance
_youtube_instance = None

def get_youtube_service() -> YouTubeService:
    """Get or create the YouTube service instance"""
    global _youtube_instance
    if _youtube_instance is None:
        _youtube_instance = YouTubeService()
    return _youtube_instance
