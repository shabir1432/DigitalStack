import { MetadataRoute } from 'next';
import { getSortedPostsData } from '@/lib/posts';

export default function sitemap(): MetadataRoute.Sitemap {
    const baseUrl = 'https://digitalstack.vercel.app';
    const allPosts = getSortedPostsData();

    const posts = allPosts.map((post) => ({
        url: `${baseUrl}/blog/${post.slug}`,
        lastModified: new Date(post.date).toISOString(),
        changeFrequency: 'weekly' as const,
        priority: 0.7,
    }));

    const routes = ['', '/blog', '/about', '/newsletter'].map((route) => ({
        url: `${baseUrl}${route}`,
        lastModified: new Date().toISOString(),
        changeFrequency: 'daily' as const,
        priority: 1.0,
    }));

    return [...routes, ...posts];
}
