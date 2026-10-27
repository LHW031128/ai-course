import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("course.db")
rows = con.execute("SELECT id, name, embedding FROM script").fetchall()
names = [r[1] for r in rows]
V = np.stack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)

# (질문, 정답 파일)
TESTS = [
    ("내 컴퓨터 GPU 메모리로 몇 B 모델까지 되는지 따져 본 코드", "week04/vram.py"),
    ("돈 내는 기능 만든 거 어디 있지?", "week05/toss/app.py"),
    ("AI한테 아니라고 우기면 말 바꾸는지 실험한 거", "week03/agree.py"),
    ("단어들 점 찍어서 그림으로 그린 코드", "week02/plot2d.py"),
    ("주차비 계산 맞는지 확인하는 파일", "week08/test_parking_calc.py"),
    ("용돈 관리 프로그램 화면 코드", "week07/account_book/main.py"),
    ("한국어가 영어보다 토큰 더 먹는지 본 거", "week03/tokens.py"),
    ("예시 몇 개 보여 주면 더 잘 맞히는지 본 실험", "week03/fewshot.py"),
    ("모델이 파이썬 함수를 직접 부르게 한 코드", "week05/tools.py"),
    ("내 컴퓨터 모델이랑 학교 서버 모델한테 같은 질문 한 거", "week05/twoservers.py"),
    ("검색이 몇 개 맞았는지 점수 매기는 코드", "week09/evalrag.py"),
    ("사과랑 애플이 비슷하게 나오는지 본 거", "week02/similarity.py"),
]

hit1 = hit3 = 0
for q, want in TESTS:
    qv = np.array(ollama.embed(model="bge-m3", input=q).embeddings[0])
    qv = qv / np.linalg.norm(qv)
    top = [names[i] for i in np.argsort(-(V @ qv))[:3]]
    ok1, ok3 = top[0] == want, want in top
    hit1 += ok1
    hit3 += ok3
    print("O" if ok1 else ("△" if ok3 else "X"), q, "->", top[0], "" if ok1 else f"(정답 {want}, 3위 안 {ok3})")
print(f"\n1위 적중 {hit1}/{len(TESTS)}, 3위 안 적중 {hit3}/{len(TESTS)}")
