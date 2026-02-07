import Header from '@/components/Header';
import Footer from '@/components/Footer';
import NewsletterForm from '@/components/NewsletterForm';

export const metadata = {
    title: 'Newsletter - DigitalStack',
    description: 'Subscribe to our weekly digest for the latest in tech and digital operations.',
};

export default function Newsletter() {
    return (
        <div className="min-h-screen bg-[#0f172a]">
            <Header />

            <main className="pt-24 pb-16 px-6">
                <div className="max-w-3xl mx-auto text-center">

                    {/* Hero Section */}
                    <section className="mb-16">
                        <span className="inline-block py-1 px-3 rounded-full bg-indigo-500/10 text-indigo-400 text-sm font-medium mb-6 border border-indigo-500/20">
                            Weekly Digest
                        </span>
                        <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
                            Stay Ahead of the <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Future</span>
                        </h1>
                        <p className="text-xl text-gray-400 leading-relaxed max-w-2xl mx-auto">
                            Join 50,000+ professionals who get our best insights on Digital Operations, Smart Tech, and Remote Work delivered straight to their inbox.
                        </p>
                    </section>

                    {/* Value Props */}
                    <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
                        <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                            <span className="text-3xl mb-4 block">🔥</span>
                            <h3 className="text-white font-bold mb-2">Trending Tech</h3>
                            <p className="text-sm text-gray-400">Curated news on the latest breakthroughs.</p>
                        </div>
                        <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                            <span className="text-3xl mb-4 block">🛠️</span>
                            <h3 className="text-white font-bold mb-2">Practical Guides</h3>
                            <p className="text-sm text-gray-400">Step-by-step tutorials for your workflow.</p>
                        </div>
                        <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                            <span className="text-3xl mb-4 block">🎁</span>
                            <h3 className="text-white font-bold mb-2">Exclusive Perks</h3>
                            <p className="text-sm text-gray-400">Early access to reports and resources.</p>
                        </div>
                    </section>

                    {/* Subscription Form */}
                    <section className="bg-gradient-to-b from-white/10 to-white/5 p-8 md:p-12 rounded-3xl border border-white/10 relative overflow-hidden">
                        {/* Background Glow */}
                        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-indigo-500/10 blur-[100px] rounded-full -z-10" />

                        <div className="max-w-md mx-auto relative z-10">
                            <h2 className="text-2xl font-bold text-white mb-6">Subscribe Now</h2>
                            <NewsletterForm />
                        </div>
                    </section>

                </div>
            </main>

            <Footer />
        </div>
    );
}
