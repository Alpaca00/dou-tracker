import logging

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, cast, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.testing.plugin.plugin_base import logging

from dt.config import DatabaseConfig
from dt.telegram.models import (
    Base,
    BotUser,
    UserSubscription,
    Category,
    Job,
)


class PostgresDatabaseConfig:
    """The database configuration."""

    user = DatabaseConfig.POSTGRES_USER
    password = DatabaseConfig.POSTGRES_PASSWORD
    db = DatabaseConfig.POSTGRES_DB
    host = DatabaseConfig.POSTGRES_HOST

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

    @staticmethod
    def add_category(name: str, description: str = None):
        """Add a category to the database."""
        with SessionManager() as session:
            category = Category(name=name, description=description)
            session.add(category)

    @staticmethod
    def get_category_by_name(name: str):
        """Get a category by name."""
        with SessionManager() as session:
            return (
                session.query(Category).filter_by(name=name).one_or_none()
            )

    @staticmethod
    def add_job(
        title: str,
        company: str,
        location: str,
        description: str,
        link: str,
        category_name: str,
    ):
        """Add a job to the database."""
        try:
            with SessionManager() as session:
                category = (
                    session.query(Category)
                    .filter_by(name=category_name)
                    .first()
                )
                if not category:
                    category = Category(name=category_name)
                    session.add(category)
                job = Job(
                    title=title,
                    company=company,
                    location=location,
                    description=description,
                    link=link,
                    category=category,
                )
                session.add(job)
        except IntegrityError as e:
            logging.error(f"Error: {e}")

    @staticmethod
    def get_jobs_by_category(category_name: str):
        """Get jobs by category."""
        with SessionManager() as session:
            category = (
                session.query(Category)
                .filter_by(name=category_name)
                .first()
            )
            if category:
                return category.jobs
            return []

    @staticmethod
    def get_all_categories():
        """Get all categories."""
        with SessionManager() as session:
            return session.query(Category).all()


Base.metadata.create_all(engine)


def initialize_database():
    """Initialize the database."""
    manager = DatabaseManagerPostgreSQL()
    return manager
