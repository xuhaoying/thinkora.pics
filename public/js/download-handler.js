// Download handler for cross-origin images
(function() {
  // Function to trigger download for cross-origin images
  async function downloadImage(url, filename) {
    try {
      // First try the simple download attribute method
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || 'image.png';
      a.target = '_blank';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      // For better UX, also try blob download in background
      // This will work if CORS is properly configured
      fetch(url, { mode: 'cors' })
        .then(response => response.blob())
        .then(blob => {
          const blobUrl = window.URL.createObjectURL(blob);
          const a2 = document.createElement('a');
          a2.href = blobUrl;
          a2.download = filename || 'image.png';
          document.body.appendChild(a2);
          a2.click();
          
          setTimeout(() => {
            document.body.removeChild(a2);
            window.URL.revokeObjectURL(blobUrl);
          }, 100);
        })
        .catch(err => {
          // Silently fail - the first method should have worked
          console.log('Blob download not available due to CORS:', err);
        });
      
    } catch (error) {
      console.error('Download failed:', error);
      // Ultimate fallback: open in new tab
      window.open(url, '_blank');
    }
  }

  // Add click handlers to download links and buttons
  document.addEventListener('DOMContentLoaded', function() {
    // Handle download button
    const downloadButton = document.querySelector('.download-button');
    if (downloadButton) {
      downloadButton.addEventListener('click', function(e) {
        e.preventDefault();
        const url = this.getAttribute('href');
        const title = document.querySelector('h1').textContent || 'image';
        const filename = title.replace(/[^a-z0-9]/gi, '_').toLowerCase() + '.png';
        downloadImage(url, filename);
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
        downloadImage(url, filename);
      });
    }

    // Add visual feedback for clickable image
    const detailImage = document.querySelector('.detail-image-wrapper img');
    if (detailImage) {
      detailImage.style.cursor = 'pointer';
      detailImage.title = 'Click to download';
    }
  });

  // Also handle existing theme switcher functionality
  const themeSwitcher = document.getElementById('theme-switcher');
  if (themeSwitcher) {
    // Get preferred theme from localStorage or system settings
    let currentTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    // Apply the theme to the <html> element
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Update the button text
    themeSwitcher.textContent = currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode';

    // Add click event listener to the switcher button
    themeSwitcher.addEventListener('click', () => {
      // Toggle theme
      const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      
      // Apply new theme
      document.documentElement.setAttribute('data-theme', newTheme);
      
      // Update localStorage
      localStorage.setItem('theme', newTheme);
      
      // Update button text
      themeSwitcher.textContent = newTheme === 'dark' ? 'Light Mode' : 'Dark Mode';
    });
  }
})();