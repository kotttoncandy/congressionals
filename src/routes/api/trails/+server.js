import { json } from '@sveltejs/kit';
import { trails } from '$lib/trailData';

export async function GET() {
    try {
        const response = await fetch(
            'https://hawaiitrails.ehawaii.gov/trails/api/trail'
        );

        const data = await response.json();
        return json(data);
    } catch (err) {
        console.log(error)
    }
}