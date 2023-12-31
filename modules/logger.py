from sys import stdout
from loguru import logger
from pytz import timezone

def setup_logger():
    logger.remove()

    frm = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> - <level>{message}</level>"

    logger.add("info.log", level="DEBUG", format=frm)
    logger.add(stdout, level="DEBUG", format=frm)

if __name__ == '__main__':
    setup_logger()

    logger.info("Привет, это сообщение уровня INFO")
    logger.warning("Внимание! Это сообщение уровня WARNING")