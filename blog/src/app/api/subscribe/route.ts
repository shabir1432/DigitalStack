import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { name, email } = body;

        if (!email || !name) {
            return NextResponse.json({ error: 'Name and Email are required' }, { status: 400 });
        }

        // Path to data directory (relative to project root in local dev)
        // Adjust path based on where you run 'next dev' from
        const dataDir = path.join(process.cwd(), '..', 'data');

        // Ensure data dir exists (Next.js runs in 'blog' dir, data is in parent)
        // Note: checking parent 'data' directory.
        if (!fs.existsSync(dataDir)) {
            return NextResponse.json({ error: 'Data configuration error' }, { status: 500 });
        }

        const filePath = path.join(dataDir, 'subscribers.json');

        // Read existing subscribers
        let subscribers = [];
        if (fs.existsSync(filePath)) {
            const fileContent = fs.readFileSync(filePath, 'utf-8');
            try {
                subscribers = JSON.parse(fileContent);
            } catch (e) {
                subscribers = [];
            }
        }

        // Check if email already exists
        const exists = subscribers.find((sub: any) => sub.email === email);
        if (exists) {
            return NextResponse.json({ message: 'Already subscribed!' }, { status: 200 });
        }

        // Add new subscriber
        const newSubscriber = {
            name,
            email,
            subscribedAt: new Date().toISOString()
        };

        subscribers.push(newSubscriber);

        // Save back to file
        fs.writeFileSync(filePath, JSON.stringify(subscribers, null, 2));

        return NextResponse.json({ message: 'Successfully subscribed!' }, { status: 200 });

    } catch (error) {
        console.error('Subscription error:', error);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
