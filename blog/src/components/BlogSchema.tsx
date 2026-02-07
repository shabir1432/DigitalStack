import Head from 'next/head';

interface BlogSchemaProps {
    title: string;
    description: string;
    slug: string;
    date: string;
    author: string;
    image: string;
    category?: string;
    keywords?: string[];
}

export default function BlogSchema({ title, description, slug, date, author, image, category, keywords }: BlogSchemaProps) {
    const baseUrl = 'https://global-news-24.vercel.app'; // Update this with actual URL
    const url = `${baseUrl}/blog/${slug}`;

    const schema = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        headline: title,
        description: description,
        image: image,
        datePublished: date,
        dateModified: date,
        author: {
            '@type': 'Person',
            name: author,
        },
        publisher: {
            '@type': 'Organization',
            name: 'AI Authority Blog',
            logo: {
                '@type': 'ImageObject',
                url: `${baseUrl}/header-logo.jpeg`, // Placeholder
            },
        },
        mainEntityOfPage: {
            '@type': 'WebPage',
            '@id': url,
        },
        keywords: keywords?.join(', ') || category || 'Tech',
    };

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
    );
}
