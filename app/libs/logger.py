from pathlib import Path
from loguru import logger
from .config import Config

class Logging:
    def configure_logging():
        # Create custom log directory if not exist
        APP_LOG_DIR = Config.APP_LOG_PATH
        APP_LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Create system log directory if not exist
        SYS_LOG_DIR = Config.SYS_LOG_PATH
        SYS_LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Remove any default handlers
        logger.remove()

        # Add handlers for different severity levels
        logger.add(APP_LOG_DIR / "debug.log", level="DEBUG", rotation="1 MB", encoding="utf-8", enqueue=True)
        logger.add(APP_LOG_DIR / "info.log", level="INFO", rotation="1 MB", encoding="utf-8", enqueue=True, filter=lambda record: record["level"].name == "INFO")
        logger.add(APP_LOG_DIR / "error.log", level="ERROR", rotation="1 MB", encoding="utf-8", enqueue=True)
        
        # System log for lifecycle/config info
        logger.add(SYS_LOG_DIR / "sys.log", level="INFO", rotation="1 MB", encoding="utf-8", enqueue=True, filter=lambda r: r["extra"].get("system") is True)

        # Optional: Also log to console if desired
        logger.add(lambda msg: print(msg, end=""), level="DEBUG")

    def console(message: str):
        # show message on screen 
        print(message)
    
    def info(message: str):
        logger.info(message)

    def debug(message: str):
        logger.debug(message)

        # Show message on screen while in Development
        if Config.RUN_ENV == "dev":
            Logging.console(message)

    def error(message: str):
        logger.error(message)

        # Show message on screen while in Development
        if Config.RUN_ENV == "dev":
            Logging.console(message)


        
