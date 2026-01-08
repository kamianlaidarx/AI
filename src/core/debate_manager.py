"""
辩论管理器模块
管理群聊辩论赛的完整流程
"""
import time
from enum import Enum, auto
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from ..utils import log


class DebateState(Enum):
    """辩论状态"""
    IDLE = auto()      # 无辩论
    JOINING = auto()   # 招募阶段
    ONGOING = auto()   # 辩论进行中
    JUDGING = auto()   # 评分中


@dataclass
class Speech:
    """发言记录"""
    user_id: str
    user_name: str
    side: str  # 'pro' or 'con'
    content: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class DebateSession:
    """辩论会话"""
    group_id: str
    topic: str
    state: DebateState = DebateState.JOINING
    pro_members: List[str] = field(default_factory=list)  # 正方成员ID
    con_members: List[str] = field(default_factory=list)  # 反方成员ID
    pro_names: Dict[str, str] = field(default_factory=dict)  # ID -> 昵称
    con_names: Dict[str, str] = field(default_factory=dict)
    speeches: List[Speech] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    scores: Dict = field(default_factory=dict)


class DebateManager:
    """辩论管理器"""

    # 触发关键词
    START_KEYWORDS = ['开始辩论', '发起辩论', '来场辩论']
    JOIN_PRO_KEYWORDS = ['正方', '加入正方', '支持正方']
    JOIN_CON_KEYWORDS = ['反方', '加入反方', '支持反方']
    BEGIN_KEYWORDS = ['开始', '开战', '开打']
    END_KEYWORDS = ['结束辩论', '终止辩论', '辩论结束']
    CANCEL_KEYWORDS = ['取消辩论', '取消']

    def __init__(self, ai_engine):
        """
        初始化辩论管理器

        Args:
            ai_engine: AI引擎实例
        """
        self.ai = ai_engine
        self.sessions: Dict[str, DebateSession] = {}  # group_id -> session

    def handle_message(self, group_id: str, user_id: str, user_name: str, content: str) -> Optional[str]:
        """
        处理消息，返回辩论相关回复

        Args:
            group_id: 群ID
            user_id: 用户ID
            user_name: 用户昵称
            content: 消息内容

        Returns:
            回复内容，如果不是辩论相关消息返回None
        """
        content = content.strip()
        session = self.sessions.get(group_id)

        # 无活跃辩论时，检查是否要开始
        if not session:
            for kw in self.START_KEYWORDS:
                if kw in content:
                    return self._start_debate(group_id, user_id, user_name, content, kw)
            return None

        # 根据状态处理
        if session.state == DebateState.JOINING:
            return self._handle_joining(session, user_id, user_name, content)
        elif session.state == DebateState.ONGOING:
            return self._handle_ongoing(session, user_id, user_name, content)
        elif session.state == DebateState.JUDGING:
            return "⏳ 正在评分中，请稍候..."

        return None

    def _start_debate(self, group_id: str, user_id: str, user_name: str,
                      content: str, keyword: str) -> str:
        """开始新辩论"""
        # 提取话题
        topic = content.split(keyword)[-1].strip()
        if not topic or len(topic) < 2:
            topic = "自由话题（请在辩论中自行确定）"

        # 创建会话
        session = DebateSession(group_id=group_id, topic=topic)
        self.sessions[group_id] = session

        log.info(f"群 {group_id} 开始辩论: {topic}")

        return f"""📢 辩论赛开始招募！

🎯 辩题：{topic}

📝 加入方式：
• 回复「正方」加入正方
• 回复「反方」加入反方

⚡ 人数就位后，任意参与者回复「开始」正式开战
❌ 回复「取消辩论」可取消"""

    def _handle_joining(self, session: DebateSession, user_id: str,
                        user_name: str, content: str) -> Optional[str]:
        """处理招募阶段"""
        # 检查取消
        for kw in self.CANCEL_KEYWORDS:
            if kw in content:
                del self.sessions[session.group_id]
                log.info(f"群 {session.group_id} 辩论已取消")
                return "❌ 辩论已取消"

        # 检查加入正方
        for kw in self.JOIN_PRO_KEYWORDS:
            if kw in content:
                return self._join_side(session, user_id, user_name, 'pro')

        # 检查加入反方
        for kw in self.JOIN_CON_KEYWORDS:
            if kw in content:
                return self._join_side(session, user_id, user_name, 'con')

        # 检查开始
        for kw in self.BEGIN_KEYWORDS:
            if content == kw or content.endswith(kw):
                return self._begin_debate(session, user_id)

        return None

    def _join_side(self, session: DebateSession, user_id: str,
                   user_name: str, side: str) -> str:
        """加入某一方"""
        # 检查是否已加入
        if user_id in session.pro_members:
            if side == 'pro':
                return "你已经在正方了"
            # 换边
            session.pro_members.remove(user_id)
            del session.pro_names[user_id]
        elif user_id in session.con_members:
            if side == 'con':
                return "你已经在反方了"
            # 换边
            session.con_members.remove(user_id)
            del session.con_names[user_id]

        # 加入
        if side == 'pro':
            session.pro_members.append(user_id)
            session.pro_names[user_id] = user_name
            side_name = "正方"
        else:
            session.con_members.append(user_id)
            session.con_names[user_id] = user_name
            side_name = "反方"

        pro_count = len(session.pro_members)
        con_count = len(session.con_members)

        status = f"当前：正方 {pro_count} 人 vs 反方 {con_count} 人"

        if pro_count > 0 and con_count > 0:
            status += "\n\n✅ 双方已就位，回复「开始」正式开战！"

        return f"✅ {user_name} 加入{side_name}！\n{status}"

    def _begin_debate(self, session: DebateSession, user_id: str) -> str:
        """正式开始辩论"""
        # 检查人数
        if not session.pro_members:
            return "⚠️ 正方还没有人，无法开始"
        if not session.con_members:
            return "⚠️ 反方还没有人，无法开始"

        # 检查发起者是否是参与者
        if user_id not in session.pro_members and user_id not in session.con_members:
            return "⚠️ 只有辩论参与者才能发起开始"

        # 更新状态
        session.state = DebateState.ONGOING
        session.start_time = time.time()

        pro_names = "、".join(session.pro_names.values())
        con_names = "、".join(session.con_names.values())

        log.info(f"群 {session.group_id} 辩论正式开始")

        return f"""⚔️ 辩论正式开始！

🎯 辩题：{session.topic}

👥 正方（{len(session.pro_members)}人）：{pro_names}
👥 反方（{len(session.con_members)}人）：{con_names}

📢 规则：
• 双方自由发言，阐述观点
• 可以反驳对方论点
• 结束时@我说「结束辩论」

🔥 开战！"""

    def _handle_ongoing(self, session: DebateSession, user_id: str,
                        user_name: str, content: str) -> Optional[str]:
        """处理辩论进行中"""
        # 检查结束
        for kw in self.END_KEYWORDS:
            if kw in content:
                return self._conclude_debate(session)

        # 记录发言（只记录参与者的）
        side = None
        if user_id in session.pro_members:
            side = 'pro'
        elif user_id in session.con_members:
            side = 'con'

        if side and len(content) > 5:  # 忽略太短的消息
            speech = Speech(
                user_id=user_id,
                user_name=user_name,
                side=side,
                content=content
            )
            session.speeches.append(speech)
            log.debug(f"记录发言: {user_name}({side}): {content[:30]}...")

        # 辩论中不主动回复，让双方自由发挥
        return None

    def _conclude_debate(self, session: DebateSession) -> str:
        """结束辩论并评分"""
        session.state = DebateState.JUDGING

        # 检查发言数量
        pro_speeches = [s for s in session.speeches if s.side == 'pro']
        con_speeches = [s for s in session.speeches if s.side == 'con']

        if not pro_speeches and not con_speeches:
            del self.sessions[session.group_id]
            return "😅 双方都没有发言，辩论无效！"

        if not pro_speeches:
            del self.sessions[session.group_id]
            return f"""🏆 辩论结束！

正方全程沉默... 反方不战而胜！

😏 正方辩友，你们是来旅游的吗？"""

        if not con_speeches:
            del self.sessions[session.group_id]
            return f"""🏆 辩论结束！

反方全程沉默... 正方不战而胜！

😏 反方辩友，键盘是不是坏了？"""

        # 构建发言记录
        pro_text = "\n".join([f"- {s.user_name}: {s.content}" for s in pro_speeches])
        con_text = "\n".join([f"- {s.user_name}: {s.content}" for s in con_speeches])

        # 调用AI评分
        try:
            result = self._ai_judge(session.topic, pro_text, con_text)
        except Exception as e:
            log.error(f"AI评分失败: {e}")
            del self.sessions[session.group_id]
            return "😵 AI裁判出了点问题，本场辩论作废..."

        # 清理会话
        del self.sessions[session.group_id]
        log.info(f"群 {session.group_id} 辩论结束")

        return result

    def _ai_judge(self, topic: str, pro_text: str, con_text: str) -> str:
        """AI评分和嘲讽"""
        prompt = f"""你是一场辩论赛的毒舌裁判，请评判以下辩论：

【辩题】{topic}

【正方观点】
{pro_text}

【反方观点】
{con_text}

请完成以下任务：
1. 分析双方论点的优劣
2. 给双方打分（0-100分）
3. 宣布获胜方
4. 用幽默尖锐的语气狠狠嘲讽输家的弱点（要好笑但不要人身攻击）

输出格式：
📊 裁判评分

正方得分：XX/100
• 优点：...
• 弱点：...

反方得分：XX/100
• 优点：...
• 弱点：...

🏆 获胜方：XX方！

😏 对输家的嘲讽：
（这里写一段尖锐好笑的嘲讽，100字左右）"""

        # 调用AI
        response = self.ai.generate_response(message=prompt, context=[])
        return f"🎬 辩论结束！\n\n{response}"

    def has_active_debate(self, group_id: str) -> bool:
        """检查群是否有进行中的辩论"""
        return group_id in self.sessions

    def get_debate_status(self, group_id: str) -> Optional[str]:
        """获取辩论状态"""
        session = self.sessions.get(group_id)
        if not session:
            return None

        state_names = {
            DebateState.JOINING: "招募中",
            DebateState.ONGOING: "进行中",
            DebateState.JUDGING: "评分中"
        }

        return f"""📋 辩论状态：{state_names.get(session.state, '未知')}

🎯 辩题：{session.topic}
👥 正方：{len(session.pro_members)}人
👥 反方：{len(session.con_members)}人
💬 发言数：{len(session.speeches)}条"""
