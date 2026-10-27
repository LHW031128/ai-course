import os
import sqlite3

# 내 ai-course 저장소의 실습 파일 목록 (week02~week09)
# 4주차의 agree, context, memory, probs, server, system.py는 3주차와 내용이 같아 뺐다.
# (파일, 주차, 분류, 쓴 도구, 설명)
ROWS = [
    ("week02/vector.py", 2, "임베딩", "Ollama bge-m3, numpy", "단어 '사과'를 1024차원 벡터로 바꿔 길이와 앞 5개 값을 보고, 사과-배와 사과-자동차의 코사인 유사도, '왕 - 남자 + 여자' 벡터 계산 결과를 비교한다"),
    ("week02/similarity.py", 2, "임베딩", "Ollama bge-m3, numpy", "문장 11쌍의 코사인 유사도를 출력한다. 같은 뜻, 반대 뜻, 어순 바꿈, 다의어 '은행', 과일 사과와 회사 애플 같은 쌍을 비교한다"),
    ("week02/multilingual.py", 2, "임베딩", "Ollama bge-m3, numpy", "한국어 문장 하나를 영어, 일본어, 중국어 번역문과 비교해 언어가 달라도 뜻이 같으면 유사도가 높은지 본다"),
    ("week02/plot2d.py", 2, "임베딩", "Ollama bge-m3, numpy, matplotlib", "과일, 탈것, 직업, 동물, 나라 단어 20개의 임베딩을 SVD로 2차원에 투영해 산점도 이미지 words2d.png로 저장한다"),
    ("week02/search.py", 2, "임베딩", "Ollama bge-m3, numpy", "학사 안내 문장 10개 중에서 질문과 코사인 유사도가 가장 높은 3개를 찾아 주는 미니 검색기"),
    ("week03/tokens.py", 3, "토큰", "transformers, Qwen3 토크나이저", "같은 뜻의 한국어와 영어 문장을 토큰으로 쪼개 토큰 수와 비율을 비교하고 어휘 크기를 출력한다"),
    ("week03/server.py", 3, "서버 호출", "openai 라이브러리, 실습 서버 gemma4", "실습 서버에 접속해 모델 목록을 확인하고 한 문장 질문을 보내는 기본 호출 함수"),
    ("week03/probs.py", 3, "모델 실험", "실습 서버 gemma4, logprobs", "첫 토큰 후보 5개와 각각의 확률을 출력한다. 수도, 덧셈처럼 답이 하나인 질문과 점심 메뉴, 영어 이름처럼 답이 여러 개인 질문을 비교한다"),
    ("week03/stream.py", 3, "모델 실험", "Ollama qwen3:8b", "봄에 대한 시를 스트리밍으로 받아 글자가 생성되는 대로 화면에 찍고, 받은 조각 수와 걸린 시간을 잰다"),
    ("week03/system.py", 3, "프롬프트 실험", "Ollama qwen3:8b", "리스트와 튜플의 차이를 묻는 같은 질문에 시스템 프롬프트를 친절한 강사, 간결한 문서 작성자, 영어로 답하는 시니어 개발자로 바꿔 답을 비교한다"),
    ("week03/memory.py", 3, "모델 실험", "Ollama qwen3:8b", "이름을 알려 준 뒤 이전 대화를 같이 보내지 않으면 모델이 이름을 기억하지 못하고, 대화 이력을 같이 보내야 기억한다는 것을 보여 준다"),
    ("week03/context.py", 3, "모델 한계", "Ollama qwen3:8b, num_ctx", "비밀 번호 문장 뒤에 채움 문장을 반복해 붙이고 num_ctx를 2048과 8192로 바꿔 가며 컨텍스트 길이를 넘으면 앞 내용을 놓치는지 확인한다"),
    ("week03/fewshot.py", 3, "프롬프트 실험", "Ollama qwen3:1.7b, qwen3:8b", "나라를 주고 수도를 맞히게 할 때 예시를 0개, 1개, 3개 주면서 모델 크기별 정답 수를 비교한다 (few-shot)"),
    ("week03/cot.py", 3, "프롬프트 실험", "Ollama qwen3:8b", "문장으로 된 산수 문제 5개를 답만 쓰게 할 때와 단계별로 풀게 할 때의 정답 수를 비교한다 (Chain of Thought)"),
    ("week03/think.py", 3, "모델 실험", "Ollama qwen3:8b, think 옵션", "생각 모드를 켜고 끌 때 답, 생각한 글자 수, 걸린 시간, 출력 토큰 수를 비교한다"),
    ("week03/limits.py", 3, "모델 한계", "Ollama qwen3:8b", "없는 논문과 없는 함수를 물어 환각을 유도하고, 노벨상 질문으로 지식 컷오프를 확인하고, temperature 0과 1.5에서 답이 달라지는지 본다"),
    ("week03/agree.py", 3, "모델 한계", "Ollama qwen3:8b", "모델이 맞게 답한 뒤 사용자가 틀렸다고 우기면 답을 바꾸는지 확인한다 (동조, 아첨)"),
    ("week04/limits.py", 4, "모델 한계", "Ollama qwen3:8b, 실습 서버 gemma4", "3주차의 환각, 지식 컷오프, 온도 실험을 내 PC 모델과 실습 서버 모델에 똑같이 돌려 결과를 나란히 비교한다"),
    ("week04/speed.py", 4, "측정", "Ollama qwen3:1.7b, qwen3:8b", "두 모델로 같은 코드를 생성하게 해서 초당 생성 토큰 수를 재고, ollama ps 결과로 GPU와 CPU에 얼마나 올라갔는지 같이 보여 준다"),
    ("week04/vram.py", 4, "측정", "계산만 함", "모델 크기별로 16비트와 4비트 양자화 때 필요한 메모리를 계산해 8GB 그래픽카드에 들어가는지 판단하고, 컨텍스트 길이별 메모리도 표로 보여 준다"),
    ("week04/calc1/calc.py", 4, "앱", "표준 라이브러리", "메뉴에서 번호를 골라 두 수를 더하고 빼고 곱하고 나누는 콘솔 계산기. 0으로 나누면 오류 메시지를 낸다"),
    ("week04/calc2/calc.py", 4, "앱", "ast 모듈", "문자열 수식을 ast로 분석해 괄호, 연산 우선순위, 음수, 소수를 처리하는 계산기. eval을 쓰지 않아 안전하다"),
    ("week04/calc2/test_calc.py", 4, "테스트", "unittest", "calc2 계산기의 사칙연산, 우선순위, 괄호, 소수, 음수, 0으로 나누기 예외를 검사하는 단위 테스트"),
    ("week04/todo/todo.py", 4, "앱", "json 모듈", "할 일을 추가, 목록 보기, 완료 표시, 삭제하는 콘솔 프로그램. 목록은 todo.json 파일에 저장한다"),
    ("week05/raw.py", 5, "서버 호출", "urllib, Ollama REST API", "라이브러리 없이 localhost:11434/api/chat 주소로 JSON 요청을 직접 보내고 응답 원문을 그대로 출력한다"),
    ("week05/chat.py", 5, "앱", "Ollama qwen3:8b", "대화 이력을 쌓으며 이어서 대화하는 터미널 챗봇. /reset으로 이력을 지우고 /history로 보고 /bye로 끝낸다"),
    ("week05/sse.py", 5, "서버 호출", "openai 라이브러리, 실습 서버 gemma4", "실습 서버에서 답을 스트리밍(SSE)으로 받아 출력하고 마지막에 입력 토큰 수와 출력 토큰 수를 보여 준다"),
    ("week05/twoservers.py", 5, "서버 호출", "openai 라이브러리, Ollama, vLLM", "base_url만 바꿔서 내 PC의 Ollama와 실습 서버의 vLLM에 같은 질문을 보내고 답을 비교한다"),
    ("week05/jsonmode.py", 5, "모델 실험", "Ollama qwen3:8b, format=json", "문장에서 이름, 학과, 학년을 JSON 형식으로만 뽑게 해서 json.loads로 파싱한다"),
    ("week05/tools.py", 5, "모델 실험", "Ollama qwen3:8b, tools", "모델이 get_time과 calc 함수를 스스로 호출하게 해서 현재 시각과 곱셈 결과를 받아 최종 답을 만든다 (도구 호출)"),
    ("week05/rag.py", 5, "RAG", "Ollama bge-m3, qwen3:8b", "메모리에 둔 문장 10개에서 질문과 가까운 문장을 찾아 프롬프트에 넣고 답하게 하는 첫 RAG"),
    ("week05/toss/app.py", 5, "앱", "Flask, 토스페이먼츠 API", "토스페이먼츠 테스트 키로 1,000원 결제를 승인하는 Flask 웹앱. 브라우저에서 온 금액을 서버에서 다시 확인한다"),
    ("week06/vague.py", 6, "프롬프트 실험", "실습 서버 gemma4", "'전화번호를 정리하는 함수 만들어줘'처럼 모호한 요청을 5번 보내 매번 함수 이름과 동작이 다르게 나오는 것을 확인한다"),
    ("week06/evalprompt.py", 6, "테스트", "실습 서버 gemma4", "프롬프트 파일을 받아 전화번호 정리 함수를 5번 생성하고, 생성된 코드를 실행해 테스트 10개로 채점한 뒤 평균 점수를 낸다"),
    ("week06/bugs/grades.py", 6, "앱", "표준 라이브러리", "점수 평균, 상위 n개, 학점(A, B, C, F), 합격률을 계산하는 함수 모음. 버그를 찾아 고치는 실습용"),
    ("week06/bugs/test_grades.py", 6, "테스트", "표준 라이브러리", "grades.py의 함수들을 기대값과 비교해 통과와 실패를 출력하는 테스트"),
    ("week06/todo/app.py", 6, "앱", "Flask", "할 일을 추가하고 완료 표시하고 삭제하는 Flask 웹앱의 주소별 처리. 제목은 100자까지"),
    ("week06/todo/db.py", 6, "앱", "sqlite3", "할 일 웹앱의 SQLite 함수. 테이블 만들기, 목록 읽기, 추가, 완료 토글, 삭제"),
    ("week06/todo/test_app.py", 6, "테스트", "unittest, Flask test_client", "임시 데이터베이스로 할 일 웹앱의 추가, 빈 제목, 100자와 101자 제목, 토글, 삭제, 없는 번호 처리를 검사한다"),
    ("week07/account_book/logic.py", 7, "앱", "json 모듈", "용돈 기입장의 계산 함수. 금액 읽기, 기록 추가와 삭제, 수입과 지출 합계와 잔액, 원 단위 표시, 기록을 글자로 바꿔 저장하고 다시 읽기"),
    ("week07/account_book/main.py", 7, "앱", "Flet", "용돈 기입장 화면. 내용, 금액, 수입과 지출 구분을 넣으면 목록에 쌓고 합계와 잔액을 보여 주며 records.json에 저장한다"),
    ("week07/account_book/test_logic.py", 7, "테스트", "표준 라이브러리", "용돈 기입장 logic.py의 함수를 스펙 문서의 표 한 줄마다 하나씩 검사하는 테스트"),
    ("week08/parking_calc.py", 8, "앱", "re 모듈", "입차와 출차 시각으로 주차 요금을 계산한다. 30분까지 무료, 이후 10분마다 500원, 한 건 최대 20,000원"),
    ("week08/parking_app.py", 8, "앱", "tkinter", "주차 요금 계산기 화면. 입차와 출차 시각을 넣고 계산하면 목록에 쌓고 오늘 받은 요금 합계를 보여 준다"),
    ("week08/test_parking_calc.py", 8, "테스트", "표준 라이브러리", "주차 요금 계산 함수를 스펙 문서의 T01~T31 표대로 검사하는 테스트"),
    ("week09/chunk.py", 9, "RAG", "표준 라이브러리", "학사 안내 문서를 문단 단위와 200자 단위로 잘라 비교한다. 글자 수로 자르면 문장이 중간에 끊긴다"),
    ("week09/index.py", 9, "RAG", "Ollama bge-m3, numpy", "문단 청크 앞에 절 제목을 붙여 임베딩하고 청크와 벡터를 index.npz 파일에 저장한다"),
    ("week09/ask.py", 9, "RAG", "Ollama bge-m3, 실습 서버 gemma4", "index.npz에서 질문과 가까운 청크 3개를 찾아 프롬프트에 붙이고 학사 안내 질문에 답한다"),
    ("week09/makedb.py", 9, "RAG", "sqlite3", "내 실습 파일 목록으로 course.db 데이터베이스를 만든다"),
    ("week09/sqlsearch.py", 9, "RAG", "sqlite3", "데이터베이스에서 LIKE로 키워드를 찾아 SQL 검색은 그 글자가 그대로 있어야만 찾는다는 한계를 본다"),
    ("week09/embeddb.py", 9, "RAG", "Ollama bge-m3, sqlite3", "데이터베이스의 행을 문장으로 바꿔 임베딩하고 그 벡터를 같은 행의 BLOB 열에 저장한다"),
    ("week09/dbask.py", 9, "RAG", "Ollama bge-m3, 실습 서버 gemma4, sqlite3", "데이터베이스에 저장된 벡터로 질문과 가까운 행 3개를 찾아 프롬프트에 넣고 답한다"),
    ("week09/evalrag.py", 9, "RAG", "Ollama bge-m3, sqlite3", "검색이 맞았는지 점수를 매긴다. 질문과 정답 쌍으로 검색 1위 적중률과 3위 안 적중률을 잰다"),
]

if os.path.exists("course.db"):
    os.remove("course.db")
con = sqlite3.connect("course.db")
con.execute("""CREATE TABLE script (
    id INTEGER PRIMARY KEY,
    name TEXT, week INTEGER, category TEXT, tools TEXT, description TEXT)""")
con.executemany("INSERT INTO script (name, week, category, tools, description) VALUES (?, ?, ?, ?, ?)", ROWS)
con.commit()
print("course.db:", len(ROWS), "행")
