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
      {/* Hero Section */}
      <section className="relative py-20 px-4 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            {t('home.hero.title')}
            <span className="text-purple-600 block">{t('home.hero.subtitle')}</span>
          </h1>
          <p className="text-xl text-gray-600 mb-4 max-w-2xl mx-auto">
            {t('home.hero.description')}
          </p>
          <div className="bg-white/90 backdrop-blur rounded-lg p-4 max-w-2xl mx-auto mb-8 border border-purple-100">
            <p className="text-sm text-gray-700 leading-relaxed">
              <strong>Digital Product Service:</strong> Our AI-powered platform generates high-quality, printable coloring pages 
              on-demand. Perfect for parents, teachers, and educators seeking unique, safe content for children aged 3-13+. 
              All content is automatically moderated for appropriateness and optimized for home printing.
            </p>
            <div className="mt-3 flex flex-wrap gap-2 justify-center">
              <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">Educational Content</span>
              <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Child-Safe AI</span>
              <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">Print-Ready Quality</span>
              <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded">Instant Download</span>
            </div>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/generate"
              className="bg-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2"
            >
              <Sparkles className="h-5 w-5" />
              <span>{t('home.hero.startCreating')}</span>
            </Link>
            <Link
              to="/gallery"
              className="border-2 border-purple-600 text-purple-600 px-8 py-4 rounded-xl font-semibold hover:bg-purple-50 transition-colors"
            >
              {t('home.hero.viewGallery')}
            </Link>
            <a
              href="#pricing"
              className="bg-green-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
            >
              <span>💰</span>
              <span>View Pricing</span>
            </a>
          </div>
          
          {/* Pricing Highlight */}
          <div className="mt-8 bg-white/80 backdrop-blur rounded-xl p-4 max-w-md mx-auto border border-purple-200">
            <p className="text-sm text-gray-600 mb-2">💸 <strong>Transparent Pricing</strong></p>
            <div className="flex justify-between items-center text-sm">
              <span>Pay-per-page: <strong>$0.50</strong></span>
              <span className="text-purple-600">•</span>
              <span>Monthly: <strong>$9.90</strong></span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            {t('home.features.title')}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-6 rounded-xl bg-white shadow-sm border border-gray-100">
                <feature.icon className="h-12 w-12 text-purple-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600 text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            {t('home.categories.title')}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category, index) => (
              <Link
                key={index}
                to={`/generate?category=${category.name.toLowerCase()}`}
                className="group p-6 rounded-xl border border-gray-200 hover:border-purple-300 hover:shadow-md transition-all text-center"
              >
                <div className="text-4xl mb-3">{category.emoji}</div>
                <h3 className="font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
                  {category.name}
                </h3>
                <p className="text-sm text-gray-500">{category.count}+ {t('home.categories.pagesCount')}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">{t('home.pricing.title')}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="p-8 rounded-xl border-2 border-gray-200 bg-white">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{t('home.pricing.payPerPage.title')}</h3>
              <div className="text-3xl font-bold text-purple-600 mb-4">{t('home.pricing.payPerPage.price')}</div>
              <p className="text-gray-600 mb-6">{t('home.pricing.payPerPage.description')}</p>
              <ul className="space-y-2 text-sm text-gray-600 mb-6">
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />{t('home.pricing.payPerPage.features.highQuality')}</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />{t('home.pricing.payPerPage.features.instant')}</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />{t('home.pricing.payPerPage.features.commercial')}</li>
              </ul>
              <button className="w-full bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors">
                {t('home.pricing.payPerPage.button')}
              </button>
            </div>
            
            <div className="p-8 rounded-xl border-2 border-purple-500 bg-purple-50 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-purple-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                {t('home.pricing.monthly.badge')}
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{t('home.pricing.monthly.title')}</h3>
              <div className="text-3xl font-bold text-purple-600 mb-4">{t('home.pricing.monthly.price')}</div>
              <p className="text-gray-600 mb-6">{t('home.pricing.monthly.description')}</p>
              <ul className="space-y-2 text-sm text-gray-600 mb-6">
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />{t('home.pricing.monthly.features.unlimited')}</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />{t('home.pricing.monthly.features.priority')}</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />{t('home.pricing.monthly.features.premium')}</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />{t('home.pricing.monthly.features.sharing')}</li>
              </ul>
              <button className="w-full bg-purple-600 text-white py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors">
                {t('home.pricing.monthly.button')}
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;