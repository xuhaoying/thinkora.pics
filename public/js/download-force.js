// Enhanced download handler with server-side proxy fallback
(function() {
  // Force download function that works with cross-origin images
  async function forceDownload(url, filename) {
    try {
      // Method 1: Try blob download first (requires CORS)
      try {
        const response = await fetch(url, { mode: 'cors' });
        if (response.ok) {
          const blob = await response.blob();
          const blobUrl = window.URL.createObjectURL(blob);
          
          const a = document.createElement('a');
          a.href = blobUrl;
          a.download = filename || 'image.png';
          a.style.display = 'none';
          document.body.appendChild(a);
          a.click();
          
          setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(blobUrl);
          }, 100);
          
          return; // Success!
        }
      } catch (e) {
        console.log('Blob download failed, trying alternative methods...');
      }
      
      // Method 2: Create a canvas and convert to blob (works for images)
      try {
        const img = new Image();
        img.crossOrigin = 'anonymous'; // Try to enable CORS
        
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
          img.src = url;
        });
        
        // Create canvas and draw image
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        
        // Convert to blob and download
        canvas.toBlob(blob => {
          const blobUrl = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = blobUrl;
          a.download = filename || 'image.png';
          document.body.appendChild(a);
          a.click();
          
          setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(blobUrl);
          }, 100);
        }, 'image/png');
        
        return; // Success!
      } catch (e) {
        console.log('Canvas method failed, using final fallback...');
      }
      
      // Method 3: Use our download proxy endpoint
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        // For local development, skip proxy
        showDownloadInstructions(url, filename);
      } else {
        // For production, use the proxy
        const proxyUrl = `/api/download-proxy?url=${encodeURIComponent(url)}&filename=${encodeURIComponent(filename)}`;
        const a = document.createElement('a');
        a.href = proxyUrl;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
      
    } catch (error) {
      console.error('Download error:', error);
      showDownloadInstructions(url, filename);
    }
  }
  
  // Show download instructions modal
  function showDownloadInstructions(url, filename) {
    // Remove existing modal if any
    const existingModal = document.getElementById('download-modal');
    if (existingModal) {
      existingModal.remove();
    }
    
    // Create modal
    const modal = document.createElement('div');
    modal.id = 'download-modal';
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
      background: white;
      padding: 30px;
      border-radius: 10px;
      max-width: 500px;
      text-align: center;
      position: relative;
    `;
    
    content.innerHTML = `
      <h2 style="margin-bottom: 20px; color: #333;">下载说明</h2>
      <p style="margin-bottom: 20px; color: #666;">
        由于浏览器安全限制，请按以下步骤保存图片：
      </p>
      <ol style="text-align: left; margin-bottom: 20px; color: #666;">
        <li>点击下方按钮在新标签页打开图片</li>
        <li>右键点击图片</li>
        <li>选择"图片另存为..."或"Save image as..."</li>
        <li>选择保存位置并确认</li>
      </ol>
      <div style="margin-top: 20px;">
        <button onclick="window.open('${url}', '_blank'); document.getElementById('download-modal').remove();" 
                style="background: #007bff; color: white; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; margin-right: 10px;">
          在新标签页打开图片
        </button>
        <button onclick="document.getElementById('download-modal').remove();" 
                style="background: #6c757d; color: white; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer;">
          关闭
        </button>
      </div>
    `;
    
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    // Close on background click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });
  }
  
  // Override the existing download handler
  document.addEventListener('DOMContentLoaded', function() {
    // Handle download button
    const downloadButton = document.querySelector('.download-button');
    if (downloadButton) {
      downloadButton.addEventListener('click', function(e) {
        e.preventDefault();
        const url = this.getAttribute('href');
        const title = document.querySelector('h1').textContent || 'image';
        const filename = title.replace(/[^a-z0-9]/gi, '_').toLowerCase() + '.png';
        forceDownload(url, filename);
      });
    }

    // Handle image click download
    const imageLink = document.querySelector('.detail-image-wrapper a');
    if (imageLink) {
      imageLink.addEventListener('click', function(e) {
        e.preventDefault();
        const url = this.getAttribute('href');
        const title = this.getAttribute('title') || 'image';
        const filename = title.replace(/Click to download /i, '').replace(/[^a-z0-9]/gi, '_').toLowerCase() + '.png';
        forceDownload(url, filename);
      });
    }

    // Add visual feedback for clickable image
    const detailImage = document.querySelector('.detail-image-wrapper img');
    if (detailImage) {
      detailImage.style.cursor = 'pointer';
      detailImage.title = 'Click to download';
    }
  });
})();