import ollama
from openai import OpenAI

# 1. 내 PC Ollama 호출 함수
def ask_ollama(prompt, temperature=0):
    r = ollama.chat(model="qwen3:8b", messages=[{"role": "user", "content": prompt}],
                    think=False, options={"temperature": temperature, "num_predict": 300})
    return r.message.content.strip()

# 2. 실습 서버(Gemma4) 호출 함수
client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
def ask_server(prompt, temperature=0):
    r = client.chat.completions.create(model="gemma4", temperature=temperature, max_tokens=300,
                    messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content.strip()

print("=== [qwen3:8b] 1. 환각 유도 ===")
for q in [
    "2019년 서울대 김민준 교수가 발표한 논문 '양자 어텐션 네트워크'의 핵심 내용을 3문장으로 설명해줘.",
    "파이썬 표준 라이브러리 함수 listx.flatten_deep()의 사용법을 예제 코드와 함께 알려줘.",
]:
    print("Q:", q)
    print("A:", ask_ollama(q)[:300], "\n")

print("=== [qwen3:8b] 2. 지식 컷오프 ===")
for q in ["2024년 노벨 물리학상 수상자는 누구인가? 한 줄로.", "2025년 노벨 물리학상 수상자는 누구인가? 한 줄로."]:
    print("Q:", q)
    print("A:", ask_ollama(q)[:200], "\n")

print("=== [qwen3:8b] 3. 온도 실험 ===")
for t in [0, 1.5]:
    print(f"temperature={t}")
    for _ in range(3):
        print("  ", ask_ollama("고양이를 주제로 문장 하나만 써줘. 한 문장.", t)[:80])

print("\n" + "="*40 + "\n")

print("=== [gemma4 26B] 1. 환각 유도 (실습 서버) ===")
print("Q: 양자 어텐션 네트워크 논문")
print("A:", ask_server("2019년 서울대 김민준 교수가 발표한 논문 '양자 어텐션 네트워크'의 핵심 내용을 3문장으로 설명해줘.")[:300], "\n")

print("=== [gemma4 26B] 2. 지식 컷오프 (실습 서버) ===")
print("Q: 2024 노벨 물리학상")
print("A:", ask_server("2024년 노벨 물리학상 수상자는 누구인가? 한 줄로.")[:200], "\n")