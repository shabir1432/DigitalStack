import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

// Path to view data
const DATA_DIR = path.join(process.cwd(), 'data');
const VIEWS_FILE = path.join(DATA_DIR, 'views.json');

interface ViewData {
    views: number;
    uniqueVisitors: string[];
    lastViewed: string;
    viewsByDate: { [date: string]: number };
    avgTimeOnPage: number;
    totalTimeSpent: number;
}

function loadViewData(): { [slug: string]: ViewData } {
    try {
        if (fs.existsSync(VIEWS_FILE)) {
            return JSON.parse(fs.readFileSync(VIEWS_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('Error loading view data:', e);
    }
    return {};
}

export async function GET() {
    try {
        const postsDirectory = path.join(process.cwd(), 'src/content/posts');
        const viewData = loadViewData();

        if (!fs.existsSync(postsDirectory)) {
            return NextResponse.json({ posts: [], stats: getEmptyStats() });
        }

        const fileNames = fs.readdirSync(postsDirectory);

        const posts = fileNames
            .filter(name => name.endsWith('.md'))
            .map(fileName => {
                const filePath = path.join(postsDirectory, fileName);
                const fileContent = fs.readFileSync(filePath, 'utf8');
                const { data } = matter(fileContent);

                const slug = data.slug || fileName.replace('.md', '');
                const postViews = viewData[slug] || {};

                // Use REAL data from view tracking
                return {
                    slug,
                    title: data.title || 'Untitled',
                    date: data.date || new Date().toISOString().split('T')[0],
                    category: data.category || 'General',
                    views: postViews.views || 0,
                    uniqueVisitors: (postViews.uniqueVisitors || []).length,
                    avgTimeOnPage: postViews.avgTimeOnPage || 0,
                    bounceRate: calculateBounceRate(postViews),
                    shares: 0, // Will implement later
                    viewsByDate: postViews.viewsByDate || {},
                    lastViewed: postViews.lastViewed || 'Never',
                    keywords: data.keywords || [],
                    tags: data.tags || [],
                };
            })
            .sort((a, b) => b.views - a.views);

        const totalViews = posts.reduce((sum, p) => sum + p.views, 0);
        const totalUniqueVisitors = posts.reduce((sum, p) => sum + p.uniqueVisitors, 0);
        const topPost = posts[0];

        // Calculate views today
        const today = new Date().toISOString().split('T')[0];
        const viewsToday = posts.reduce((sum, p) => sum + (p.viewsByDate[today] || 0), 0);

        const stats = {
            totalViews,
            totalPosts: posts.length,
            avgViews: posts.length > 0 ? Math.round(totalViews / posts.length) : 0,
            topPost: topPost?.title || '',
            totalUniqueVisitors,
            viewsToday,
        };

        return NextResponse.json({ posts, stats });
    } catch (error) {
        console.error('Analytics error:', error);
        return NextResponse.json({ posts: [], stats: getEmptyStats() });
    }
}

function calculateBounceRate(viewData: ViewData): number {
    // Bounce rate: visitors who spent less than 10 seconds
    if (!viewData.views || viewData.views === 0) return 0;
    if (!viewData.avgTimeOnPage) return 50; // Default if no time data

    // Lower avg time = higher bounce rate
    if (viewData.avgTimeOnPage < 10) return 70;
    if (viewData.avgTimeOnPage < 30) return 50;
    if (viewData.avgTimeOnPage < 60) return 35;
    return 25;
}

function getEmptyStats() {
    return {
        totalViews: 0,
        totalPosts: 0,
        avgViews: 0,
        topPost: '',
        totalUniqueVisitors: 0,
        viewsToday: 0,
    };
}
