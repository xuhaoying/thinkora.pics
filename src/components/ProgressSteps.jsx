import React from 'react';
import { User, Palette, BookOpen, Sparkles, Check } from 'lucide-react';

const ProgressSteps = ({ currentStep, stepMessage }) => {
  const steps = [
    {
      id: 1,
      title: '分析创意',
      description: '理解故事主题和角色',
      icon: Sparkles,
      color: 'text-purple-600'
    },
    {
      id: 2,
      title: '创建角色',
      description: '生成主角形象和性格',
      icon: User,
      color: 'text-blue-600'
    },
    {
      id: 3,
      title: '绘制插画',
      description: '创作4张精美场景图',
      icon: Palette,
      color: 'text-pink-600'
    },
    {
      id: 4,
      title: '编写故事',
      description: '生成完整故事文本',
      icon: BookOpen,
      color: 'text-green-600'
    },
    {
      id: 5,
      title: '完成创作',
      description: '整理和展示结果',
      icon: Check,
      color: 'text-emerald-600'
    }
  ];

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            🎨 AI正在创作中...
          </h2>
          <p className="text-gray-600">{stepMessage}</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-600">进度</span>
            <span className="text-sm text-gray-600">{Math.round((currentStep / 5) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${(currentStep / 5) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Steps */}
        <div className="space-y-4">
          {steps.map((step) => {
            const Icon = step.icon;
            const isCompleted = currentStep > step.id;
            const isCurrent = currentStep === step.id;
            const isPending = currentStep < step.id;

            return (
              <div
                key={step.id}
                className={`flex items-center space-x-4 p-4 rounded-lg transition-all duration-500 ${
                  isCurrent 
                    ? 'bg-purple-50 border border-purple-200 scale-105' 
                    : isCompleted 
                    ? 'bg-green-50 border border-green-200' 
                    : 'bg-gray-50 border border-gray-200'
                }`}
              >
                <div
                  className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-500 ${
                    isCompleted
                      ? 'bg-green-500 text-white'
                      : isCurrent
                      ? 'bg-purple-500 text-white animate-pulse'
                      : 'bg-gray-300 text-gray-500'
                  }`}
                >
                  {isCompleted ? (
                    <Check className="w-5 h-5" />
                  ) : (
                    <Icon className="w-5 h-5" />
                  )}
                </div>
                
                <div className="flex-1">
                  <h3
                    className={`font-medium transition-colors duration-500 ${
                      isCompleted
                        ? 'text-green-800'
                        : isCurrent
                        ? 'text-purple-800'
                        : 'text-gray-600'
                    }`}
                  >
                    {step.title}
                  </h3>
                  <p
                    className={`text-sm transition-colors duration-500 ${
                      isCompleted
                        ? 'text-green-600'
                        : isCurrent
                        ? 'text-purple-600'
                        : 'text-gray-500'
                    }`}
                  >
                    {step.description}
                  </p>
                </div>

                {isCurrent && (
                  <div className="flex-shrink-0">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-600"></div>
                  </div>
                )}

                {isCompleted && (
                  <div className="flex-shrink-0">
                    <div className="text-green-500">✓</div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Estimated Time */}
        <div className="mt-8 text-center">
          <div className="bg-blue-50 rounded-lg p-4">
            <p className="text-blue-800 text-sm">
              ⏱️ 预计还需要 {Math.max(0, (5 - currentStep) * 30)} 秒完成
            </p>
            <p className="text-blue-600 text-xs mt-1">
              请耐心等待，AI正在为您精心创作...
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressSteps;