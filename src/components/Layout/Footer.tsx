import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Heart, Palette, Mail, MapPin, Phone } from 'lucide-react';

const Footer = () => {
  const { t } = useTranslation();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Company Info & Contact */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Palette className="h-6 w-6 text-purple-600" />
              <span className="text-lg font-bold text-gray-900">🎨 {t('nav.brandName')}</span>
            </div>
            <p className="text-gray-600 text-sm mb-4">
              AI-powered coloring page generator creating unique, safe, and educational content for children. 
              Digital product service for personal and educational use.
            </p>
            
            {/* Contact Information */}
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-gray-600 text-sm">
                <Mail className="h-4 w-4" />
                <a href="mailto:support@thinkora.pics" className="hover:text-purple-600 transition-colors">
                  support@thinkora.pics
                </a>
              </div>
              <div className="flex items-center space-x-2 text-gray-600 text-sm">
                <Phone className="h-4 w-4" />
                <span>Business Hours: 9 AM - 6 PM UTC</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600 text-sm">
                <MapPin className="h-4 w-4" />
                <span>[Your Business Address]</span>
              </div>
            </div>
          </div>
          
          {/* Quick Navigation */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
              Quick Links
            </h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  🏠 {t('nav.home')}
                </Link>
              </li>
              <li>
                <Link to="/generate" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  🎨 {t('nav.generate')}
                </Link>
              </li>
              <li>
                <Link to="/gallery" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  🖼️ {t('nav.gallery')}
                </Link>
              </li>
              <li>
                <a href="/#pricing" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  💰 Pricing
                </a>
              </li>
            </ul>
          </div>
          
          {/* Legal & Support */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
              Legal & Support
            </h3>
            <ul className="space-y-2">
              <li>
                <Link to="/privacy" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  🔒 Privacy Policy
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  📋 Terms of Service
                </Link>
              </li>
              <li>
                <a href="mailto:support@thinkora.pics" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  📧 Customer Support
                </a>
              </li>
              <li>
                <a href="mailto:legal@thinkora.pics" className="text-gray-600 hover:text-purple-600 text-sm transition-colors">
                  ⚖️ Legal Inquiries
                </a>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-200 mt-8 pt-6">
          {/* Business Information */}
          <div className="mb-4 text-center">
            <p className="text-gray-600 text-xs leading-relaxed">
              <strong>Business Description:</strong> Thinkora.pics operates as a digital product service providing AI-generated 
              coloring pages for educational and recreational purposes. We specialize in creating child-safe, unique content 
              suitable for personal use, educational institutions, and limited commercial applications. Our service uses 
              advanced AI technology to transform user prompts into high-quality, printable coloring pages.
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row justify-between items-center">
            <p className="text-gray-500 text-sm mb-2 sm:mb-0">
              © {new Date().getFullYear()} Thinkora.pics. All rights reserved. Digital Product Service.
            </p>
            <p className="text-gray-500 text-sm flex items-center">
              Made with <Heart className="h-4 w-4 text-red-500 mx-1" /> for children worldwide
            </p>
          </div>
          
          {/* Product Categories */}
          <div className="mt-4 text-center">
            <p className="text-gray-400 text-xs">
              Digital Products: AI-Generated Content • Educational Materials • Printable Coloring Pages • Creative Templates
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;