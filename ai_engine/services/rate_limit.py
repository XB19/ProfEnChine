import time

_LAST_RATE_LIMIT_LOG_TIME = None


def should_log_rate_limit(last_logged_at, now=None, cooldown_seconds=60):
    """Return (should_log, updated_last_logged_at)."""
    if now is None:
        now = time.monotonic()

    if last_logged_at is None or (now - last_logged_at) >= cooldown_seconds:
        return True, now

    return False, last_logged_at


def is_rate_limit_error(error) -> bool:
    error_str = str(error).lower()
    return "429" in str(error) or "rate_limit" in error_str or "tokens per day" in error_str
