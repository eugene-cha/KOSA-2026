import csv
import sqlite3
from pathlib import Path

CSV_FILE = "userinfo.csv"
DB_FILE = "userinfo.db"

# =========================
# 1. DB 생성 및 테이블 생성
# =========================
def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS userinfo (
            id TEXT PRIMARY KEY,
            email TEXT,
            name TEXT,
            age INTEGER,
            address TEXT
        )
    """)
    conn.commit()

# =========================
# 2. CSV → SQLite 저장
# =========================
def import_csv_to_db(conn):
    conn.execute("DELETE FROM userinfo") # 초기화 (선택)

    with open(CSV_FILE, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["id"],
                row["email"],
                row["name"],
                int(row["age"]),
                row["address"],
            )
            for row in reader
        ]

    conn.executemany("""
        INSERT INTO userinfo (id, email, name, age, address)
        VALUES (?, ?, ?, ?, ?)
    """, rows)
    conn.commit()

# =========================
# 3. 나이대별 평균 나이 SQL
# =========================
def query_age_group_avg(conn):
    query = """
        SELECT
            (age / 10) * 10 AS age_group,
            ROUND(AVG(age), 1) AS avg_age,
            COUNT(*) AS cnt
        FROM userinfo
        GROUP BY age_group
        ORDER BY age_group
    """

    cursor = conn.execute(query)
    return cursor.fetchall()

# =========================
# 4. 실행
# =========================
def main():
    if not Path(CSV_FILE).exists():
        raise FileNotFoundError(f"{CSV_FILE} 파일이 없습니다.")

    conn = sqlite3.connect(DB_FILE)

    try:
        create_table(conn)
        import_csv_to_db(conn)

        result = query_age_group_avg(conn)

        print("\n📊 나이대별 평균 나이")
        print("-" * 40)
        for age_group, avg_age, cnt in result:
            print(f'{age_group}대 | 평균 {avg_age}세 | {cnt}명')

    finally:
        conn.close()

if __name__ == "__main__":
    main()