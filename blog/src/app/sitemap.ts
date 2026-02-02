import { MetadataRoute } from 'next';
import { getSortedPostsData } from '@/lib/posts';

// Revalidate sitemap every hour to pick up new blogs
export const revalidate = 3600;

// Helper to determine change frequency based on post age
function getChangeFrequency(postDate: Date): 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' {
  const now = new Date();
  const diffHours = (now.getTime() - postDate.getTime()) / (1000 * 60 * 60);

  if (diffHours < 24) return 'hourly';      // Posts < 24 hours old
  if (diffHours < 168) return 'daily';       // Posts < 7 days old
  if (diffHours < 720) return 'weekly';      // Posts < 30 days old
  return 'monthly';                           // Older posts
}

// Helper to determine priority based on post age (newer = higher priority)
function getPriority(postDate: Date): number {
  const now = new Date();
  const diffDays = (now.getTime() - postDate.getTime()) / (1000 * 60 * 60 * 24);

  if (diffDays < 1) return 0.9;              // Brand new posts
  if (diffDays < 7) return 0.8;               // This week's posts
  if (diffDays < 30) return 0.7;              // This month's posts
  return 0.6;                                  // Older posts
}

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://global-news-24.vercel.app';
  const posts = getSortedPostsData();

  // Generate sitemap entries for all blog posts with smart frequency/priority
  const blogPosts = posts.map((post) => {
    const postDate = new Date(post.date);
    return {
      url: `${baseUrl}/blog/${post.slug}`,
      lastModified: postDate,
      changeFrequency: getChangeFrequency(postDate),
      priority: getPriority(postDate),
    };
  });

  // Static pages - homepage and blog list update frequently with new content
  const staticPages = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'hourly' as const,  // Homepage shows latest posts
      priority: 1.0,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: new Date(),
      changeFrequency: 'hourly' as const,  // Blog list updates with every new post
      priority: 0.95,
    },
  ];

  return [...staticPages, ...blogPosts];
}
