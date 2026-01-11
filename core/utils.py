from datetime import datetime, date
from typing import Optional
from core.config import PL_DATE_FMT, PL_DATETIME_FMT

def now_pl_date() -> str:
    return datetime.now().strftime(PL_DATE_FMT)

def now_pl_datetime() -> str:
    return datetime.now().strftime(PL_DATETIME_FMT)

def parse_pl_date(s: str) -> date:
    return datetime.strptime(s, PL_DATE_FMT).date()

def to_pl_date_from_any(s: str) -> str:
    if not s:
        return ""
    return s.strip()

def to_pl_datetime_from_any(s: str) -> str:
    if not s:
        return ""
    return s.strip()

def parse_date_pl_or_iso(s: str) -> Optional[date]:
    if not s:
        return None
    try:
        return parse_pl_date(s.strip())
    except Exception:
        return None

def days_left_signed(s: str) -> Optional[int]:
    d = parse_date_pl_or_iso(s)
    if not d:
        return None
    return (d - date.today()).days