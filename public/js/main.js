// ---
// Thinkora.pics - Simple Theme Switcher
// ---

(function() {
  const themeSwitcher = document.getElementById('theme-switcher');
  if (!themeSwitcher) return;

  // 1. Get preferred theme from localStorage or system settings
  let currentTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  
  // 2. Apply the theme to the <html> element
  document.documentElement.setAttribute('data-theme', currentTheme);
  
  // 3. Update the button text
  themeSwitcher.textContent = currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode';

  // 4. Add click event listener to the switcher button
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
})();
