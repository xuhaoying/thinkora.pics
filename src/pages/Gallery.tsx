import React, { useState } from 'react';
import { Search, Filter, Download, Heart, Grid, List } from 'lucide-react';
import { useColoringBook } from '../context/ColoringBookContext';

const Gallery = () => {
  const { state } = useColoringBook();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Mock data for demonstration
  const mockPages = [
    {
      id: '1',
      prompt: 'Cute unicorn with rainbow',
      imageUrl: 'https://via.placeholder.com/300x300/ffffff/000000?text=Unicorn',
      category: 'fantasy',
      createdAt: new Date('2025-01-01'),
      likes: 42
    },
    {
      id: '2',
      prompt: 'Friendly dragon flying',
      imageUrl: 'https://via.placeholder.com/300x300/ffffff/000000?text=Dragon',
      category: 'fantasy',
      createdAt: new Date('2025-01-02'),
      likes: 38
    },
    {
      id: '3',
      prompt: 'Playful puppies in garden',
      imageUrl: 'https://via.placeholder.com/300x300/ffffff/000000?text=Puppies',
      category: 'animals',
      createdAt: new Date('2025-01-03'),
      likes: 55
    },
    {
      id: '4',
      prompt: 'Princess in castle',
      imageUrl: 'https://via.placeholder.com/300x300/ffffff/000000?text=Princess',
      category: 'fantasy',
      createdAt: new Date('2025-01-04'),
      likes: 67
    },
    {
      id: '5',
      prompt: 'Race car speeding',
      imageUrl: 'https://via.placeholder.com/300x300/ffffff/000000?text=Race+Car',
      category: 'vehicles',
      createdAt: new Date('2025-01-05'),
      likes: 29
    },
    {
      id: '6',
      prompt: 'Beautiful flowers',
      imageUrl: 'https://via.placeholder.com/300x300/ffffff/000000?text=Flowers',
      category: 'nature',
      createdAt: new Date('2025-01-06'),
      likes: 44
    }
  ];

  const allPages = [...state.coloringPages, ...mockPages];

  const categories = ['all', 'animals', 'fantasy', 'nature', 'vehicles', 'holidays', 'educational'];

  const filteredPages = allPages.filter(page => {
    const matchesSearch = page.prompt.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || page.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Coloring Page Gallery
        </h1>
        <p className="text-lg text-gray-600">
          Discover and download beautiful AI-generated coloring pages
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search coloring pages..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          {/* Category Filter */}
          <div className="flex items-center space-x-2">
            <Filter className="h-5 w-5 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* View Mode Toggle */}
          <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'grid' 
                  ? 'bg-white text-purple-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Grid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'list' 
                  ? 'bg-white text-purple-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <List className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="mb-6">
        <p className="text-gray-600">
          Showing {filteredPages.length} coloring page{filteredPages.length !== 1 ? 's' : ''}
          {selectedCategory !== 'all' && ` in ${selectedCategory}`}
          {searchTerm && ` matching "${searchTerm}"`}
        </p>
      </div>

      {/* Gallery Grid */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredPages.map((page) => (
            <div key={page.id} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow group">
              <div className="aspect-square bg-gray-50 relative overflow-hidden">
                <img
                  src={page.imageUrl}
                  alt={page.prompt}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-300 flex items-center justify-center">
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity space-x-2">
                    <button className="bg-white text-purple-600 p-2 rounded-full shadow-lg hover:bg-purple-50 transition-colors">
                      <Download className="h-5 w-5" />
                    </button>
                    <button className="bg-white text-red-500 p-2 rounded-full shadow-lg hover:bg-red-50 transition-colors">
                      <Heart className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-medium text-gray-900 mb-2 line-clamp-2">{page.prompt}</h3>
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span className="capitalize bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs">
                    {page.category}
                  </span>
                  <div className="flex items-center space-x-1">
                    <Heart className="h-4 w-4" />
                    <span>{page.likes}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {filteredPages.map((page) => (
            <div key={page.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center space-x-6">
                <div className="w-24 h-24 bg-gray-50 rounded-lg overflow-hidden flex-shrink-0">
                  <img
                    src={page.imageUrl}
                    alt={page.prompt}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-gray-900 mb-2">{page.prompt}</h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span className="capitalize bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs">
                      {page.category}
                    </span>
                    <span>{page.createdAt.toLocaleDateString()}</span>
                    <div className="flex items-center space-x-1">
                      <Heart className="h-4 w-4" />
                      <span>{page.likes}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center space-x-2">
                    <Download className="h-4 w-4" />
                    <span>Download</span>
                  </button>
                  <button className="border border-gray-300 text-gray-700 p-2 rounded-lg hover:bg-gray-50 transition-colors">
                    <Heart className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {filteredPages.length === 0 && (
        <div className="text-center py-12">
          <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Search className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No coloring pages found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your search terms or filters, or create a new coloring page!
          </p>
          <button className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors">
            Create New Page
          </button>
        </div>
      )}
    </div>
  );
};

export default Gallery;