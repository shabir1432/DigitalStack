'use client';

import Script from 'next/script';

interface GoogleAnalyticsProps {
    measurementId: string;
}

export default function GoogleAnalytics({ measurementId }: GoogleAnalyticsProps) {
    if (!measurementId) return null;

    return (
        <>
            <Script
                src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
                strategy="afterInteractive"
            />
            <Script id="google-analytics" strategy="afterInteractive">
                {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${measurementId}', {
            page_path: window.location.pathname,
          });
        `}
            </Script>
        </>
    );
}

// Track page views
export function trackPageView(url: string, measurementId: string) {
    if (typeof window !== 'undefined' && (window as any).gtag) {
        (window as any).gtag('config', measurementId, {
            page_path: url,
        });
    }
}

// Track custom events
export function trackEvent(action: string, category: string, label?: string, value?: number) {
    if (typeof window !== 'undefined' && (window as any).gtag) {
        (window as any).gtag('event', action, {
            event_category: category,
            event_label: label,
            value: value,
        });
    }
}
