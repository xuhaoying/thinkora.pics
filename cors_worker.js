
// Cloudflare Worker代码
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // 获取原始响应
  const response = await fetch(request)
  
  // 创建新的响应，添加CORS头
  const newResponse = new Response(response.body, response)
  
  // 添加CORS头
  newResponse.headers.set('Access-Control-Allow-Origin', '*')
  newResponse.headers.set('Access-Control-Allow-Methods', 'GET, HEAD')
  newResponse.headers.set('Access-Control-Allow-Headers', '*')
  newResponse.headers.set('Access-Control-Max-Age', '3600')
  
  return newResponse
}
