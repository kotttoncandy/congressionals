import { json } from '@sveltejs/kit';
import { trails } from '$lib/trailData';

export async function GET({ url }) {
    const trail = url.searchParams.get('trail');
    console.log(trail)
    try {
        if (trail == null) {
            const response = await fetch(
                `https://hawaiitrails.ehawaii.gov/trails/api/trail`
            );
            const data = await response.json();
            return json(data);
        } else {
            const response = await fetch(
                `https://hawaiitrails.ehawaii.gov/trails/api/trail/${trail}`
            );
            console.log("trail")
            const data = await response.json();
            return json(data);
        }


    } catch (err) {
        console.log(error)
    }
}