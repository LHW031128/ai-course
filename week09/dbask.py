import sys
import sqlite3
import ollama
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
con = sqlite3.connect("course.db")

rows = con.execute("SELECT id, name, week, category, tools, description, embedding FROM script").fetchall()
V = np.stack([np.frombuffer(r[-1], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)


def search(question, k=3):
    q = np.array(ollama.embed(model="bge-m3", input=question).embeddings[0])
    q = q / np.linalg.norm(q)
    sims = V @ q
    return [(float(sims[i]), rows[i][:-1]) for i in np.argsort(-sims)[:k]]


def answer(question):
    found = search(question)
    context = "\n".join(f"- {name} ({week}주차, {cat}, {tools}): {desc}"
                        for _, (id_, name, week, cat, tools, desc) in found)
    prompt = f"""아래 실습 파일 목록만 근거로 질문에 답한다. 목록에 없는 내용은 "자료에 없습니다"라고 답한다. 답은 두 문장 이내로 쓴다.

실습 파일 목록:
{context}

질문: {question}"""
    r = client.chat.completions.create(model="gemma4", temperature=0,
                                       messages=[{"role": "user", "content": prompt}])
    return found, r.choices[0].message.content.strip()


questions = sys.argv[1:] or [
    "돈 내는 기능 만든 거 어디 있지?",
    "AI한테 아니라고 우기면 말 바꾸는지 실험한 거",
    "주차비 계산 맞는지 확인하는 파일",
    "모델이 파이썬 함수를 직접 부르게 한 코드",
    "엑셀 파일 읽는 코드 있어?",
]
for q in questions:
    found, a = answer(q)
    print("Q:", q)
    for s, (id_, name, *_rest) in found:
        print(f"   {s:.3f} {name}")
    print("   답:", a)
    print()
