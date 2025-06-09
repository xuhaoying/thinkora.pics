import { ReplicateService } from './replicateApi.js';

export class StoryGenerator {
  // 从故事创意中提取角色名称
  static extractCharacterName(idea) {
    const namePatterns = {
      '兔子': ['小白', '布布', '跳跳'],
      '女孩': ['小雨', '小花', '小美'],
      '男孩': ['小明', '小勇', '小杰'],
      '机器人': ['小蓝', '机机', '智智'],
      '鱼': ['小波', '泡泡', '游游'],
      '猫': ['小咪', '喵喵', '毛毛'],
      '狗': ['小汪', '旺旺', '毛球'],
      '公主': ['艾莎', '小星', '美美'],
      '王子': ['小勇', '亚瑟', '强强'],
      '魔法': ['小星', '魔魔', '奇奇'],
      '恐龙': ['小龙', '壮壮', '吼吼'],
      '熊': ['小熊', '萌萌', '胖胖']
    };
    
    for (const [keyword, names] of Object.entries(namePatterns)) {
      if (idea.includes(keyword)) {
        return names[Math.floor(Math.random() * names.length)];
      }
    }
    
    // 默认名称
    const defaultNames = ['小勇', '小美', '小智', '小星', '小花'];
    return defaultNames[Math.floor(Math.random() * defaultNames.length)];
  }

  // 生成角色描述
  static generateCharacterDescription(idea, characterName) {
    const traits = ['善良', '勇敢', '聪明', '好奇', '友善', '活泼'];
    const randomTraits = traits.sort(() => 0.5 - Math.random()).slice(0, 2);
    
    return {
      name: characterName,
      description: `${idea}故事中的主人公`,
      personality: randomTraits.join('、'),
      background: `${characterName}是一个充满${randomTraits[0]}和${randomTraits[1]}的角色，总是准备着开始新的冒险。`
    };
  }

  // 生成完整的故事文本
  static generateStoryText(idea, character) {
    const storyTemplates = [
      `从前，有一个叫${character.name}的小伙伴。${idea}。在这个神奇的冒险中，${character.name}遇到了许多有趣的挑战。通过自己的${character.personality}，${character.name}不仅解决了遇到的困难，还帮助了其他需要帮助的朋友。最终，${character.name}收获了珍贵的友谊和成长，这真是一个充满温暖的美好故事！`,
      
      `在一个美好的日子里，${character.name}开始了一段特别的旅程。${idea}。这个冒险让${character.name}学会了很多新东西。凭借着${character.personality}的品质，${character.name}克服了路上的重重困难。故事的最后，${character.name}不仅实现了自己的梦想，还让身边的每个人都感受到了快乐和希望。`,
      
      `${character.name}是一个特别的小朋友。${idea}。在这个充满奇迹的故事里，${character.name}用自己的${character.personality}感动了所有人。经历了许多有趣的事情后，${character.name}明白了友谊和勇气的真正含义。这个故事告诉我们，只要心怀善意，就能创造出最美好的奇迹。`
    ];
    
    return storyTemplates[Math.floor(Math.random() * storyTemplates.length)];
  }

  // 获取场景描述
  static getSceneDescriptions() {
    return [
      { title: '故事开始', description: '介绍主角和故事背景' },
      { title: '遇到挑战', description: '主角面临困难或问题' },
      { title: '冒险过程', description: '主角努力解决问题' },
      { title: '圆满结局', description: '故事获得美好结果' }
    ];
  }

  // 生成场景提示词
  static generateScenePrompts(storyIdea, character, sceneIndex) {
    const baseStyle = "children's book illustration, cartoon style, bright colors, friendly atmosphere, digital art, high quality";
    
    const scenePrompts = [
      `${character.name} the character introduction scene, ${storyIdea}, beginning of the story, ${baseStyle}`,
      `${character.name} facing a challenge, ${storyIdea}, dramatic moment, ${baseStyle}`,
      `${character.name} on an adventure, ${storyIdea}, exciting action scene, ${baseStyle}`,
      `${character.name} happy ending scene, ${storyIdea}, celebration and joy, ${baseStyle}`
    ];
    
    return scenePrompts[sceneIndex] || scenePrompts[0];
  }

  // 生成完整故事
  static async generateCompleteStory(storyIdea, onProgress) {
    try {
      // 步骤1: 创建角色
      onProgress(1, '正在分析故事创意并创建角色...');
      await new Promise(resolve => setTimeout(resolve, 1000));

      const characterName = this.extractCharacterName(storyIdea);
      const character = this.generateCharacterDescription(storyIdea, characterName);

      // 步骤2: 生成角色头像
      onProgress(2, `正在为${characterName}生成角色形象...`);
      let characterImage;
      
      if (ReplicateService.isConfigured()) {
        const characterPrompt = `adorable cartoon character portrait of ${character.name}, ${character.description}, cute anime style, colorful, friendly expression, children's book character, digital art, high quality`;
        characterImage = await ReplicateService.generateImage(characterPrompt);
      } else {
        characterImage = ReplicateService.createMockImage(`${character.name} 角色形象`);
      }

      // 步骤3: 生成故事插画
      onProgress(3, '正在创作精美的故事插画...');
      const scenes = [];
      const sceneDescriptions = this.getSceneDescriptions();

      for (let i = 0; i < 4; i++) {
        onProgress(3, `正在生成第${i + 1}张插画 (${sceneDescriptions[i].title})...`);
        
        let sceneImage;
        if (ReplicateService.isConfigured()) {
          const scenePrompt = this.generateScenePrompts(storyIdea, character, i);
          sceneImage = await ReplicateService.generateImage(scenePrompt);
        } else {
          sceneImage = ReplicateService.createMockImage(`${sceneDescriptions[i].title}: ${sceneDescriptions[i].description}`);
        }

        scenes.push({
          id: i + 1,
          url: sceneImage,
          title: sceneDescriptions[i].title,
          description: sceneDescriptions[i].description
        });
      }

      // 步骤4: 生成故事文本
      onProgress(4, '正在编写精彩的故事内容...');
      await new Promise(resolve => setTimeout(resolve, 1500));
      const storyText = this.generateStoryText(storyIdea, character);

      // 步骤5: 完成
      onProgress(5, '故事创作完成！');

      return {
        character: {
          ...character,
          avatar: characterImage
        },
        scenes,
        storyText,
        originalIdea: storyIdea,
        createdAt: new Date().toLocaleString(),
        isDemo: !ReplicateService.isConfigured()
      };

    } catch (error) {
      console.error('故事生成错误:', error);
      throw new Error(`故事生成失败: ${error.message}`);
    }
  }

  // 获取示例故事创意
  static getExampleIdeas() {
    return [
      '小兔子想要找到彩虹的尽头',
      '小女孩发现了一个会说话的玩具熊',
      '机器人学会了做美味的蛋糕',
      '小鱼想要看看大海之外的世界',
      '小猫咪开了一家神奇的咖啡店',
      '勇敢的小男孩拯救了森林里的动物们'
    ];
  }
}