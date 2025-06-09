interface GenerationRequest {
  prompt: string;
  category: string;
  style: string;
  complexity: string;
}

interface GenerationResponse {
  id: string;
  imageUrl: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}

import { getApiKey } from '../utils/env';

class AIService {
  private baseUrl = 'https://api.replicate.com/v1';
  private apiKey = getApiKey('VITE_REPLICATE_API_KEY');

  async generateColoringPage(request: GenerationRequest): Promise<GenerationResponse> {
    // Check if API key is properly configured
    if (!this.apiKey) {
      console.log('No valid API key found, using mock service');
      return this.generateColoringPageMock(request);
    }

    const enhancedPrompt = this.buildPrompt(request);
    
    try {
      // Create prediction using Replicate API
      const response = await fetch(`${this.baseUrl}/predictions`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          version: 'f2ab8a5569070d258f8e806fe15d585e29ab4a8a6a2dd73d95a1e25c2e48de59',
          input: {
            prompt: enhancedPrompt,
            num_inference_steps: 4,
            guidance_scale: 0,
            width: 512,
            height: 512,
          }
        })
      });

      if (!response.ok) {
        console.error('API request failed:', response.status, response.statusText);
        // Fallback to mock if API fails
        return this.generateColoringPageMock(request);
      }

      const prediction = await response.json();
      console.log('Initial prediction response:', prediction);
      
      // If prediction is not complete, poll for result
      if (prediction.status === 'starting' || prediction.status === 'processing') {
        return await this.pollForResult(prediction.id);
      }
      
      return {
        id: prediction.id,
        imageUrl: prediction.output?.[0] || '',
        status: prediction.status
      };
    } catch (error) {
      console.error('Error generating coloring page:', error);
      // Fallback to mock on any error
      return this.generateColoringPageMock(request);
    }
  }

  private async pollForResult(predictionId: string): Promise<GenerationResponse> {
    const maxAttempts = 60; // 5 minutes max
    const pollInterval = 5000; // 5 seconds
    
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      try {
        await new Promise(resolve => setTimeout(resolve, pollInterval));
        
        const response = await fetch(`${this.baseUrl}/predictions/${predictionId}`, {
          headers: {
            'Authorization': `Token ${this.apiKey}`,
          }
        });

        if (!response.ok) {
          throw new Error(`Polling failed: ${response.statusText}`);
        }

        const prediction = await response.json();
        console.log(`Poll attempt ${attempt + 1}:`, prediction.status);
        
        if (prediction.status === 'succeeded') {
          return {
            id: prediction.id,
            imageUrl: prediction.output?.[0] || '',
            status: 'completed'
          };
        } else if (prediction.status === 'failed') {
          throw new Error('Prediction failed: ' + (prediction.error || 'Unknown error'));
        }
        
        // Continue polling if still processing
      } catch (error) {
        console.error(`Poll attempt ${attempt + 1} failed:`, error);
        if (attempt === maxAttempts - 1) {
          throw error;
        }
      }
    }
    
    throw new Error('Prediction timed out');
  }

  async getPredictionStatus(predictionId: string): Promise<GenerationResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/predictions/${predictionId}`, {
        headers: {
          'Authorization': `Token ${this.apiKey}`,
        }
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
      }

      const prediction = await response.json();
      
      return {
        id: prediction.id,
        imageUrl: prediction.output?.[0] || '',
        status: prediction.status
      };
    } catch (error) {
      console.error('Error checking prediction status:', error);
      throw new Error('Failed to check generation status');
    }
  }

  private buildPrompt(request: GenerationRequest): string {
    // Professional coloring book prompt template
    const basePrompt = [
      'professional coloring book page',
      'black and white line art only',
      'NO shading, NO colors, NO gradients',
      'crisp clean outlines',
      'thick black lines on white background',
      'printable quality',
      'child-friendly design'
    ].join(', ');

    const complexityEnhancers = {
      simple: 'very simple shapes, large areas to color, minimal details, thick 3-4px outlines, suitable for ages 3-6',
      medium: 'moderate detail level, clear sections, balanced complexity, 2-3px outlines, suitable for ages 7-12',
      complex: 'intricate patterns, fine details, complex compositions, 1-2px outlines, suitable for ages 13+'
    };

    const styleEnhancers = {
      'simple lines': 'minimalist clean line art, simple geometric shapes',
      'detailed': 'detailed realistic line drawing with clear boundaries',
      'cute cartoon': 'adorable cartoon style, friendly expressions, rounded shapes',
      'realistic': 'realistic proportions and details, nature-accurate',
      'mandala': 'symmetrical mandala pattern, geometric repetition',
      'geometric': 'geometric patterns and abstract shapes'
    };

    // Category-specific quality enhancers
    const categoryEnhancers = {
      animals: 'cute friendly animal, clear facial features, simple body shapes',
      fantasy: 'magical creatures, whimsical elements, child-appropriate fantasy',
      nature: 'flowers, trees, natural scenes, organic shapes',
      vehicles: 'simple vehicle designs, clear mechanical shapes',
      holidays: 'festive decorations, celebration themes, seasonal elements',
      educational: 'learning elements, letters, numbers, educational objects',
      cartoon: 'fun cartoon characters, expressive features',
      abstract: 'simple abstract patterns, easy to color shapes'
    };

    const complexity = complexityEnhancers[request.complexity as keyof typeof complexityEnhancers] || complexityEnhancers.medium;
    const style = styleEnhancers[request.style as keyof typeof styleEnhancers] || 'simple line art';
    const categoryHint = categoryEnhancers[request.category as keyof typeof categoryEnhancers] || '';

    // Construct optimized prompt
    return `${basePrompt}, ${style}, ${complexity}, ${categoryHint}, ${request.prompt}. Make sure the design is perfect for coloring with clear distinct areas separated by bold outlines.`;
  }

  // Mock service for development/testing
  async generateColoringPageMock(request: GenerationRequest): Promise<GenerationResponse> {
    console.log('Using mock AI service for:', request.prompt);
    
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const mockId = `mock_${Date.now()}`;
      
      // Generate a local SVG image as data URL
      const mockUrl = this.generateMockSVG(request);
      
      console.log('Mock generation completed, returning:', { id: mockId, imageUrl: mockUrl });
      
      return {
        id: mockId,
        imageUrl: mockUrl,
        status: 'completed'
      };
    } catch (error) {
      console.error('Error in mock service:', error);
      throw new Error('Mock service failed');
    }
  }

  private generateMockSVG(request: GenerationRequest): string {
    // Create different SVG patterns based on category
    const categoryPatterns = {
      animals: this.createAnimalSVG(),
      fantasy: this.createFantasySVG(),
      nature: this.createNatureSVG(),
      vehicles: this.createVehicleSVG(),
      holidays: this.createHolidaySVG(),
      educational: this.createEducationalSVG(),
      cartoon: this.createCartoonSVG(),
      abstract: this.createAbstractSVG()
    };

    const pattern = categoryPatterns[request.category as keyof typeof categoryPatterns] 
      || this.createDefaultSVG();

    // Only use safe ASCII characters for the text
    const safePrompt = request.prompt.replace(/[^\x00-\x7F]/g, "?"); // Replace non-ASCII with ?
    const safeCategory = request.category.replace(/[^\x00-\x7F]/g, "?");

    const svg = `
      <svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
        <rect width="512" height="512" fill="white"/>
        ${pattern}
        <text x="256" y="480" text-anchor="middle" font-family="Arial" font-size="16" fill="#666">
          ${safePrompt} - ${safeCategory}
        </text>
      </svg>
    `;

    try {
      // Convert SVG to data URL using encodeURIComponent instead of btoa
      const dataUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
      return dataUrl;
    } catch (error) {
      console.error('Error encoding SVG:', error);
      // Fallback to simple data URL without base64
      return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(this.createSimpleFallbackSVG())}`;
    }
  }

  private createSimpleFallbackSVG(): string {
    return `
      <svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
        <rect width="512" height="512" fill="white"/>
        <rect x="150" y="150" width="200" height="200" rx="20" fill="none" stroke="black" stroke-width="3"/>
        <circle cx="256" cy="250" r="50" fill="none" stroke="black" stroke-width="3"/>
        <text x="256" y="260" text-anchor="middle" font-family="Arial" font-size="24" fill="black">OK</text>
        <text x="256" y="400" text-anchor="middle" font-family="Arial" font-size="16" fill="#666">
          Coloring Page Generated
        </text>
      </svg>
    `;
  }

  private createAnimalSVG(): string {
    return `
      <!-- Cute cat head -->
      <ellipse cx="256" cy="220" rx="90" ry="85" fill="none" stroke="black" stroke-width="4"/>
      
      <!-- Cat ears -->
      <path d="M 180 160 L 200 120 L 220 160 Z" fill="none" stroke="black" stroke-width="3"/>
      <path d="M 292 160 L 312 120 L 332 160 Z" fill="none" stroke="black" stroke-width="3"/>
      <path d="M 190 150 L 200 135 L 210 150 Z" fill="none" stroke="black" stroke-width="2"/>
      <path d="M 302 150 L 312 135 L 322 150 Z" fill="none" stroke="black" stroke-width="2"/>
      
      <!-- Eyes -->
      <ellipse cx="220" cy="200" rx="15" ry="18" fill="none" stroke="black" stroke-width="3"/>
      <ellipse cx="292" cy="200" rx="15" ry="18" fill="none" stroke="black" stroke-width="3"/>
      <circle cx="220" cy="195" r="5" fill="black"/>
      <circle cx="292" cy="195" r="5" fill="black"/>
      
      <!-- Nose -->
      <path d="M 250 230 L 260 230 L 255 240 Z" fill="none" stroke="black" stroke-width="3"/>
      
      <!-- Mouth -->
      <path d="M 255 245 Q 235 265 215 250" fill="none" stroke="black" stroke-width="3"/>
      <path d="M 255 245 Q 275 265 295 250" fill="none" stroke="black" stroke-width="3"/>
      
      <!-- Whiskers -->
      <line x1="170" y1="235" x2="210" y2="240" stroke="black" stroke-width="2"/>
      <line x1="170" y1="250" x2="210" y2="250" stroke="black" stroke-width="2"/>
      <line x1="302" y1="240" x2="342" y2="235" stroke="black" stroke-width="2"/>
      <line x1="302" y1="250" x2="342" y2="250" stroke="black" stroke-width="2"/>
      
      <!-- Body outline -->
      <ellipse cx="256" cy="360" rx="70" ry="60" fill="none" stroke="black" stroke-width="3"/>
      
      <!-- Paws -->
      <circle cx="210" cy="410" r="20" fill="none" stroke="black" stroke-width="3"/>
      <circle cx="302" cy="410" r="20" fill="none" stroke="black" stroke-width="3"/>
      
      <!-- Tail -->
      <path d="M 320 350 Q 380 320 390 380 Q 370 420 340 390" fill="none" stroke="black" stroke-width="3"/>
    `;
  }

  private createFantasySVG(): string {
    return `
      <!-- Unicorn head -->
      <ellipse cx="256" cy="250" rx="75" ry="80" fill="none" stroke="black" stroke-width="4"/>
      
      <!-- Unicorn horn -->
      <path d="M 256 170 L 246 120 L 266 120 Z" fill="none" stroke="black" stroke-width="3"/>
      <line x1="246" y1="140" x2="266" y2="140" stroke="black" stroke-width="2"/>
      <line x1="248" y1="130" x2="264" y2="130" stroke="black" stroke-width="2"/>
      <line x1="250" y1="150" x2="262" y2="150" stroke="black" stroke-width="2"/>
      
      <!-- Eyes -->
      <ellipse cx="230" cy="230" rx="12" ry="15" fill="none" stroke="black" stroke-width="3"/>
      <ellipse cx="282" cy="230" rx="12" ry="15" fill="none" stroke="black" stroke-width="3"/>
      <circle cx="230" cy="225" r="4" fill="black"/>
      <circle cx="282" cy="225" r="4" fill="black"/>
      
      <!-- Eyelashes -->
      <path d="M 220 215 Q 215 210 220 205" fill="none" stroke="black" stroke-width="2"/>
      <path d="M 292 215 Q 297 210 292 205" fill="none" stroke="black" stroke-width="2"/>
      
      <!-- Nose -->
      <ellipse cx="256" cy="260" rx="8" ry="6" fill="none" stroke="black" stroke-width="2"/>
      
      <!-- Mouth -->
      <path d="M 240 280 Q 256 290 272 280" fill="none" stroke="black" stroke-width="3"/>
      
      <!-- Mane -->
      <path d="M 180 200 Q 160 180 170 150 Q 190 160 200 180" fill="none" stroke="black" stroke-width="3"/>
      <path d="M 190 220 Q 150 200 160 170 Q 180 180 190 200" fill="none" stroke="black" stroke-width="3"/>
      <path d="M 332 200 Q 352 180 342 150 Q 322 160 312 180" fill="none" stroke="black" stroke-width="3"/>
      <path d="M 322 220 Q 362 200 352 170 Q 332 180 322 200" fill="none" stroke="black" stroke-width="3"/>
      
      <!-- Stars around -->
      <polygon points="150,100 155,115 170,115 158,125 163,140 150,130 137,140 142,125 130,115 145,115" 
               fill="none" stroke="black" stroke-width="2"/>
      <polygon points="350,120 355,135 370,135 358,145 363,160 350,150 337,160 342,145 330,135 345,135" 
               fill="none" stroke="black" stroke-width="2"/>
      <polygon points="380,250 385,265 400,265 388,275 393,290 380,280 367,290 372,275 360,265 375,265" 
               fill="none" stroke="black" stroke-width="2"/>
      
      <!-- Magic sparkles -->
      <circle cx="120" cy="150" r="3" fill="none" stroke="black" stroke-width="2"/>
      <circle cx="390" cy="180" r="3" fill="none" stroke="black" stroke-width="2"/>
      <circle cx="180" cy="350" r="3" fill="none" stroke="black" stroke-width="2"/>
    `;
  }

  private createNatureSVG(): string {
    return `
      <!-- Large flower center -->
      <circle cx="256" cy="200" r="25" fill="none" stroke="black" stroke-width="4"/>
      
      <!-- Flower petals -->
      <ellipse cx="256" cy="150" rx="20" ry="35" fill="none" stroke="black" stroke-width="3"/>
      <ellipse cx="306" cy="175" rx="35" ry="20" fill="none" stroke="black" stroke-width="3" transform="rotate(60 306 175)"/>
      <ellipse cx="306" cy="225" rx="35" ry="20" fill="none" stroke="black" stroke-width="3" transform="rotate(120 306 225)"/>
      <ellipse cx="256" cy="250" rx="20" ry="35" fill="none" stroke="black" stroke-width="3"/>
      <ellipse cx="206" cy="225" rx="35" ry="20" fill="none" stroke="black" stroke-width="3" transform="rotate(240 206 225)"/>
      <ellipse cx="206" cy="175" rx="35" ry="20" fill="none" stroke="black" stroke-width="3" transform="rotate(300 206 175)"/>
      
      <!-- Flower details -->
      <circle cx="256" cy="200" r="8" fill="none" stroke="black" stroke-width="2"/>
      <circle cx="246" cy="195" r="3" fill="black"/>
      <circle cx="266" cy="195" r="3" fill="black"/>
      <circle cx="256" cy="185" r="3" fill="black"/>
      <circle cx="246" cy="205" r="3" fill="black"/>
      <circle cx="266" cy="205" r="3" fill="black"/>
      
      <!-- Stem -->
      <rect x="250" y="250" width="12" height="150" fill="none" stroke="black" stroke-width="4"/>
      
      <!-- Leaves -->
      <ellipse cx="220" cy="280" rx="25" ry="15" fill="none" stroke="black" stroke-width="3" transform="rotate(-30 220 280)"/>
      <ellipse cx="292" cy="320" rx="25" ry="15" fill="none" stroke="black" stroke-width="3" transform="rotate(30 292 320)"/>
      
      <!-- Leaf veins -->
      <line x1="210" y1="280" x2="230" y2="280" stroke="black" stroke-width="1"/>
      <line x1="282" y1="320" x2="302" y2="320" stroke="black" stroke-width="1"/>
      
      <!-- Small flowers -->
      <circle cx="180" cy="150" r="12" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="180" cy="135" rx="8" ry="12" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="195" cy="142" rx="12" ry="8" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="195" cy="158" rx="12" ry="8" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="180" cy="165" rx="8" ry="12" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="165" cy="158" rx="12" ry="8" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="165" cy="142" rx="12" ry="8" fill="none" stroke="black" stroke-width="2"/>
      
      <!-- Butterfly -->
      <ellipse cx="350" cy="140" rx="15" ry="20" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="370" cy="140" rx="15" ry="20" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="350" cy="165" rx="12" ry="15" fill="none" stroke="black" stroke-width="2"/>
      <ellipse cx="370" cy="165" rx="12" ry="15" fill="none" stroke="black" stroke-width="2"/>
      <line x1="360" y1="120" x2="360" y2="185" stroke="black" stroke-width="2"/>
      <circle cx="360" cy="115" r="3" fill="black"/>
    `;
  }

  private createVehicleSVG(): string {
    return `
      <rect x="150" y="200" width="200" height="80" rx="10" fill="none" stroke="black" stroke-width="3"/>
      <circle cx="200" cy="300" r="30" fill="none" stroke="black" stroke-width="3"/>
      <circle cx="300" cy="300" r="30" fill="none" stroke="black" stroke-width="3"/>
      <rect x="170" y="180" width="160" height="40" rx="5" fill="none" stroke="black" stroke-width="2"/>
      <rect x="200" y="160" width="100" height="30" rx="3" fill="none" stroke="black" stroke-width="2"/>
    `;
  }

  private createHolidaySVG(): string {
    return `
      <polygon points="256,120 280,200 360,200 300,250 320,330 256,290 192,330 212,250 152,200 232,200" 
               fill="none" stroke="black" stroke-width="3"/>
      <rect x="250" y="330" width="12" height="50" fill="none" stroke="black" stroke-width="3"/>
      <circle cx="256" cy="140" r="15" fill="none" stroke="black" stroke-width="2"/>
    `;
  }

  private createEducationalSVG(): string {
    return `
      <rect x="180" y="150" width="150" height="200" rx="10" fill="none" stroke="black" stroke-width="3"/>
      <line x1="200" y1="180" x2="310" y2="180" stroke="black" stroke-width="2"/>
      <line x1="200" y1="210" x2="310" y2="210" stroke="black" stroke-width="2"/>
      <line x1="200" y1="240" x2="310" y2="240" stroke="black" stroke-width="2"/>
      <circle cx="256" cy="300" r="30" fill="none" stroke="black" stroke-width="3"/>
      <text x="256" y="308" text-anchor="middle" font-family="Arial" font-size="20" fill="black">A</text>
    `;
  }

  private createCartoonSVG(): string {
    return `
      <circle cx="256" cy="200" r="80" fill="none" stroke="black" stroke-width="4"/>
      <circle cx="230" cy="180" r="15" fill="black"/>
      <circle cx="282" cy="180" r="15" fill="black"/>
      <path d="M 220 240 Q 256 270 292 240" fill="none" stroke="black" stroke-width="4"/>
      <path d="M 200 150 Q 180 120 160 140" fill="none" stroke="black" stroke-width="3"/>
      <path d="M 312 150 Q 332 120 352 140" fill="none" stroke="black" stroke-width="3"/>
    `;
  }

  private createAbstractSVG(): string {
    return `
      <circle cx="200" cy="200" r="60" fill="none" stroke="black" stroke-width="3"/>
      <rect x="280" y="140" width="80" height="120" fill="none" stroke="black" stroke-width="3"/>
      <polygon points="150,300 200,350 250,300 220,280 180,280" fill="none" stroke="black" stroke-width="3"/>
      <line x1="100" y1="100" x2="400" y2="400" stroke="black" stroke-width="2"/>
    `;
  }

  private createDefaultSVG(): string {
    return `
      <rect x="150" y="150" width="200" height="200" rx="20" fill="none" stroke="black" stroke-width="3"/>
      <circle cx="256" cy="250" r="50" fill="none" stroke="black" stroke-width="3"/>
      <text x="256" y="260" text-anchor="middle" font-family="Arial" font-size="24" fill="black">?</text>
    `;
  }

  // Validate image for child safety
  async validateImage(imageUrl: string): Promise<boolean> {
    // This would integrate with content moderation APIs like:
    // - Google Cloud Vision API
    // - AWS Rekognition
    // - Microsoft Content Moderator
    
    try {
      // Mock validation - in production, call actual moderation service
      console.log('Validating image for child safety:', imageUrl);
      
      // Simulate moderation delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Mock approval (in production, this would be actual moderation result)
      return true;
    } catch (error) {
      console.error('Error validating image:', error);
      return false;
    }
  }

  // Convert image to PDF for download
  async convertToPDF(imageUrl: string): Promise<Blob> {
    try {
      // This would use a PDF generation library like jsPDF
      // For now, return the image as blob
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      return blob;
    } catch (error) {
      console.error('Error converting to PDF:', error);
      throw new Error('Failed to convert to PDF');
    }
  }
}

export const aiService = new AIService();
export default aiService;