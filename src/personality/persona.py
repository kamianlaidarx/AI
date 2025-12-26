"""
人格系统模块
管理AI女友的性格、说话风格和记忆
"""
import yaml
from pathlib import Path
from typing import Dict, Any, List


class Persona:
    """人格管理类"""

    def __init__(self, config_path: str = "config/persona.yaml"):
        """
        初始化人格系统

        Args:
            config_path: 人格配置文件路径
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.memory: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """加载人格配置"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"人格配置文件不存在: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def get_system_prompt(self) -> str:
        """
        生成系统提示词

        Returns:
            系统提示词
        """
        # 获取基本信息
        name = self.config.get('name', '小雨')
        age = self.config.get('age', 22)
        description = self.config.get('description', '')

        # 获取性格特征
        personality = self.config.get('personality', {})
        traits = personality.get('traits', [])
        traits_text = '、'.join(traits)

        # 获取说话风格
        speaking_style = self.config.get('speaking_style', {})
        tone = speaking_style.get('tone', '温柔亲切')
        particles = speaking_style.get('particles', [])
        particles_text = '、'.join(particles)

        sentence_style = speaking_style.get('sentence_style', [])
        style_text = '\n  - '.join(sentence_style)

        # 获取兴趣爱好
        interests = self.config.get('interests', [])
        interests_text = '、'.join(interests)

        # 构建系统提示词
        system_prompt = f"""你是{name}，一个{age}岁的女生。{description}

你的性格特点：{traits_text}

说话风格：
- 语气{tone}
- 常用语气词：{particles_text}
- 句式特点：
  - {style_text}

你的兴趣爱好：{interests_text}

请注意：
1. 保持性格一致，不要突然改变说话风格
2. 适当使用语气词和emoji，但不要过度
3. 回复要简洁自然，像真实的聊天一样
4. 关心对方的感受，适时表达关心
5. 记住之前的对话内容，保持连贯性
6. 不要说你是AI或机器人
7. 回复长度控制在1-3句话，不要太长"""

        return system_prompt

    def update_memory(self, key: str, value: Any):
        """
        更新记忆

        Args:
            key: 记忆键
            value: 记忆值
        """
        self.memory[key] = value

    def get_memory(self, key: str, default: Any = None) -> Any:
        """
        获取记忆

        Args:
            key: 记忆键
            default: 默认值

        Returns:
            记忆值
        """
        return self.memory.get(key, default)

    def get_speaking_style(self) -> Dict[str, Any]:
        """
        获取说话风格配置

        Returns:
            说话风格字典
        """
        return self.config.get('speaking_style', {})

    def get_personality_traits(self) -> List[str]:
        """
        获取性格特征列表

        Returns:
            性格特征列表
        """
        personality = self.config.get('personality', {})
        return personality.get('traits', [])

    def reload(self):
        """重新加载人格配置"""
        self._load_config()
        self.memory.clear()
