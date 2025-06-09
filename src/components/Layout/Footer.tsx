import React from 'react';
import { Heart, Palette } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Palette className="h-6 w-6 text-purple-600" />
              <span className="text-lg font-bold text-gray-900">🎨 智绘本</span>
            </div>
            <p className="text-gray-600 text-sm">
              使用AI技术为孩子们创造独特、安全、有趣的涂色页。支持多种主题和年龄段，让创意无限延伸。
            </p>
          </div>
          
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
              快速导航
            </h3>
            <ul className="space-y-2">
              <li><a href="/generate" className="text-gray-600 hover:text-purple-600 text-sm">🎨 开始创作</a></li>
              <li><a href="/gallery" className="text-gray-600 hover:text-purple-600 text-sm">🖼️ 作品图库</a></li>
              <li><a href="/about" className="text-gray-600 hover:text-purple-600 text-sm">📖 关于我们</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
              帮助支持
            </h3>
            <ul className="space-y-2">
              <li><a href="/help" className="text-gray-600 hover:text-purple-600 text-sm">❓ 使用帮助</a></li>
              <li><a href="/privacy" className="text-gray-600 hover:text-purple-600 text-sm">🔒 隐私政策</a></li>
              <li><a href="/terms" className="text-gray-600 hover:text-purple-600 text-sm">📋 使用条款</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-200 mt-8 pt-6">
          <div className="flex flex-col sm:flex-row justify-between items-center">
            <p className="text-gray-500 text-sm">
              © 2025 智绘本 AI涂色页生成器. 保留所有权利.
            </p>
            <p className="text-gray-500 text-sm flex items-center">
              用 <Heart className="h-4 w-4 text-red-500 mx-1" /> 为全世界的孩子们而制作
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;