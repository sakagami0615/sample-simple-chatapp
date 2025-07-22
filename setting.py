from dotenv import load_dotenv

from common.create_logger import create_logger

# ページ上部に表示するタイトル文字
TITLE = "langchain-streamlit-chat"

# ロガー情報（ロガー名、ログレベル）
LOG_NAME = "simple-chat"
LOG_LEVEL = "DEBUG"


load_dotenv()

LOGGER = create_logger(LOG_NAME, LOG_LEVEL)
