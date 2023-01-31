from loguru import logger
from pathlib import Path
from datetime import date

from ..settings import BASE_DIR, PROJECT_NAME

def setup_logger(app_name=PROJECT_NAME):
    log_folder = Path(BASE_DIR).parent.joinpath("logs")
    if not log_folder.exists:
        log_folder.mkdir
    
    file = log_folder.joinpath("{}_{}.log".format(app_name, str(date.today())))
    logger.add(file, format="{time} - {level} - {name}:{function}[{line}]{process}.{thread}: {message}", rotation="5 MB")