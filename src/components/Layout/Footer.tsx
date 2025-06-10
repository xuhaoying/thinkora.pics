import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Heart, Palette, Mail, MapPin, Phone, Sparkles, Shield, Star } from 'lucide-react';

const Footer = () => {
  const { t } = useTranslation();

  return (
    <footer className="relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-surface-900 to-brand-950"></div>
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-gradient-to-r from-brand-600/20 to-purple-600/20 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-gradient-to-r from-pink-600/20 to-rose-600/20 rounded-full blur-3xl"></div>
      
      <div className="relative">
        {/* Main Footer Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            
            {/* Company Info & Contact */}
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-3 mb-6">
                <div className="relative">
                  <div className="bg-gradient-to-r from-brand-600 to-purple-600 p-3 rounded-xl shadow-lg">
                    <Palette className="h-6 w-6 text-white" />
                  </div>
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-pink-500 to-rose-500 rounded-full animate-pulse shadow-lg"></div>
                </div>
                <div>
                  <span className="text-xl font-display font-bold text-white">
                    🎨 <span className="text-gradient">{t('nav.brandName')}</span>
                  </span>
                  <div className="text-sm text-gray-400 font-medium">
                    {t('nav.brandSubtitle')}
                  </div>
                </div>
              </div>
              
              <p className="text-gray-300 leading-relaxed mb-6">
                AI-powered coloring page generator creating unique, safe, and educational content for children. 
                Digital product service for personal and educational use with premium quality guaranteed.
              </p>
              
              {/* Feature Highlights */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                    <Shield className="h-4 w-4 text-green-400" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">Child-Safe</div>
                    <div className="text-xs text-gray-400">AI Protected</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    <Sparkles className="h-4 w-4 text-blue-400" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">AI-Powered</div>
                    <div className="text-xs text-gray-400">Instant Results</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center">
                    <Star className="h-4 w-4 text-purple-400" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">Premium</div>
                    <div className="text-xs text-gray-400">300 DPI Quality</div>
                  </div>
                </div>
              </div>
              
              {/* Contact Information */}
              <div className="space-y-3">
                <div className="flex items-center space-x-3 text-gray-300">
                  <div className="w-8 h-8 bg-brand-500/20 rounded-lg flex items-center justify-center">
                    <Mail className="h-4 w-4 text-brand-400" />
                  </div>
                  <a href="mailto:support@thinkora.pics" className="hover:text-brand-400 transition-colors">
                    support@thinkora.pics
                  </a>
                </div>
                <div className="flex items-center space-x-3 text-gray-300">
                  <div className="w-8 h-8 bg-brand-500/20 rounded-lg flex items-center justify-center">
                    <Phone className="h-4 w-4 text-brand-400" />
                  </div>
                  <span>Business Hours: 9 AM - 6 PM UTC</span>
                </div>
                <div className="flex items-center space-x-3 text-gray-300">
                  <div className="w-8 h-8 bg-brand-500/20 rounded-lg flex items-center justify-center">
                    <MapPin className="h-4 w-4 text-brand-400" />
                  </div>
                  <span>Global Digital Service</span>
                </div>
              </div>
            </div>
            
            {/* Quick Navigation */}
            <div>
              <h3 className="text-lg font-display font-semibold text-white mb-6">
                Quick Links
              </h3>
              <ul className="space-y-4">
                <li>
                  <Link to="/" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">🏠</span>
                    </div>
                    <span>{t('nav.home')}</span>
                  </Link>
                </li>
                <li>
                  <Link to="/generate" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">🎨</span>
                    </div>
                    <span>{t('nav.generate')}</span>
                  </Link>
                </li>
                <li>
                  <Link to="/gallery" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">🖼️</span>
                    </div>
                    <span>{t('nav.gallery')}</span>
                  </Link>
                </li>
                <li>
                  <a href="/#pricing" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">💰</span>
                    </div>
                    <span>Pricing</span>
                  </a>
                </li>
              </ul>
            </div>
            
            {/* Legal & Support */}
            <div>
              <h3 className="text-lg font-display font-semibold text-white mb-6">
                Legal & Support
              </h3>
              <ul className="space-y-4">
                <li>
                  <Link to="/privacy" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">🔒</span>
                    </div>
                    <span>Privacy Policy</span>
                  </Link>
                </li>
                <li>
                  <Link to="/terms" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">📋</span>
                    </div>
                    <span>Terms of Service</span>
                  </Link>
                </li>
                <li>
                  <a href="mailto:support@thinkora.pics" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">📧</span>
                    </div>
                    <span>Customer Support</span>
                  </a>
                </li>
                <li>
                  <a href="mailto:legal@thinkora.pics" className="group flex items-center space-x-2 text-gray-300 hover:text-brand-400 transition-colors">
                    <div className="w-6 h-6 bg-gray-700 group-hover:bg-brand-500/20 rounded-lg flex items-center justify-center transition-colors">
                      <span className="text-xs">⚖️</span>
                    </div>
                    <span>Legal Inquiries</span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Bottom Section */}
        <div className="border-t border-gray-700/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Business Information */}
            <div className="glass rounded-2xl p-6 mb-8 border border-gray-700/50">
              <h4 className="text-sm font-semibold text-white mb-3 uppercase tracking-wider">Business Description</h4>
              <p className="text-gray-300 text-sm leading-relaxed">
                Thinkora.pics operates as a premium digital product service providing AI-generated coloring pages for educational 
                and recreational purposes. We specialize in creating child-safe, unique content suitable for personal use, 
                educational institutions, and limited commercial applications. Our service uses advanced AI technology to 
                transform user prompts into high-quality, printable coloring pages.
              </p>
            </div>
            
            <div className="flex flex-col lg:flex-row justify-between items-center space-y-4 lg:space-y-0">
              <div className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-6">
                <p className="text-gray-400 text-sm">
                  © {new Date().getFullYear()} Thinkora.pics. All rights reserved.
                </p>
                <p className="text-gray-400 text-sm flex items-center">
                  Made with <Heart className="h-4 w-4 text-red-500 mx-1 animate-pulse" /> for children worldwide
                </p>
              </div>
              
              {/* Trust Indicators */}
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-1 text-gray-400 text-xs">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span>Secure</span>
                </div>
                <div className="flex items-center space-x-1 text-gray-400 text-xs">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                  <span>Verified</span>
                </div>
                <div className="flex items-center space-x-1 text-gray-400 text-xs">
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                  <span>Premium</span>
                </div>
              </div>
            </div>
            
            {/* Product Categories */}
            <div className="mt-6 text-center">
              <p className="text-gray-500 text-xs">
                Digital Products: AI-Generated Content • Educational Materials • Printable Coloring Pages • Creative Templates
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;