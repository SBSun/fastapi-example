from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

note_tag_association = Table(
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(36), ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id"))
)

class Note(Base):
    __tablename__ = "Note"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(36), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    memo_date: Mapped[str] = mapped_column(String(8), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    # 다대다 관계를 맺, back_populates 옵션을 이용해 note 객체를 조회할 때 연관된 tag 객도 모두 가져온다.
    tags = relationship(
        "Tag",
        secondary=note_tag_association,
        back_populates="notes",
        lazy="joined"
    )

class Tag(Base):
    __tablename__ = "Tag"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    notes = relationship(
        "Note",
        secondary=note_tag_association,
        back_populates="tags",
        lazy="joined"
    )