// Enhanced JavaScript for Thinkora.pics - SEO Optimized

(function() {
    'use strict';

    // DOM Elements
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const searchInfo = document.getElementById('search-info');
    const imageGrid = document.getElementById('image-grid');
    const imageCards = document.querySelectorAll('.image-card');

    // State
    let allImages = Array.from(imageCards);
    let searchTimeout;

    // Initialize
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        // Set up search functionality
        if (searchInput) {
            searchInput.addEventListener('input', handleSearch);
            searchInput.addEventListener('keypress', handleSearchKeypress);
        }

        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', clearSearch);
        }

        // Lazy loading enhancement
        enhanceLazyLoading();

        // Add keyboard navigation
        setupKeyboardNavigation();

        // Add performance monitoring
        monitorPerformance();

        // Set up image error handling
        handleImageErrors();

        // Add smooth scroll
        setupSmoothScroll();

        // Initialize analytics (privacy-focused)
        initAnalytics();
    }

    // Search functionality
    function handleSearch(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value.toLowerCase().trim();

        // Show/hide clear button
        clearSearchBtn.style.display = query ? 'block' : 'none';

        // Debounce search
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    }

    function handleSearchKeypress(e) {
        if (e.key === 'Escape') {
            clearSearch();
        }
    }

    function performSearch(query) {
        if (!query) {
            showAllImages();
            updateSearchInfo(allImages.length);
            return;
        }

        let visibleCount = 0;
        const searchTerms = query.toLowerCase().split(' ').filter(term => term.length > 0);

        allImages.forEach(card => {
            const title = card.querySelector('.image-card__title')?.textContent.toLowerCase() || '';
            const tags = Array.from(card.querySelectorAll('.image-card__tag')).map(tag => tag.textContent.toLowerCase());
            const author = card.querySelector('.image-card__author')?.textContent.toLowerCase() || '';
            const size = card.querySelector('.image-card__size')?.textContent.toLowerCase() || '';
            
            // Extract all searchable content
            const searchContent = [title, author, size, ...tags].join(' ');
            
            // Check if ALL search terms match (AND search)
            const allTermsMatch = searchTerms.every(term => searchContent.includes(term));
            
            // Calculate relevance score
            let relevanceScore = 0;
            if (allTermsMatch) {
                searchTerms.forEach(term => {
                    // Higher score for title matches
                    if (title.includes(term)) relevanceScore += 3;
                    // Medium score for tag matches
                    tags.forEach(tag => {
                        if (tag === term) relevanceScore += 2; // Exact tag match
                        else if (tag.includes(term)) relevanceScore += 1; // Partial tag match
                    });
                    // Lower score for other matches
                    if (author.includes(term)) relevanceScore += 1;
                    if (size.includes(term)) relevanceScore += 1;
                });
            }

            if (allTermsMatch && relevanceScore > 0) {
                card.style.display = '';
                card.dataset.relevance = relevanceScore;
                visibleCount++;
                // Add highlight effect
                card.classList.add('search-match');
            } else {
                card.style.display = 'none';
                card.classList.remove('search-match');
                card.dataset.relevance = '0';
            }
        });

        // Sort visible results by relevance
        if (visibleCount > 0) {
            const container = imageGrid;
            const visibleCards = allImages.filter(card => card.style.display !== 'none');
            
            // Sort by relevance score (descending)
            visibleCards.sort((a, b) => {
                return parseInt(b.dataset.relevance) - parseInt(a.dataset.relevance);
            });
            
            // Re-append in sorted order
            visibleCards.forEach(card => container.appendChild(card));
        }

        updateSearchInfo(visibleCount, query);
        
        // Log search for analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'search', {
                search_term: query,
                results_count: visibleCount
            });
        }
    }

    function clearSearch() {
        searchInput.value = '';
        clearSearchBtn.style.display = 'none';
        showAllImages();
        updateSearchInfo(allImages.length);
        searchInput.focus();
    }

    function showAllImages() {
        allImages.forEach(card => {
            card.style.display = '';
            card.classList.remove('search-match');
        });
    }

    function updateSearchInfo(count, query = '') {
        if (searchInfo) {
            if (query) {
                searchInfo.textContent = `Found ${count} image${count !== 1 ? 's' : ''} matching "${query}"`;
            } else {
                searchInfo.textContent = `${count} free transparent PNG images available`;
            }
        }
    }

    // Enhanced lazy loading with intersection observer
    function enhanceLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src && !img.src) {
                            img.src = img.dataset.src;
                            img.classList.add('loaded');
                            observer.unobserve(img);
                        }
                    }
                });
            }, {
                rootMargin: '50px'
            });

            document.querySelectorAll('img[loading="lazy"]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // Keyboard navigation
    function setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Focus search on '/'
            if (e.key === '/' && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput?.focus();
            }

            // Navigate images with arrow keys
            if (e.key.startsWith('Arrow') && document.activeElement.closest('.image-card')) {
                e.preventDefault();
                navigateImages(e.key);
            }
        });
    }

    function navigateImages(direction) {
        const currentCard = document.activeElement.closest('.image-card');
        const visibleCards = allImages.filter(card => card.style.display !== 'none');
        const currentIndex = visibleCards.indexOf(currentCard);

        let nextIndex;
        switch(direction) {
            case 'ArrowRight':
                nextIndex = (currentIndex + 1) % visibleCards.length;
                break;
            case 'ArrowLeft':
                nextIndex = (currentIndex - 1 + visibleCards.length) % visibleCards.length;
                break;
            case 'ArrowDown':
                nextIndex = Math.min(currentIndex + getColumnsCount(), visibleCards.length - 1);
                break;
            case 'ArrowUp':
                nextIndex = Math.max(currentIndex - getColumnsCount(), 0);
                break;
        }

        if (nextIndex !== undefined && visibleCards[nextIndex]) {
            visibleCards[nextIndex].querySelector('a').focus();
        }
    }

    function getColumnsCount() {
        const gridComputedStyle = window.getComputedStyle(imageGrid);
        const gridTemplateColumns = gridComputedStyle.getPropertyValue('grid-template-columns');
        return gridTemplateColumns.split(' ').length;
    }

    // Performance monitoring
    function monitorPerformance() {
        if ('PerformanceObserver' in window) {
            // Monitor Largest Contentful Paint
            try {
                const lcpObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
                });
                lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            } catch (e) {
                // LCP not supported
            }

            // Monitor long tasks
            if ('PerformanceLongTaskTiming' in window) {
                const longTaskObserver = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        console.log('Long task detected:', entry);
                    }
                });
                longTaskObserver.observe({ entryTypes: ['longtask'] });
            }
        }
    }

    // Image error handling
    function handleImageErrors() {
        document.addEventListener('error', (e) => {
            if (e.target.tagName === 'IMG') {
                e.target.classList.add('error');
                // Could replace with a placeholder image
                console.error('Image failed to load:', e.target.src);
            }
        }, true);
    }

    // Smooth scroll
    function setupSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Privacy-focused analytics
    function initAnalytics() {
        // Track page performance
        if (window.performance && window.performance.timing) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const timing = window.performance.timing;
                    const pageLoadTime = timing.loadEventEnd - timing.navigationStart;
                    const domReadyTime = timing.domContentLoadedEventEnd - timing.navigationStart;
                    
                    console.log('Page Load Time:', pageLoadTime + 'ms');
                    console.log('DOM Ready Time:', domReadyTime + 'ms');
                    
                    // Send to analytics if available
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'page_timing', {
                            page_load_time: pageLoadTime,
                            dom_ready_time: domReadyTime
                        });
                    }
                }, 0);
            });
        }

        // Track visibility changes
        document.addEventListener('visibilitychange', () => {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'visibility_change', {
                    visibility_state: document.visibilityState
                });
            }
        });
    }

    // Expose API for external use
    window.ThinkoraPics = {
        search: performSearch,
        clearSearch: clearSearch,
        getVisibleImages: () => allImages.filter(card => card.style.display !== 'none')
    };

})();

// Service Worker Registration (for PWA support)
if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('ServiceWorker registration successful');
            })
            .catch(err => {
                console.log('ServiceWorker registration failed:', err);
            });
    });
}