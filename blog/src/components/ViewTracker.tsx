'use client';

import { useEffect, useRef } from 'react';

interface ViewTrackerProps {
    slug: string;
}

export default function ViewTracker({ slug }: ViewTrackerProps) {
    const startTime = useRef<number>(Date.now());
    const tracked = useRef<boolean>(false);

    useEffect(() => {
        // Generate or retrieve visitor ID
        let visitorId = localStorage.getItem('visitor_id');
        if (!visitorId) {
            visitorId = 'v_' + Math.random().toString(36).substr(2, 9) + Date.now();
            localStorage.setItem('visitor_id', visitorId);
        }

        // Track page view on mount (only once)
        if (!tracked.current) {
            tracked.current = true;

            fetch('/api/views', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slug, visitorId }),
            }).catch(() => { });
        }

        // Track time spent when leaving
        const handleBeforeUnload = () => {
            const timeSpent = Math.round((Date.now() - startTime.current) / 1000);

            // Use sendBeacon for reliable tracking on page exit
            if (navigator.sendBeacon) {
                navigator.sendBeacon('/api/views', JSON.stringify({
                    slug,
                    visitorId,
                    timeSpent,
                }));
            }
        };

        window.addEventListener('beforeunload', handleBeforeUnload);

        return () => {
            window.removeEventListener('beforeunload', handleBeforeUnload);
        };
    }, [slug]);

    return null;
}
