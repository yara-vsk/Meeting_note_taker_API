from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.db import Base
from sqlalchemy import String

from src.models.meetings import Meeting


class AudioRecord(Base):
    __tablename__ = "audiorecord"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(500), unique=True)
    audio_note: Mapped[Optional[str]] = mapped_column(String(1000))
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id", ondelete="cascade"))

    def __repr__(self) -> str:
        return f"AudioRecords(id={self.id!r})"


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(1000))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    meeting_id: Mapped[int] = mapped_column(ForeignKey('meeting.id', ondelete="cascade"), nullable=False)

    audio_record: Mapped["AudioRecord"] = relationship(AudioRecord)
    meeting: Mapped["Meeting"] = relationship(Meeting)

    def __repr__(self) -> str:
        return f"Items(id={self.id!r})"