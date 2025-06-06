import os
from dotenv import load_dotenv

load_dotenv()

KEY: str = os.environ.get("KEY") or ""
ALGORITHM: str = os.environ.get("ALGORITHM") or ""
ACCESS_TOKEN_EXPIRE_MINUTES: float = float(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "0")
)

if not KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise RuntimeError(
        "KEY, ALGORITHM, or ACCESS_TOKEN_EXPIRE_MINUTES env vars are not set"
    )
