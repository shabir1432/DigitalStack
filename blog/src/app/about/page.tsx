import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata = {
    title: 'About Us - DigitalStack',
    description: 'Learn more about our mission to provide cutting-edge insights into the world of technology.',
};

export default function About() {
    return (
        <div className="min-h-screen bg-[#0f172a]">
            <Header />

            <main className="pt-24 pb-16 px-6">
                <div className="max-w-4xl mx-auto space-y-16">

                    {/* Hero Section */}
                    <section className="text-center">
                        <h1 className="text-4xl md:text-5xl font-bold text-white mb-6">About Us</h1>
                        <p className="text-xl text-gray-400 leading-relaxed max-w-2xl mx-auto">
                            Welcome to <span className="text-indigo-400 font-semibold">DigitalStack</span>, your premier destination for in-depth analysis and expert perspectives on the ever-evolving landscape of technology.
                        </p>
                    </section>

                    {/* Mission Stats */}
                    <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="bg-white/5 p-8 rounded-2xl border border-white/10 text-center">
                            <span className="text-4xl font-bold text-indigo-400 block mb-2">500+</span>
                            <span className="text-gray-400 text-sm uppercase tracking-wider">Articles Published</span>
                        </div>
                        <div className="bg-white/5 p-8 rounded-2xl border border-white/10 text-center">
                            <span className="text-4xl font-bold text-purple-400 block mb-2">50k+</span>
                            <span className="text-gray-400 text-sm uppercase tracking-wider">Monthly Readers</span>
                        </div>
                        <div className="bg-white/5 p-8 rounded-2xl border border-white/10 text-center">
                            <span className="text-4xl font-bold text-emerald-400 block mb-2">Daily</span>
                            <span className="text-gray-400 text-sm uppercase tracking-wider">Updates</span>
                        </div>
                    </section>

                    {/* Our Story */}
                    <section className="space-y-6 text-gray-300 leading-relaxed text-lg">
                        <h2 className="text-3xl font-bold text-white">Our Mission</h2>
                        <p>
                            In a world saturated with information, clarity is power. At DigitalStack, we cut through the noise to bring you actionable insights on Digital Operations, Smart Living, and the Future of Work.
                        </p>
                        <p>
                            Whether you are a tech professional optimizing your workflow, a remote worker building the perfect setup, or a homeowner making your space smarter, we provide the expert guides you need to make informed decisions.
                        </p>
                    </section>

                    {/* Contact Section */}
                    <section id="contact" className="bg-gradient-to-br from-indigo-900/20 to-purple-900/20 p-8 md:p-12 rounded-3xl border border-white/10">
                        <div className="max-w-2xl mx-auto">
                            <h2 className="text-3xl font-bold text-white mb-4 text-center">Contact Us</h2>
                            <p className="text-gray-400 text-center mb-8">
                                Have a question, feedback, or looking for promotion opportunities? We'd love to hear from you.
                            </p>

                            <form
                                action="https://formsubmit.co/officialglobalnews24@gmail.com"
                                method="POST"
                                className="space-y-6"
                            >
                                {/* Honeypot for spam */}
                                <input type="text" name="_honey" style={{ display: 'none' }} />

                                {/* Disable Captcha */}
                                <input type="hidden" name="_captcha" value="false" />

                                {/* Next Page Redirect */}
                                <input type="hidden" name="_next" value="http://localhost:3000/about?success=true" />

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label htmlFor="name" className="text-sm font-medium text-gray-300">Name</label>
                                        <input
                                            type="text"
                                            id="name"
                                            name="name"
                                            required
                                            className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-500 transition-all"
                                            placeholder="Your Name"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label htmlFor="email" className="text-sm font-medium text-gray-300">Email</label>
                                        <input
                                            type="email"
                                            id="email"
                                            name="email"
                                            required
                                            className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-500 transition-all"
                                            placeholder="you@example.com"
                                        />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label htmlFor="subject" className="text-sm font-medium text-gray-300">Subject</label>
                                    <select
                                        id="subject"
                                        name="subject"
                                        required
                                        defaultValue=""
                                        className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white transition-all appearance-none"
                                    >
                                        <option value="" disabled>Select a topic</option>
                                        <option value="General Inquiry">General Inquiry</option>
                                        <option value="Promotion/Advertising">Promotion & Advertising</option>
                                        <option value="Feedback">Feedback</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>

                                <div className="space-y-2">
                                    <label htmlFor="message" className="text-sm font-medium text-gray-300">Message</label>
                                    <textarea
                                        id="message"
                                        name="message"
                                        rows={5}
                                        required
                                        className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-500 transition-all resize-none"
                                        placeholder="How can we help you?"
                                    ></textarea>
                                </div>

                                <div className="pt-2">
                                    <button
                                        type="submit"
                                        className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl shadow-lg shadow-indigo-500/25 transition-all transform hover:-translate-y-1"
                                    >
                                        Send Message
                                    </button>
                                </div>
                            </form>
                        </div>
                    </section>

                </div>
            </main>

            <Footer />
        </div>
    );
}
