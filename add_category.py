import os
import re

# 스크린샷에서 확인된 사용자님의 절대 경로입니다.
POSTS_DIR = r"D:\newsite\my-blowfish-blog\content\posts"
CATEGORY_NAME = "이글루스 백업"


def add_category_to_files():
    print(f"작업을 시작합니다. 대상 폴더: {POSTS_DIR}")

    if not os.path.exists(POSTS_DIR):
        print(f"에러: 경로를 찾을 수 없습니다 -> {POSTS_DIR}")
        return

    count = 0
    # 폴더 내 모든 .md 파일을 검색합니다.
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # 이미 categories 설정이 있으면 건너뜁니다 (중복 방지)
                    if "categories:" in content:
                        continue

                    # 파일 맨 첫 줄의 --- 바로 다음에 카테고리를 삽입합니다.
                    new_content = re.sub(
                        r"^---\n",
                        f'---\ncategories: ["{CATEGORY_NAME}"]\n',
                        content,
                        count=1,
                    )

                    if new_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        count += 1
                        if count % 100 == 0:
                            print(f"진행 중... {count}개 처리 완료")
                except Exception as e:
                    print(f"파일 처리 중 오류 발생 ({file}): {e}")

    print(f"\n성공! 총 {count}개의 파일에 '{CATEGORY_NAME}' 카테고리를 추가했습니다.")


if __name__ == "__main__":
    add_category_to_files()
