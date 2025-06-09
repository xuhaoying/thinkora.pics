import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Palette, Sparkles, Home, Images } from 'lucide-react';

const Header = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: '首页', icon: Home },
    { path: '/generate', label: '创作', icon: Sparkles },
    { path: '/gallery', label: '图库', icon: Images },
  ];

  return (
    <header className="bg-white shadow-sm border-b-2 border-purple-100">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="relative">
              <Palette className="h-8 w-8 text-purple-600" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-pink-500 rounded-full animate-pulse"></div>
            </div>
            <div>
              <span className="text-xl font-bold text-gray-900">🎨 智绘本</span>
              <div className="text-xs text-purple-600">AI涂色页生成器</div>
            </div>
          </Link>
          
          <div className="flex space-x-8">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === path
                    ? 'text-purple-600 bg-purple-50'
                    : 'text-gray-600 hover:text-purple-600 hover:bg-purple-50'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{label}</span>
              </Link>
            ))}
          </div>

          <div className="flex items-center space-x-4">
            <button className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-2 rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all shadow-md hover:shadow-lg">
              🚀 开始创作
            </button>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;