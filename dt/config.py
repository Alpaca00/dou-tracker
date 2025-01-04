import ast
import os

from dotenv import load_dotenv

from dt.extension import conf

load_dotenv()

class ScrapperConfig:
    PROXY_ORIGIN_HOST = conf.SCRAPER.proxy_origin_host
    PROXY_FALLBACK_HOST = conf.SCRAPER.proxy_fallback_host
    PROXY_VERIFY_HOST = conf.SCRAPER.proxy_verify_host
    MAIN_HOST = conf.SCRAPER.main_host



class GlobalConfig:
    LOGGING = bool(ast.literal_eval(conf.GLOBAL.logging))


class ServerConfig:
    TITLE = "DOU Vacancies API"
    DESCRIPTION = "API for fetching job vacancies from the DOU website."
    SERVER_VERSION = "1.0.0"
    API_VERSION = "v1"
    API_KEY = os.environ.get("API_KEY")


class BotConfig:
    TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TELEGRAM_TOKEN")
    VACANCIES_HOST = conf.BOT.vacancies_host
    API_CLIENT = conf.BOT.api_client_base_url
    API_CLIENT_TIMEOUT = int(conf.BOT.api_client_timeout)
    SCHEDULER_INTERVAL = int(conf.BOT.scheduler_interval)


class DatabaseConfig:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
