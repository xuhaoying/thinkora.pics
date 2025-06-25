'use client';

import { useQueryState } from 'nuqs';
import { useDebouncedCallback } from 'use-debounce';

export function SearchBar() {
  const [query, setQuery] = useQueryState('q');

  const debouncedSetQuery = useDebouncedCallback((value: string) => {
    setQuery(value || null);
  }, 300); // 300ms debounce delay

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <input
          type="search"
          defaultValue={query || ''}
          onChange={(e) => debouncedSetQuery(e.target.value)}
          placeholder="Search for transparent PNG images..."
          className="w-full px-12 py-4 text-lg border border-gray-200 dark:border-gray-700 rounded-full shadow-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
        />
        <div className="absolute left-4 top-1/2 transform -translate-y-1/2">
          <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 justify-center mt-4">
        <span className="text-sm text-gray-500 dark:text-gray-400">Popular:</span>
        {['technology', 'business', 'nature', 'abstract', 'people'].map((tag) => (
          <button
            key={tag}
            onClick={() => setQuery(tag)}
            className="text-sm px-3 py-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
          >
            {tag}
          </button>
        ))}
      </div>
    </div>
  );
} 