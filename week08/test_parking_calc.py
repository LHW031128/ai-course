"""SPEC.md 8장 테스트 표(T01~T31). 실행: python week08/test_parking_calc.py"""

import sys

from parking_calc import calc_fee, format_duration, format_won, make_record, total_fee

# (번호, 함수, 입력 인자, 기대 결과)
# make_record의 기대 결과는 dict에서 확인할 키와 값, ValueError는 예외 기대
CASES = [
    ("T01", calc_fee, (1,), 0),
    ("T02", calc_fee, (30,), 0),
    ("T03", calc_fee, (31,), 500),
    ("T04", calc_fee, (40,), 500),
    ("T05", calc_fee, (41,), 1000),
    ("T06", calc_fee, (60,), 1500),
    ("T07", calc_fee, (430,), 20000),
    ("T08", calc_fee, (431,), 20000),
    ("T09", make_record, ("09:00", "09:30"), {"minutes": 30, "fee": 0}),
    ("T10", make_record, ("09:30", "11:05"), {"minutes": 95, "fee": 3500}),
    ("T11", make_record, ("9:05", "10:00"), {"minutes": 55, "fee": 1500, "entry": "09:05"}),
    ("T12", make_record, (" 08:00 ", "08:40"), {"minutes": 40, "fee": 500}),
    ("T13", make_record, ("00:00", "23:59"), {"minutes": 1439, "fee": 20000}),
    ("T14", make_record, ("", "10:00"), ValueError),
    ("T15", make_record, ("09:00", ""), ValueError),
    ("T16", make_record, ("24:00", "10:00"), ValueError),
    ("T17", make_record, ("09:00", "12:60"), ValueError),
    ("T18", make_record, ("0930", "10:00"), ValueError),
    ("T19", make_record, ("ab:cd", "10:00"), ValueError),
    ("T20", make_record, ("10:00", "10:00"), ValueError),
    ("T21", make_record, ("23:00", "01:00"), ValueError),
    ("T22", format_won, (0,), "0원"),
    ("T23", format_won, (1500,), "1,500원"),
    ("T24", format_won, (20000,), "20,000원"),
    ("T25", format_won, (1234567,), "1,234,567원"),
    ("T26", format_duration, (45,), "45분"),
    ("T27", format_duration, (60,), "1시간"),
    ("T28", format_duration, (95,), "1시간 35분"),
    ("T29", total_fee, ([],), 0),
    ("T30", total_fee, ([500, 3500, 20000],), 24000),
    ("T31", total_fee, ([500, 20000],), 20500),
]


def run_case(func, args, expected):
    """통과면 None, 실패면 "기대 ..., 실제 ..." 문자열을 돌려준다."""
    if expected is ValueError:
        try:
            result = func(*args)
        except ValueError:
            return None
        except Exception as e:
            return f"기대 ValueError, 실제 {type(e).__name__}"
        return f"기대 ValueError, 실제 {result!r}"

    try:
        result = func(*args)
    except Exception as e:
        return f"기대 {expected!r}, 실제 {type(e).__name__}: {e}"

    if isinstance(expected, dict):
        for key, value in expected.items():
            actual = result.get(key)
            if actual != value:
                return f"기대 {key}={value!r}, 실제 {key}={actual!r}"
        return None

    if result != expected:
        return f"기대 {expected!r}, 실제 {result!r}"
    return None


def main():
    passed = 0
    failed = 0
    for number, func, args, expected in CASES:
        error = run_case(func, args, expected)
        if error is None:
            passed += 1
            print(f"통과 {number}")
        else:
            failed += 1
            print(f"실패 {number}: {error}")

    print(f"통과 {passed}개 / 실패 {failed}개")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
