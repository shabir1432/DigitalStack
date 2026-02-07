'use client';

import { useState } from 'react';

export default function NewsletterForm() {
    const [formData, setFormData] = useState({ name: '', email: '' });
    const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus('loading');

        try {
            const res = await fetch('/api/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (res.ok) {
                setStatus('success');
                setFormData({ name: '', email: '' });
            } else {
                setStatus('error');
            }
        } catch (error) {
            setStatus('error');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <input
                    type="text"
                    name="name"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-5 py-4 bg-black/40 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-500 transition-all text-center"
                    placeholder="First Name"
                />
            </div>
            <div>
                <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-5 py-4 bg-black/40 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-white placeholder-gray-500 transition-all text-center"
                    placeholder="Email Address"
                />
            </div>

            <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold rounded-xl shadow-lg shadow-indigo-500/25 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {status === 'loading' ? 'Joining...' : 'Join the Community'}
            </button>

            {status === 'success' && (
                <p className="text-emerald-400 text-sm mt-4 font-medium animate-fade-in">
                    🎉 Welcome aboard! Check your inbox soon.
                </p>
            )}
            {status === 'error' && (
                <p className="text-red-400 text-sm mt-4 font-medium animate-fade-in">
                    ❌ Something went wrong. Please try again.
                </p>
            )}

            <p className="text-xs text-gray-500 mt-4">
                No spam, ever. Unsubscribe at any time.
            </p>
        </form>
    );
}
