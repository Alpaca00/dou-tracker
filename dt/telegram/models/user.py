from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from dt.telegram.models import Base


class BotUser(Base):
    __tablename__ = "bot_users"  # noqa

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False)
    chat_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship(
        "UserSubscription",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"  # noqa

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        String, ForeignKey("bot_users.user_id"), nullable=False
    )
    subscription_name = Column(String, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("BotUser", back_populates="subscriptions")
