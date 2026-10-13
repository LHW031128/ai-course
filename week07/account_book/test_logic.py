# test_logic.py
# logic.py의 함수를 검사한다. SPEC.md 4절의 표 한 줄이 check 하나다.
# 실행: python test_logic.py

import sys

import logic

passed = 0
failed = 0


def check(name, actual, expected):
    """실제 결과가 기대하는 결과와 값도 종류도 같으면 통과."""
    global passed, failed
    if actual == expected and type(actual) is type(expected):
        passed += 1
    else:
        failed += 1
        print(f"실패: {name}")
        print(f"  기대: {expected!r}")
        print(f"  실제: {actual!r}")


def income(memo, amount):
    return {"kind": "수입", "memo": memo, "amount": amount}


def expense(memo, amount):
    return {"kind": "지출", "memo": memo, "amount": amount}


MSG_EMPTY = "금액을 입력합니다"
MSG_BAD = "금액은 0보다 큰 정수로 입력합니다"
MSG_KIND = "구분을 고릅니다"
MSG_LOAD = "저장된 기록을 읽지 못했습니다"


# parse_amount
check('parse_amount("1000")', logic.parse_amount("1000"), 1000)
check('parse_amount("1,000")', logic.parse_amount("1,000"), 1000)
check('parse_amount(" 1000 ")', logic.parse_amount(" 1000 "), 1000)
check('parse_amount("1,234,567")', logic.parse_amount("1,234,567"), 1234567)
check('parse_amount("10,00")', logic.parse_amount("10,00"), 1000)
check('parse_amount("0500")', logic.parse_amount("0500"), 500)
check('parse_amount("1")', logic.parse_amount("1"), 1)
check('parse_amount("12345678901234567890")',
      logic.parse_amount("12345678901234567890"), 12345678901234567890)
check('parse_amount("9" * 5000)', logic.parse_amount("9" * 5000), 10 ** 5000 - 1)
check('parse_amount("")', logic.parse_amount(""), None)
check('parse_amount("   ")', logic.parse_amount("   "), None)
check('parse_amount(",")', logic.parse_amount(","), None)
check('parse_amount("0")', logic.parse_amount("0"), None)
check('parse_amount("000")', logic.parse_amount("000"), None)
check('parse_amount("-500")', logic.parse_amount("-500"), None)
check('parse_amount("+500")', logic.parse_amount("+500"), None)
check('parse_amount("1000.0")', logic.parse_amount("1000.0"), None)
check('parse_amount("12.5")', logic.parse_amount("12.5"), None)
check('parse_amount("천원")', logic.parse_amount("천원"), None)
check('parse_amount("1000원")', logic.parse_amount("1000원"), None)
check('parse_amount("1 000")', logic.parse_amount("1 000"), None)
check('parse_amount("１０００") 전각 숫자', logic.parse_amount("１０００"), None)
check('parse_amount(None)', logic.parse_amount(None), None)

# clean_memo
check('clean_memo("점심")', logic.clean_memo("점심"), "점심")
check('clean_memo("  점심  ")', logic.clean_memo("  점심  "), "점심")
check('clean_memo("편의점 간식")', logic.clean_memo("편의점 간식"), "편의점 간식")
check('clean_memo("")', logic.clean_memo(""), "(내용 없음)")
check('clean_memo("   ")', logic.clean_memo("   "), "(내용 없음)")
check('clean_memo(None)', logic.clean_memo(None), "(내용 없음)")

# add_entry
check("add_entry 지출 추가",
      logic.add_entry([], "지출", "점심", "8000"),
      ([expense("점심", 8000)], ""))
check("add_entry 수입 추가, 공백과 쉼표 정리",
      logic.add_entry([], "수입", " 용돈 ", "50,000"),
      ([income("용돈", 50000)], ""))
check("add_entry 빈 내용",
      logic.add_entry([], "지출", "", "1000"),
      ([expense("(내용 없음)", 1000)], ""))
check("add_entry 맨 뒤에 붙는다",
      logic.add_entry([income("용돈", 50000)], "지출", "점심", "8000"),
      ([income("용돈", 50000), expense("점심", 8000)], ""))
check("add_entry 같은 내용 두 번",
      logic.add_entry([expense("점심", 8000)], "지출", "점심", "8000"),
      ([expense("점심", 8000), expense("점심", 8000)], ""))
check("add_entry 금액 빈 칸",
      logic.add_entry([], "지출", "점심", ""), ([], MSG_EMPTY))
check("add_entry 금액 공백뿐",
      logic.add_entry([], "지출", "점심", "  "), ([], MSG_EMPTY))
check("add_entry 금액 0",
      logic.add_entry([], "지출", "점심", "0"), ([], MSG_BAD))
check("add_entry 금액 글자",
      logic.add_entry([], "지출", "점심", "천원"), ([], MSG_BAD))
check("add_entry 금액 음수",
      logic.add_entry([], "지출", "점심", "-500"), ([], MSG_BAD))
check("add_entry 실패하면 목록 그대로",
      logic.add_entry([income("용돈", 50000)], "지출", "점심", "1.5"),
      ([income("용돈", 50000)], MSG_BAD))
check("add_entry 없는 구분",
      logic.add_entry([], "기타", "점심", "8000"), ([], MSG_KIND))
check("add_entry 구분을 먼저 검사",
      logic.add_entry([], None, "점심", ""), ([], MSG_KIND))
original = [income("용돈", 50000)]
logic.add_entry(original, "지출", "점심", "8000")
check("add_entry 받은 목록을 고치지 않는다", original, [income("용돈", 50000)])

# remove_entry
three = [income("용돈", 50000), expense("점심", 8000), expense("버스", 1500)]
check("remove_entry 가운데 줄",
      logic.remove_entry(three, 1), [income("용돈", 50000), expense("버스", 1500)])
check("remove_entry 첫 줄",
      logic.remove_entry(three, 0), [expense("점심", 8000), expense("버스", 1500)])
check("remove_entry 마지막 줄",
      logic.remove_entry(three, 2), [income("용돈", 50000), expense("점심", 8000)])
check("remove_entry 없는 번호 3", logic.remove_entry(three, 3), three)
check("remove_entry 없는 번호 -1", logic.remove_entry(three, -1), three)
check("remove_entry 번호 None", logic.remove_entry(three, None), three)
check("remove_entry 빈 목록", logic.remove_entry([], 0), [])
logic.remove_entry(three, 1)
check("remove_entry 받은 목록을 고치지 않는다", three,
      [income("용돈", 50000), expense("점심", 8000), expense("버스", 1500)])

# totals
check("totals 빈 목록", logic.totals([]), (0, 0, 0))
check("totals 수입만", logic.totals([income("용돈", 50000)]), (50000, 0, 50000))
check("totals 지출만", logic.totals([expense("점심", 8000)]), (0, 8000, -8000))
check("totals 수입 하나 지출 둘", logic.totals(three), (50000, 9500, 40500))
check("totals 수입 둘 지출 하나",
      logic.totals([income("용돈", 50000), income("알바", 30000), expense("점심", 8000)]),
      (80000, 8000, 72000))
check("totals 잔액 0",
      logic.totals([income("용돈", 5000), expense("책", 5000)]), (5000, 5000, 0))
check("totals 지운 뒤 다시 계산",
      logic.totals(logic.remove_entry(three, 1)), (50000, 1500, 48500))

# format_won
check("format_won(0)", logic.format_won(0), "0원")
check("format_won(999)", logic.format_won(999), "999원")
check("format_won(1000)", logic.format_won(1000), "1,000원")
check("format_won(50000)", logic.format_won(50000), "50,000원")
check("format_won(1234567)", logic.format_won(1234567), "1,234,567원")
check("format_won(-5000)", logic.format_won(-5000), "-5,000원")
check("format_won(12345678901234567890)",
      logic.format_won(12345678901234567890), "12,345,678,901,234,567,890원")

# format_signed
check("format_signed 수입", logic.format_signed("수입", 50000), "+50,000원")
check("format_signed 지출", logic.format_signed("지출", 8000), "-8,000원")
check("format_signed 수입 1", logic.format_signed("수입", 1), "+1원")
check("format_signed 지출 큰 수", logic.format_signed("지출", 1234567), "-1,234,567원")

# is_minus
check("is_minus(-1)", logic.is_minus(-1), True)
check("is_minus(0)", logic.is_minus(0), False)
check("is_minus(42000)", logic.is_minus(42000), False)

# entries_to_text
check("entries_to_text 빈 목록", logic.entries_to_text([]), "[]")
check("entries_to_text 한 줄",
      logic.entries_to_text([income("용돈", 50000)]),
      '[{"kind": "수입", "memo": "용돈", "amount": 50000}]')
check("entries_to_text 두 줄",
      logic.entries_to_text([income("용돈", 50000), expense("점심", 8000)]),
      '[{"kind": "수입", "memo": "용돈", "amount": 50000}, '
      '{"kind": "지출", "memo": "점심", "amount": 8000}]')

# entries_from_text
GOOD = '{"kind": "수입", "memo": "용돈", "amount": 50000}'      # 용돈 기록
check("entries_from_text None (파일 없음)", logic.entries_from_text(None), ([], ""))
check('entries_from_text "[]"', logic.entries_from_text("[]"), ([], ""))
check("entries_from_text 한 줄",
      logic.entries_from_text(f"[{GOOD}]"), ([income("용돈", 50000)], ""))
check("entries_from_text 저장했다 읽으면 그대로",
      logic.entries_from_text(logic.entries_to_text(three)), (three, ""))
huge = [income("큰돈", 10 ** 5000 - 1)]
check("entries_from_text 5000자리 금액을 저장했다 읽기",
      logic.entries_from_text(logic.entries_to_text(huge)), (huge, ""))
check('entries_from_text "" (빈 파일)', logic.entries_from_text(""), ([], MSG_LOAD))
check('entries_from_text "abc"', logic.entries_from_text("abc"), ([], MSG_LOAD))
check("entries_from_text 배열이 아님", logic.entries_from_text(GOOD), ([], MSG_LOAD))
check('entries_from_text "[" 100000번',
      logic.entries_from_text("[" * 100000), ([], MSG_LOAD))
check("entries_from_text 없는 구분 1건",
      logic.entries_from_text(f'[{GOOD}, {{"kind": "기타", "memo": "x", "amount": 1}}]'),
      ([income("용돈", 50000)], "저장된 기록 1건을 읽지 못했습니다"))
check("entries_from_text 잘못된 금액 5건",
      logic.entries_from_text(
          f'[{GOOD},'
          ' {"kind": "지출", "memo": "a", "amount": "8000"},'
          ' {"kind": "지출", "memo": "b", "amount": 0},'
          ' {"kind": "지출", "memo": "c", "amount": -5},'
          ' {"kind": "지출", "memo": "d", "amount": 1.5},'
          ' {"kind": "지출", "memo": "e", "amount": true}]'),
      ([income("용돈", 50000)], "저장된 기록 5건을 읽지 못했습니다"))
check("entries_from_text 잘못된 내용 2건",
      logic.entries_from_text(
          f'[{GOOD},'
          ' {"kind": "지출", "amount": 8000},'
          ' {"kind": "지출", "memo": 3, "amount": 8000}]'),
      ([income("용돈", 50000)], "저장된 기록 2건을 읽지 못했습니다"))
check("entries_from_text 기록이 아닌 것 4건",
      logic.entries_from_text(f'[3, "a", null, [1], {GOOD}]'),
      ([income("용돈", 50000)], "저장된 기록 4건을 읽지 못했습니다"))
check("entries_from_text 내용 정리",
      logic.entries_from_text(
          '[{"kind": "지출", "memo": "  점심  ", "amount": 8000},'
          ' {"kind": "지출", "memo": "", "amount": 1000}]'),
      ([expense("점심", 8000), expense("(내용 없음)", 1000)], ""))
check("entries_from_text 다른 항목은 버린다",
      logic.entries_from_text(
          '[{"kind": "지출", "memo": "점심", "amount": 8000, "date": "10-13"}]'),
      ([expense("점심", 8000)], ""))

print(f"통과 {passed}개, 실패 {failed}개")
sys.exit(1 if failed else 0)
