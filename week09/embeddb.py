import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("course.db")
columns = [c[1] for c in con.execute("PRAGMA table_info(script)")]
if "embedding" not in columns:
    con.execute("ALTER TABLE script ADD COLUMN embedding BLOB")


def row_to_text(name, week, category, tools, description):
    return f"{name}. {week}주차 실습. {category}. 사용: {tools}. {description}"


rows = con.execute("SELECT id, name, week, category, tools, description FROM script").fetchall()
for i, (id_, *fields) in enumerate(rows):
    text = row_to_text(*fields)
    v = np.array(ollama.embed(model="bge-m3", input=text).embeddings[0], dtype=np.float32)
    con.execute("UPDATE script SET embedding = ? WHERE id = ?", (v.tobytes(), id_))
    print(f"\r{i + 1}/{len(rows)} {text[:40]}", end="   ")
con.commit()
print("\n완료")
print("예:", row_to_text(*rows[0][1:]))
