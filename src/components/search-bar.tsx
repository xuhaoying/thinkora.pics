'use client';

import { useQueryState } from 'nuqs';
import { useDebouncedCallback } from 'use-debounce';

export function SearchBar() {
  const [query, setQuery] = useQueryState('q');

  const debouncedSetQuery = useDebouncedCallback((value: string) => {
    setQuery(value || null);
  }, 300); // 300ms debounce delay

  return (
    <div className="w-full max-w-lg mx-auto mb-12">
      <input
        type="search"
        defaultValue={query || ''}
        onChange={(e) => debouncedSetQuery(e.target.value)}
        placeholder="Search for images (e.g., 'cat', 'tree', 'abstract')..."
        className="w-full px-4 py-3 text-lg border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
  );
} 