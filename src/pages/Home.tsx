import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Download, Shield, Heart, Star } from 'lucide-react';
import { useTranslation } from 'react-i18next';

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
      {/* Premium Hero Section */}
      <section className="relative overflow-hidden py-24 px-4">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-brand-50/50 via-purple-50/30 to-pink-50/50 dark:from-surface-950 dark:via-surface-900 dark:to-surface-950"></div>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-gradient-to-r from-brand-400/20 to-purple-400/20 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-gradient-to-r from-pink-400/20 to-rose-400/20 rounded-full blur-3xl animate-float" style={{animationDelay: '2s'}}></div>
        
        <div className="relative max-w-7xl mx-auto text-center">
          {/* Main Heading */}
          <div className="animate-in mb-8">
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-display text-gray-900 dark:text-white mb-6 leading-tight">
              {t('home.hero.title')}
              <span className="block text-gradient animate-gradient bg-gradient-to-r from-brand-600 via-purple-600 to-pink-600">
                {t('home.hero.subtitle')}
              </span>
            </h1>
          </div>
          
          {/* Description */}
          <div className="animate-fade" style={{animationDelay: '0.2s'}}>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-6 max-w-3xl mx-auto leading-relaxed">
              {t('home.hero.description')}
            </p>
          </div>
          
          {/* Feature Pills */}
          <div className="animate-fade mb-12" style={{animationDelay: '0.4s'}}>
            <div className="glass rounded-2xl p-6 max-w-4xl mx-auto mb-8 border border-white/20 dark:border-surface-700/50">
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <span className="text-gradient font-semibold">Digital Product Service:</span> Our AI-powered platform generates high-quality, printable coloring pages 
                on-demand. Perfect for parents, teachers, and educators seeking unique, safe content for children aged 3-13+.
              </p>
              <div className="flex flex-wrap gap-3 justify-center">
                <span className="inline-flex items-center px-4 py-2 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 border border-green-200 dark:border-green-800">
                  ✅ Educational Content
                </span>
                <span className="inline-flex items-center px-4 py-2 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-200 dark:border-blue-800">
                  🛡️ Child-Safe AI
                </span>
                <span className="inline-flex items-center px-4 py-2 rounded-full text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400 border border-purple-200 dark:border-purple-800">
                  🖨️ Print-Ready Quality
                </span>
                <span className="inline-flex items-center px-4 py-2 rounded-full text-xs font-medium bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400 border border-orange-200 dark:border-orange-800">
                  ⚡ Instant Download
                </span>
              </div>
            </div>
          </div>
          
          {/* CTA Buttons */}
          <div className="animate-fade mb-12" style={{animationDelay: '0.6s'}}>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/generate" className="btn-primary group">
                <Sparkles className="h-5 w-5 transition-transform group-hover:rotate-12" />
                <span>{t('home.hero.startCreating')}</span>
              </Link>
              <Link to="/gallery" className="btn-secondary group">
                <span>{t('home.hero.viewGallery')}</span>
              </Link>
              <a href="#pricing" className="relative inline-flex items-center justify-center px-8 py-4 font-medium text-white bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl shadow-lg shadow-green-500/25 transition-all duration-300 hover:shadow-xl hover:shadow-green-500/40 hover:scale-105 active:scale-95 group">
                <span className="mr-2">💰</span>
                <span>View Pricing</span>
              </a>
            </div>
          </div>
          
          {/* Pricing Highlight */}
          <div className="animate-fade" style={{animationDelay: '0.8s'}}>
            <div className="glass rounded-2xl p-6 max-w-md mx-auto border border-white/20 dark:border-surface-700/50">
              <div className="flex items-center justify-center mb-3">
                <span className="text-2xl mr-2">💸</span>
                <span className="text-gradient font-semibold">Transparent Pricing</span>
              </div>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="text-center">
                  <div className="font-bold text-lg text-gray-900 dark:text-white">$0.50</div>
                  <div className="text-gray-600 dark:text-gray-400">Per Page</div>
                </div>
                <div className="text-center">
                  <div className="font-bold text-lg text-gray-900 dark:text-white">$9.90</div>
                  <div className="text-gray-600 dark:text-gray-400">Monthly</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

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

      {/* Pricing Section */}
      <section id="pricing" className="py-24 px-4 relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-50 via-white to-brand-50/30 dark:from-surface-950 dark:via-surface-900 dark:to-surface-950"></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-gradient-to-r from-brand-400/20 to-purple-400/20 rounded-full blur-3xl animate-float"></div>
        
        <div className="relative max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-display text-gray-900 dark:text-white mb-6">
              {t('home.pricing.title')}
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Choose the perfect plan for your creative needs with transparent, fair pricing
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Pay Per Page */}
            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-gray-100 to-gray-200 dark:from-surface-800 dark:to-surface-700 rounded-3xl blur-lg opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
              <div className="relative card p-10 bg-white/80 dark:bg-surface-800/80 backdrop-blur-sm border border-gray-200/50 dark:border-surface-700/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl">
                <div className="text-center">
                  <h3 className="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-4">
                    {t('home.pricing.payPerPage.title')}
                  </h3>
                  <div className="mb-6">
                    <div className="text-5xl font-display font-bold text-gray-900 dark:text-white mb-2">
                      {t('home.pricing.payPerPage.price')}
                    </div>
                    <p className="text-gray-600 dark:text-gray-300">
                      {t('home.pricing.payPerPage.description')}
                    </p>
                  </div>
                  
                  <div className="space-y-4 mb-8">
                    <div className="flex items-center text-gray-700 dark:text-gray-300">
                      <div className="w-5 h-5 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mr-3">
                        <Star className="h-3 w-3 text-green-600 dark:text-green-400" />
                      </div>
                      <span>{t('home.pricing.payPerPage.features.highQuality')}</span>
                    </div>
                    <div className="flex items-center text-gray-700 dark:text-gray-300">
                      <div className="w-5 h-5 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mr-3">
                        <Star className="h-3 w-3 text-green-600 dark:text-green-400" />
                      </div>
                      <span>{t('home.pricing.payPerPage.features.instant')}</span>
                    </div>
                    <div className="flex items-center text-gray-700 dark:text-gray-300">
                      <div className="w-5 h-5 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mr-3">
                        <Star className="h-3 w-3 text-green-600 dark:text-green-400" />
                      </div>
                      <span>{t('home.pricing.payPerPage.features.commercial')}</span>
                    </div>
                  </div>
                  
                  <button className="w-full bg-gradient-to-r from-gray-600 to-gray-700 text-white py-4 rounded-xl font-medium transition-all duration-300 hover:shadow-lg hover:shadow-gray-500/25 hover:scale-105 active:scale-95">
                    {t('home.pricing.payPerPage.button')}
                  </button>
                </div>
              </div>
            </div>
            
            {/* Monthly Plan */}
            <div className="group relative">
              {/* Popular Badge */}
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-20">
                <div className="bg-gradient-to-r from-brand-600 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-medium shadow-lg animate-pulse">
                  {t('home.pricing.monthly.badge')}
                </div>
              </div>
              
              {/* Glow Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-brand-600/20 to-purple-600/20 rounded-3xl blur-lg opacity-0 group-hover:opacity-60 transition-opacity duration-300"></div>
              
              <div className="relative card p-10 bg-gradient-to-br from-brand-50 to-purple-50 dark:from-brand-950/20 dark:to-purple-950/20 backdrop-blur-sm border-2 border-brand-200 dark:border-brand-800 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-brand-500/25">
                <div className="text-center">
                  <h3 className="text-2xl font-display font-semibold text-gray-900 dark:text-white mb-4">
                    {t('home.pricing.monthly.title')}
                  </h3>
                  <div className="mb-6">
                    <div className="text-5xl font-display font-bold text-brand-600 dark:text-brand-400 mb-2">
                      {t('home.pricing.monthly.price')}
                    </div>
                    <p className="text-gray-600 dark:text-gray-300">
                      {t('home.pricing.monthly.description')}
                    </p>
                  </div>
                  
                  <div className="space-y-4 mb-8">
                    <div className="flex items-center text-gray-700 dark:text-gray-300">
                      <div className="w-5 h-5 bg-brand-100 dark:bg-brand-900/30 rounded-full flex items-center justify-center mr-3">
                        <Star className="h-3 w-3 text-brand-600 dark:text-brand-400" />
                      </div>
                      <span>{t('home.pricing.monthly.features.unlimited')}</span>
                    </div>
                    <div className="flex items-center text-gray-700 dark:text-gray-300">
                      <div className="w-5 h-5 bg-brand-100 dark:bg-brand-900/30 rounded-full flex items-center justify-center mr-3">
                        <Star className="h-3 w-3 text-brand-600 dark:text-brand-400" />
                      </div>
                      <span>{t('home.pricing.monthly.features.priority')}</span>
                    </div>
                    <div className="flex items-center text-gray-700 dark:text-gray-300">
                      <div className="w-5 h-5 bg-brand-100 dark:bg-brand-900/30 rounded-full flex items-center justify-center mr-3">
                        <Star className="h-3 w-3 text-brand-600 dark:text-brand-400" />
                      </div>
                      <span>{t('home.pricing.monthly.features.premium')}</span>
                    </div>
                    <div className="flex items-center text-gray-700 dark:text-gray-300">
                      <div className="w-5 h-5 bg-brand-100 dark:bg-brand-900/30 rounded-full flex items-center justify-center mr-3">
                        <Star className="h-3 w-3 text-brand-600 dark:text-brand-400" />
                      </div>
                      <span>{t('home.pricing.monthly.features.sharing')}</span>
                    </div>
                  </div>
                  
                  <button className="w-full bg-gradient-to-r from-brand-600 to-purple-600 text-white py-4 rounded-xl font-medium transition-all duration-300 hover:shadow-xl hover:shadow-brand-500/40 hover:scale-105 active:scale-95 relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
                    <span className="relative z-10">{t('home.pricing.monthly.button')}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          {/* Trust Badges */}
          <div className="mt-16 text-center">
            <div className="inline-flex items-center space-x-8 p-6 glass rounded-2xl border border-white/20 dark:border-surface-700/50">
              <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-300">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">30-Day Money Back</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-300">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Secure Payment</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-300">
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Cancel Anytime</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;