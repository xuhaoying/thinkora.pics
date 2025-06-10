import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Palette, Sparkles, Home, Images, Moon, Sun } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../ThemeProvider';
import LanguageSwitcher from '../LanguageSwitcher';
import { Button } from '../ui/Button';
import { motion, useScroll, useMotionValueEvent, AnimatePresence } from 'framer-motion';

const cn = (...classes: string[]) => classes.filter(Boolean).join(' ');

const Header = () => {
  const location = useLocation();
  const { t } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const { scrollY } = useScroll();
  const [showBackground, setShowBackground] = useState(false);

  useMotionValueEvent(scrollY, "change", (value) => {
    if (value > 100) {
      setShowBackground(true);
    } else {
      setShowBackground(false);
    }
  });

  const navItems = [
    { path: '/', label: t('nav.home'), icon: Home },
    { path: '/generate', label: t('nav.generate'), icon: Sparkles },
    { path: '/gallery', label: t('nav.gallery'), icon: Images },
  ];

  return (
    <motion.nav
      initial={{
        y: -80,
      }}
      animate={{
        y: 0,
      }}
      transition={{
        ease: [0.6, 0.05, 0.1, 0.9],
        duration: 0.8,
      }}
      className="max-w-7xl fixed top-4 mx-auto inset-x-0 z-50 w-[95%] lg:w-full"
    >
      <div
        className={cn(
          "w-full flex relative justify-between px-4 py-2 rounded-full bg-transparent transition duration-200",
          showBackground &&
            "bg-neutral-50 dark:bg-neutral-900 shadow-[0px_-2px_0px_0px_var(--neutral-100),0px_2px_0px_0px_var(--neutral-100)] dark:shadow-[0px_-2px_0px_0px_var(--neutral-800),0px_2px_0px_0px_var(--neutral-800)]"
        )}
      >
        <AnimatePresence>
          {showBackground && (
            <motion.div
              key={String(showBackground)}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{
                duration: 1,
              }}
              className="absolute inset-0 h-full w-full bg-neutral-100 dark:bg-neutral-800 pointer-events-none [mask-image:linear-gradient(to_bottom,white,transparent,white)] rounded-full"
            />
          )}
        </AnimatePresence>
        
        <div className="flex flex-row gap-2 items-center">
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
                🎨 <span className="bg-gradient-to-r from-brand-600 to-purple-600 bg-clip-text text-transparent">{t('nav.brandName')}</span>
              </span>
              <div className="text-xs text-gray-600 dark:text-gray-400 font-medium">
                {t('nav.brandSubtitle')}
              </div>
            </div>
          </Link>
          
          {/* Navigation Items */}
          <div className="hidden md:flex items-center gap-1.5">
            {navItems.map(({ path, label }) => (
              <Link
                key={path}
                to={path}
                className={cn(
                  "text-sm font-medium text-gray-500 dark:text-muted-dark p-4 rounded-md relative transition-colors",
                  location.pathname === path 
                    ? "text-white dark:text-black" 
                    : "hover:text-black dark:hover:text-neutral-400"
                )}
              >
                {location.pathname === path && (
                  <motion.span
                    layoutId="active-nav"
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    className="absolute inset-0 bg-black dark:bg-white rounded-md"
                  />
                )}
                <span className="relative z-10">{label}</span>
              </Link>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex space-x-2 items-center">
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
          
          {/* CTA Buttons */}
          <Button variant="simple" as={Link} to="/gallery">
            {t('nav.gallery')}
          </Button>
          <Button as={Link} to="/generate">
            <Sparkles className="h-4 w-4 mr-2" />
            {t('nav.startCreating')}
          </Button>
        </div>
      </div>
    </motion.nav>
  );
};

export default Header;