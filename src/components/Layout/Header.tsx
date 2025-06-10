import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Palette, Sparkles, Home, Images, Moon, Sun } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../ThemeProvider';
import LanguageSwitcher from '../LanguageSwitcher';

const Header = () => {
  const location = useLocation();
  const { t } = useTranslation();
  const { theme, toggleTheme } = useTheme();

  const navItems = [
    { path: '/', label: t('nav.home'), icon: Home },
    { path: '/generate', label: t('nav.generate'), icon: Sparkles },
    { path: '/gallery', label: t('nav.gallery'), icon: Images },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass backdrop-blur-glass border-0 transition-all duration-300">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-18">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="relative">
              <div className="absolute -inset-2 bg-gradient-to-r from-brand-600 to-purple-600 rounded-xl opacity-0 group-hover:opacity-20 blur transition-all duration-300"></div>
              <div className="relative bg-white dark:bg-surface-800 p-2 rounded-xl shadow-sm">
                <Palette className="h-6 w-6 text-brand-600 animate-float" />
              </div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-gradient-to-r from-pink-500 to-rose-500 rounded-full animate-pulse shadow-lg"></div>
            </div>
            <div className="hidden sm:block">
              <span className="text-xl font-display text-gray-900 dark:text-white">
                🎨 <span className="text-gradient">{t('nav.brandName')}</span>
              </span>
              <div className="text-xs text-gray-600 dark:text-gray-400 font-medium">
                {t('nav.brandSubtitle')}
              </div>
            </div>
          </Link>
          
          {/* Navigation */}
          <div className="hidden md:flex items-center space-x-2">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`group relative flex items-center space-x-2 px-4 py-2 rounded-xl font-medium transition-all duration-300 ${
                  location.pathname === path
                    ? 'text-brand-600 dark:text-brand-400 bg-brand-50 dark:bg-brand-950/50'
                    : 'text-gray-600 dark:text-gray-300 hover:text-brand-600 dark:hover:text-brand-400 hover:bg-white/50 dark:hover:bg-surface-800/50'
                }`}
              >
                <Icon className="h-4 w-4 transition-transform group-hover:scale-110" />
                <span className="text-sm">{label}</span>
                {location.pathname === path && (
                  <div className="absolute inset-0 bg-gradient-to-r from-brand-600/10 to-purple-600/10 rounded-xl animate-pulse"></div>
                )}
              </Link>
            ))}
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-3">
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-xl bg-white/50 dark:bg-surface-800/50 border border-gray-200/50 dark:border-surface-700/50 hover:bg-white dark:hover:bg-surface-800 transition-all duration-300 hover:scale-105 active:scale-95"
              aria-label="Toggle theme"
            >
              {theme === 'light' ? (
                <Moon className="h-4 w-4 text-gray-600 dark:text-gray-300" />
              ) : (
                <Sun className="h-4 w-4 text-gray-600 dark:text-gray-300" />
              )}
            </button>
            
            {/* Language Switcher */}
            <LanguageSwitcher />
            
            {/* CTA Button */}
            <Link 
              to="/generate"
              className="btn-primary group relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <Sparkles className="h-4 w-4 transition-transform group-hover:rotate-12" />
              <span className="relative z-10">{t('nav.startCreating')}</span>
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;