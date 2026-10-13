# logic.py
# 용돈 기입장의 계산과 판정. 화면(Flet)은 모른다.
# 기록 한 건은 {"kind": "지출", "memo": "점심", "amount": 8000} 모양의 dict다.
# 함수는 받은 목록을 고치지 않고 새 목록을 돌려준다.

import sys

# 파이썬 3.11부터는 4300자리가 넘는 정수를 글자와 서로 바꾸지 못하게 막아 둔다.
# 금액에 상한을 두지 않기로 했으므로 이 제한을 푼다.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

INCOME = "수입"
EXPENSE = "지출"
KINDS = (INCOME, EXPENSE)
NO_MEMO = "(내용 없음)"

MSG_KIND = "구분을 고릅니다"
MSG_AMOUNT_EMPTY = "금액을 입력합니다"
MSG_AMOUNT_BAD = "금액은 0보다 큰 정수로 입력합니다"


def parse_amount(text):
    """금액 칸의 글자를 0보다 큰 정수로 바꾼다. 바꿀 수 없으면 None."""
    if not isinstance(text, str):
        return None
    digits = text.strip().replace(",", "")
    if digits == "" or any(ch not in "0123456789" for ch in digits):
        return None
    amount = int(digits)
    if amount <= 0:
        return None
    return amount


def clean_memo(text):
    """내용 칸의 글자에서 앞뒤 공백을 자른다. 비어 있으면 "(내용 없음)"."""
    if not isinstance(text, str):
        return NO_MEMO
    memo = text.strip()
    if memo == "":
        return NO_MEMO
    return memo


def add_entry(entries, kind, memo, amount_text):
    """기록을 맨 뒤에 붙인 (새 목록, "")을 돌려준다.
    입력이 잘못됐으면 (그대로인 목록, 안내 문구)를 돌려준다."""
    if kind not in KINDS:
        return list(entries), MSG_KIND
    amount = parse_amount(amount_text)
    if amount is None:
        if not isinstance(amount_text, str) or amount_text.strip() == "":
            return list(entries), MSG_AMOUNT_EMPTY
        return list(entries), MSG_AMOUNT_BAD
    entry = {"kind": kind, "memo": clean_memo(memo), "amount": amount}
    return list(entries) + [entry], ""


def remove_entry(entries, index):
    """index번 줄(0부터)을 뺀 새 목록을 돌려준다. 없는 번호면 그대로 돌려준다."""
    if not isinstance(index, int) or not 0 <= index < len(entries):
        return list(entries)
    return list(entries[:index]) + list(entries[index + 1:])


def totals(entries):
    """(수입 합계, 지출 합계, 잔액)을 돌려준다."""
    income = sum(e["amount"] for e in entries if e["kind"] == INCOME)
    expense = sum(e["amount"] for e in entries if e["kind"] == EXPENSE)
    return income, expense, income - expense


def format_won(amount):
    """천 단위마다 쉼표를 넣고 "원"을 붙인다. 1234567 -> "1,234,567원" """
    return f"{amount:,}원"


def format_signed(kind, amount):
    """목록의 줄에 보여 줄 금액. 수입은 "+", 지출은 "-"를 앞에 붙인다."""
    sign = "+" if kind == INCOME else "-"
    return sign + format_won(amount)


def is_minus(amount):
    """음수면 True. 잔액 색을 정할 때 쓴다."""
    return amount < 0
