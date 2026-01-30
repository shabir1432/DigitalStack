import Link from 'next/link';
import Image from 'next/image';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSortedPostsData } from '@/lib/posts';

export const metadata = {
  title: 'TrendPulse - Blog & Magazine',
  description: 'Discover the latest trending topics and stories from around the world.',
};

export default function Home() {
  const allPosts = getSortedPostsData();
  const featured = allPosts[0];
  const latestPosts = allPosts.slice(1, 4);
  const sidebarPosts = allPosts.slice(0, 5);
  const gridPosts = allPosts.slice(1, 3);

  return (
    <div className="min-h-screen bg-white">
      <Header />

      <main className="pt-20">
        {/* Hero Section - Like Logen */}
        <section className="px-6 py-12">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left - Featured Article */}
              {featured ? (
                <Link href={`/blog/${featured.slug}`} className="group relative">
                  {/* Image Container */}
                  <div className="relative h-[450px] rounded-lg overflow-hidden">
                    <img
                      src={featured.image}
                      alt={featured.title}
                      className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />

                    {/* Author Avatar */}
                    <div className="absolute top-6 right-6 flex items-center gap-3 bg-white/90 backdrop-blur-sm rounded-full pl-1 pr-4 py-1">
                      <div className="w-8 h-8 rounded-full bg-[#1a4d3e] flex items-center justify-center text-white text-sm font-bold">
                        {(featured.author || 'E')[0]}
                      </div>
                      <span className="text-sm font-medium text-gray-800">{featured.author || 'Editorial'}</span>
                    </div>

                    {/* Content Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
                    <div className="absolute bottom-0 left-0 right-0 p-8">
                      <h1 className="text-3xl md:text-4xl font-bold text-white leading-tight mb-4 group-hover:underline decoration-2 underline-offset-4">
                        {featured.title}
                      </h1>
                      <p className="text-white/80 line-clamp-2 mb-4">
                        {featured.description || 'Discover the latest trending story that everyone is talking about.'}
                      </p>
                    </div>
                  </div>
                </Link>
              ) : (
                <EmptyHero />
              )}

              {/* Right - Grid of Posts */}
              <div className="grid grid-cols-2 gap-4">
                {gridPosts.length > 0 ? (
                  gridPosts.map((post, index) => (
                    <Link key={post.slug} href={`/blog/${post.slug}`} className="group">
                      <div className="relative h-[220px] rounded-lg overflow-hidden">
                        <img
                          src={post.image}
                          alt={post.title}
                          className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
                        <div className="absolute bottom-0 left-0 right-0 p-4">
                          <h3 className="text-white font-semibold line-clamp-2 group-hover:underline">
                            {post.title}
                          </h3>
                        </div>
                      </div>
                    </Link>
                  ))
                ) : null}

                {/* Category Card */}
                <div className="col-span-2 bg-gray-50 rounded-lg p-6">
                  <span className="subtitle">Explore</span>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">Trending Topics</h3>
                  <div className="flex items-center gap-4">
                    <div className="w-px h-8 bg-gray-300" />
                    <p className="text-gray-500 text-sm">
                      Discover trending stories from technology, sports, entertainment and more.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Latest Articles Section */}
        <section className="px-6 py-16 bg-white">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
              {/* Main Content - Latest Articles */}
              <div className="lg:col-span-2">
                <div className="mb-8">
                  <span className="subtitle">Recent Posts</span>
                  <h2 className="text-3xl font-bold text-gray-900 section-title">Latest Articles</h2>
                </div>

                <div className="space-y-8">
                  {latestPosts.length > 0 ? (
                    latestPosts.map((post) => (
                      <ArticleCard key={post.slug} post={post} />
                    ))
                  ) : (
                    <EmptyArticles />
                  )}
                </div>
              </div>

              {/* Sidebar */}
              <aside className="lg:col-span-1">
                {/* Author Card */}
                <div className="bg-gray-50 rounded-lg p-6 mb-8 text-center">
                  <div className="w-20 h-20 mx-auto rounded-full bg-[#1a4d3e] flex items-center justify-center text-white text-2xl font-bold mb-4">
                    TP
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1">TrendPulse</h3>
                  <p className="text-sm text-gray-500 mb-4">Editorial Team</p>
                  <p className="text-sm text-gray-600">
                    Bringing you the latest trending stories from around the world.
                  </p>
                </div>

                {/* Posts List */}
                <div>
                  <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <span className="text-[#1a4d3e]">●</span> Popular Posts
                  </h3>

                  <div className="space-y-0">
                    {sidebarPosts.map((post, index) => (
                      <Link key={post.slug} href={`/blog/${post.slug}`} className="post-list-item group">
                        <div className="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0">
                          <img
                            src={post.image}
                            alt={post.title}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="text-sm font-semibold text-gray-900 line-clamp-2 group-hover:text-[#1a4d3e] transition-colors">
                            {post.title}
                          </h4>
                          <span className="text-xs text-gray-400 mt-1 block">{post.date}</span>
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              </aside>
            </div>
          </div>
        </section>

        {/* Categories Section */}
        <section className="px-6 py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-12">
              <span className="subtitle">Explore</span>
              <h2 className="text-3xl font-bold text-gray-900">Popular Categories</h2>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <CategoryCard icon="💻" title="Technology" count={12} />
              <CategoryCard icon="⚽" title="Sports" count={8} />
              <CategoryCard icon="🎬" title="Entertainment" count={15} />
              <CategoryCard icon="💰" title="Business" count={10} />
            </div>
          </div>
        </section>

        {/* Newsletter */}
        <section className="px-6 py-16 bg-[#1a4d3e]">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Subscribe to our Newsletter
            </h2>
            <p className="text-white/70 mb-8">
              Get the latest trending stories delivered to your inbox weekly.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-5 py-3 rounded-lg bg-white text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50"
              />
              <button className="px-6 py-3 bg-white text-[#1a4d3e] font-semibold rounded-lg hover:bg-gray-100 transition-colors">
                Subscribe
              </button>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

// Article Card Component with Image
function ArticleCard({ post }: { post: any }) {
  return (
    <Link href={`/blog/${post.slug}`} className="group flex gap-6">
      {/* Image */}
      <div className="w-64 h-44 rounded-lg overflow-hidden flex-shrink-0">
        <img
          src={post.image}
          alt={post.title}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
        />
      </div>

      {/* Content */}
      <div className="flex-1 py-2">
        <span className="badge mb-3">{post.category || 'Trending'}</span>
        <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-[#1a4d3e] transition-colors line-clamp-2">
          {post.title}
        </h3>
        <p className="text-gray-500 text-sm line-clamp-2 mb-4">
          {post.description || 'Discover the latest updates on this trending topic.'}
        </p>
        <span className="read-more">
          Read More
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </span>
      </div>
    </Link>
  );
}

// Category Card Component
function CategoryCard({ icon, title, count }: { icon: string; title: string; count: number }) {
  return (
    <Link href="/blog" className="group bg-white rounded-lg p-6 text-center hover:shadow-lg transition-shadow border border-gray-100">
      <div className="w-16 h-16 mx-auto rounded-full bg-[#1a4d3e]/10 flex items-center justify-center text-3xl mb-4 group-hover:bg-[#1a4d3e]/20 transition-colors">
        {icon}
      </div>
      <h3 className="font-bold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-500">{count} articles</p>
    </Link>
  );
}

// Empty States
function EmptyHero() {
  return (
    <div className="relative h-[450px] rounded-lg overflow-hidden bg-gradient-to-br from-[#1a4d3e] to-[#2d6a5a] flex items-center justify-center">
      <div className="text-center text-white p-8">
        <span className="text-6xl mb-4 block">📰</span>
        <h2 className="text-2xl font-bold mb-2">Coming Soon</h2>
        <p className="text-white/70">Fresh trending articles will appear here.</p>
      </div>
    </div>
  );
}

function EmptyArticles() {
  return (
    <div className="bg-gray-50 rounded-lg p-12 text-center">
      <span className="text-4xl mb-4 block">📝</span>
      <h3 className="font-bold text-gray-900 mb-2">No Articles Yet</h3>
      <p className="text-gray-500 text-sm">Run the content generator to create articles.</p>
    </div>
  );
}
