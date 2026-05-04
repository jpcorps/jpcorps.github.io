import os
import re
import shutil
from PIL import Image

# 1. 경로 설정
BACKUP_DIR = r"C:\Users\jpcor\Desktop\EGtoTS\chulin28ho\post"
POSTS_DIR = r"D:\newsite\my-blowfish-blog\content\posts"
OUTPUT_IMG_DIR = r"D:\newsite\my-blowfish-blog\static\images"

# 정적 이미지 폴더 생성
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

# 압축 설정 (최대 가로 픽셀, JPG 품질)
MAX_WIDTH = 1024
JPEG_QUALITY = 80


def process_images():
    image_map = {}
    print("이미지 탐색 및 압축 복사를 시작합니다...")

    for root, dirs, files in os.walk(BACKUP_DIR):
        for file in files:
            ext = file.lower().split(".")[-1]
            if ext in ["jpg", "jpeg", "png", "gif"]:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(OUTPUT_IMG_DIR, file)

                # 파일명이 중복될 경우 덮어쓰기 방지 처리 없이 진행 (이글루스 특성상 파일명 중복 확률 낮음)
                image_map[file] = f"/images/{file}"

                # 이미 변환된 파일이 있다면 스킵 (재실행 시 속도 향상)
                if os.path.exists(dest_path):
                    continue

                try:
                    if ext in ["jpg", "jpeg", "png"]:
                        img = Image.open(src_path)

                        # 해상도가 크면 리사이징
                        if img.width > MAX_WIDTH:
                            ratio = MAX_WIDTH / img.width
                            new_size = (MAX_WIDTH, int(img.height * ratio))
                            img = img.resize(new_size, Image.Resampling.LANCZOS)

                        # 알파 채널이 있는 PNG를 JPG 포맷으로 저장할 때의 오류 방지
                        if img.mode in ("RGBA", "P") and ext in ["jpg", "jpeg"]:
                            img = img.convert("RGB")

                        img.save(dest_path, optimize=True, quality=JPEG_QUALITY)
                    else:
                        # GIF는 애니메이션이 깨질 수 있으므로 단순 복사
                        shutil.copy2(src_path, dest_path)
                except Exception as e:
                    print(f"이미지 처리 오류 ({file}): {e}, 원본을 단순 복사합니다.")
                    shutil.copy2(src_path, dest_path)

    print(f"이미지 처리 완료. 총 {len(image_map)}개의 이미지가 매핑되었습니다.")
    return image_map


def update_markdown(image_map):
    print("마크다운 문서 내부의 링크 치환을 시작합니다...")

    # 정규표현식: 마크다운 이미지 ![alt](http...) 및 HTML <img> 태그 모두 탐지
    md_img_pattern = re.compile(r"!\[([^\]]*)\]\((http[^\)]+)\)")
    html_img_pattern = re.compile(r'<img[^>]+src=["\'](http[^"\']+)["\'][^>]*>')

    updated_files_count = 0

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                try:
                    with open(md_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # 간혹 인코딩이 다른 파일이 있을 경우를 대비
                    with open(md_path, "r", encoding="cp949") as f:
                        content = f.read()

                original_content = content

                # 마크다운 문법 치환 함수
                def repl_md(match):
                    alt = match.group(1)
                    url = match.group(2)
                    filename = url.split("/")[-1].split("?")[
                        0
                    ]  # 파라미터가 붙어있을 경우 제거
                    if filename in image_map:
                        return f"![{alt}]({image_map[filename]})"
                    return match.group(0)

                # HTML 태그 치환 함수
                def repl_html(match):
                    full_tag = match.group(0)
                    url = match.group(1)
                    filename = url.split("/")[-1].split("?")[0]
                    if filename in image_map:
                        return full_tag.replace(url, image_map[filename])
                    return full_tag

                content = md_img_pattern.sub(repl_md, content)
                content = html_img_pattern.sub(repl_html, content)

                if content != original_content:
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    updated_files_count += 1

    print(f"문서 치환 완료. 총 {updated_files_count}개의 문서가 수정되었습니다.")


if __name__ == "__main__":
    # 안전을 위해 미리 content/posts 폴더를 백업해두십시오.
    img_map = process_images()
    update_markdown(img_map)
