// Vercel Edge Function for proxying image downloads
export const config = {
  runtime: 'edge',
};

export default async function handler(request) {
  const url = new URL(request.url);
  const imageUrl = url.searchParams.get('url');
  const filename = url.searchParams.get('filename') || 'download.png';
  
  if (!imageUrl) {
    return new Response('Missing image URL', { status: 400 });
  }
  
  try {
    // Validate that the URL is from our R2 bucket
    if (!imageUrl.startsWith('https://img.thinkora.pics/')) {
      return new Response('Invalid image URL', { status: 403 });
    }
    
    // Fetch the image from R2
    const imageResponse = await fetch(imageUrl);
    
    if (!imageResponse.ok) {
      return new Response('Failed to fetch image', { status: imageResponse.status });
    }
    
    // Get the image data
    const imageData = await imageResponse.arrayBuffer();
    
    // Return the image with download headers
    return new Response(imageData, {
      status: 200,
      headers: {
        'Content-Type': 'image/png',
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (error) {
    console.error('Download proxy error:', error);
    return new Response('Internal server error', { status: 500 });
  }
}