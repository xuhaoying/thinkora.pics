import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Download, Shield, Heart, Star } from 'lucide-react';
import { HiArrowRight } from 'react-icons/hi2';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';

const Home = () => {
  const { t } = useTranslation();
  
  const features = [
    {
      icon: Sparkles,
      title: t('home.features.aiPowered.title'),
      description: t('home.features.aiPowered.description')
    },
    {
      icon: Download,
      title: t('home.features.highQuality.title'),
      description: t('home.features.highQuality.description')
    },
    {
      icon: Shield,
      title: t('home.features.childSafe.title'),
      description: t('home.features.childSafe.description')
    },
    {
      icon: Heart,
      title: t('home.features.educational.title'),
      description: t('home.features.educational.description')
    }
  ];

  const categories = [
    { name: t('home.categories.animals'), emoji: '🐾', count: 50 },
    { name: t('home.categories.fantasy'), emoji: '🦄', count: 30 },
    { name: t('home.categories.nature'), emoji: '🌸', count: 40 },
    { name: t('home.categories.vehicles'), emoji: '🚗', count: 25 },
    { name: t('home.categories.holidays'), emoji: '🎄', count: 35 },
    { name: t('home.categories.educational'), emoji: '📚', count: 20 }
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section - Template Style */}
      <div className="flex flex-col min-h-screen pt-20 md:pt-40 relative overflow-hidden">
        <motion.div
          initial={{
            y: 40,
            opacity: 0,
          }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          transition={{
            ease: "easeOut",
            duration: 0.5,
          }}
          className="flex justify-center"
        >
          <Badge onClick={() => window.location.href = "#pricing"}>
            🎨 AI-Powered Coloring Pages for Kids
          </Badge>
        </motion.div>
        
        <motion.h1
          initial={{
            y: 40,
            opacity: 0,
          }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          transition={{
            ease: "easeOut",
            duration: 0.5,
          }}
          className="text-2xl md:text-4xl lg:text-8xl font-semibold max-w-6xl mx-auto text-center mt-6 relative z-10"
        >
          <span className="text-balance">
            Generate Creative Coloring Pages with AI
          </span>
        </motion.h1>
        
        <motion.p
          initial={{
            y: 40,
            opacity: 0,
          }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          transition={{
            ease: "easeOut",
            duration: 0.5,
            delay: 0.2,
          }}
          className="text-center mt-6 text-base md:text-xl text-muted dark:text-muted-dark max-w-3xl mx-auto relative z-10"
        >
          <span className="text-balance">
            Thinkora.pics seamlessly integrates AI technology to create unique, safe, and educational coloring pages
            perfect for children aged 3-13+. Generate high-quality printable content with a single click.
          </span>
        </motion.p>
        
        <motion.div
          initial={{
            y: 80,
            opacity: 0,
          }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          transition={{
            ease: "easeOut",
            duration: 0.5,
            delay: 0.4,
          }}
          className="flex items-center gap-4 justify-center mt-6 relative z-10"
        >
          <Button as={Link} to="/generate">
            <Sparkles className="h-4 w-4 mr-2" />
            Get started
          </Button>
          <Button
            variant="simple"
            as={Link}
            to="/gallery"
            className="flex space-x-2 items-center group"
          >
            <span>View Gallery</span>
            <HiArrowRight className="text-muted group-hover:translate-x-1 stroke-[1px] h-3 w-3 transition-transform duration-200 dark:text-muted-dark" />
          </Button>
        </motion.div>
        
        <div className="p-4 border border-neutral-200 bg-neutral-100 dark:bg-neutral-800 dark:border-neutral-700 rounded-[32px] mt-20 relative max-w-5xl mx-auto">
          <div className="absolute inset-x-0 bottom-0 h-40 w-full bg-gradient-to-b from-transparent via-white to-white dark:via-black/50 dark:to-black scale-[1.1] pointer-events-none" />
          <div className="p-2 bg-white dark:bg-black dark:border-neutral-700 border border-neutral-200 rounded-[24px]">
            <div className="rounded-[20px] bg-gradient-to-br from-brand-50 to-purple-50 dark:from-brand-950/20 dark:to-purple-950/20 p-8 min-h-[400px] flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">🎨</div>
                <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
                  AI Coloring Page Generator
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  High-quality, printable coloring pages generated instantly
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section - Bento Grid */}
      <section className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-display text-gray-900 dark:text-white mb-6">
              {t('home.features.title')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Discover the powerful features that make our AI coloring page generator the perfect choice for creative education
            </p>
          </div>
          
          <div className="bento-grid">
            {/* AI-Powered Generation - Large */}
            <div className="bento-item bento-large group bg-gradient-to-br from-brand-50 to-purple-50 dark:from-brand-950/20 dark:to-purple-950/20 border-brand-200 dark:border-brand-800">
              <div className="absolute top-6 right-6 p-3 bg-white/80 dark:bg-surface-800/80 rounded-xl backdrop-blur-sm">
                <Sparkles className="h-8 w-8 text-brand-600 dark:text-brand-400" />
              </div>
              <div className="relative z-10">
                <h3 className="text-2xl font-display text-gray-900 dark:text-white mb-4">
                  {features[0].title}
                </h3>
                <p className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed mb-6">
                  {features[0].description}
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 rounded-full text-sm font-medium">
                    Advanced AI
                  </span>
                  <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm font-medium">
                    Instant Results
                  </span>
                </div>
              </div>
              <div className="absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-tl from-brand-600/10 to-transparent rounded-tl-full"></div>
            </div>
            
            {/* High-Quality Downloads */}
            <div className="bento-item group bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/20 dark:to-cyan-950/20 border-blue-200 dark:border-blue-800">
              <div className="absolute -top-2 -right-2 w-16 h-16 bg-blue-500/20 rounded-full blur-lg"></div>
              <Download className="h-12 w-12 text-blue-600 dark:text-blue-400 mb-6 transition-transform group-hover:scale-110" />
              <h3 className="text-xl font-display text-gray-900 dark:text-white mb-3">
                {features[1].title}
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                {features[1].description}
              </p>
            </div>
            
            {/* Child-Safe Content */}
            <div className="bento-item group bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 border-green-200 dark:border-green-800">
              <div className="absolute -top-2 -left-2 w-20 h-20 bg-green-500/20 rounded-full blur-lg"></div>
              <Shield className="h-12 w-12 text-green-600 dark:text-green-400 mb-6 transition-transform group-hover:scale-110" />
              <h3 className="text-xl font-display text-gray-900 dark:text-white mb-3">
                {features[2].title}
              </h3>
              <p className="text-gray-700 dark:text-gray-300">
                {features[2].description}
              </p>
            </div>
            
            {/* Educational Value - Tall */}
            <div className="bento-item bento-tall group bg-gradient-to-br from-orange-50 to-rose-50 dark:from-orange-950/20 dark:to-rose-950/20 border-orange-200 dark:border-orange-800">
              <div className="absolute top-4 right-4 w-24 h-24 bg-gradient-to-br from-orange-400/20 to-rose-400/20 rounded-full blur-xl"></div>
              <Heart className="h-12 w-12 text-rose-600 dark:text-rose-400 mb-6 transition-transform group-hover:scale-110" />
              <h3 className="text-xl font-display text-gray-900 dark:text-white mb-4">
                {features[3].title}
              </h3>
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                {features[3].description}
              </p>
              
              {/* Stats */}
              <div className="mt-auto space-y-4">
                <div className="flex justify-between items-center p-3 bg-white/60 dark:bg-surface-800/60 rounded-xl backdrop-blur-sm">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Age Groups</span>
                  <span className="font-bold text-rose-600 dark:text-rose-400">3-13+</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-white/60 dark:bg-surface-800/60 rounded-xl backdrop-blur-sm">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Categories</span>
                  <span className="font-bold text-rose-600 dark:text-rose-400">6+</span>
                </div>
              </div>
            </div>
            
            {/* Performance Stats */}
            <div className="bento-item group bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-950/20 dark:to-purple-950/20 border-indigo-200 dark:border-indigo-800">
              <div className="text-center">
                <div className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">99.9%</div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-4">Success Rate</div>
                <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mb-2">30s</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Avg. Generation</div>
              </div>
            </div>
            
            {/* Quality Guarantee */}
            <div className="bento-item group bg-gradient-to-br from-amber-50 to-yellow-50 dark:from-amber-950/20 dark:to-yellow-950/20 border-amber-200 dark:border-amber-800">
              <Star className="h-12 w-12 text-amber-600 dark:text-amber-400 mb-4 transition-transform group-hover:rotate-12" />
              <h3 className="text-lg font-display text-gray-900 dark:text-white mb-2">
                Premium Quality
              </h3>
              <p className="text-gray-700 dark:text-gray-300 text-sm">
                300 DPI resolution, perfect for professional printing and classroom use.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-24 px-4 relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-white via-brand-50/30 to-purple-50/40 dark:from-surface-950 dark:via-surface-900 dark:to-surface-950"></div>
        <div className="absolute top-1/2 left-0 w-96 h-96 bg-gradient-to-r from-brand-400/10 to-purple-400/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-gradient-to-r from-pink-400/10 to-rose-400/10 rounded-full blur-3xl"></div>
        
        <div className="relative max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-display text-gray-900 dark:text-white mb-6">
              {t('home.categories.title')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Explore our diverse collection of themes and topics designed to inspire creativity and learning
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category, index) => (
              <Link
                key={index}
                to={`/generate?category=${category.name.toLowerCase()}`}
                className="group relative"
              >
                <div className="card card-hover p-6 text-center bg-white/60 dark:bg-surface-800/60 backdrop-blur-sm border border-white/20 dark:border-surface-700/50 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-brand-500/20">
                  {/* Glow effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-brand-600/0 via-brand-600/5 to-brand-600/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
                  
                  <div className="relative z-10">
                    <div className="text-4xl mb-4 transform transition-transform group-hover:scale-110 group-hover:rotate-3">
                      {category.emoji}
                    </div>
                    <h3 className="font-display font-semibold text-gray-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors mb-2">
                      {category.name}
                    </h3>
                    <div className="inline-flex items-center px-3 py-1 bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 rounded-full text-sm font-medium">
                      {category.count}+ {t('home.categories.pagesCount')}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section - Template Style */}
      <section id="pricing" className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-semibold text-gray-900 dark:text-white mb-6">
              {t('home.pricing.title')}
            </h2>
            <p className="text-xl text-muted dark:text-muted-dark max-w-3xl mx-auto">
              Choose the perfect plan for your creative needs with transparent, fair pricing
            </p>
          </div>
          
          {/* Pricing Toggle */}
          <div className="flex items-center justify-center bg-neutral-100 dark:bg-neutral-800 w-fit mx-auto mb-12 rounded-md overflow-hidden">
            <motion.button
              className="text-sm font-medium text-gray-500 dark:text-muted-dark p-4 rounded-md relative text-white dark:text-black"
            >
              <motion.span
                layoutId="pricing-toggle"
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                className="absolute inset-0 bg-black dark:bg-white rounded-md"
              />
              <span className="relative z-10">Pay Per Page</span>
            </motion.button>
            <button className="text-sm font-medium text-gray-500 dark:text-muted-dark p-4 rounded-md relative">
              <span className="relative z-10">Monthly Plan</span>
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Pay Per Page */}
            <div className="rounded-lg px-6 py-8 h-full flex flex-col justify-between bg-white dark:bg-black border border-neutral-200 dark:border-neutral-800">
              <div>
                <h3 className="text-base font-semibold leading-7 text-muted dark:text-muted-dark">
                  {t('home.pricing.payPerPage.title')}
                </h3>
                <p className="mt-4">
                  <motion.span
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ duration: 0.2, ease: "easeOut" }}
                    className="text-4xl font-bold tracking-tight text-neutral-900 dark:text-neutral-200 inline-block"
                  >
                    {t('home.pricing.payPerPage.price')}
                  </motion.span>
                </p>
                <p className="mt-6 text-sm leading-7 text-neutral-600 dark:text-neutral-300">
                  {t('home.pricing.payPerPage.description')}
                </p>
                <ul role="list" className="mt-8 space-y-3 text-sm leading-6 text-neutral-600 dark:text-neutral-300">
                  <li className="flex gap-x-3">
                    <Star className="h-6 w-5 flex-none text-muted dark:text-muted-dark" />
                    {t('home.pricing.payPerPage.features.highQuality')}
                  </li>
                  <li className="flex gap-x-3">
                    <Star className="h-6 w-5 flex-none text-muted dark:text-muted-dark" />
                    {t('home.pricing.payPerPage.features.instant')}
                  </li>
                  <li className="flex gap-x-3">
                    <Star className="h-6 w-5 flex-none text-muted dark:text-muted-dark" />
                    {t('home.pricing.payPerPage.features.commercial')}
                  </li>
                </ul>
              </div>
              <div>
                <Button
                  variant="outline"
                  className="mt-8 rounded-full py-2.5 px-3.5 text-center text-sm font-semibold block w-full"
                >
                  {t('home.pricing.payPerPage.button')}
                </Button>
              </div>
            </div>
            
            {/* Monthly Plan - Featured */}
            <div className="relative bg-[radial-gradient(164.75%_100%_at_50%_0%,#334155_0%,#0F172A_48.73%)] shadow-2xl rounded-lg px-6 py-8 h-full flex flex-col justify-between">
              <div>
                <h3 className="text-base font-semibold leading-7 text-white">
                  {t('home.pricing.monthly.title')}
                </h3>
                <p className="mt-4">
                  <motion.span
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ duration: 0.2, ease: "easeOut" }}
                    className="text-4xl font-bold tracking-tight text-white inline-block"
                  >
                    {t('home.pricing.monthly.price')}
                  </motion.span>
                </p>
                <p className="mt-6 text-sm leading-7 text-neutral-300">
                  {t('home.pricing.monthly.description')}
                </p>
                <ul role="list" className="mt-8 space-y-3 text-sm leading-6 text-neutral-300">
                  <li className="flex gap-x-3">
                    <Star className="h-6 w-5 flex-none text-white" />
                    {t('home.pricing.monthly.features.unlimited')}
                  </li>
                  <li className="flex gap-x-3">
                    <Star className="h-6 w-5 flex-none text-white" />
                    {t('home.pricing.monthly.features.priority')}
                  </li>
                  <li className="flex gap-x-3">
                    <Star className="h-6 w-5 flex-none text-white" />
                    {t('home.pricing.monthly.features.premium')}
                  </li>
                  <li className="flex gap-x-3">
                    <Star className="h-6 w-5 flex-none text-white" />
                    {t('home.pricing.monthly.features.sharing')}
                  </li>
                </ul>
              </div>
              <div>
                <Button
                  className="mt-8 rounded-full py-2.5 px-3.5 text-center text-sm font-semibold block w-full bg-white text-black shadow-sm hover:bg-white/90 focus-visible:outline-white"
                >
                  {t('home.pricing.monthly.button')}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;