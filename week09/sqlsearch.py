import sqlite3

con = sqlite3.connect("course.db")
for kw in ["결제", "돈", "그림", "주차"]:
    rows = con.execute("SELECT name FROM script WHERE name LIKE ? OR description LIKE ?",
                       (f"%{kw}%", f"%{kw}%")).fetchall()
    print(kw, [r[0] for r in rows])
