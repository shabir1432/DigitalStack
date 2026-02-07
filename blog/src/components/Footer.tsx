import Link from 'next/link';
import Image from 'next/image';

export default function Footer() {
    return (
        <footer className="footer-dark py-16">
            <div className="max-w-7xl mx-auto px-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
                    {/* Brand */}
                    <div className="md:col-span-1">
                        <Link href="/" className="flex items-center gap-2 mb-4 group">
                            <div className="relative w-8 h-8 transition-transform group-hover:scale-105">
                                <Image
                                    src="/header-logo.jpeg"
                                    alt="DigitalStack Logo"
                                    width={32}
                                    height={32}
                                    className="rounded-lg shadow-lg shadow-indigo-500/20"
                                />
                            </div>
                            <span className="text-xl font-bold text-white tracking-tight">
                                Digital<span className="font-light text-indigo-400">Stack</span>
                            </span>
                        </Link>
                        <p className="text-gray-400 text-sm mb-6 leading-relaxed">
                            Your definitive source for future tech insights, remote work strategies, and smart living technologies.
                        </p>
                        {/* Social Icons */}
                        <div className="flex items-center gap-3">
                            <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center text-gray-400 hover:bg-indigo-600 hover:text-white transition-all border border-white/5 hover:border-indigo-500 hover:shadow-lg hover:shadow-indigo-500/20">
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" /></svg>
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center text-gray-400 hover:bg-indigo-600 hover:text-white transition-all border border-white/5 hover:border-indigo-500 hover:shadow-lg hover:shadow-indigo-500/20">
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z" /></svg>
                            </a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="font-bold text-white mb-4">Quick Links</h4>
                        <ul className="space-y-3">
                            <li><Link href="/" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Home</Link></li>
                            <li><Link href="/blog" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Articles</Link></li>
                            <li><Link href="/blog" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Categories</Link></li>
                            <li><Link href="/blog" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Contact</Link></li>
                        </ul>
                    </div>

                    {/* Categories */}
                    <div>
                        <h4 className="font-bold text-white mb-4">Categories</h4>
                        <ul className="space-y-3">
                            <li><Link href="/blog" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Technology</Link></li>
                            <li><Link href="/blog" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Digital Ops</Link></li>
                            <li><Link href="/blog" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Smart Living</Link></li>
                            <li><Link href="/blog" className="text-gray-400 hover:text-indigo-400 text-sm transition-colors">Work Future</Link></li>
                        </ul>
                    </div>

                    {/* Newsletter */}
                    <div>
                        <h4 className="font-bold text-white mb-4">Newsletter</h4>
                        <p className="text-gray-400 text-sm mb-4">
                            Subscribe to get the latest news and updates.
                        </p>
                        <div className="flex gap-2">
                            <input
                                type="email"
                                placeholder="Your email"
                                className="flex-1 px-4 py-2 text-sm bg-white/5 border border-white/10 text-white rounded-lg focus:outline-none focus:border-indigo-500"
                            />
                            <button className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-500 transition-colors">
                                →
                            </button>
                        </div>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
                    <p className="text-gray-500 text-sm">
                        © {new Date().getFullYear()} DigitalStack. All rights reserved.
                    </p>
                    <div className="flex items-center gap-6">
                        <span className="text-gray-500 text-sm hover:text-indigo-400 cursor-pointer transition-colors">Privacy Policy</span>
                        <span className="text-gray-500 text-sm hover:text-indigo-400 cursor-pointer transition-colors">Terms of Service</span>
                    </div>
                </div>
            </div>
        </footer>
    );
}
