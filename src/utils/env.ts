/**
 * 环境变量验证和安全管理
 * 确保敏感信息不会意外暴露
 */

// 验证必要的环境变量
export const validateEnvVars = () => {
  const requiredVars = {
    // VITE_APP_URL is not actually required for basic functionality
  };

  const optionalVars = {
    VITE_APP_URL: import.meta.env.VITE_APP_URL,
    VITE_REPLICATE_API_KEY: import.meta.env.VITE_REPLICATE_API_KEY,
    VITE_SUPABASE_URL: import.meta.env.VITE_SUPABASE_URL,
    VITE_SUPABASE_ANON_KEY: import.meta.env.VITE_SUPABASE_ANON_KEY,
    VITE_STRIPE_PUBLISHABLE_KEY: import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY,
  };

  // 检查必需变量
  const missingRequired = Object.entries(requiredVars)
    .filter(([, value]) => !value)
    .map(([key]) => key);

  if (missingRequired.length > 0) {
    console.warn('Missing required environment variables:', missingRequired);
  }

  // 检查可选变量（用于功能启用）
  const missingOptional = Object.entries(optionalVars)
    .filter(([, value]) => !value || value === 'your_api_key_here' || value.includes('your_'))
    .map(([key]) => key);

  if (missingOptional.length > 0) {
    console.info('Optional features disabled due to missing env vars:', missingOptional);
  }

  return {
    hasReplicateKey: !!optionalVars.VITE_REPLICATE_API_KEY && 
                     !optionalVars.VITE_REPLICATE_API_KEY.includes('your_'),
    hasSupabase: !!optionalVars.VITE_SUPABASE_URL && 
                 !optionalVars.VITE_SUPABASE_URL.includes('your_'),
    hasStripe: !!optionalVars.VITE_STRIPE_PUBLISHABLE_KEY && 
               !optionalVars.VITE_STRIPE_PUBLISHABLE_KEY.includes('your_'),
  };
};

// 安全地获取API密钥（不在日志中暴露）
export const getApiKey = (keyName: string): string | null => {
  const key = import.meta.env[keyName];
  
  // 验证密钥格式
  if (!key || key.includes('your_') || key.length < 10) {
    return null;
  }
  
  return key;
};

// 开发环境安全检查
export const securityChecks = () => {
  if (import.meta.env.DEV) {
    // 检查是否意外在生产构建中包含了开发密钥
    const devKeys = [
      'test_key',
      'demo_key',
      'localhost',
      'development'
    ];

    Object.entries(import.meta.env).forEach(([key, value]) => {
      if (typeof value === 'string') {
        devKeys.forEach(devKey => {
          if (value.toLowerCase().includes(devKey)) {
            console.warn(`🚨 Potential development key in ${key}: ${value.slice(0, 10)}...`);
          }
        });
      }
    });
  }

  // 生产环境检查
  if (import.meta.env.PROD) {
    const prodRequirements = {
      'HTTPS required': window.location.protocol === 'https:' || window.location.hostname === 'localhost',
      'No debug flags': !window.location.search.includes('debug'),
    };

    Object.entries(prodRequirements).forEach(([check, passed]) => {
      if (!passed) {
        console.error(`🚨 Production security check failed: ${check}`);
      }
    });
  }
};

// 初始化安全检查
securityChecks();