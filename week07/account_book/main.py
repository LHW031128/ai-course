# main.py
# 용돈 기입장의 화면. 계산과 판정은 전부 logic.py의 함수를 불러서 한다.
import flet as ft

import logic


def main(page: ft.Page):
    page.title = "용돈 기입장"
    page.window.width = 440
    page.window.height = 600
    page.window.resizable = False

    entries = []     # 기록 목록. logic.py가 돌려준 새 목록으로 바꿔 넣는다

    memo = ft.TextField(label="내용", value="", width=170)
    amount = ft.TextField(label="금액", value="", width=120)
    kind = ft.Dropdown(label="구분", value=logic.EXPENSE, width=100,
                       options=[ft.dropdown.Option(logic.INCOME),
                                ft.dropdown.Option(logic.EXPENSE)])
    notice = ft.Text(value="", color=ft.Colors.RED)
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

    def on_add(e):
        nonlocal entries
        entries, message = logic.add_entry(entries, kind.value, memo.value, amount.value)
        notice.value = message
        if message == "":
            memo.value = ""
            amount.value = ""
            show()
        page.update()

    def on_delete(e):
        nonlocal entries
        entries = logic.remove_entry(entries, e.control.data)   # 버튼을 만들 때 data에 넣어 둔 번호
        notice.value = ""
        show()
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
