'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <header className="fixed top-0 left-0 right-0 z-50 header-glass">
            <div className="max-w-7xl mx-auto px-6">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2 md:gap-3 group">
                        <div className="relative w-8 h-8 md:w-10 md:h-10 transition-transform group-hover:scale-105">
                            <Image
                                src="/header-logo.jpeg"
                                alt="DigitalStack Logo"
                                width={40}
                                height={40}
                                className="rounded-xl shadow-lg shadow-indigo-500/20"
                            />
                        </div>
                        <span className="text-lg md:text-2xl font-bold text-white tracking-tight group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-indigo-400 group-hover:to-purple-400 transition-all">
                            Digital<span className="font-light text-indigo-400">Stack</span>
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex items-center gap-6">
                        <Link href="/" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">Home</Link>
                        <Link href="/blog" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">Articles</Link>
                        <Link href="/about" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">About</Link>
                        <Link href="/newsletter" className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white text-sm font-medium rounded-lg transition-all border border-white/5 backdrop-blur-sm">
                            Subscribe
                        </Link>
                    </nav>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="md:hidden p-2 text-gray-300 hover:text-white"
                    >
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            {mobileMenuOpen ? (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            ) : (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            )}
                        </svg>
                    </button>
                </div>

                {/* Mobile Menu */}
                {mobileMenuOpen && (
                    <div className="md:hidden py-4 border-t border-gray-800 bg-[#0f172a]">
                        <nav className="flex flex-col gap-2">
                            <Link href="/" className="px-4 py-2 text-gray-300 hover:bg-white/5 rounded-lg">Home</Link>
                            <Link href="/blog" className="px-4 py-2 text-gray-300 hover:bg-white/5 rounded-lg">Articles</Link>
                            <Link href="/about" className="px-4 py-2 text-gray-300 hover:bg-white/5 rounded-lg">About</Link>
                        </nav>
                    </div>
                )}
            </div>
        </header>
    );
}
