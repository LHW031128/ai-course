import os
import tempfile
import unittest

import db
from app import app


class TodoTest(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        app.config["DATABASE"] = self.path
        app.config["TESTING"] = True
        db.init_db(self.path)
        self.client = app.test_client()

    def tearDown(self):
        os.remove(self.path)

    def todos(self):
        return db.list_todos(self.path)

    def page(self):
        return self.client.get("/").get_data(as_text=True)

    # 목록 보기
    def test_list(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    # 추가
    def test_add(self):
        r = self.client.post("/add", data={"title": "우유 사기"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("우유 사기", self.page())

    def test_add_defaults(self):
        self.client.post("/add", data={"title": "책 읽기"})
        todo = self.todos()[0]
        self.assertEqual(todo["done"], 0)
        self.assertRegex(todo["created_at"], r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    def test_add_100_chars(self):
        r = self.client.post("/add", data={"title": "가" * 100})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(self.todos()), 1)

    # 완료 표시와 해제
    def test_toggle(self):
        self.client.post("/add", data={"title": "빨래"})
        r = self.client.post("/toggle/1")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.todos()[0]["done"], 1)

    def test_toggle_twice(self):
        self.client.post("/add", data={"title": "빨래"})
        self.client.post("/toggle/1")
        self.client.post("/toggle/1")
        self.assertEqual(self.todos()[0]["done"], 0)

    def test_done_items_below(self):
        self.client.post("/add", data={"title": "할일A"})
        self.client.post("/add", data={"title": "할일B"})
        self.client.post("/toggle/1")
        html = self.page()
        self.assertLess(html.index("할일B"), html.index("할일A"))

    # 삭제
    def test_delete(self):
        self.client.post("/add", data={"title": "청소"})
        r = self.client.post("/delete/1")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(self.todos()), 0)

    # 잘못된 입력
    def test_add_empty(self):
        r = self.client.post("/add", data={"title": ""})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(len(self.todos()), 0)
        self.assertIn("제목을 입력하세요.", r.get_data(as_text=True))

    def test_add_101_chars(self):
        r = self.client.post("/add", data={"title": "가" * 101})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(len(self.todos()), 0)
        self.assertIn("제목은 100자 이하로 입력하세요.", r.get_data(as_text=True))

    def test_toggle_missing(self):
        self.assertEqual(self.client.post("/toggle/999").status_code, 404)

    def test_delete_missing(self):
        self.assertEqual(self.client.post("/delete/999").status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
