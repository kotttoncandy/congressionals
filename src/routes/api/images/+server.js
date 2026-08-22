import { json } from '@sveltejs/kit';
import { load } from 'cheerio';


export async function GET({ url }) {
    const query = url.searchParams.get('q');

    if (!query) {
        return json({ error: 'Missing query' }, { status: 400 });
    }

    try {
        const response = await fetch(
            `https://www.bing.com/images/search?q=${encodeURIComponent("basketball")}&first=1`,
            {
                headers: {
                    'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139.0.0.0 Safari/537.36'
                }
            }
        );

        const html = await response.text();

        const $ = load(html);

        

        return response
    } catch (err) {
        console.error(err);

        return json(
            { error: 'Failed to fetch Bing' },
            { status: 500 }
        );
    }
}