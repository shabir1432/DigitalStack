import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// Path to store view data
const DATA_DIR = path.join(process.cwd(), 'data');
const VIEWS_FILE = path.join(DATA_DIR, 'views.json');

interface ViewData {
    [slug: string]: {
        views: number;
        uniqueVisitors: Set<string> | string[];
        lastViewed: string;
        viewsByDate: { [date: string]: number };
        avgTimeOnPage: number;
        totalTimeSpent: number;
    };
}

function ensureDataDir() {
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }
}

function loadViewData(): ViewData {
    try {
        ensureDataDir();
        if (fs.existsSync(VIEWS_FILE)) {
            const data = JSON.parse(fs.readFileSync(VIEWS_FILE, 'utf8'));
            return data;
        }
    } catch (e) {
        console.error('Error loading view data:', e);
    }
    return {};
}

function saveViewData(data: ViewData) {
    try {
        ensureDataDir();
        // Convert Sets to arrays for JSON serialization
        const serializable: any = {};
        for (const [slug, viewData] of Object.entries(data)) {
            serializable[slug] = {
                ...viewData,
                uniqueVisitors: Array.isArray(viewData.uniqueVisitors)
                    ? viewData.uniqueVisitors
                    : Array.from(viewData.uniqueVisitors || []),
            };
        }
        fs.writeFileSync(VIEWS_FILE, JSON.stringify(serializable, null, 2));
    } catch (e) {
        console.error('Error saving view data:', e);
    }
}

// Track a page view
export async function POST(request: Request) {
    try {
        const { slug, visitorId, timeSpent } = await request.json();

        if (!slug) {
            return NextResponse.json({ error: 'Slug required' }, { status: 400 });
        }

        const data = loadViewData();
        const today = new Date().toISOString().split('T')[0];

        if (!data[slug]) {
            data[slug] = {
                views: 0,
                uniqueVisitors: [],
                lastViewed: today,
                viewsByDate: {},
                avgTimeOnPage: 0,
                totalTimeSpent: 0,
            };
        }

        // Increment views
        data[slug].views += 1;
        data[slug].lastViewed = today;

        // Track by date
        data[slug].viewsByDate[today] = (data[slug].viewsByDate[today] || 0) + 1;

        // Track unique visitors
        if (visitorId) {
            const visitors = Array.isArray(data[slug].uniqueVisitors)
                ? data[slug].uniqueVisitors
                : [];
            if (!visitors.includes(visitorId)) {
                visitors.push(visitorId);
                data[slug].uniqueVisitors = visitors;
            }
        }

        // Track time spent
        if (timeSpent && timeSpent > 0) {
            data[slug].totalTimeSpent = (data[slug].totalTimeSpent || 0) + timeSpent;
            data[slug].avgTimeOnPage = Math.round(data[slug].totalTimeSpent / data[slug].views);
        }

        saveViewData(data);

        return NextResponse.json({
            success: true,
            views: data[slug].views
        });
    } catch (error) {
        console.error('Track view error:', error);
        return NextResponse.json({ error: 'Failed to track' }, { status: 500 });
    }
}

// Get view data for a specific post or all posts
export async function GET(request: Request) {
    try {
        const { searchParams } = new URL(request.url);
        const slug = searchParams.get('slug');

        const data = loadViewData();

        if (slug) {
            return NextResponse.json(data[slug] || { views: 0 });
        }

        // Return all view data
        return NextResponse.json(data);
    } catch (error) {
        console.error('Get views error:', error);
        return NextResponse.json({}, { status: 500 });
    }
}
