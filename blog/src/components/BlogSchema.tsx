'use client';

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

export default function BlogSchema({
    title,
    description,
    slug,
    date,
    author,
    image,
    category,
    keywords,
}: BlogSchemaProps) {
    const baseUrl = 'https://global-news-24.vercel.app';

    const jsonLd = {
        '@context': 'https://schema.org',
        '@type': 'NewsArticle',
        headline: title,
        description: description,
        image: image,
        datePublished: date,
        dateModified: date,
        author: {
            '@type': 'Person',
            name: author || 'Editorial Team',
        },
        publisher: {
            '@type': 'Organization',
            name: 'Global News 24',
            logo: {
                '@type': 'ImageObject',
                url: `${baseUrl}/logo.png`,
            },
        },
        mainEntityOfPage: {
            '@type': 'WebPage',
            '@id': `${baseUrl}/blog/${slug}`,
        },
        keywords: keywords?.join(', ') || category || 'news, trending',
        articleSection: category || 'News',
        url: `${baseUrl}/blog/${slug}`,
    };

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
    );
}
