import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSortedPostsData } from '@/lib/posts';

export const metadata = {
    title: 'All Articles - Tech Authority Blog',
    description: 'Browse our complete collection of articles on Technology, Digital Trends, and Future Innovations.',
};

export default function BlogIndex() {
    const allPosts = getSortedPostsData();

    return (
        <div className="min-h-screen">
            <Header />

            <main className="pt-24 pb-16 px-6">
                <div className="max-w-7xl mx-auto">
                    {/* Page Header */}
                    <div className="mb-12 text-center">
                        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                            All Articles
                        </h1>
                        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
                            Explore our latest insights, tutorials, and deep dives into the world of future technology and digital innovation.
                        </p>
                    </div>

                    {/* Articles Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {allPosts.length > 0 ? (
                            allPosts.map((post) => (
                                <ArticleCard key={post.slug} post={post} />
                            ))
                        ) : (
                            <div className="col-span-full">
                                <EmptyArticles />
                            </div>
                        )}
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}

// Reuse Article Card Component
function ArticleCard({ post }: { post: any }) {
    return (
        <Link href={`/blog/${post.slug}`} className="card group flex flex-col overflow-hidden rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all h-full">
            {/* Image */}
            <div className="h-48 overflow-hidden relative">
                <img
                    src={post.image}
                    alt={post.title}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute top-3 left-3">
                    <span className="px-2 py-1 bg-black/60 backdrop-blur-md text-white/90 text-xs font-bold rounded">
                        {post.category || 'Tech'}
                    </span>
                </div>
            </div>

            {/* Content */}
            <div className="p-5 flex flex-col flex-1">
                <div className="flex items-center gap-2 text-xs text-gray-500 mb-3">
                    <span>{post.date}</span>
                    <span>•</span>
                    <span>{post.readTime || '5 min read'}</span>
                </div>
                <h3 className="text-xl font-bold text-white mb-3 group-hover:text-indigo-400 transition-colors leading-snug">
                    {post.title}
                </h3>
                <p className="text-gray-400 text-sm line-clamp-3 mb-4 leading-relaxed flex-1">
                    {post.description || 'Read full article...'}
                </p>
                <div className="mt-auto pt-4 border-t border-white/5">
                    <span className="text-indigo-400 font-medium text-sm inline-flex items-center gap-1 group-hover:gap-2 transition-all">
                        Read Article <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                    </span>
                </div>
            </div>
        </Link>
    );
}

function EmptyArticles() {
    return (
        <div className="bg-white/5 rounded-2xl p-12 text-center border border-white/10">
            <span className="text-4xl mb-4 block text-gray-600">📝</span>
            <h3 className="font-bold text-white mb-2">No Articles Yet</h3>
            <p className="text-gray-500 text-sm">Check back soon for new content.</p>
        </div>
    );
}
