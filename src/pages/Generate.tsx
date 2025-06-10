import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Sparkles, Download, Wand2 } from 'lucide-react';
import { useColoringBook } from '../context/ColoringBookContext';
import aiService from '../services/aiService';
import { validateEnvVars } from '../utils/env';
import { useTranslation } from 'react-i18next';

interface GenerateForm {
  prompt: string;
  category: string;
  ageGroup: string;
  style?: string;
}

const Generate = () => {
  const { state, dispatch } = useColoringBook();
  const { t } = useTranslation();
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<GenerateForm>({
    defaultValues: {
      ageGroup: 'medium',
      style: 'cute cartoon'
    }
  });
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Check if API key is configured using secure validation
  const envStatus = validateEnvVars();
  const hasApiKey = envStatus.hasReplicateKey;

  const categories = [
    { id: 'animals', name: t('generate.categories.animals'), emoji: '🐾', examples: t('generate.categories.examples.animals') },
    { id: 'fantasy', name: t('generate.categories.fantasy'), emoji: '🦄', examples: t('generate.categories.examples.fantasy') },
    { id: 'nature', name: t('generate.categories.nature'), emoji: '🌸', examples: t('generate.categories.examples.nature') },
    { id: 'vehicles', name: t('generate.categories.vehicles'), emoji: '🚗', examples: t('generate.categories.examples.vehicles') },
    { id: 'holidays', name: t('generate.categories.holidays'), emoji: '🎄', examples: t('generate.categories.examples.holidays') },
    { id: 'educational', name: t('generate.categories.educational'), emoji: '📚', examples: t('generate.categories.examples.educational') }
  ];

  const ageGroups = [
    { value: 'simple', label: t('generate.ageGroups.simple.label'), description: t('generate.ageGroups.simple.description') },
    { value: 'medium', label: t('generate.ageGroups.medium.label'), description: t('generate.ageGroups.medium.description') },
    { value: 'complex', label: t('generate.ageGroups.complex.label'), description: t('generate.ageGroups.complex.description') }
  ];

  const quickPrompts = t('generate.quickPrompts', { returnObjects: true }) as string[];

  const onSubmit = async (data: GenerateForm) => {
    dispatch({ type: 'SET_GENERATING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      console.log('Starting coloring page generation with data:', data);
      
      // Convert form data to service format
      const requestData = {
        prompt: data.prompt,
        category: data.category,
        style: data.style || 'cute cartoon',
        complexity: data.ageGroup
      };
      
      // Generate coloring page (will auto-fallback to mock if no valid API key)
      const result = await aiService.generateColoringPage(requestData);
      console.log('Generation result:', result);
      
      setGeneratedImage(result.imageUrl);
      
      // Add to context
      dispatch({
        type: 'ADD_COLORING_PAGE',
        payload: {
          id: result.id,
          prompt: data.prompt,
          imageUrl: result.imageUrl,
          createdAt: new Date(),
          category: data.category
        }
      });

      // Update credits if user is paying per image
      if (state.user && !state.user.subscription) {
        dispatch({ type: 'UPDATE_CREDITS', payload: state.user.credits - 1 });
      }
      
    } catch (error) {
      console.error('Generation error:', error);
      dispatch({ type: 'SET_ERROR', payload: `${t('common.error')}: ${error instanceof Error ? error.message : t('common.error')}` });
    } finally {
      dispatch({ type: 'SET_GENERATING', payload: false });
    }
  };

  const promptValue = watch('prompt');
  const categoryValue = watch('category');
  const ageGroupValue = watch('ageGroup');

  // Download function
  const handleDownload = async () => {
    if (!generatedImage) return;
    
    try {
      let downloadUrl = generatedImage;
      let filename = `coloring-page-${Date.now()}`;
      
      // Handle different image types
      if (generatedImage.startsWith('data:image/svg+xml')) {
        // Convert SVG to PNG for better compatibility
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        canvas.width = 512;
        canvas.height = 512;
        
        await new Promise((resolve, reject) => {
          img.onload = () => {
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
            downloadUrl = canvas.toDataURL('image/png');
            filename += '.png';
            resolve(null);
          };
          img.onerror = reject;
          img.src = generatedImage;
        });
      } else if (generatedImage.startsWith('http')) {
        // External URL - fetch and convert to blob
        const response = await fetch(generatedImage);
        const blob = await response.blob();
        downloadUrl = URL.createObjectURL(blob);
        filename += '.png';
      } else {
        filename += '.png';
      }
      
      // Create download link
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up object URL if created
      if (downloadUrl.startsWith('blob:')) {
        URL.revokeObjectURL(downloadUrl);
      }
      
    } catch (error) {
      console.error('Download failed:', error);
      alert(`${t('common.download')} ${t('common.error')}, ${t('common.retry')}`);
    }
  };

  // Regenerate function
  const handleRegenerate = () => {
    if (!promptValue || !categoryValue) {
      alert(t('generate.form.promptRequired'));
      return;
    }
    
    if (state.isGenerating) {
      return; // Prevent double-generation
    }
    
    const formData = {
      prompt: promptValue,
      category: categoryValue,
      ageGroup: ageGroupValue || 'medium',
      style: watch('style') || 'cute cartoon'
    };
    
    // Clear previous image and trigger new generation
    setGeneratedImage(null);
    onSubmit(formData);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          🎨 {t('generate.title')}
        </h1>
        <p className="text-lg text-gray-600">
          {t('generate.subtitle')}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Generation Form */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            
            {/* Quick Prompts */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                💡 {t('generate.form.quickPrompts')}
              </label>
              <div className="grid grid-cols-2 gap-2">
                {quickPrompts.map((prompt, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => setValue('prompt', prompt)}
                    className="text-left px-3 py-2 text-sm bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg transition-colors"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            {/* Main Prompt Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🖍️ {t('generate.form.promptLabel')}
              </label>
              <textarea
                {...register('prompt', { required: t('generate.form.promptRequired') })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                rows={3}
                placeholder={t('generate.form.promptPlaceholder')}
              />
              {errors.prompt && (
                <p className="text-red-500 text-sm mt-1">{errors.prompt.message}</p>
              )}
            </div>

            {/* Category Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                🏷️ {t('generate.form.categoryLabel')}
              </label>
              <div className="grid grid-cols-2 gap-3">
                {categories.map(category => (
                  <label key={category.id} className="cursor-pointer">
                    <input
                      {...register('category', { required: t('generate.form.categoryRequired') })}
                      type="radio"
                      value={category.id}
                      className="sr-only"
                    />
                    <div className={`p-4 rounded-lg border-2 transition-all hover:border-purple-300 ${
                      categoryValue === category.id 
                        ? 'border-purple-500 bg-purple-50' 
                        : 'border-gray-200 bg-white'
                    }`}>
                      <div className="text-2xl mb-2">{category.emoji}</div>
                      <div className="font-medium text-gray-900">{category.name}</div>
                      <div className="text-xs text-gray-500 mt-1">{category.examples}</div>
                    </div>
                  </label>
                ))}
              </div>
              {errors.category && (
                <p className="text-red-500 text-sm mt-1">{errors.category.message}</p>
              )}
            </div>

            {/* Age Group Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                👶 {t('generate.form.ageLabel')}
              </label>
              <div className="grid grid-cols-3 gap-3">
                {ageGroups.map(group => (
                  <label key={group.value} className="cursor-pointer">
                    <input
                      {...register('ageGroup')}
                      type="radio"
                      value={group.value}
                      className="sr-only"
                    />
                    <div className={`p-3 rounded-lg border-2 text-center transition-all hover:border-purple-300 ${
                      ageGroupValue === group.value 
                        ? 'border-purple-500 bg-purple-50' 
                        : 'border-gray-200 bg-white'
                    }`}>
                      <div className="font-medium text-gray-900">{group.label}</div>
                      <div className="text-xs text-gray-500 mt-1">{group.description}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Advanced Options */}
            <div>
              <button
                type="button"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="text-sm text-purple-600 hover:text-purple-700 flex items-center space-x-1"
              >
                <span>{showAdvanced ? '收起' : '展开'} 高级设置</span>
                <span className={`transform transition-transform ${showAdvanced ? 'rotate-180' : ''}`}>▼</span>
              </button>
              
              {showAdvanced && (
                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    🎨 绘画风格（可选）
                  </label>
                  <select
                    {...register('style')}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="cute cartoon">可爱卡通（推荐）</option>
                    <option value="simple lines">简单线条</option>
                    <option value="detailed">精细写实</option>
                    <option value="mandala">曼陀罗图案</option>
                    <option value="geometric">几何图形</option>
                  </select>
                </div>
              )}
            </div>

            {/* API Status Indicator */}
            <div className={`rounded-lg p-3 text-sm ${hasApiKey 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-blue-50 border border-blue-200'
            }`}>
              {hasApiKey ? (
                <p className="text-green-700">
                  ✅ <strong>AI生成已启用</strong> - 将使用真实的AI技术为您生成独特的涂色页
                </p>
              ) : (
                <div className="text-blue-700">
                  <p className="font-medium mb-1">🔧 当前使用演示模式</p>
                  <p className="text-xs">
                    如需启用真正的AI生成，请在 .env 文件中配置 VITE_REPLICATE_API_KEY
                  </p>
                </div>
              )}
            </div>

            {state.error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-700 text-sm">{state.error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={state.isGenerating}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 px-6 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
            >
              {state.isGenerating ? (
                <>
                  <Wand2 className="h-5 w-5 animate-spin" />
                  <span>AI正在创作中...</span>
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5" />
                  <span>✨ 立即生成涂色页</span>
                </>
              )}
            </button>

            {/* Preview */}
            {promptValue && (
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <h4 className="font-medium text-purple-900 mb-2">📝 生成预览：</h4>
                <p className="text-purple-700 text-sm">
                  为{ageGroups.find(g => g.value === ageGroupValue)?.label || ''}的孩子创作
                  「{promptValue}」涂色页
                  {categoryValue && `，主题：${categories.find(c => c.id === categoryValue)?.name}`}
                </p>
              </div>
            )}
          </form>
        </div>

        {/* Result Display */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
            <span>🖼️</span>
            <span>你的专属涂色页</span>
          </h3>
          
          {generatedImage ? (
            <div className="space-y-4">
              <div className="border-2 border-dashed border-purple-300 rounded-lg p-4 bg-purple-50">
                <img
                  src={generatedImage}
                  alt="Generated coloring page"
                  className="w-full h-auto rounded-lg shadow-sm"
                />
              </div>
              <div className="space-y-3">
                <button 
                  onClick={handleDownload}
                  className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-4 rounded-lg hover:from-green-600 hover:to-green-700 transition-all shadow-md hover:shadow-lg flex items-center justify-center space-x-2"
                >
                  <Download className="h-5 w-5" />
                  <span>📄 下载图片</span>
                </button>
                <button 
                  onClick={handleRegenerate}
                  disabled={state.isGenerating}
                  className="w-full border border-purple-300 text-purple-700 py-3 px-4 rounded-lg hover:bg-purple-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  <span>🔄</span>
                  <span>{state.isGenerating ? '生成中...' : '重新生成'}</span>
                </button>
              </div>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p className="text-yellow-800 text-sm">
                  💡 <strong>小贴士：</strong> 建议使用A4纸张打印，调整打印机设置为"黑白"模式效果更佳！
                </p>
              </div>
            </div>
          ) : state.isGenerating ? (
            <div className="border-2 border-dashed border-purple-300 rounded-lg p-8 text-center bg-purple-50">
              <Wand2 className="h-16 w-16 text-purple-600 mx-auto mb-4 animate-spin" />
              <p className="text-purple-800 font-medium">🎨 AI智能创作中...</p>
              <p className="text-purple-600 text-sm mt-2">正在为您生成专属涂色页</p>
              <div className="mt-4 space-y-2">
                <div className="bg-purple-200 rounded-full h-2">
                  <div className="bg-purple-600 h-2 rounded-full animate-pulse" style={{width: '60%'}}></div>
                </div>
                <p className="text-xs text-purple-500">⏱️ 预计需要 30-120 秒，请耐心等待</p>
                <div className="mt-4 text-xs text-purple-400 space-y-1">
                  <p>🔄 正在分析您的描述...</p>
                  <p>🎯 正在匹配最佳风格...</p>
                  <p>🖼️ 正在生成高清图像...</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <div className="text-6xl mb-4">🎨</div>
              <p className="text-gray-600 font-medium">你的涂色页将在这里显示</p>
              <p className="text-sm text-gray-500 mt-2">
                填写左侧表单，点击生成按钮开始创作
              </p>
              <div className="mt-4 space-y-2">
                <div className="text-xs text-gray-400">
                  ✅ 高清画质 • ✅ 打印友好 • ✅ 安全内容
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Tips Section */}
      <div className="mt-12 bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4 text-center">
          🌟 使用小贴士
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl mb-2">📝</div>
            <h4 className="font-semibold text-gray-900 mb-2">描述要具体</h4>
            <p className="text-sm text-gray-600">
              详细描述你想要的内容，比如"一只戴帽子的小猫在下雨天打伞"
            </p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-2">🎯</div>
            <h4 className="font-semibold text-gray-900 mb-2">选择合适年龄</h4>
            <p className="text-sm text-gray-600">
              年龄小的孩子适合简单图案，年龄大的可以选择复杂图案
            </p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-2">🖨️</div>
            <h4 className="font-semibold text-gray-900 mb-2">打印效果最佳</h4>
            <p className="text-sm text-gray-600">
              生成的涂色页专为打印优化，在纸上涂色体验更好
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Generate;