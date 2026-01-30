import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import html from 'remark-html';

// Try multiple possible post directories
const possiblePostsDirs = [
  path.join(process.cwd(), 'src/content/posts'),
  path.join(process.cwd(), '../data/posts'),
  path.join(process.cwd(), 'posts'),
];

function getPostsDirectory(): string {
  for (const dir of possiblePostsDirs) {
    if (fs.existsSync(dir)) {
      return dir;
    }
  }
  // Default to first option even if it doesn't exist yet
  return possiblePostsDirs[0];
}

export interface PostData {
  slug: string;
  title: string;
  date: string;
  description?: string;
  author?: string;
  tags?: string[];
  keywords?: string[];
  category?: string;
  featured?: boolean;
  image?: string;
  content?: string;
  contentHtml?: string;
}

export function getSortedPostsData(): PostData[] {
  const postsDirectory = getPostsDirectory();

  // Create directory if it doesn't exist
  if (!fs.existsSync(postsDirectory)) {
    fs.mkdirSync(postsDirectory, { recursive: true });
    return [];
  }

  // Get file names
  const fileNames = fs.readdirSync(postsDirectory);
  const allPostsData = fileNames
    .filter((fileName) => fileName.endsWith('.md'))
    .map((fileName, index) => {
      // Remove ".md" from file name to get slug
      const slug = fileName.replace(/\.md$/, '');

      // Read markdown file as string
      const fullPath = path.join(postsDirectory, fileName);
      const fileContents = fs.readFileSync(fullPath, 'utf8');

      // Use gray-matter to parse the post metadata section
      const matterResult = matter(fileContents);

      // Generate a stable image ID based on the title or slug
      const imageId = Math.abs(slug.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % 1000) + 100;

      // Generate a realistic author name based on slug hash
      const authorNames = ['James Wilson', 'Sarah Mitchell', 'Michael Chen', 'Emily Parker', 'David Brooks', 'Jessica Adams', 'Robert Taylor', 'Amanda Collins'];
      const authorIndex = Math.abs(slug.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)) % authorNames.length;
      const defaultAuthor = authorNames[authorIndex];

      // Combine the data with the slug
      return {
        slug,
        title: matterResult.data.title || slug,
        date: matterResult.data.date || '',
        description: matterResult.data.description || '',
        author: matterResult.data.author === 'AI Writer' ? defaultAuthor : (matterResult.data.author || defaultAuthor),
        tags: matterResult.data.tags || [],
        keywords: matterResult.data.keywords || [],
        category: matterResult.data.category || '',
        featured: matterResult.data.featured || false,
        image: matterResult.data.image || `https://picsum.photos/seed/${imageId}/800/600`,
      } as PostData;
    });

  // Sort posts by date
  return allPostsData.sort((a, b) => {
    if (a.date < b.date) {
      return 1;
    } else {
      return -1;
    }
  });
}

export function getAllPostSlugs() {
  const postsDirectory = getPostsDirectory();

  if (!fs.existsSync(postsDirectory)) {
    return [];
  }

  const fileNames = fs.readdirSync(postsDirectory);
  return fileNames
    .filter((fileName) => fileName.endsWith('.md'))
    .map((fileName) => {
      return {
        params: {
          slug: fileName.replace(/\.md$/, ''),
        },
      };
    });
}

export async function getPostData(slug: string): Promise<PostData | null> {
  const postsDirectory = getPostsDirectory();

  // First try direct file lookup
  let fullPath = path.join(postsDirectory, `${slug}.md`);

  // If not found, search by frontmatter slug or partial match
  if (!fs.existsSync(fullPath)) {
    const files = fs.readdirSync(postsDirectory).filter(f => f.endsWith('.md'));

    for (const fileName of files) {
      const filePath = path.join(postsDirectory, fileName);
      const content = fs.readFileSync(filePath, 'utf8');
      const { data } = matter(content);

      // Check if frontmatter slug matches or filename contains the slug
      if (data.slug === slug || fileName.includes(slug)) {
        fullPath = filePath;
        break;
      }
    }
  }

  if (!fs.existsSync(fullPath)) {
    return null;
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8');

  // Use gray-matter to parse the post metadata section
  const matterResult = matter(fileContents);

  // Use remark to convert markdown into HTML string
  const processedContent = await remark()
    .use(html, { sanitize: false })
    .process(matterResult.content);
  const contentHtml = processedContent.toString();

  // Use frontmatter slug if available, otherwise use the provided slug
  const finalSlug = matterResult.data.slug || slug;

  // Combine the data with the slug and contentHtml
  return {
    slug: finalSlug,
    contentHtml,
    content: matterResult.content,
    title: matterResult.data.title || finalSlug,
    date: matterResult.data.date || '',
    description: matterResult.data.description || '',
    author: matterResult.data.author || 'Editorial Team',
    tags: matterResult.data.tags || [],
    keywords: matterResult.data.keywords || [],
    category: matterResult.data.category || '',
    featured: matterResult.data.featured || false,
  };
}

export function getFeaturedPosts(limit: number = 3): PostData[] {
  const allPosts = getSortedPostsData();
  return allPosts.filter(post => post.featured).slice(0, limit);
}

export function getPostsByCategory(category: string): PostData[] {
  const allPosts = getSortedPostsData();
  return allPosts.filter(post =>
    post.category?.toLowerCase() === category.toLowerCase()
  );
}

export function getPostsByTag(tag: string): PostData[] {
  const allPosts = getSortedPostsData();
  return allPosts.filter(post =>
    post.tags?.some(t => t.toLowerCase() === tag.toLowerCase())
  );
}
