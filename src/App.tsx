import React from 'react';
import { Analytics } from '@vercel/analytics/react';
// @ts-ignore
import StoryFactory from './components/StoryFactory';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      <StoryFactory />
      <Analytics />
    </div>
  );
}

export default App;
