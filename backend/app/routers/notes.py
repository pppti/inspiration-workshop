import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.models.note import InspirationNote
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("", response_model=NoteListResponse)
async def list_notes(
    page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
    search: str | None = None, category: str | None = None, tag: str | None = None,
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
):
    q = select(InspirationNote)
    count_q = select(func.count(InspirationNote.id))

    if search:
        like = f"%{search}%"
        q = q.where(InspirationNote.title.like(like) | InspirationNote.body.like(like))
        count_q = count_q.where(InspirationNote.title.like(like) | InspirationNote.body.like(like))
    if category:
        q = q.where(InspirationNote.category == category)
        count_q = count_q.where(InspirationNote.category == category)

    total_r = await db.execute(count_q)
    total = total_r.scalar() or 0

    q = q.order_by(InspirationNote.created_at.desc()).offset((page - 1) * limit).limit(limit)
    items = []
    result = await db.execute(q)
    for n in result.scalars().all():
        items.append(_note_to_response(n))
        # Filter by tag in Python (since tags in JSON)
    if tag:
        items = [it for it in items if tag in it.tags]
        total = len(items)

    return NoteListResponse(items=items, total=total, page=page, limit=limit)


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(InspirationNote).where(InspirationNote.id == note_id))
    n = r.scalar_one_or_none()
    if not n: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return _note_to_response(n)


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(req: NoteCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    note = InspirationNote(
        title=req.title, body=req.body, category=req.category, source=req.source,
        tags_json=json.dumps(req.tags, ensure_ascii=False),
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return _note_to_response(note)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, req: NoteUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(InspirationNote).where(InspirationNote.id == note_id))
    n = r.scalar_one_or_none()
    if not n: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    for field in ["title", "body", "category", "source"]:
        if getattr(req, field) is not None: setattr(n, field, getattr(req, field))
    if req.tags is not None:
        n.tags_json = json.dumps(req.tags, ensure_ascii=False)
    n.updated_at = datetime.utcnow().isoformat()
    await db.commit()
    await db.refresh(n)
    return _note_to_response(n)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(InspirationNote).where(InspirationNote.id == note_id))
    n = r.scalar_one_or_none()
    if not n: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await db.delete(n)
    await db.commit()


def _note_to_response(n: InspirationNote) -> NoteResponse:
    try: tags = json.loads(n.tags_json or "[]")
    except json.JSONDecodeError: tags = []
    return NoteResponse(id=n.id, title=n.title, body=n.body, category=n.category, source=n.source, tags=tags, created_at=n.created_at, updated_at=n.updated_at)
