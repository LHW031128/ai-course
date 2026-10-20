"""주차 요금 계산기 화면 (SPEC.md 5·6장). 계산은 parking_calc의 함수만 사용한다."""

import tkinter as tk

from parking_calc import format_duration, format_won, make_record, total_fee

HEADERS = ["입차", "출차", "주차 시간", "요금", "삭제"]
COLUMN_WIDTHS = [80, 80, 120, 100, 70]


def main():
    root = tk.Tk()
    root.title("주차 요금 계산기")
    root.geometry("560x480")

    records = []

    # 위쪽: 입력칸과 [계산] 버튼
    input_frame = tk.Frame(root, padx=12, pady=10)
    input_frame.pack(fill="x")

    tk.Label(input_frame, text="입차 시각").grid(row=0, column=0, sticky="w")
    entry_input = tk.Entry(input_frame, width=10)
    entry_input.grid(row=0, column=1, padx=(4, 12))

    tk.Label(input_frame, text="출차 시각").grid(row=0, column=2, sticky="w")
    exit_input = tk.Entry(input_frame, width=10)
    exit_input.grid(row=0, column=3, padx=(4, 12))

    calc_button = tk.Button(input_frame, text="계산", width=8)
    calc_button.grid(row=0, column=4)

    tk.Label(input_frame, text="예: 09:30", fg="gray").grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 0))

    # 그 아래: 빨간 글씨 오류 라벨
    error_label = tk.Label(root, text="", fg="red", anchor="w", justify="left", wraplength=530, padx=12)
    error_label.pack(fill="x")

    # 아래쪽: 오늘 합계
    total_label = tk.Label(root, text="", font=("TkDefaultFont", 12, "bold"), anchor="e", padx=12, pady=10)
    total_label.pack(side="bottom", fill="x")

    # 가운데: 세로 스크롤 목록 (Canvas + 안쪽 Frame + Scrollbar)
    list_area = tk.Frame(root, padx=12, pady=6)
    list_area.pack(fill="both", expand=True)

    canvas = tk.Canvas(list_area, highlightthickness=1, highlightbackground="#cccccc")
    scrollbar = tk.Scrollbar(list_area, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    list_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=list_frame, anchor="nw")
    list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

    for col, width in enumerate(COLUMN_WIDTHS):
        list_frame.grid_columnconfigure(col, minsize=width)

    def redraw():
        """목록 위젯을 전부 지우고 records로 다시 그린 뒤 합계를 갱신한다."""
        for widget in list_frame.winfo_children():
            widget.destroy()

        for col, title in enumerate(HEADERS):
            tk.Label(list_frame, text=title, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=col, pady=(4, 6))

        for i, record in enumerate(records):
            row = i + 1
            values = [record["entry"], record["exit"], format_duration(record["minutes"]), format_won(record["fee"])]
            for col, value in enumerate(values):
                tk.Label(list_frame, text=value).grid(row=row, column=col, pady=2)
            tk.Button(list_frame, text="삭제", command=lambda i=i: delete_record(i)).grid(row=row, column=4, pady=2)

        fees = [record["fee"] for record in records]
        total_label.config(text=f"오늘 합계: {format_won(total_fee(fees))} ({len(records)}건)")

    def calculate(event=None):
        try:
            record = make_record(entry_input.get(), exit_input.get())
        except ValueError as e:
            error_label.config(text=str(e))
            return
        records.append(record)
        redraw()
        canvas.update_idletasks()
        canvas.yview_moveto(1.0)
        entry_input.delete(0, tk.END)
        exit_input.delete(0, tk.END)
        error_label.config(text="")
        entry_input.focus_set()

    def delete_record(i):
        del records[i]
        redraw()

    calc_button.config(command=calculate)
    root.bind("<Return>", calculate)

    redraw()
    entry_input.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
