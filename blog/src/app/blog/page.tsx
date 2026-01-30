import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSortedPostsData } from '@/lib/posts';

export const metadata = {
    title: 'All Articles - TrendPulse',
    description: 'Browse all trending articles and stories',
};

export default function BlogPage() {
    const posts = getSortedPostsData();
    const categories = [...new Set(posts.map(p => p.category || 'General'))];
    const featuredPost = posts[0];
    const otherPosts = posts.slice(1);

    return (
        <div className="min-h-screen bg-white">
            <Header />

            <main className="pt-20">
                {/* Page Header */}
                <section className="px-6 py-12 bg-gray-50">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center">
                            <span className="subtitle">Blog</span>
                            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mt-2 mb-4">
                                Latest Articles
                            </h1>
                            <p className="text-gray-500 max-w-lg mx-auto">
                                Explore our collection of {posts.length} trending articles from around the world.
                            </p>
                        </div>
                    </div>
                </section>

                {/* Categories */}
                <section className="px-6 py-6 border-b border-gray-100">
                    <div className="max-w-7xl mx-auto">
                        <div className="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-hide">
                            <button className="px-5 py-2 rounded-full text-sm font-medium bg-[#1a4d3e] text-white">
                                All
                            </button>
                            {categories.slice(0, 6).map((cat) => (
                                <button
                                    key={cat}
                                    className="px-5 py-2 rounded-full text-sm font-medium bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors whitespace-nowrap"
                                >
                                    {cat}
                                </button>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Featured Article */}
                {featuredPost && (
                    <section className="px-6 py-12">
                        <div className="max-w-7xl mx-auto">
                            <Link href={`/blog/${featuredPost.slug}`} className="group grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                                {/* Image */}
                                <div className="relative h-[350px] rounded-lg overflow-hidden">
                                    <img
                                        src={featuredPost.image}
                                        alt={featuredPost.title}
                                        className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                                    />
                                </div>

                                {/* Content */}
                                <div>
                                    <span className="badge mb-4">{featuredPost.category || 'Featured'}</span>
                                    <h2 className="text-3xl font-bold text-gray-900 mb-4 group-hover:text-[#1a4d3e] transition-colors">
                                        {featuredPost.title}
                                    </h2>
                                    <p className="text-gray-500 mb-6 line-clamp-3">
                                        {featuredPost.description || 'Discover the latest updates on this trending topic that everyone is talking about.'}
                                    </p>
                                    <div className="flex items-center gap-4 mb-6">
                                        <div className="w-10 h-10 rounded-full bg-[#1a4d3e] flex items-center justify-center text-white font-bold">
                                            {(featuredPost.author || 'E')[0]}
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-900 text-sm">{featuredPost.author || 'Editorial'}</p>
                                            <p className="text-gray-400 text-xs">{featuredPost.date} · 5 min read</p>
                                        </div>
                                    </div>
                                    <span className="read-more">
                                        Read Article
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                        </svg>
                                    </span>
                                </div>
                            </Link>
                        </div>
                    </section>
                )}

                {/* Articles Grid */}
                <section className="px-6 py-12 bg-gray-50">
                    <div className="max-w-7xl mx-auto">
                        <h2 className="text-2xl font-bold text-gray-900 mb-8 section-title">All Articles</h2>

                        {otherPosts.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                {otherPosts.map((post, index) => (
                                    <ArticleCard key={post.slug} post={post} />
                                ))}
                            </div>
                        ) : posts.length === 0 ? (
                            <EmptyState />
                        ) : null}
                    </div>
                </section>
            </main>

            <Footer />
        </div>
    );
}

function ArticleCard({ post }: { post: any }) {
    return (
        <Link href={`/blog/${post.slug}`} className="group card overflow-hidden">
            {/* Image */}
            <div className="relative h-48 overflow-hidden">
                <img
                    src={post.image}
                    alt={post.title}
                    className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
                <div className="absolute top-4 left-4">
                    <span className="badge">{post.category || 'News'}</span>
                </div>
            </div>

            {/* Content */}
            <div className="p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-[#1a4d3e] transition-colors line-clamp-2">
                    {post.title}
                </h3>
                <p className="text-gray-500 text-sm line-clamp-2 mb-4">
                    {post.description || 'Discover the latest updates on this trending topic.'}
                </p>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-xs font-bold text-gray-600">
                            {(post.author || 'E')[0]}
                        </div>
                        <span className="text-xs text-gray-500">{post.author || 'Editorial'}</span>
                    </div>
                    <span className="text-xs text-gray-400">{post.date}</span>
                </div>
            </div>
        </Link>
    );
}

function EmptyState() {
    return (
        <div className="bg-white rounded-lg border border-gray-200 p-16 text-center">
            <span className="text-6xl mb-6 block">📝</span>
            <h3 className="text-xl font-bold text-gray-900 mb-3">No Articles Yet</h3>
            <p className="text-gray-500 max-w-md mx-auto mb-6">
                Run the content generator to create trending articles.
            </p>
            <code className="inline-block px-4 py-2 bg-gray-100 rounded-lg text-[#1a4d3e] font-mono text-sm">
                python main.py --trending --publish
            </code>
        </div>
    );
}
