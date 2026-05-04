import os
import re

posts_dir = "content/posts"  # 경로는 본인 환경에 맞춰 확인

md_img_re = re.compile(r"!\[.*?\]\((.*?)\)")
html_img_re = re.compile(r'<img.*?src=["\'](.*?)["\']')


def update_posts():
    for root, dirs, files in os.walk(posts_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue

                front_matter = parts[1]
                body = parts[2]

                # 이미 image 설정이 되어 있어도 잘못된 따옴표가 있다면 수정하기 위해 체크 해제
                # if 'image:' in front_matter: continue

                match = md_img_re.search(body) or html_img_re.search(body)

                if match:
                    img_url = (
                        match.group(1).split()[0].strip('"').strip("'")
                    )  # 공백 뒤 타이틀 제거 및 따옴표 정리

                    # 기존 image 항목이 있다면 제거하고 새로 삽입
                    lines = [
                        line
                        for line in front_matter.split("\n")
                        if not line.startswith("image:")
                    ]
                    new_front_matter = (
                        "\n".join(lines).rstrip() + f'\nimage: "{img_url}"\n'
                    )
                    new_content = f"---{new_front_matter}---{body}"

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed: {file}")


if __name__ == "__main__":
    update_posts()
