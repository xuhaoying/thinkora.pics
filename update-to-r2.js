/**
 * 简单的脚本来更新index.html使用R2 URL
 * 运行: node update-to-r2.js
 */

const fs = require('fs');

// Cloudflare R2配置
const R2_PUBLIC_URL = 'https://your-r2-public-url.r2.dev';

// 更新metadata.json
function updateMetadata() {
    const metadata = JSON.parse(fs.readFileSync('metadata.json', 'utf8'));
    
    metadata.forEach(item => {
        const imageId = item.id.replace('unsplash_', '');
        const filename = `${imageId}.png`;
        const r2Url = `${R2_PUBLIC_URL}/images/${filename}`;
        
        item.urls = {
            thumbnail: r2Url,
            regular: r2Url,
            download: r2Url
        };
    });
    
    fs.writeFileSync('metadata.json', JSON.stringify(metadata, null, 2));
    console.log('✅ Updated metadata.json with R2 URLs');
}

// 运行更新
updateMetadata();