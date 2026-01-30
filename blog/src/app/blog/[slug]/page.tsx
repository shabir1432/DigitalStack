import Link from 'next/link';
import { notFound } from 'next/navigation';
import { format } from 'date-fns';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ViewTracker from '@/components/ViewTracker';
import { getPostData, getSortedPostsData } from '@/lib/posts';

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
    const posts = getSortedPostsData();
    return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: PageProps) {
    const { slug } = await params;
    try {
        const post = await getPostData(slug);
        return {
            title: `${post?.title || 'Post'} - TrendPulse`,
            description: post?.description,
        };
    } catch {
        return { title: 'Post Not Found - TrendPulse' };
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
        <div className="min-h-screen bg-white">
            <Header />
            <ViewTracker slug={slug} />

            <main className="pt-20">
                {/* Hero Image */}
                <section className="relative h-[400px] md:h-[500px]">
                    <img
                        src={postImage}
                        alt={post.title}
                        className="absolute inset-0 w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-black/20" />

                    {/* Content Overlay */}
                    <div className="absolute bottom-0 left-0 right-0 p-6 md:p-12">
                        <div className="max-w-4xl mx-auto">
                            {/* Breadcrumb */}
                            <div className="flex items-center gap-2 text-sm text-white/70 mb-6">
                                <Link href="/" className="hover:text-white transition-colors">Home</Link>
                                <span>/</span>
                                <Link href="/blog" className="hover:text-white transition-colors">Articles</Link>
                                <span>/</span>
                                <span className="text-white truncate max-w-[200px]">{post.title}</span>
                            </div>

                            {/* Category Badge */}
                            {post.category && (
                                <span className="inline-block px-4 py-1 bg-[#1a4d3e] text-white text-xs font-semibold uppercase tracking-wide rounded mb-4">
                                    {post.category}
                                </span>
                            )}

                            {/* Title */}
                            <h1 className="text-3xl md:text-5xl font-bold text-white mb-6 leading-tight">
                                {post.title}
                            </h1>

                            {/* Meta */}
                            <div className="flex flex-wrap items-center gap-6 text-sm text-white/80">
                                {post.author && (
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-[#1a4d3e] flex items-center justify-center text-white font-bold">
                                            {post.author[0]}
                                        </div>
                                        <span>{post.author}</span>
                                    </div>
                                )}
                                {formattedDate && (
                                    <span className="flex items-center gap-2">
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
                                        {formattedDate}
                                    </span>
                                )}
                                <span className="flex items-center gap-2">
                                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    5 min read
                                </span>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Article Content */}
                <article className="px-6 py-12">
                    <div className="max-w-3xl mx-auto">
                        {/* Description */}
                        {post.description && (
                            <p className="text-xl text-gray-600 mb-8 leading-relaxed border-l-4 border-[#1a4d3e] pl-6">
                                {post.description}
                            </p>
                        )}

                        {/* Content */}
                        <div
                            className="prose prose-lg max-w-none 
                                prose-headings:text-gray-900 prose-headings:font-bold
                                prose-h2:text-2xl prose-h2:mt-8 prose-h2:mb-4
                                prose-h3:text-xl prose-h3:mt-6 prose-h3:mb-3
                                prose-p:text-gray-600 prose-p:leading-relaxed prose-p:mb-6
                                prose-a:text-[#1a4d3e] prose-a:font-medium
                                prose-strong:text-gray-900
                                prose-ul:text-gray-600 prose-ol:text-gray-600
                                prose-li:mb-2
                                prose-blockquote:border-l-4 prose-blockquote:border-[#1a4d3e] prose-blockquote:pl-6 prose-blockquote:italic
                                prose-img:rounded-lg prose-img:shadow-md"
                            dangerouslySetInnerHTML={{ __html: post.contentHtml || '' }}
                        />
                    </div>
                </article>

                {/* Tags */}
                {post.tags && post.tags.length > 0 && (
                    <section className="px-6 pb-12">
                        <div className="max-w-3xl mx-auto">
                            <div className="border-t border-gray-200 pt-8">
                                <div className="flex flex-wrap items-center gap-3">
                                    <span className="text-sm font-semibold text-gray-500">Tags:</span>
                                    {post.tags.map((tag: string) => (
                                        <span
                                            key={tag}
                                            className="px-4 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-[#1a4d3e]/10 hover:text-[#1a4d3e] transition-colors cursor-pointer"
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
                        <div className="bg-gray-50 rounded-lg p-6 flex items-center gap-6">
                            <div className="w-16 h-16 rounded-full bg-[#1a4d3e] flex items-center justify-center text-white text-2xl font-bold flex-shrink-0">
                                {(post.author || 'E')[0]}
                            </div>
                            <div>
                                <h3 className="font-bold text-gray-900">{post.author || 'Editorial Team'}</h3>
                                <p className="text-sm text-gray-500 mt-1">
                                    Bringing you the latest trending stories from around the world.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Related Posts */}
                {relatedPosts.length > 0 && (
                    <section className="px-6 py-12 bg-gray-50">
                        <div className="max-w-7xl mx-auto">
                            <div className="mb-8">
                                <span className="subtitle">Keep Reading</span>
                                <h2 className="text-2xl font-bold text-gray-900 section-title">Related Articles</h2>
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
        <Link href={`/blog/${post.slug}`} className="group card overflow-hidden">
            <div className="relative h-48 overflow-hidden">
                <img
                    src={postImage}
                    alt={post.title}
                    className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
                <div className="absolute top-4 left-4">
                    <span className="badge">{post.category || 'News'}</span>
                </div>
            </div>
            <div className="p-5">
                <h3 className="font-bold text-gray-900 group-hover:text-[#1a4d3e] transition-colors line-clamp-2">
                    {post.title}
                </h3>
                <p className="text-sm text-gray-500 mt-2">{post.date}</p>
            </div>
        </Link>
    );
}
