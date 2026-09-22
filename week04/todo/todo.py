import json
import os

TODO_FILE = 'todo.json'

def load_todos():
    """todo.json 파일에서 할 일 목록을 불러옵니다."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos):
    """할 일 목록을 todo.json 파일에 저장합니다."""
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def add_todo(todos, task):
    """새로운 할 일을 추가합니다."""
    todos.append({"task": task, "completed": False})
    print(f"'{task}' 항목이 추가되었습니다.")

def list_todos(todos):
    """할 일 목록을 출력합니다."""
    if not todos:
        print("\n현재 할 일이 없습니다.")
        return

    print("\n--- 할 일 목록 ---")
    for i, todo in enumerate(todos, 1):
        status = "[V]" if todo['completed'] else "[ ]"
        print(f"{i}. {status} {todo['task']}")
    print("------------------")

def complete_todo(todos, index):
    """할 일을 완료 상태로 표시합니다."""
    try:
        todos[index - 1]['completed'] = True
        print(f"'{todos[index - 1]['task']}' 항목을 완료 처리했습니다.")
    except IndexError:
        print("잘못된 번호입니다.")

def delete_todo(todos, index):
    """할 일을 삭제합니다."""
    try:
        removed = todos.pop(index - 1)
        print(f"'{removed['task']}' 항목이 삭제되었습니다.")
    except IndexError:
        print("잘못된 번호입니다.")

def main():
    todos = load_todos()

    while True:
        print("\n=== 할 일 관리 프로그램 ===")
        print("1. 할 일 추가")
        print("2. 목록 보기")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요 (1-5): ")

        if choice == '1':
            task = input("추가할 할 일을 입력하세요: ").strip()
            if task:
                add_todo(todos, task)
                save_todos(todos)
            else:
                print("할 일을 입력해야 합니다.")
        elif choice == '2':
            list_todos(todos)
        elif choice == '3':
            list_todos(todos)
            if todos:
                try:
                    idx = int(input("완료 처리할 번호를 입력하세요: "))
                    complete_todo(todos, idx)
                    save_todos(todos)
                except ValueError:
                    print("숫자를 입력해주세요.")
        elif choice == '4':
            list_todos(todos)
            if todos:
                try:
                    idx = int(input("삭제할 번호를 입력하세요: "))
                    delete_todo(todos, idx)
                    save_todos(todos)
                except ValueError:
                    print("숫자를 입력해주세요.")
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
