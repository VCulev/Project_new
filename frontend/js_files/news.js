$(document).ready(async () => {
    try {
        const response = await fetch('http://localhost:4000/api/scrape-newsletter', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            const html = data.map(item => `
                <div class="newsletter-item bg-white rounded-lg shadow-md p-6 mb-4">
                    <h3 class="newsletter-item-title text-xl font-bold mb-2">${item.title}</h3>
                    <a href="${item.link}" class="newsletter-item-link text-blue-500 hover:text-blue-700" target="_blank">Read more</a>
                </div>
            `).join('');
            $('#newsletter-container').html(html);
        } else {
            throw new Error('Failed to fetch Stack Overflow questions');
        }
    } catch (error) {
        $('#newsletter-container').html(`<p class="text-red-500">Error: ${error.message}</p>`);
    }
});
