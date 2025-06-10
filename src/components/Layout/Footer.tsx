import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Palette } from 'lucide-react';

const Footer = () => {
  const { t } = useTranslation();

  const links = [
    {
      name: t('nav.home'),
      href: "/",
    },
    {
      name: t('nav.generate'),
      href: "/generate",
    },
    {
      name: t('nav.gallery'),
      href: "/gallery",
    },
  ];
  
  const legal = [
    {
      name: "Privacy Policy",
      href: "/privacy",
    },
    {
      name: "Terms of Service",
      href: "/terms",
    },
    {
      name: "Contact Support",
      href: "mailto:support@thinkora.pics",
    },
  ];
  
  const socials = [
    {
      name: "Contact",
      href: "mailto:support@thinkora.pics",
    },
    {
      name: "Support",
      href: "mailto:support@thinkora.pics",
    },
    {
      name: "Business",
      href: "mailto:legal@thinkora.pics",
    },
  ];

  return (
    <div className="relative">
      <div className="border-t border-neutral-100 dark:border-neutral-800 px-8 pt-20 pb-32 relative bg-white dark:bg-black">
        <div className="max-w-7xl mx-auto text-sm text-neutral-500 dark:text-neutral-400 flex sm:flex-row flex-col justify-between items-start">
          <div>
            <div className="mr-4 md:flex mb-4">
              <Link to="/" className="flex items-center space-x-3 group">
                <div className="relative">
                  <div className="relative bg-white dark:bg-surface-800 p-2 rounded-xl shadow-sm">
                    <Palette className="h-6 w-6 text-brand-600" />
                  </div>
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-gradient-to-r from-pink-500 to-rose-500 rounded-full animate-pulse shadow-lg"></div>
                </div>
                <div>
                  <span className="text-lg font-display font-bold text-gray-900 dark:text-white">
                    🎨 <span className="bg-gradient-to-r from-brand-600 to-purple-600 bg-clip-text text-transparent">{t('nav.brandName')}</span>
                  </span>
                </div>
              </Link>
            </div>
            <div>Copyright &copy; {new Date().getFullYear()} Thinkora.pics</div>
            <div className="mt-2">All rights reserved</div>
          </div>
          <div className="grid grid-cols-3 gap-10 items-start mt-10 md:mt-0">
            <div className="flex justify-center space-y-4 flex-col mt-4">
              {links.map((link) => (
                <Link
                  key={link.name}
                  className="transition-colors hover:text-black text-muted dark:text-muted-dark dark:hover:text-neutral-400 text-xs sm:text-sm"
                  to={link.href}
                >
                  {link.name}
                </Link>
              ))}
            </div>
            <div className="flex justify-center space-y-4 flex-col mt-4">
              {legal.map((link) => (
                <Link
                  key={link.name}
                  className="transition-colors hover:text-black text-muted dark:text-muted-dark dark:hover:text-neutral-400 text-xs sm:text-sm"
                  to={link.href}
                >
                  {link.name}
                </Link>
              ))}
            </div>
            <div className="flex justify-center space-y-4 flex-col mt-4">
              {socials.map((link) => (
                <a
                  key={link.name}
                  className="transition-colors hover:text-black text-muted dark:text-muted-dark dark:hover:text-neutral-400 text-xs sm:text-sm"
                  href={link.href}
                >
                  {link.name}
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
      <p className="text-center text-5xl md:text-9xl lg:text-[18rem] font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 dark:from-neutral-950 to-neutral-200 dark:to-neutral-800 inset-x-0">
        THINKORA
      </p>
    </div>
  );
};

export default Footer;