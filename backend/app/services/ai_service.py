import httpx
from app.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


def _is_available() -> bool:
    return bool(ANTHROPIC_API_KEY)


async def call_claude(system_prompt: str, messages: list[dict], max_tokens: int = 1000) -> str:
    if not _is_available():
        return "[AI 未配置] 请设置 ANTHROPIC_API_KEY 环境变量。"

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": ANTHROPIC_MODEL,
                    "max_tokens": max_tokens,
                    "system": system_prompt,
                    "messages": messages,
                },
            )
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            return f"[AI 错误: {response.status_code}]"
    except Exception as e:
        return f"[AI 错误: {str(e)[:100]}]"


# ─── Chat ───

CHAT_SYSTEM = """你是一位创意写作助手，擅长提供灵感、构思情节、塑造人物。
你的回答应当：
- 富有创造力和启发性
- 给出具体可操作的写作建议
- 适当引用经典文学作品或写作技法
- 使用中文
- 不要使用"作为AI"之类的表述"""


async def chat_reply(history: list[dict], user_message: str) -> str:
    messages = []
    for h in history[-20:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": user_message})
    return await call_claude(CHAT_SYSTEM, messages, max_tokens=800)


# ─── Import ───

IMPORT_PROMPT = """用户提供了一段灵感随笔，请整理归类。返回纯JSON（不要markdown代码块）：
{
  "title": "简短标题",
  "body": "整理后的正文，保留所有关键信息",
  "category": "character/plot/dialogue/scene/material/essay 中选一个",
  "tags": ["标签1", "标签2"]
}"""

# ─── Inspire ───

INSPIRE_PROMPT = """用户需要创作灵感。根据用户给出的方向，提供3-5个具体、有创意的灵感建议。
每个建议包含一个标题和简要说明（2-3句话）。回复使用中文，简洁有力。"""

# ─── Summarize ───

SUMMARIZE_PROMPT = """用户提供了多条灵感笔记。请生成一份简洁的汇总分析：
1. 主要主题和类型
2. 可以串联的思路或情节线
3. 创作建议（1-2条）
总字数控制在200字以内。"""

# ─── Search ───

SEARCH_PROMPT = """用户正在寻找与某个主题相关的灵感笔记。系统会列出用户的灵感笔记。
请从中找出最相关的记录，并给出推荐理由。如果没有完全匹配的，也可以给出接近的结果。
返回纯JSON（不要markdown代码块）：
{
  "results": [{"id": 记录ID, "title": "标题", "snippet": "相关片段(50字内)", "relevance": "匹配理由(20字内)"}],
  "summary": "一句话总结搜索结果"
}
返回最多5条结果。"""
