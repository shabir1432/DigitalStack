import Link from 'next/link';
import { format } from 'date-fns';

interface Post {
    slug: string;
    title: string;
    description?: string;
    date?: string;
    category?: string;
    author?: string;
}

interface PostCardProps {
    post: Post;
    featured?: boolean;
    index?: number;
}

export default function PostCard({ post, featured = false, index = 0 }: PostCardProps) {
    const date = post.date ? format(new Date(post.date), 'MMM d, yyyy') : '';

    if (featured) {
        return (
            <Link href={`/blog/${post.slug}`} className="group block">
                <article className="featured-glow relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#1a1a25] to-[#12121a] border border-white/10 p-8 md:p-10 min-h-[400px] flex flex-col justify-end shine">
                    {/* Background Pattern */}
                    <div className="absolute inset-0 bg-grid-pattern opacity-30" />

                    {/* Gradient Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0f] via-transparent to-transparent" />

                    {/* Floating Badge */}
                    <div className="absolute top-6 left-6">
                        <span className="badge">
                            ✨ Featured
                        </span>
                    </div>

                    {/* Content */}
                    <div className="relative z-10">
                        <div className="flex items-center gap-3 mb-4">
                            {post.category && (
                                <span className="px-3 py-1 text-xs font-semibold bg-violet-500/20 text-violet-400 rounded-full border border-violet-500/30">
                                    {post.category}
                                </span>
                            )}
                            {date && (
                                <span className="text-sm text-zinc-500">{date}</span>
                            )}
                        </div>

                        <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 group-hover:gradient-text transition-all duration-300 leading-tight">
                            {post.title}
                        </h2>

                        {post.description && (
                            <p className="text-zinc-400 mb-6 line-clamp-2 max-w-2xl">
                                {post.description}
                            </p>
                        )}

                        <div className="flex items-center gap-4">
                            <span className="flex items-center gap-2 text-sm font-semibold text-violet-400 group-hover:text-cyan-400 transition-colors">
                                Read Article
                                <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                </svg>
                            </span>
                        </div>
                    </div>

                    {/* Corner Glow */}
                    <div className="absolute -top-20 -right-20 w-40 h-40 bg-violet-500/20 rounded-full blur-3xl group-hover:bg-cyan-500/20 transition-colors duration-500" />
                </article>
            </Link>
        );
    }

    return (
        <Link
            href={`/blog/${post.slug}`}
            className="group block animate-fade-up"
            style={{ animationDelay: `${index * 0.1}s` }}
        >
            <article className="glass-card overflow-hidden h-full flex flex-col">
                {/* Top Gradient Bar */}
                <div className="h-1 bg-gradient-to-r from-violet-500 via-cyan-500 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                {/* Content */}
                <div className="p-6 flex flex-col flex-grow">
                    {/* Category & Date */}
                    <div className="flex items-center justify-between mb-4">
                        {post.category && (
                            <span className="badge text-xs">
                                {post.category}
                            </span>
                        )}
                        {date && (
                            <span className="text-xs text-zinc-500">{date}</span>
                        )}
                    </div>

                    {/* Title */}
                    <h3 className="text-lg font-bold text-white mb-3 group-hover:text-violet-400 transition-colors line-clamp-2 leading-snug">
                        {post.title}
                    </h3>

                    {/* Description */}
                    {post.description && (
                        <p className="text-zinc-500 text-sm leading-relaxed mb-4 flex-grow line-clamp-3">
                            {post.description}
                        </p>
                    )}

                    {/* Read More */}
                    <div className="flex items-center gap-2 text-sm font-medium text-violet-400 group-hover:text-cyan-400 transition-colors mt-auto pt-4 border-t border-white/5">
                        <span>Read more</span>
                        <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                    </div>
                </div>
            </article>
        </Link>
    );
}
