"""주차 요금 계산 로직 (SPEC.md 7장). tkinter, print, input을 쓰지 않는다."""

import re

FREE_MINUTES = 30
UNIT_FEE = 500
MAX_FEE = 20000

TIME_PATTERN = re.compile(r"^([0-9]{1,2}):([0-9]{2})$")


def parse_time(text, label):
    """'시:분' 문자열을 자정부터의 분(int)으로 바꾼다. label은 "입차"/"출차"."""
    text = text.strip()
    if text == "":
        raise ValueError(f"{label} 시각을 입력하세요.")
    match = TIME_PATTERN.match(text)
    if match is None:
        raise ValueError(f"{label} 시각이 올바르지 않습니다. 00:00~23:59 사이로 입력하세요. (예: 09:30)")
    hour = int(match.group(1))
    minute = int(match.group(2))
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"{label} 시각이 올바르지 않습니다. 00:00~23:59 사이로 입력하세요. (예: 09:30)")
    return hour * 60 + minute


def calc_fee(minutes):
    """주차 시간(분)으로 요금(int)을 계산한다. 한 건 최대 20,000원."""
    if minutes <= FREE_MINUTES:
        return 0
    over = minutes - FREE_MINUTES
    units = (over + 9) // 10  # 10분 단위 올림 (정수 계산)
    return min(units * UNIT_FEE, MAX_FEE)


def format_duration(minutes):
    """분을 "45분", "1시간", "1시간 35분" 형식으로 바꾼다."""
    hours, mins = divmod(minutes, 60)
    if hours == 0:
        return f"{mins}분"
    if mins == 0:
        return f"{hours}시간"
    return f"{hours}시간 {mins}분"


def format_won(amount):
    """금액을 "1,500원" 형식으로 바꾼다."""
    return f"{amount:,}원"


def make_record(entry_text, exit_text):
    """입차·출차 문자열로 기록 dict를 만든다. 오류면 ValueError."""
    entry = parse_time(entry_text, "입차")
    exit_ = parse_time(exit_text, "출차")
    if exit_ <= entry:
        raise ValueError("출차 시각은 입차 시각보다 늦어야 합니다. (자정을 넘긴 주차는 계산하지 않습니다)")
    minutes = exit_ - entry
    return {
        "entry": "%02d:%02d" % divmod(entry, 60),
        "exit": "%02d:%02d" % divmod(exit_, 60),
        "minutes": minutes,
        "fee": calc_fee(minutes),
    }


def total_fee(fees):
    """요금 리스트의 합계(int). 합계에는 상한이 없다."""
    return sum(fees)
