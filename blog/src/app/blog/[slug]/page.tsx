import Link from 'next/link';
import { notFound } from 'next/navigation';
import { format } from 'date-fns';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ViewTracker from '@/components/ViewTracker';
import BlogSchema from '@/components/BlogSchema';
import { getPostData, getSortedPostsData } from '@/lib/posts';

// Revalidate pages every hour to pick up new content
export const revalidate = 3600;

// Allow new blog posts not generated at build time to be rendered on-demand
export const dynamicParams = true;

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
    const posts = getSortedPostsData();
    return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: PageProps) {
    const { slug } = await params;
    const baseUrl = 'https://global-news-24.vercel.app';

    try {
        const post = await getPostData(slug);
        const imageId = Math.abs(slug.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % 1000) + 100;
        const postImage = post?.image || `https://picsum.photos/seed/${imageId}/1200/600`;

        return {
            title: `${post?.title || 'Post'} - AI Authority Blog`,
            description: post?.description,
            keywords: post?.keywords?.join(', '),
            alternates: {
                canonical: `${baseUrl}/blog/${slug}`,
            },
            openGraph: {
                title: post?.title,
                description: post?.description,
                url: `${baseUrl}/blog/${slug}`,
                siteName: 'AI Authority Blog',
                images: [{ url: postImage, width: 1200, height: 630, alt: post?.title }],
                type: 'article',
                publishedTime: post?.date,
                authors: [post?.author || 'Editorial Team'],
            },
            twitter: {
                card: 'summary_large_image',
                title: post?.title,
                description: post?.description,
                images: [postImage],
            },
        };
    } catch {
        return { title: 'Post Not Found - AI Authority Blog' };
    }
}

export default async function BlogPost({ params }: PageProps) {
    const { slug } = await params;

    let post;
    try {
        post = await getPostData(slug);
    } catch {
        notFound();
    }

    if (!post) {
        notFound();
    }

    const allPosts = getSortedPostsData();
    const relatedPosts = allPosts
        .filter(p => p.slug !== slug)
        .slice(0, 3);

    const formattedDate = post.date
        ? format(new Date(post.date), 'MMMM d, yyyy')
        : '';

    // Generate image URL for this post
    const imageId = Math.abs(slug.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % 1000) + 100;
    const postImage = `https://picsum.photos/seed/${imageId}/1200/600`;

    return (
        <div className="min-h-screen">
            <Header />
            <ViewTracker slug={slug} />
            <BlogSchema
                title={post.title}
                description={post.description || ''}
                slug={slug}
                date={post.date}
                author={post.author || 'Editorial Team'}
                image={post.image || postImage}
                category={post.category}
                keywords={post.keywords}
            />

            <main className="pt-20">
                {/* Hero Image */}
                <section className="relative h-[400px] md:h-[500px]">
                    <img
                        src={postImage}
                        alt={post.title}
                        className="absolute inset-0 w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#0f172a] via-[#0f172a]/80 to-[#0f172a]/20" />

                    {/* Content Overlay */}
                    <div className="absolute bottom-0 left-0 right-0 p-6 md:p-12">
                        <div className="max-w-4xl mx-auto">
                            {/* Breadcrumb */}
                            <div className="flex items-center gap-2 text-sm text-gray-400 mb-6">
                                <Link href="/" className="hover:text-white transition-colors">Home</Link>
                                <span>/</span>
                                <Link href="/blog" className="hover:text-white transition-colors">Articles</Link>
                                <span>/</span>
                                <span className="text-white truncate max-w-[200px]">{post.title}</span>
                            </div>

                            {/* Category Badge */}
                            {post.category && (
                                <span className="inline-block px-4 py-1 bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-xs font-bold uppercase tracking-wide rounded-full mb-4 backdrop-blur-md">
                                    {post.category}
                                </span>
                            )}

                            {/* Title */}
                            <h1 className="text-3xl md:text-5xl font-bold text-white mb-6 leading-tight text-glow">
                                {post.title}
                            </h1>

                            {/* Meta */}
                            <div className="flex flex-wrap items-center gap-6 text-sm text-gray-300">
                                {post.author && (
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 p-[2px]">
                                            <div className="w-full h-full rounded-full bg-[#0f172a] flex items-center justify-center text-white font-bold">
                                                {post.author[0]}
                                            </div>
                                        </div>
                                        <span className="font-medium text-white">{post.author}</span>
                                    </div>
                                )}
                                {formattedDate && (
                                    <span className="flex items-center gap-2">
                                        <svg className="w-4 h-4 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
                                        {formattedDate}
                                    </span>
                                )}
                                <span className="flex items-center gap-2">
                                    <svg className="w-4 h-4 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    5 min read
                                </span>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Article Content */}
                <article className="px-6 py-12 relative">
                    {/* Background Glow */}
                    <div className="absolute top-20 right-0 w-[500px] h-[500px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none" />

                    <div className="max-w-3xl mx-auto relative z-10">
                        {/* Description */}
                        {post.description && (
                            <p className="text-xl text-gray-300 mb-10 leading-relaxed pl-6 border-l-4 border-indigo-500 italic">
                                {post.description}
                            </p>
                        )}

                        {/* Content */}
                        <div
                            className="prose prose-lg max-w-none 
                                prose-headings:text-white prose-headings:font-bold
                                prose-h2:text-3xl prose-h2:mt-12 prose-h2:mb-6 prose-h2:text-indigo-200
                                prose-h3:text-2xl prose-h3:mt-8 prose-h3:mb-4 prose-h3:text-white
                                prose-p:text-gray-300 prose-p:leading-8 prose-p:mb-6
                                prose-a:text-indigo-400 prose-a:font-medium hover:prose-a:text-indigo-300
                                prose-strong:text-white
                                prose-ul:text-gray-300 prose-ul:my-6
                                prose-li:mb-2 prose-li:marker:text-indigo-500
                                prose-blockquote:border-l-4 prose-blockquote:border-indigo-500 prose-blockquote:pl-6 prose-blockquote:italic prose-blockquote:text-gray-400 prose-blockquote:bg-white/5 prose-blockquote:py-4 prose-blockquote:pr-4 prose-blockquote:rounded-r-lg
                                prose-img:rounded-xl prose-img:shadow-2xl prose-img:shadow-indigo-500/10 prose-img:my-10 prose-img:border prose-img:border-white/10"
                            dangerouslySetInnerHTML={{ __html: post.contentHtml || '' }}
                        />
                    </div>
                </article>

                {/* Tags */}
                {post.tags && post.tags.length > 0 && (
                    <section className="px-6 pb-12">
                        <div className="max-w-3xl mx-auto">
                            <div className="border-t border-white/10 pt-8">
                                <div className="flex flex-wrap items-center gap-3">
                                    <span className="text-sm font-semibold text-gray-400">Tags:</span>
                                    {post.tags.map((tag: string) => (
                                        <span
                                            key={tag}
                                            className="px-4 py-1.5 text-sm bg-white/5 border border-white/10 text-gray-300 rounded-full hover:bg-indigo-500/20 hover:border-indigo-500/50 hover:text-white transition-all cursor-pointer"
                                        >
                                            #{tag}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </section>
                )}

                {/* Author Card */}
                <section className="px-6 pb-12">
                    <div className="max-w-3xl mx-auto">
                        <div className="card p-8 flex items-center gap-6">
                            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 p-[2px] flex-shrink-0">
                                <div className="w-full h-full rounded-full bg-[#0f172a] flex items-center justify-center text-white text-3xl font-bold">
                                    {(post.author || 'E')[0]}
                                </div>
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-white mb-2">{post.author || 'Editorial Team'}</h3>
                                <p className="text-gray-400 leading-relaxed">
                                    Expert insights from our dedicated editorial team, bringing you the latest in AI, technology, and future work trends.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Related Posts */}
                {relatedPosts.length > 0 && (
                    <section className="px-6 py-16 bg-white/5 border-t border-white/5">
                        <div className="max-w-7xl mx-auto">
                            <div className="mb-10 flex items-center gap-3">
                                <span className="text-2xl">📚</span>
                                <h2 className="text-2xl font-bold text-white">Keep Reading</h2>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                {relatedPosts.map((relatedPost) => (
                                    <RelatedPostCard key={relatedPost.slug} post={relatedPost} />
                                ))}
                            </div>
                        </div>
                    </section>
                )}
            </main>

            <Footer />
        </div>
    );
}

function RelatedPostCard({ post }: { post: any }) {
    // Generate image URL
    const imageId = Math.abs(post.slug.split('').reduce((acc: number, char: string) => acc + char.charCodeAt(0), 0) % 1000) + 100;
    const postImage = `https://picsum.photos/seed/${imageId}/600/400`;

    return (
        <Link href={`/blog/${post.slug}`} className="group card overflow-hidden hover:bg-white/10">
            <div className="relative h-48 overflow-hidden">
                <img
                    src={postImage}
                    alt={post.title}
                    className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute top-4 left-4">
                    <span className="px-2 py-1 bg-black/60 backdrop-blur-md text-white/90 text-xs font-bold rounded">
                        {post.category || 'News'}
                    </span>
                </div>
            </div>
            <div className="p-5">
                <h3 className="font-bold text-white group-hover:text-indigo-400 transition-colors line-clamp-2 mb-2">
                    {post.title}
                </h3>
                <p className="text-sm text-gray-500">{post.date}</p>
            </div>
        </Link>
    );
}
