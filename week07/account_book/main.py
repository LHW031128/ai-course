# main.py
# 용돈 기입장의 화면. 계산과 판정은 전부 logic.py의 함수를 불러서 한다.
from pathlib import Path

import flet as ft

import logic

SAVE_PATH = Path(__file__).with_name("records.json")     # 기록을 저장하는 파일. main.py와 같은 폴더


def read_saved():
    """저장 파일의 글자를 돌려준다. 파일이 없으면 None, 읽지 못하면 ""."""
    if not SAVE_PATH.exists():
        return None
    try:
        return SAVE_PATH.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return ""


def write_saved(text):
    """저장 파일에 글자를 쓴다. 쓰지 못하면 False."""
    try:
        SAVE_PATH.write_text(text, encoding="utf-8")
        return True
    except OSError:
        return False


def main(page: ft.Page):
    page.title = "용돈 기입장"
    page.window.width = 440
    page.window.height = 600
    page.window.resizable = False

    # 기록 목록. logic.py가 돌려준 새 목록으로 바꿔 넣는다. 처음에는 저장 파일에서 불러온다
    entries, load_message = logic.entries_from_text(read_saved())

    memo = ft.TextField(label="내용", value="", width=170)
    amount = ft.TextField(label="금액", value="", width=120)
    kind = ft.Dropdown(label="구분", value=logic.EXPENSE, width=100,
                       options=[ft.dropdown.Option(logic.INCOME),
                                ft.dropdown.Option(logic.EXPENSE)])
    notice = ft.Text(value=load_message, color=ft.Colors.RED)
    items = ft.ListView(expand=True, spacing=4)
    income_total = ft.Text(value="", color=ft.Colors.BLUE)
    expense_total = ft.Text(value="", color=ft.Colors.RED)
    balance = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)

    def show():
        """entries를 목록과 합계에 다시 그린다."""
        items.controls.clear()
        for i, entry in enumerate(entries):
            if entry["kind"] == logic.INCOME:
                amount_color = ft.Colors.BLUE
            else:
                amount_color = ft.Colors.RED
            items.controls.append(ft.Row(controls=[
                ft.Text(value=entry["memo"], expand=True),
                ft.Text(value=logic.format_signed(entry["kind"], entry["amount"]),
                        color=amount_color),
                ft.Button(content="삭제", data=i, on_click=on_delete),   # data는 줄 번호
            ]))
        income_sum, expense_sum, rest = logic.totals(entries)
        income_total.value = logic.format_won(income_sum)
        expense_total.value = logic.format_won(expense_sum)
        balance.value = logic.format_won(rest)
        if logic.is_minus(rest):
            balance.color = ft.Colors.RED
        else:
            balance.color = ft.Colors.BLUE

    def save():
        """entries를 저장 파일에 쓴다. 쓰지 못하면 안내 문구를 보여 준다."""
        if not write_saved(logic.entries_to_text(entries)):
            notice.value = logic.MSG_SAVE

    def on_add(e):
        nonlocal entries
        entries, message = logic.add_entry(entries, kind.value, memo.value, amount.value)
        notice.value = message
        if message == "":
            memo.value = ""
            amount.value = ""
            show()
            save()
        page.update()

    def on_delete(e):
        nonlocal entries
        entries = logic.remove_entry(entries, e.control.data)   # 버튼을 만들 때 data에 넣어 둔 번호
        notice.value = ""
        show()
        save()
        page.update()

    show()
    page.add(
        ft.Row(controls=[memo, amount, kind]),
        ft.Row(controls=[
            ft.Button(content="추가", on_click=on_add, expand=True, height=44,
                      bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        ]),
        notice,
        items,
        ft.Row(controls=[ft.Text(value="수입 합계", expand=True), income_total]),
        ft.Row(controls=[ft.Text(value="지출 합계", expand=True), expense_total]),
        ft.Row(controls=[ft.Text(value="잔액", size=20, weight=ft.FontWeight.BOLD, expand=True),
                         balance]),
    )


ft.run(main)
