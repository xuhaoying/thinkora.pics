import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Analytics } from '@vercel/analytics/react';
import { ColoringBookProvider } from './context/ColoringBookContext';
import { ThemeProvider } from './components/ThemeProvider';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Home from './pages/Home';
import Gallery from './pages/Gallery';
import About from './pages/About';
import PrivacyPolicy from './pages/PrivacyPolicy';
import TermsOfService from './pages/TermsOfService';

// Simplified Generate component to avoid complex dependencies
const SimpleGenerate = () => (
  <div className="max-w-4xl mx-auto px-4 py-8">
    <div className="text-center mb-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        🎨 AI Smart Coloring Page Generator
      </h1>
      <p className="text-lg text-gray-600">
        Tell me what you want to draw, and AI will create a unique coloring page for you!
      </p>
    </div>
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
      <h2 className="text-xl font-semibold mb-4">Coming Soon</h2>
      <p className="text-gray-600">
        The AI generation feature is being prepared. Please check back soon!
      </p>
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Features</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• AI-powered coloring page generation</li>
          <li>• Multiple age groups (3-6, 7-12, 13+ years)</li>
          <li>• Various categories (animals, fantasy, nature, vehicles)</li>
          <li>• High-quality, print-ready downloads</li>
        </ul>
      </div>
    </div>
  </div>
);

function App() {
  return (
    <ThemeProvider>
      <ColoringBookProvider>
        <Router>
          <div className="min-h-screen bg-white dark:bg-black transition-colors duration-300">
            <Header />
            <main className="pt-20">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/generate" element={<SimpleGenerate />} />
                <Route path="/gallery" element={<Gallery />} />
                <Route path="/about" element={<About />} />
                <Route path="/privacy" element={<PrivacyPolicy />} />
                <Route path="/terms" element={<TermsOfService />} />
              </Routes>
            </main>
            <Footer />
            <Analytics />
          </div>
        </Router>
      </ColoringBookProvider>
    </ThemeProvider>
  );
}

export default App;
