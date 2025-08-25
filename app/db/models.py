from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey, Index, Boolean, UniqueConstraint



class Base(DeclarativeBase):
    pass


class Number(Base):
    __tablename__ = "numbers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    country: Mapped[str] = mapped_column(String(2), index=True)
    last4: Mapped[str] = mapped_column(String(4))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reports: Mapped[list[Report]] = relationship(back_populates="number", cascade="all, delete-orphan")
    appeals: Mapped[list[Appeal]] = relationship(back_populates="number", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_numbers_country_hash", "country", "phone_hash"),)


class Report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number_id: Mapped[int] = mapped_column(ForeignKey("numbers.id", ondelete="CASCADE"), index=True)
    channel: Mapped[str] = mapped_column(String(8), index=True)
    reason: Mapped[str] = mapped_column(String(64), index=True)
    details: Mapped[str] = mapped_column(Text)
    evidence_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    reporter_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    ip_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_moderated: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    number: Mapped[Number] = relationship(back_populates="reports")
    __table_args__ = (
    Index("ix_reports_number_time", "number_id", "created_at"),
    UniqueConstraint("number_id", "reporter_id", "channel", name="uq_report_once_per_reporter_channel"),
)


class Appeal(Base):
    __tablename__ = "appeals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number_id: Mapped[int] = mapped_column(ForeignKey("numbers.id", ondelete="CASCADE"), index=True)
    claimant_token: Mapped[str] = mapped_column(String(64), index=True)
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    number: Mapped[Number] = relationship(back_populates="appeals")