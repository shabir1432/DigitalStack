'use client';

import { useState, useEffect } from 'react';
import { format } from 'date-fns';

const ADMIN_PASSWORD = 'trendpulse2026';

interface PostAnalytics {
    slug: string;
    fileName?: string;
    title: string;
    date: string;
    category: string;
    views: number;
    uniqueVisitors: number;
    avgTimeOnPage: number;
    bounceRate: number;
    shares: number;
    lastViewed?: string;
}

interface EditingPost {
    fileName: string;
    frontmatter: any;
    content: string;
}

export default function AnalyticsDashboard() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [posts, setPosts] = useState<PostAnalytics[]>([]);
    const [stats, setStats] = useState({
        totalViews: 0,
        totalPosts: 0,
        avgViews: 0,
        topPost: '',
        viewsToday: 0,
    });
    const [activeTab, setActiveTab] = useState<'analytics' | 'manage'>('analytics');
    const [editingPost, setEditingPost] = useState<EditingPost | null>(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const auth = sessionStorage.getItem('admin_auth');
        if (auth === 'true') {
            setIsAuthenticated(true);
            loadAnalytics();
        }
    }, []);

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        if (password === ADMIN_PASSWORD) {
            setIsAuthenticated(true);
            sessionStorage.setItem('admin_auth', 'true');
            setError('');
            loadAnalytics();
        } else {
            setError('Invalid password');
        }
    };

    const loadAnalytics = async () => {
        try {
            const res = await fetch('/api/analytics');
            const data = await res.json();

            // Get file names for each post
            const postsRes = await fetch('/api/posts');
            const postsData = await postsRes.json();

            const postsWithFiles = (data.posts || []).map((p: PostAnalytics) => {
                const match = postsData.posts?.find((pp: any) => pp.slug === p.slug);
                return { ...p, fileName: match?.fileName };
            });

            setPosts(postsWithFiles);
            setStats(data.stats || stats);
        } catch {
            console.error('Failed to load analytics');
        }
    };

    const handleEdit = async (post: PostAnalytics) => {
        if (!post.fileName) return;

        setLoading(true);
        try {
            const res = await fetch(`/api/posts?slug=${post.slug}`);
            const data = await res.json();
            setEditingPost({
                fileName: post.fileName,
                frontmatter: data.frontmatter,
                content: data.content,
            });
        } catch {
            setMessage('Failed to load post');
        }
        setLoading(false);
    };

    const handleSave = async () => {
        if (!editingPost) return;

        setLoading(true);
        try {
            const res = await fetch('/api/posts', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(editingPost),
            });

            if (res.ok) {
                setMessage('Post saved successfully!');
                setEditingPost(null);
                loadAnalytics();
            } else {
                setMessage('Failed to save post');
            }
        } catch {
            setMessage('Failed to save post');
        }
        setLoading(false);
        setTimeout(() => setMessage(''), 3000);
    };

    const handleDelete = async (post: PostAnalytics) => {
        if (!post.fileName) return;
        if (!confirm(`Delete "${post.title}"? This cannot be undone.`)) return;

        setLoading(true);
        try {
            const res = await fetch(`/api/posts?fileName=${encodeURIComponent(post.fileName)}`, {
                method: 'DELETE',
            });

            if (res.ok) {
                setMessage('Post deleted!');
                loadAnalytics();
            } else {
                setMessage('Failed to delete post');
            }
        } catch {
            setMessage('Failed to delete post');
        }
        setLoading(false);
        setTimeout(() => setMessage(''), 3000);
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
        sessionStorage.removeItem('admin_auth');
        setPassword('');
    };

    // Login Screen
    if (!isAuthenticated) {
        return (
            <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center px-6">
                <div className="glass-card p-8 w-full max-w-md">
                    <div className="text-center mb-8">
                        <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-violet-500 via-cyan-500 to-pink-500 flex items-center justify-center text-3xl">
                            🔒
                        </div>
                        <h1 className="text-2xl font-bold text-white">Admin Access</h1>
                        <p className="text-zinc-500 text-sm mt-2">Enter password to continue</p>
                    </div>

                    <form onSubmit={handleLogin}>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter password..."
                            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder:text-zinc-600 focus:outline-none focus:border-violet-500 mb-4"
                            autoFocus
                        />
                        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}
                        <button type="submit" className="w-full py-3 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-lg font-medium hover:from-violet-600 hover:to-purple-700 transition-all">
                            Access Dashboard
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    // Edit Modal
    if (editingPost) {
        return (
            <div className="min-h-screen bg-[#0a0a0f] p-6">
                <div className="max-w-4xl mx-auto">
                    <div className="flex items-center justify-between mb-6">
                        <h1 className="text-2xl font-bold text-white">✏️ Edit Post</h1>
                        <button onClick={() => setEditingPost(null)} className="text-zinc-400 hover:text-white">
                            ✕ Close
                        </button>
                    </div>

                    <div className="glass-card p-6 mb-6">
                        <h2 className="text-lg font-semibold text-white mb-4">Post Details</h2>

                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <label className="block text-sm text-zinc-400 mb-2">Title</label>
                                <input
                                    type="text"
                                    value={editingPost.frontmatter.title || ''}
                                    onChange={(e) => setEditingPost({
                                        ...editingPost,
                                        frontmatter: { ...editingPost.frontmatter, title: e.target.value }
                                    })}
                                    className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-violet-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm text-zinc-400 mb-2">Category</label>
                                <input
                                    type="text"
                                    value={editingPost.frontmatter.category || ''}
                                    onChange={(e) => setEditingPost({
                                        ...editingPost,
                                        frontmatter: { ...editingPost.frontmatter, category: e.target.value }
                                    })}
                                    className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-violet-500"
                                />
                            </div>
                        </div>

                        <div className="mb-4">
                            <label className="block text-sm text-zinc-400 mb-2">Description</label>
                            <input
                                type="text"
                                value={editingPost.frontmatter.description || ''}
                                onChange={(e) => setEditingPost({
                                    ...editingPost,
                                    frontmatter: { ...editingPost.frontmatter, description: e.target.value }
                                })}
                                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-violet-500"
                            />
                        </div>
                    </div>

                    <div className="glass-card p-6 mb-6">
                        <h2 className="text-lg font-semibold text-white mb-4">Content (Markdown)</h2>
                        <textarea
                            value={editingPost.content}
                            onChange={(e) => setEditingPost({ ...editingPost, content: e.target.value })}
                            rows={20}
                            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white font-mono text-sm focus:outline-none focus:border-violet-500"
                        />
                    </div>

                    <div className="flex gap-4">
                        <button
                            onClick={handleSave}
                            disabled={loading}
                            className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg font-medium hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50"
                        >
                            {loading ? 'Saving...' : '💾 Save Changes'}
                        </button>
                        <button
                            onClick={() => setEditingPost(null)}
                            className="px-6 py-3 bg-white/5 border border-white/10 text-zinc-400 rounded-lg hover:text-white hover:border-white/20 transition-all"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0f] p-6">
            {/* Header */}
            <div className="max-w-7xl mx-auto mb-8">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-white">📊 Admin Dashboard</h1>
                        <p className="text-zinc-500 mt-1">Manage your blog posts and view analytics</p>
                    </div>
                    <button onClick={handleLogout} className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-zinc-400 hover:text-white hover:border-white/20 transition-all">
                        Logout
                    </button>
                </div>
            </div>

            {/* Message Toast */}
            {message && (
                <div className="fixed top-6 right-6 px-6 py-3 bg-green-500 text-white rounded-lg shadow-lg z-50">
                    {message}
                </div>
            )}

            {/* Tabs */}
            <div className="max-w-7xl mx-auto mb-8">
                <div className="flex gap-2">
                    <button
                        onClick={() => setActiveTab('analytics')}
                        className={`px-6 py-3 rounded-lg font-medium transition-all ${activeTab === 'analytics'
                                ? 'bg-violet-500 text-white'
                                : 'bg-white/5 text-zinc-400 hover:text-white'
                            }`}
                    >
                        📈 Analytics
                    </button>
                    <button
                        onClick={() => setActiveTab('manage')}
                        className={`px-6 py-3 rounded-lg font-medium transition-all ${activeTab === 'manage'
                                ? 'bg-violet-500 text-white'
                                : 'bg-white/5 text-zinc-400 hover:text-white'
                            }`}
                    >
                        📝 Manage Posts
                    </button>
                </div>
            </div>

            {activeTab === 'analytics' ? (
                <>
                    {/* Stats Cards */}
                    <div className="max-w-7xl mx-auto mb-8">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <StatCard title="Total Views" value={stats.totalViews.toLocaleString()} icon="👁️" gradient="from-violet-500 to-purple-600" />
                            <StatCard title="Total Posts" value={stats.totalPosts.toString()} icon="📝" gradient="from-cyan-500 to-blue-600" />
                            <StatCard title="Avg Views/Post" value={stats.avgViews.toLocaleString()} icon="📈" gradient="from-pink-500 to-rose-600" />
                            <StatCard title="Views Today" value={stats.viewsToday?.toString() || '0'} icon="🔥" gradient="from-orange-500 to-amber-600" />
                        </div>
                    </div>

                    {/* Analytics Table */}
                    <div className="max-w-7xl mx-auto">
                        <div className="glass-card overflow-hidden">
                            <div className="p-6 border-b border-white/5">
                                <h2 className="text-xl font-bold text-white">Post Performance</h2>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="text-left text-sm text-zinc-500 border-b border-white/5">
                                            <th className="px-6 py-4 font-medium">Post</th>
                                            <th className="px-6 py-4 font-medium">Date</th>
                                            <th className="px-6 py-4 font-medium text-right">Views</th>
                                            <th className="px-6 py-4 font-medium text-right">Unique</th>
                                            <th className="px-6 py-4 font-medium text-right">Avg Time</th>
                                            <th className="px-6 py-4 font-medium text-right">Bounce</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {posts.map((post, index) => (
                                            <tr key={post.slug} className={`border-b border-white/5 hover:bg-white/5 ${index === 0 ? 'bg-violet-500/5' : ''}`}>
                                                <td className="px-6 py-4">
                                                    <div className="flex items-center gap-3">
                                                        {index === 0 && <span>👑</span>}
                                                        <span className="text-white font-medium line-clamp-1">{post.title}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 text-zinc-400">{post.date}</td>
                                                <td className="px-6 py-4 text-right font-mono text-white">{post.views}</td>
                                                <td className="px-6 py-4 text-right font-mono text-cyan-400">{post.uniqueVisitors || 0}</td>
                                                <td className="px-6 py-4 text-right font-mono text-zinc-400">
                                                    {Math.floor((post.avgTimeOnPage || 0) / 60)}m {(post.avgTimeOnPage || 0) % 60}s
                                                </td>
                                                <td className="px-6 py-4 text-right">
                                                    <span className={`font-mono ${post.bounceRate < 30 ? 'text-green-400' : post.bounceRate < 50 ? 'text-yellow-400' : 'text-red-400'}`}>
                                                        {post.bounceRate || 0}%
                                                    </span>
                                                </td>
                                            </tr>
                                        ))}
                                        {posts.length === 0 && (
                                            <tr>
                                                <td colSpan={6} className="px-6 py-12 text-center text-zinc-500">
                                                    No posts yet. Generate content to see analytics.
                                                </td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </>
            ) : (
                /* Manage Posts Tab */
                <div className="max-w-7xl mx-auto">
                    <div className="glass-card overflow-hidden">
                        <div className="p-6 border-b border-white/5 flex items-center justify-between">
                            <h2 className="text-xl font-bold text-white">All Posts ({posts.length})</h2>
                            <button onClick={loadAnalytics} className="text-sm text-violet-400 hover:text-violet-300">
                                🔄 Refresh
                            </button>
                        </div>

                        <div className="divide-y divide-white/5">
                            {posts.map((post) => (
                                <div key={post.slug} className="p-6 flex items-center justify-between hover:bg-white/5 transition-colors">
                                    <div className="flex-1 min-w-0 mr-4">
                                        <h3 className="text-white font-medium truncate">{post.title}</h3>
                                        <div className="flex items-center gap-4 mt-1 text-sm text-zinc-500">
                                            <span>{post.date}</span>
                                            <span className="px-2 py-0.5 bg-violet-500/20 text-violet-400 rounded text-xs">
                                                {post.category || 'General'}
                                            </span>
                                            <span>{post.views} views</span>
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-2">
                                        <a
                                            href={`/blog/${post.slug}`}
                                            target="_blank"
                                            className="px-3 py-2 text-sm bg-white/5 text-zinc-400 rounded-lg hover:text-white hover:bg-white/10 transition-all"
                                        >
                                            👁️ View
                                        </a>
                                        <button
                                            onClick={() => handleEdit(post)}
                                            className="px-3 py-2 text-sm bg-cyan-500/20 text-cyan-400 rounded-lg hover:bg-cyan-500/30 transition-all"
                                        >
                                            ✏️ Edit
                                        </button>
                                        <button
                                            onClick={() => handleDelete(post)}
                                            className="px-3 py-2 text-sm bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-all"
                                        >
                                            🗑️ Delete
                                        </button>
                                    </div>
                                </div>
                            ))}

                            {posts.length === 0 && (
                                <div className="p-12 text-center text-zinc-500">
                                    No posts yet. Run the blog generator to create content.
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Footer */}
            <div className="max-w-7xl mx-auto mt-8 text-center text-zinc-600 text-sm">
                <p>Last updated: {format(new Date(), 'MMM d, yyyy HH:mm')}</p>
            </div>
        </div>
    );
}

function StatCard({ title, value, icon, gradient }: { title: string; value: string; icon: string; gradient: string }) {
    return (
        <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
                <span className="text-sm text-zinc-500">{title}</span>
                <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${gradient} flex items-center justify-center text-lg`}>{icon}</div>
            </div>
            <div className="text-3xl font-bold text-white">{value}</div>
        </div>
    );
}
