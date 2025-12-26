"""
提示词模板模块
存储各种场景的提示词模板
"""


class PromptTemplates:
    """提示词模板类"""

    # 首次对话提示词
    FIRST_CONVERSATION = """这是你们的第一次对话，请表现得自然、友好，但不要过于热情。"""

    # 长时间未联系提示词
    LONG_TIME_NO_SEE = """你们已经有一段时间没有联系了，可以适当表达想念，但要自然。"""

    # 情绪识别提示词
    EMOTION_DETECTION = """请识别对方的情绪状态（开心/难过/生气/焦虑等），并给予适当的回应。"""

    # 关心提示词
    CARING_RESPONSE = """对方似乎遇到了困难或心情不好，请表达关心和支持。"""

    # 分享日常提示词
    DAILY_SHARING = """可以适当分享一些你的"日常"，让对话更生动有趣。"""

    # 晚安提示词
    GOODNIGHT = """对方要休息了，给一个温馨的晚安回复。"""

    # 早安提示词
    GOODMORNING = """早上好！给对方一个元气满满的问候。"""

    @staticmethod
    def get_emotion_prompt(emotion: str) -> str:
        """
        根据情绪获取提示词

        Args:
            emotion: 情绪类型

        Returns:
            提示词
        """
        emotion_prompts = {
            "happy": "对方心情很好，可以一起分享快乐。",
            "sad": "对方心情不好，请给予安慰和支持。",
            "angry": "对方似乎有些生气，请温柔地安抚。",
            "anxious": "对方有些焦虑，请帮助ta放松心情。",
            "tired": "对方很累了，请表达关心，建议ta休息。"
        }

        return emotion_prompts.get(emotion, "")

    @staticmethod
    def get_time_based_prompt(hour: int) -> str:
        """
        根据时间获取提示词

        Args:
            hour: 小时（0-23）

        Returns:
            提示词
        """
        if 5 <= hour < 12:
            return "现在是早上，可以问候早安，询问对方的计划。"
        elif 12 <= hour < 14:
            return "现在是中午，可以关心对方吃饭了吗。"
        elif 14 <= hour < 18:
            return "现在是下午，可以聊聊工作或学习的情况。"
        elif 18 <= hour < 22:
            return "现在是晚上，可以聊聊今天发生的事情。"
        else:
            return "现在是深夜，如果对方还没睡，可以关心一下为什么还不休息。"
