const REPLICATE_API_TOKEN = import.meta.env.VITE_REPLICATE_API_TOKEN;
const FLUX_MODEL = "8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f";

export class ReplicateService {
  static async generateImage(prompt) {
    try {
      console.log('Generating image with prompt:', prompt);
      
      const response = await fetch('https://api.replicate.com/v1/predictions', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${REPLICATE_API_TOKEN}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          version: FLUX_MODEL,
          input: {
            prompt,
            width: 1024,
            height: 1024,
            num_outputs: 1,
            scheduler: "K_EULER",
            num_inference_steps: 4,
            guidance_scale: 3.5
          }
        })
      });

      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`);
      }

      const prediction = await response.json();
      console.log('Prediction created:', prediction.id);
      
      return await this.pollForResult(prediction.id);
    } catch (error) {
      console.error('图像生成错误:', error);
      throw error;
    }
  }

  static async pollForResult(predictionId) {
    let attempts = 0;
    const maxAttempts = 60; // 5分钟超时
    const pollInterval = 5000; // 5秒轮询

    while (attempts < maxAttempts) {
      try {
        console.log(`Polling attempt ${attempts + 1} for prediction ${predictionId}`);
        
        const response = await fetch(`https://api.replicate.com/v1/predictions/${predictionId}`, {
          headers: {
            'Authorization': `Token ${REPLICATE_API_TOKEN}`,
          }
        });

        const prediction = await response.json();
        console.log('Prediction status:', prediction.status);

        if (prediction.status === 'succeeded') {
          console.log('Generation completed:', prediction.output[0]);
          return prediction.output[0];
        } else if (prediction.status === 'failed') {
          throw new Error(`图像生成失败: ${prediction.error || '未知错误'}`);
        }

        await new Promise(resolve => setTimeout(resolve, pollInterval));
        attempts++;
      } catch (error) {
        console.error('轮询错误:', error);
        attempts++;
        if (attempts >= maxAttempts) {
          throw error;
        }
        await new Promise(resolve => setTimeout(resolve, pollInterval));
      }
    }

    throw new Error('生成超时，请重试');
  }

  // 检查API密钥是否配置
  static isConfigured() {
    return REPLICATE_API_TOKEN && REPLICATE_API_TOKEN !== 'your_replicate_api_key_here';
  }

  // 创建演示图片（当API不可用时）
  static createMockImage(description) {
    // 创建一个SVG占位图
    const svg = `
      <svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg">
        <rect width="1024" height="1024" fill="#f0f0f0"/>
        <rect x="50" y="50" width="924" height="924" fill="white" stroke="#ddd" stroke-width="2"/>
        <text x="512" y="400" text-anchor="middle" font-family="Arial" font-size="24" fill="#666">
          ${description}
        </text>
        <text x="512" y="450" text-anchor="middle" font-family="Arial" font-size="16" fill="#999">
          演示图片 - 配置API密钥后将生成真实图像
        </text>
        <circle cx="512" cy="600" r="100" fill="none" stroke="#ddd" stroke-width="3"/>
        <path d="M 462 580 Q 512 620 562 580" fill="none" stroke="#ddd" stroke-width="3"/>
        <circle cx="480" cy="570" r="8" fill="#ddd"/>
        <circle cx="544" cy="570" r="8" fill="#ddd"/>
      </svg>
    `;
    
    return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`;
  }
}