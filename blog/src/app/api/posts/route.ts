import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const POSTS_DIR = path.join(process.cwd(), 'src/content/posts');

// GET all posts or a single post
export async function GET(request: Request) {
    try {
        const { searchParams } = new URL(request.url);
        const slug = searchParams.get('slug');

        if (!fs.existsSync(POSTS_DIR)) {
            return NextResponse.json({ posts: [] });
        }

        if (slug) {
            // Get single post
            const fileName = fs.readdirSync(POSTS_DIR).find(f => {
                const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf8');
                const { data } = matter(content);
                return data.slug === slug || f.replace('.md', '').includes(slug);
            });

            if (!fileName) {
                return NextResponse.json({ error: 'Post not found' }, { status: 404 });
            }

            const filePath = path.join(POSTS_DIR, fileName);
            const content = fs.readFileSync(filePath, 'utf8');
            const { data, content: body } = matter(content);

            return NextResponse.json({
                fileName,
                frontmatter: data,
                content: body,
            });
        }

        // Get all posts
        const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
        const posts = files.map(fileName => {
            const content = fs.readFileSync(path.join(POSTS_DIR, fileName), 'utf8');
            const { data } = matter(content);
            return {
                fileName,
                slug: data.slug || fileName.replace('.md', ''),
                title: data.title || 'Untitled',
                date: data.date,
                category: data.category,
            };
        });

        return NextResponse.json({ posts });
    } catch (error) {
        console.error('Error:', error);
        return NextResponse.json({ error: 'Failed to get posts' }, { status: 500 });
    }
}

// UPDATE a post
export async function PUT(request: Request) {
    try {
        const { fileName, frontmatter, content } = await request.json();

        if (!fileName) {
            return NextResponse.json({ error: 'fileName required' }, { status: 400 });
        }

        const filePath = path.join(POSTS_DIR, fileName);

        if (!fs.existsSync(filePath)) {
            return NextResponse.json({ error: 'Post not found' }, { status: 404 });
        }

        // Create new markdown content
        const newContent = matter.stringify(content || '', frontmatter || {});
        fs.writeFileSync(filePath, newContent, 'utf8');

        return NextResponse.json({ success: true, message: 'Post updated' });
    } catch (error) {
        console.error('Error:', error);
        return NextResponse.json({ error: 'Failed to update post' }, { status: 500 });
    }
}

// DELETE a post
export async function DELETE(request: Request) {
    try {
        const { searchParams } = new URL(request.url);
        const fileName = searchParams.get('fileName');

        if (!fileName) {
            return NextResponse.json({ error: 'fileName required' }, { status: 400 });
        }

        const filePath = path.join(POSTS_DIR, fileName);

        if (!fs.existsSync(filePath)) {
            return NextResponse.json({ error: 'Post not found' }, { status: 404 });
        }

        fs.unlinkSync(filePath);

        return NextResponse.json({ success: true, message: 'Post deleted' });
    } catch (error) {
        console.error('Error:', error);
        return NextResponse.json({ error: 'Failed to delete post' }, { status: 500 });
    }
}
