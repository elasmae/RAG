from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}")
__all__ = ["logger"]
