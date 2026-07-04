from pathlib import Path

import yfinance as yf

YFINANCE_CACHE_DIR = Path("data/cache/yfinance")


def configure_yfinance_cache(cache_dir: Path = YFINANCE_CACHE_DIR) -> None:
    """Keep yfinance cache inside the project workspace."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    yf.set_tz_cache_location(str(cache_dir))
