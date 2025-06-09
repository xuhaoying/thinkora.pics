import React, { useState } from 'react';
import { Wand2, Lightbulb, ArrowRight } from 'lucide-react';
import { StoryGenerator } from '../services/storyGenerator';

const StoryInput = ({ onGenerate, error }) => {
  const [storyIdea, setStoryIdea] = useState('');
  const [showExamples, setShowExamples] = useState(false);

  const examples = StoryGenerator.getExampleIdeas();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (storyIdea.trim()) {
      onGenerate(storyIdea);
    }
  };

  const handleExampleClick = (example) => {
    setStoryIdea(example);
    setShowExamples(false);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            ✨ 开始创作你的故事
          </h2>
          <p className="text-gray-600">
            输入一个简单的故事创意，AI会为你创造完整的角色、插图和故事文本
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📝 故事创意 (一句话即可)
            </label>
            <textarea
              value={storyIdea}
              onChange={(e) => setStoryIdea(e.target.value)}
              placeholder="例如：小兔子想要找到彩虹的尽头..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none h-24"
              maxLength={200}
            />
            <div className="flex justify-between items-center mt-2">
              <span className="text-xs text-gray-500">
                {storyIdea.length}/200 字符
              </span>
              <button
                type="button"
                onClick={() => setShowExamples(!showExamples)}
                className="text-xs text-purple-600 hover:text-purple-700 flex items-center space-x-1"
              >
                <Lightbulb className="w-3 h-3" />
                <span>需要灵感？</span>
              </button>
            </div>
          </div>

          {/* Examples */}
          {showExamples && (
            <div className="bg-purple-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-purple-900 mb-3">
                💡 点击使用示例创意：
              </h4>
              <div className="space-y-2">
                {examples.map((example, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => handleExampleClick(example)}
                    className="block w-full text-left px-3 py-2 text-sm text-purple-700 hover:bg-purple-100 rounded transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!storyIdea.trim()}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 px-6 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
          >
            <Wand2 className="w-5 h-5" />
            <span>开始创作故事</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </form>

        {/* Tips */}
        <div className="mt-8 bg-blue-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-blue-900 mb-2">
            💡 创作小贴士：
          </h4>
          <ul className="text-xs text-blue-700 space-y-1">
            <li>• 简单描述即可：谁想要做什么</li>
            <li>• 可以包含角色、地点、目标</li>
            <li>• 例如：小猫想开咖啡店、机器人学做蛋糕</li>
            <li>• AI会自动补充细节和创造完整故事</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default StoryInput;