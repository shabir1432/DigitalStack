import Link from 'next/link';
import Image from 'next/image';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { getSortedPostsData } from '@/lib/posts';

export const metadata = {
  title: 'DigitalStack - Future Tech & Operations',
  description: 'Deep dives into Digital Operations, Remote Work, and Smart Technology.',
};

export default function Home() {
  const allPosts = getSortedPostsData();
  const featured = allPosts[0];
  const latestPosts = allPosts.slice(1, 4);
  const sidebarPosts = allPosts.slice(0, 5);
  const gridPosts = allPosts.slice(1, 3);

  return (
    <div className="min-h-screen">
      <Header />

      <main className="pt-20">
        {/* Hero Section */}
        <section className="px-6 py-12 relative overflow-hidden">
          {/* Background Glow */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-indigo-500/20 blur-[120px] rounded-full -z-10" />

          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left - Featured Article */}
              {featured ? (
                <Link href={`/blog/${featured.slug}`} className="group relative block h-[500px] rounded-2xl overflow-hidden shadow-2xl shadow-indigo-500/10 border border-white/10">
                  {/* Image Container */}
                  <div className="absolute inset-0">
                    <img
                      src={featured.image}
                      alt={featured.title}
                      className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#0f172a] via-[#0f172a]/60 to-transparent" />
                  </div>

                  {/* Content Overlay */}
                  <div className="absolute bottom-0 left-0 right-0 p-8">
                    <div className="flex items-center gap-3 mb-4">
                      <span className="badge">Featured</span>
                      <span className="text-white/70 text-sm font-medium">{featured.date}</span>
                    </div>

                    <h1 className="text-3xl md:text-5xl font-bold text-white leading-tight mb-4 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-indigo-200 transition-all">
                      {featured.title}
                    </h1>
                    <p className="text-gray-300 line-clamp-2 text-lg mb-6">
                      {featured.description || 'Discover the latest trending story that everyone is talking about.'}
                    </p>

                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 p-[2px]">
                        <div className="w-full h-full rounded-full bg-[#0f172a] flex items-center justify-center text-white text-xs font-bold">
                          {(featured.author || 'E')[0]}
                        </div>
                      </div>
                      <span className="text-white font-medium">{featured.author || 'Editorial Team'}</span>
                    </div>
                  </div>
                </Link>
              ) : (
                <EmptyHero />
              )}

              {/* Right - Grid of Posts */}
              <div className="grid grid-cols-1 gap-6">
                {gridPosts.length > 0 ? (
                  gridPosts.map((post, index) => (
                    <Link key={post.slug} href={`/blog/${post.slug}`} className="group relative flex h-[240px] rounded-2xl overflow-hidden border border-white/10 bg-white/5 hover:bg-white/10 transition-colors">
                      <div className="w-1/3 relative overflow-hidden">
                        <img
                          src={post.image}
                          alt={post.title}
                          className="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                        />
                      </div>
                      <div className="w-2/3 p-6 flex flex-col justify-center">
                        <span className="text-indigo-400 text-xs font-bold uppercase tracking-wider mb-2">{post.category || 'Tech'}</span>
                        <h3 className="text-xl font-bold text-white mb-2 leading-snug group-hover:text-indigo-300 transition-colors">
                          {post.title}
                        </h3>
                        <p className="text-gray-400 text-sm line-clamp-2">{post.description}</p>
                      </div>
                    </Link>
                  ))
                ) : null}

                {/* Category Card */}
                {gridPosts.length === 0 && (
                  <div className="bg-white/5 border border-white/10 rounded-2xl p-8 flex items-center justify-center text-center">
                    <div>
                      <span className="text-4xl mb-4 block">🚀</span>
                      <h3 className="text-white font-bold text-xl">Content Engine Running</h3>
                      <p className="text-gray-400">Generate more articles to fill this grid.</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* Latest Articles Section */}
        <section className="px-6 py-16">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-12">
              <h2 className="text-3xl font-bold text-white flex items-center gap-3">
                <span className="w-2 h-8 bg-indigo-500 rounded-full"></span>
                Latest Insights
              </h2>
              <Link href="/blog" className="text-indigo-400 hover:text-indigo-300 font-medium flex items-center gap-1">
                View All <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
              </Link>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
              {/* Main Content - Latest Articles */}
              <div className="lg:col-span-2 space-y-8">
                {latestPosts.length > 0 ? (
                  latestPosts.map((post) => (
                    <ArticleCard key={post.slug} post={post} />
                  ))
                ) : (
                  <EmptyArticles />
                )}
              </div>

              {/* Sidebar */}
              <aside className="lg:col-span-1 space-y-8">
                {/* About Card */}
                <div className="card p-6">
                  <div className="relative w-16 h-16 mx-auto mb-4 transition-transform hover:scale-105">
                    <Image
                      src="/header-logo.jpeg"
                      alt="DigitalStack Logo"
                      fill
                      className="object-contain rounded-2xl shadow-lg shadow-indigo-500/20"
                    />
                  </div>
                  <h3 className="font-bold text-white text-lg mb-2">DigitalStack</h3>
                  <p className="text-sm text-gray-400 mb-6 leading-relaxed">
                    Exploring the frontiers of Technology, Work Culture, and Smart Living. Expert insights daily.
                  </p>
                  <button className="w-full py-3 rounded-lg bg-white/5 hover:bg-white/10 text-white font-medium border border-white/10 transition-colors">
                    Follow Updates
                  </button>
                </div>

                {/* Trending List */}
                <div className="card p-6">
                  <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                    <span className="text-indigo-500">⚡</span> Trending Now
                  </h3>

                  <div className="space-y-4">
                    {sidebarPosts.map((post, index) => (
                      <Link key={post.slug} href={`/blog/${post.slug}`} className="flex gap-4 group">
                        <span className="text-4xl font-black text-white/5 group-hover:text-indigo-500/20 transition-colors">
                          0{index + 1}
                        </span>
                        <div>
                          <h4 className="text-sm font-semibold text-gray-200 group-hover:text-indigo-400 transition-colors line-clamp-2">
                            {post.title}
                          </h4>
                          <span className="text-xs text-gray-500 mt-1 block">{post.date}</span>
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
        <section className="px-6 py-16 bg-white/5 border-t border-white/5">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-12">
              <span className="text-indigo-400 font-bold tracking-wider text-xs uppercase mb-2 block">Explore Topics</span>
              <h2 className="text-3xl font-bold text-white">Curated Collections</h2>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <CategoryCard icon="🤖" title="Digital Ops" count={12} bg="from-blue-500/20 to-cyan-500/20" />
              <CategoryCard icon="🧠" title="Generative Tech" count={8} bg="from-purple-500/20 to-pink-500/20" />
              <CategoryCard icon="🏡" title="Smart Home" count={15} bg="from-emerald-500/20 to-teal-500/20" />
              <CategoryCard icon="💻" title="Remote Work" count={10} bg="from-orange-500/20 to-red-500/20" />
            </div>
          </div>
        </section>

        {/* Newsletter */}
        <section className="px-6 py-24 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-indigo-900/20" />
          <div className="max-w-2xl mx-auto text-center relative z-10">
            <div className="inline-block p-1 rounded-full bg-white/5 border border-white/10 mb-6">
              <div className="px-4 py-1 rounded-full bg-white/5 text-xs text-indigo-300 font-medium">
                Weekly Digest
              </div>
            </div>
            <h2 className="text-4xl font-bold text-white mb-4 tracking-tight">
              Stay Ahead of the Curve
            </h2>
            <p className="text-gray-400 mb-8 text-lg">
              Get the latest authority articles delivered to your inbox every morning. No spam, just value.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-5 py-3 rounded-lg bg-white/5 text-white border border-white/10 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 placeholder:text-gray-500"
              />
              <button className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-600/25">
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
    <Link href={`/blog/${post.slug}`} className="card group flex flex-col md:flex-row gap-6 p-5 hover:bg-white/5 transition-all">
      {/* Image */}
      <div className="w-full md:w-64 h-48 rounded-lg overflow-hidden flex-shrink-0 relative">
        <img
          src={post.image}
          alt={post.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        <div className="absolute top-3 left-3">
          <span className="px-2 py-1 bg-black/60 backdrop-blur-md text-white/90 text-xs font-bold rounded">{post.category || 'Tech'}</span>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 py-1">
        <div className="flex items-center gap-2 text-xs text-gray-500 mb-3">
          <span>{post.date}</span>
          <span>•</span>
          <span>{post.readTime || '5 min read'}</span>
        </div>
        <h3 className="text-2xl font-bold text-white mb-3 group-hover:text-indigo-400 transition-colors leading-snug">
          {post.title}
        </h3>
        <p className="text-gray-400 text-sm line-clamp-2 mb-4 leading-relaxed">
          {post.description || 'Discover the latest updates on this trending topic.'}
        </p>
        <span className="text-indigo-400 font-medium text-sm inline-flex items-center gap-1 group-hover:gap-2 transition-all">
          Read Article <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
        </span>
      </div>
    </Link>
  );
}

// Category Card Component
function CategoryCard({ icon, title, count, bg }: { icon: string; title: string; count: number; bg: string }) {
  return (
    <Link href="/blog" className={`group relative rounded-xl p-6 text-center border border-white/5 hover:border-white/20 transition-all overflow-hidden`}>
      <div className={`absolute inset-0 bg-gradient-to-br ${bg} opacity-0 group-hover:opacity-100 transition-opacity`} />
      <div className="relative z-10">
        <div className="w-14 h-14 mx-auto rounded-full bg-white/10 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <h3 className="font-bold text-white mb-1 group-hover:text-white transition-colors">{title}</h3>
        <p className="text-xs text-gray-500 group-hover:text-white/70">{count} articles</p>
      </div>
    </Link>
  );
}

// Empty States
function EmptyHero() {
  return (
    <div className="relative h-[450px] rounded-2xl overflow-hidden bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="text-center text-white p-8">
        <span className="text-6xl mb-4 block animate-pulse">⚡</span>
        <h2 className="text-2xl font-bold mb-2">Generating Content...</h2>
        <p className="text-gray-400">The AI is crafting the next viral hit.</p>
      </div>
    </div>
  );
}

function EmptyArticles() {
  return (
    <div className="bg-white/5 rounded-2xl p-12 text-center border border-white/10">
      <span className="text-4xl mb-4 block text-gray-600">📝</span>
      <h3 className="font-bold text-white mb-2">No Articles Yet</h3>
      <p className="text-gray-500 text-sm">Run the content generator to create articles.</p>
    </div>
  );
}
