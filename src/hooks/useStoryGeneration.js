import { useState } from 'react';
import { StoryGenerator } from '../services/storyGenerator.js';

export const useStoryGeneration = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [storyResult, setStoryResult] = useState(null);
  const [error, setError] = useState('');
  const [stepMessage, setStepMessage] = useState('');

  const generateStory = async (storyIdea) => {
    if (!storyIdea.trim()) {
      setError('请输入故事创意');
      return;
    }

    setIsGenerating(true);
    setError('');
    setStoryResult(null);
    setCurrentStep(1);
    setStepMessage('');

    try {
      const result = await StoryGenerator.generateCompleteStory(
        storyIdea,
        (step, message) => {
          setCurrentStep(step);
          setStepMessage(message);
          console.log(`Step ${step}: ${message}`);
        }
      );

      setStoryResult(result);
      console.log('故事生成完成:', result);
    } catch (err) {
      setError(err.message || '生成过程中出现错误，请重试');
      console.error('故事生成错误:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const resetStory = () => {
    setStoryResult(null);
    setError('');
    setCurrentStep(1);
    setStepMessage('');
  };

  const downloadImage = async (imageUrl, filename) => {
    try {
      // 处理data URL
      if (imageUrl.startsWith('data:')) {
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        return;
      }

      // 处理外部URL
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('下载失败:', error);
      alert('下载失败，请稍后重试');
    }
  };

  const shareStory = (platform) => {
    if (!storyResult) return;

    const shareText = `我用AI创作了一个精彩故事！主角是${storyResult.character.name}，故事是：${storyResult.originalIdea}`;
    const shareUrl = window.location.href;

    const shareUrls = {
      weibo: `https://service.weibo.com/share/share.php?url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(shareText)}`,
      wechat: `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(shareUrl)}`,
      qq: `https://connect.qq.com/widget/shareqq/index.html?url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(shareText)}`
    };

    if (shareUrls[platform]) {
      if (platform === 'wechat') {
        // 微信分享显示二维码
        const qrWindow = window.open('', '_blank', 'width=300,height=300');
        qrWindow.document.write(`
          <div style="text-align: center; padding: 20px;">
            <h3>微信扫码分享</h3>
            <img src="${shareUrls[platform]}" alt="微信分享二维码" />
            <p>用微信扫描二维码分享</p>
          </div>
        `);
      } else {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
      }
    }
  };

  return {
    isGenerating,
    currentStep,
    storyResult,
    error,
    stepMessage,
    generateStory,
    resetStory,
    downloadImage,
    shareStory
  };
};