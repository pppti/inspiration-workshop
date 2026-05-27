from datetime import datetime
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class InspirationNote(Base):
    __tablename__ = "inspiration_note"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str | None] = mapped_column(String(500))
    body: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str | None] = mapped_column(String(50))
    source: Mapped[str | None] = mapped_column(String(200))
    tags_json: Mapped[str | None] = mapped_column(default="[]")  # JSON array string
    created_at: Mapped[str] = mapped_column(String(25), default=lambda: datetime.utcnow().isoformat())
    updated_at: Mapped[str] = mapped_column(String(25), default=lambda: datetime.utcnow().isoformat())
