import React from 'react';
import { BookOpen, Sparkles, Users, Zap } from 'lucide-react';
import StoryInput from './StoryInput';
import ProgressSteps from './ProgressSteps';
import StoryResult from './StoryResult';
import { useStoryGeneration } from '../hooks/useStoryGeneration';

const StoryFactory = () => {
  const {
    isGenerating,
    currentStep,
    storyResult,
    error,
    stepMessage,
    generateStory,
    resetStory,
    downloadImage,
    shareStory
  } = useStoryGeneration();

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <header className="text-center mb-12">
        <div className="flex items-center justify-center mb-6">
          <div className="relative">
            <BookOpen className="w-16 h-16 text-purple-600" />
            <Sparkles className="w-6 h-6 text-yellow-500 absolute -top-1 -right-1 animate-pulse" />
          </div>
        </div>
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
          AI角色故事工厂
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          只需一句话，AI帮你创造完整故事：角色 + 插图 + 文本，一键生成精彩内容
        </p>
        
        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-12">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <Users className="w-8 h-8 text-purple-600 mx-auto mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">角色创作</h3>
            <p className="text-sm text-gray-600">AI自动生成独特角色形象和性格描述</p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <Sparkles className="w-8 h-8 text-purple-600 mx-auto mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">精美插画</h3>
            <p className="text-sm text-gray-600">4张高质量故事场景插图，适合分享</p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <Zap className="w-8 h-8 text-purple-600 mx-auto mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">完整故事</h3>
            <p className="text-sm text-gray-600">自动编写温馨有趣的完整故事文本</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto">
        {!storyResult && !isGenerating && (
          <StoryInput onGenerate={generateStory} error={error} />
        )}

        {isGenerating && (
          <ProgressSteps 
            currentStep={currentStep} 
            stepMessage={stepMessage} 
          />
        )}

        {storyResult && (
          <StoryResult 
            story={storyResult}
            onReset={resetStory}
            onDownload={downloadImage}
            onShare={shareStory}
          />
        )}
      </div>

      {/* Footer */}
      <footer className="mt-16 text-center text-gray-500 text-sm">
        <p>专为家长、教育工作者、内容创作者设计 • 让创意无限延伸</p>
      </footer>
    </div>
  );
};

export default StoryFactory;