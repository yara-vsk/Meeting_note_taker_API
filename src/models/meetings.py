from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base
from sqlalchemy import String
from src.models.users import User


class Meeting(Base):
    __tablename__ = "meeting"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="cascade"), nullable=False)

    user: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"Meeting(id={self.id!r})"