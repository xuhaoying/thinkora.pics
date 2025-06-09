import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Download, Shield, Heart, Star } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Generation',
      description: 'Create unique coloring pages instantly with advanced AI technology.'
    },
    {
      icon: Download,
      title: 'High-Quality Downloads',
      description: 'Download crisp, print-ready PDFs perfect for any printer.'
    },
    {
      icon: Shield,
      title: 'Child-Safe Content',
      description: 'All content is moderated and designed specifically for children.'
    },
    {
      icon: Heart,
      title: 'Educational Value',
      description: 'Promote creativity, focus, and learning through coloring.'
    }
  ];

  const categories = [
    { name: 'Animals', emoji: '🐾', count: 50 },
    { name: 'Fantasy', emoji: '🦄', count: 30 },
    { name: 'Nature', emoji: '🌸', count: 40 },
    { name: 'Vehicles', emoji: '🚗', count: 25 },
    { name: 'Holidays', emoji: '🎄', count: 35 },
    { name: 'Educational', emoji: '📚', count: 20 }
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="relative py-20 px-4 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Create Magic with
            <span className="text-purple-600 block">AI Coloring Pages</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Transform your imagination into beautiful, unique coloring pages. 
            Safe, educational, and endlessly creative for children of all ages.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/generate"
              className="bg-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2"
            >
              <Sparkles className="h-5 w-5" />
              <span>Start Creating</span>
            </Link>
            <Link
              to="/gallery"
              className="border-2 border-purple-600 text-purple-600 px-8 py-4 rounded-xl font-semibold hover:bg-purple-50 transition-colors"
            >
              View Gallery
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Why Choose AI Coloring Book?
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
            Popular Categories
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
                <p className="text-sm text-gray-500">{category.count}+ pages</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Simple, Fair Pricing</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="p-8 rounded-xl border-2 border-gray-200 bg-white">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Pay Per Page</h3>
              <div className="text-3xl font-bold text-purple-600 mb-4">$0.50</div>
              <p className="text-gray-600 mb-6">Perfect for occasional use</p>
              <ul className="space-y-2 text-sm text-gray-600 mb-6">
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />High-quality downloads</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />Instant generation</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />Commercial use allowed</li>
              </ul>
              <button className="w-full bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors">
                Get Started
              </button>
            </div>
            
            <div className="p-8 rounded-xl border-2 border-purple-500 bg-purple-50 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-purple-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                Most Popular
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Monthly Unlimited</h3>
              <div className="text-3xl font-bold text-purple-600 mb-4">$9.90</div>
              <p className="text-gray-600 mb-6">Best value for families</p>
              <ul className="space-y-2 text-sm text-gray-600 mb-6">
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />Unlimited generations</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />Priority processing</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />Premium templates</li>
                <li className="flex items-center"><Star className="h-4 w-4 text-yellow-500 mr-2" />Family sharing</li>
              </ul>
              <button className="w-full bg-purple-600 text-white py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors">
                Start Free Trial
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;