import React, { useState } from 'react';
import { 
  Download, 
  Share2, 
  RotateCcw, 
  Heart, 
  User, 
  BookOpen,
  Image,
  Copy,
  Check
} from 'lucide-react';

const StoryResult = ({ story, onReset, onDownload, onShare }) => {
  const [activeTab, setActiveTab] = useState('character');
  const [copiedText, setCopiedText] = useState(false);

  const handleCopyStory = async () => {
    try {
      await navigator.clipboard.writeText(story.storyText);
      setCopiedText(true);
      setTimeout(() => setCopiedText(false), 2000);
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

  const handleDownloadAll = () => {
    // 下载角色头像
    onDownload(story.character.avatar, `${story.character.name}-头像.png`);
    
    // 下载所有场景图
    story.scenes.forEach((scene, index) => {
      setTimeout(() => {
        onDownload(scene.url, `${story.character.name}-场景${index + 1}-${scene.title}.png`);
      }, index * 1000);
    });
  };

  const tabs = [
    { id: 'character', label: '角色', icon: User },
    { id: 'scenes', label: '插画', icon: Image },
    { id: 'story', label: '故事', icon: BookOpen }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Success Header */}
      <div className="text-center bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          故事创作完成！
        </h2>
        <p className="text-gray-600 mb-4">
          AI为您创作了一个精彩的《{story.character.name}》的故事
        </p>
        {story.isDemo && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
            <p className="text-blue-700 text-sm">
              🔧 当前为演示模式，配置API密钥后可生成真实AI图像
            </p>
          </div>
        )}
        <div className="flex flex-wrap justify-center gap-3">
          <button
            onClick={handleDownloadAll}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>下载全部</span>
          </button>
          <button
            onClick={() => onShare('weibo')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
          >
            <Share2 className="w-4 h-4" />
            <span>分享</span>
          </button>
          <button
            onClick={onReset}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors flex items-center space-x-2"
          >
            <RotateCcw className="w-4 h-4" />
            <span>重新创作</span>
          </button>
        </div>
      </div>

      {/* Content Tabs */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        {/* Tab Navigation */}
        <div className="border-b border-gray-200">
          <nav className="flex">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 px-6 py-4 text-sm font-medium transition-colors flex items-center justify-center space-x-2 ${
                    activeTab === tab.id
                      ? 'text-purple-600 border-b-2 border-purple-600 bg-purple-50'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {/* Character Tab */}
          {activeTab === 'character' && (
            <div className="space-y-6">
              <div className="text-center">
                <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden border-4 border-purple-200">
                  <img
                    src={story.character.avatar}
                    alt={story.character.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {story.character.name}
                </h3>
                <div className="max-w-md mx-auto">
                  <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    <h4 className="font-medium text-gray-900 mb-2">角色描述</h4>
                    <p className="text-gray-600 text-sm">{story.character.description}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    <h4 className="font-medium text-gray-900 mb-2">性格特点</h4>
                    <p className="text-gray-600 text-sm">{story.character.personality}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">角色背景</h4>
                    <p className="text-gray-600 text-sm">{story.character.background}</p>
                  </div>
                </div>
                <button
                  onClick={() => onDownload(story.character.avatar, `${story.character.name}-头像.png`)}
                  className="mt-4 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center space-x-2 mx-auto"
                >
                  <Download className="w-4 h-4" />
                  <span>下载头像</span>
                </button>
              </div>
            </div>
          )}

          {/* Scenes Tab */}
          {activeTab === 'scenes' && (
            <div className="space-y-6">
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">故事插画</h3>
                <p className="text-gray-600">4张精美的故事场景图</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {story.scenes.map((scene) => (
                  <div key={scene.id} className="bg-gray-50 rounded-lg overflow-hidden">
                    <div className="aspect-square">
                      <img
                        src={scene.url}
                        alt={scene.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="p-4">
                      <h4 className="font-medium text-gray-900 mb-1">
                        {scene.title}
                      </h4>
                      <p className="text-sm text-gray-600 mb-3">
                        {scene.description}
                      </p>
                      <button
                        onClick={() => onDownload(scene.url, `${story.character.name}-${scene.title}.png`)}
                        className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2"
                      >
                        <Download className="w-4 h-4" />
                        <span>下载图片</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Story Tab */}
          {activeTab === 'story' && (
            <div className="space-y-6">
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">完整故事</h3>
                <p className="text-gray-600">AI为您编写的温馨故事</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="prose prose-gray max-w-none">
                  <p className="text-gray-800 leading-relaxed whitespace-pre-line">
                    {story.storyText}
                  </p>
                </div>
                <div className="flex justify-center mt-6">
                  <button
                    onClick={handleCopyStory}
                    className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center space-x-2"
                  >
                    {copiedText ? (
                      <>
                        <Check className="w-4 h-4" />
                        <span>已复制</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        <span>复制故事</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Story Info */}
      <div className="bg-white rounded-lg border border-gray-100 p-4">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>创作时间: {story.createdAt}</span>
          <span>原始创意: {story.originalIdea}</span>
        </div>
      </div>
    </div>
  );
};

export default StoryResult;