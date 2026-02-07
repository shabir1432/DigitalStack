const fs = require('fs');
const path = require('path');

// Simulate the logic in lib/posts.ts
const postsDirectory = path.join(process.cwd(), 'src/content/posts');

console.log('Posts Directory:', postsDirectory);

if (!fs.existsSync(postsDirectory)) {
    console.error('Directory does not exist!');
    process.exit(1);
}

const fileNames = fs.readdirSync(postsDirectory);
console.log(`Found ${fileNames.length} files.`);

// Filter for the specific problematic file
const targetFile = fileNames.find(f => f.includes('maxwell'));
console.log('Target File:', targetFile);

if (targetFile) {
    const slug = targetFile.replace(/\.md$/, '');
    console.log('Derived Slug:', slug);

    // Simulate getPostData lookup
    const lookupPath = path.join(postsDirectory, `${slug}.md`);
    console.log('Lookup Path:', lookupPath);

    if (fs.existsSync(lookupPath)) {
        console.log('SUCCESS: File found via slug lookup.');

        // Try to read and parse
        try {
            const content = fs.readFileSync(lookupPath, 'utf8');
            console.log('File content length:', content.length);
            console.log('First 100 chars:', content.substring(0, 100));

            // Check for valid frontmatter fences
            if (!content.startsWith('---\n')) {
                console.error('ERROR: processed content does not start with frontmatter fence ---');
            } else {
                console.log('Frontmatter fence found.');
            }

            // Attempt to use gray-matter if available
            try {
                const matter = require('gray-matter');
                const parsed = matter(content);
                console.log('Gray-matter parsed successfully.');
                console.log('Title:', parsed.data.title);
            } catch (e) {
                console.log('Skipping gray-matter check (module might not be found mostly), but basic checks passed.');
            }

        } catch (err) {
            console.error('Error reading file:', err);
        }

        // Check for URI encoding issues
        const encodedSlug = encodeURIComponent(slug);
        console.log('Encoded Slug:', encodedSlug);

        if (slug !== encodedSlug) {
            console.log('WARNING: Slug contains encoded characters. Browser might request:', encodedSlug);
        }
    } else {
        console.error('FAILURE: File NOT found via slug lookup (this should likely not happen if we just derived it).');
    }
} else {
    console.error('Target file with "maxwell" not found in directory.');
}
