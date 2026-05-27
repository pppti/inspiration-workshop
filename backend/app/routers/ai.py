import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.user import User
from app.models.note import InspirationNote
from app.models.ai import AiConversation, AiMessage
from app.schemas.ai import *
from app.services.ai_service import call_claude, IMPORT_PROMPT, INSPIRE_PROMPT, SUMMARIZE_PROMPT, SEARCH_PROMPT, CHAT_SYSTEM
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/ai", tags=["ai"])


# ─── Chat ───

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    conv = None
    if req.conversation_id:
        r = await db.execute(select(AiConversation).where(AiConversation.id == req.conversation_id))
        conv = r.scalar_one_or_none()
    if not conv:
        conv = AiConversation(title=req.message[:30] + ("..." if len(req.message) > 30 else ""))
        db.add(conv)
        await db.flush()

    db.add(AiMessage(conversation_id=conv.id, role="user", content=req.message))
    r = await db.execute(select(AiMessage).where(AiMessage.conversation_id == conv.id).order_by(AiMessage.created_at))
    history = [{"role": m.role, "content": m.content} for m in r.scalars().all()]
    messages = history[-20:]
    reply = await call_claude(CHAT_SYSTEM, messages, max_tokens=800)
    db.add(AiMessage(conversation_id=conv.id, role="assistant", content=reply))
    await db.commit()
    return ChatResponse(conversation_id=conv.id, reply=reply)


@router.get("/conversations", response_model=AiConversationListResponse)
async def list_conversations(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(AiConversation).options(selectinload(AiConversation.messages)).order_by(AiConversation.created_at.desc()).limit(30))
    convs = r.unique().scalars().all()
    return AiConversationListResponse(items=[AiConversationResponse(id=c.id, title=c.title, created_at=c.created_at, messages=[AiMessageResponse(id=m.id, role=m.role, content=m.content, created_at=m.created_at) for m in c.messages]) for c in convs])


@router.delete("/conversations/{conv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(conv_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(AiConversation).where(AiConversation.id == conv_id))
    conv = r.scalar_one_or_none()
    if not conv: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await db.delete(conv)
    await db.commit()


# ─── Import ───

@router.post("/import", response_model=ImportResponse)
async def smart_import(req: ImportRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    reply = await call_claude(IMPORT_PROMPT, [{"role": "user", "content": req.text}], max_tokens=500)
    try:
        reply_clean = reply.strip()
        if reply_clean.startswith("```"): reply_clean = reply_clean.split("\n", 1)[1].rsplit("\n```")[0]
        data = json.loads(reply_clean)
        return ImportResponse(title=data.get("title", ""), body=data.get("body", req.text), category=data.get("category"), tags=data.get("tags", []))
    except (json.JSONDecodeError, KeyError):
        return ImportResponse(title="", body=req.text, tags=[])


# ─── Inspire ───

@router.post("/inspire", response_model=AiInspireResponse)
async def inspire(req: AiInspireRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    reply = await call_claude(INSPIRE_PROMPT, [{"role": "user", "content": f"我需要以下方向的灵感：{req.direction}"}], max_tokens=800)
    return AiInspireResponse(suggestions=reply)


# ─── Summarize ───

@router.post("/summarize", response_model=AiSummarizeResponse)
async def summarize(req: AiSummarizeRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not req.note_ids: raise HTTPException(status_code=400, detail="No note IDs")
    r = await db.execute(select(InspirationNote).where(InspirationNote.id.in_(req.note_ids)))
    notes = r.scalars().all()
    text = "\n\n".join([f"[{n.category or '未分类'}] {n.title or '无标题'}\n{n.body}" for n in notes])
    summary = await call_claude(SUMMARIZE_PROMPT, [{"role": "user", "content": f"请汇总以下{len(notes)}条灵感笔记：\n\n{text}"}], max_tokens=500)
    return AiSummarizeResponse(summary=summary)


# ─── Search ───

@router.post("/search", response_model=AiSearchResponse)
async def ai_search(req: AiSearchRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(InspirationNote).order_by(InspirationNote.created_at.desc()).limit(100))
    all_notes = r.scalars().all()
    notes_text = "\n".join([f"ID:{n.id} | [{n.category or '未分类'}] {n.title or '无标题'} | {n.body[:200]}" for n in all_notes])
    reply = await call_claude(SEARCH_PROMPT, [{"role": "user", "content": f"用户搜索：{req.query}\n\n灵感笔记列表：\n{notes_text}"}], max_tokens=600)
    try:
        reply_clean = reply.strip()
        if reply_clean.startswith("```"): reply_clean = reply_clean.split("\n", 1)[1].rsplit("\n```")[0]
        data = json.loads(reply_clean)
        return AiSearchResponse(results=data.get("results", []), summary=data.get("summary", ""))
    except (json.JSONDecodeError, KeyError):
        return AiSearchResponse(results=[], summary=reply[:200])
