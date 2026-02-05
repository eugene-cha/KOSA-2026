import csv
import random
import string
from pathlib import Path

# =========================
# 데이터 풀 정의
# =========================

LAST_NAMES = [
    "김", "이", "박", "최", "정", "강", "조", "윤", "장", "임"
]

FIRST_NAMES = [
    "민준", "서준", "도윤", "예준", "시우",
    "하준", "지호", "주원", "지훈", "윤수",
    "서연", "지우", "서윤", "하은", "민서",
    "수빈", "지민", "예은", "윤아", "지현"
]

# 도-시-구 관계 (실제 행정 구조 기준)
ADDRESS_MAP = {
    "서울특별시": {
        "강남구": ["역삼동", "삼성동"],
        "마포구": ["서교동", "합정동"],
        "송파구": ["잠실동", "문정동"]
    },
    "경기도": {
        "안양시": ["평촌구", "동안구"],
        "성남시": ["분당구", "중원구"],
        "수원시": ["영통구", "팔달구"]
    },
    "부산광역시": {
        "해운대구": ["우동", "중동"],
        "수영구": ["광안동", "민락동"]
    }
}

# =========================
# 유틸 함수
# =========================

def generate_user_id():
    length = random.randint(4, 7)
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_name():
    return random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)


def generate_address():
    province = random.choice(list(ADDRESS_MAP.keys()))
    city = random.choice(list(ADDRESS_MAP[province].keys()))
    district = random.choice(ADDRESS_MAP[province][city])
    return f"{province} {city} {district}"


# =========================
# CSV 생성 로직
# =========================

def generate_userinfo_csv(count=100, filename="userinfo.csv"):
    output_path = Path(filename)

    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "email", "name", "age", "address"])

        used_ids = set()

        while len(used_ids) < count:
            user_id = generate_user_id()
            if user_id in used_ids:
                continue

            used_ids.add(user_id)

            email = f"{user_id}@example.com"
            name = generate_name()
            age = random.randint(10, 100)
            address = generate_address()

            writer.writerow([user_id, email, name, age, address])

    print(f"✅ {count}건의 사용자 정보가 {output_path.absolute()} 에 생성되었습니다.")


# =========================
# 실행 진입점
# =========================

if __name__ == "__main__":
    generate_userinfo_csv(100)
