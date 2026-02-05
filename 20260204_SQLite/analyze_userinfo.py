import csv
from collections import defaultdict
from pathlib import Path


CSV_FILE = Path("userinfo.csv")


def get_age_group(age: int) -> str:
    """나이를 나이대로 변환 (예: 27 -> '20대')"""
    decade = (age // 10) * 10
    return f"{decade}대"


def analyze_userinfo_csv():
    age_group_sum = defaultdict(int)
    age_group_count = defaultdict(int)

    city_count = defaultdict(int)

    with open(CSV_FILE, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            age = int(row["age"])
            address = row["address"]

            # 나이대 계산
            age_group = get_age_group(age)
            age_group_sum[age_group] += age
            age_group_count[age_group] += 1

            # 도시(도/광역시) 추출
            city = address.split()[0]
            city_count[city] += 1

    # =========================
    # 결과 출력
    # =========================

    print("\n📊 나이대별 평균 나이")
    print("-" * 30)
    for age_group in sorted(age_group_sum.keys(), key=lambda x: int(x.replace('대', ''))):
        avg_age = age_group_sum[age_group] / age_group_count[age_group]
        print(f"{age_group}: 평균 {avg_age:.1f}세")

    print("\n🏙 도시별 사용자 수")
    print("-" * 30)
    for city, count in sorted(city_count.items()):
        print(f"{city}: {count}명")


if __name__ == "__main__":
    analyze_userinfo_csv()
