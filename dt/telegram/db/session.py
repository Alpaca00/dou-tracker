import logging

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, cast, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.testing.plugin.plugin_base import logging

from dt.telegram.config.bot_config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_HOST,
)
from dt.telegram.models import Base, BotUser, UserSubscription


class PostgresDatabaseConfig:
    """The database configuration."""

    user = POSTGRES_USER
    password = POSTGRES_PASSWORD
    db = POSTGRES_DB
    host = POSTGRES_HOST

    @classmethod
    def get_database_url(cls):
        """Return the database full URL."""
        return f"postgresql+psycopg2://{cls.user}:{cls.password}@{cls.host}/{cls.db}"


DATABASE_URL = PostgresDatabaseConfig.get_database_url()

engine = create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


class SessionManager:
    """The session manager."""

    def __init__(self):
        self.session = Session()

    def __enter__(self):
        """Return the session object when entering the context manager."""
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """Commit the session if no exceptions occurred, otherwise rollback."""
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()


class DatabaseManagerPostgreSQL:
    """The database manager for PostgreSQL."""

    @staticmethod
    def add_user(user_id: str, chat_id: str):
        """Add a user to the database."""
        with SessionManager() as session:
            user = BotUser(user_id=cast(user_id, String), chat_id=chat_id)
            session.add(user)

    @staticmethod
    def get_user(user_id: str):
        """Get a user from the database."""
        with SessionManager() as session:
            return (
                session.query(BotUser)
                .filter_by(user_id=cast(user_id, String))
                .one_or_none()
            )

    @staticmethod
    def get_all_users():
        """Get all users from the database."""
        with SessionManager() as session:
            return session.query(BotUser).all()

    @staticmethod
    def delete_user(user_id: str):
        """Delete a user from the database."""
        with SessionManager() as session:
            user = (
                session.query(BotUser)
                .filter_by(user_id=cast(user_id, String))
                .first()
            )
            session.delete(user)

    @staticmethod
    def add_subscribe_vacancy(user_id: str, subscription_name: str):
        """Subscribe a user to a vacancy."""
        try:
            with SessionManager() as session:
                subscription = UserSubscription(
                    user_id=user_id, subscription_name=subscription_name
                )
                session.add(subscription)
        except IntegrityError as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def delete_subscribe_vacancy(user_id: str, subscription_name: str):
        """Unsubscribe a user from a vacancy."""
        with SessionManager() as session:
            subscription = (
                session.query(UserSubscription)
                .filter_by(
                    user_id=cast(user_id, String),
                    subscription_name=subscription_name,
                )
                .first()
            )
            session.delete(subscription)

    @staticmethod
    def get_user_subscriptions(user_id: str):
        """Get a user's subscriptions."""
        with SessionManager() as session:
            user = (
                session.query(BotUser)
                .filter_by(user_id=cast(user_id, String))
                .first()
            )
            subscriptions = (
                session.query(UserSubscription)
                .filter_by(user_id=cast(user.user_id, String))
                .all()
            )
            return [
                subscription.subscription_name
                for subscription in subscriptions
            ]

    @staticmethod
    def get_all_subscriptions():
        """Get all subscriptions."""
        with SessionManager() as session:
            subscriptions = (
                session.query(UserSubscription).distinct().all()
            )
            return [
                subscription.subscription_name
                for subscription in subscriptions
            ]


Base.metadata.create_all(engine)


def initialize_database():
    """Initialize the database."""
    manager = DatabaseManagerPostgreSQL()
    return manager
