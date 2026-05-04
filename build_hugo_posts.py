import os
import re
import shutil
import urllib.parse
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from PIL import Image

# 경로 설정
BACKUP_DIR = r"C:\Users\jpcor\Desktop\EGtoTS\chulin28ho\post"
POSTS_DIR = r"D:\newsite\my-blowfish-blog\content\posts"
OUTPUT_IMG_DIR = r"D:\newsite\my-blowfish-blog\static\images"

# 설정값
MAX_WIDTH = 1024
JPEG_QUALITY = 80


def clean_directory(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def process_image(src_path, dest_filename):
    dest_path = os.path.join(OUTPUT_IMG_DIR, dest_filename)
    if os.path.exists(dest_path):
        return True

    ext = src_path.lower().split(".")[-1]
    try:
        if ext in ["jpg", "jpeg", "png"]:
            img = Image.open(src_path)
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                new_size = (MAX_WIDTH, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            if img.mode in ("RGBA", "P") and ext in ["jpg", "jpeg"]:
                img = img.convert("RGB")

            img.save(dest_path, optimize=True, quality=JPEG_QUALITY)
        else:
            shutil.copy2(src_path, dest_path)
        return True
    except Exception as e:
        print(f"이미지 처리 오류 ({src_path}): {e}")
        try:
            shutil.copy2(src_path, dest_path)
            return True
        except Exception:
            return False


def build_posts():
    print("기존 데이터 초기화 및 재구축 시작...")
    clean_directory(POSTS_DIR)
    clean_directory(OUTPUT_IMG_DIR)

    processed_count = 0

    for root, dirs, files in os.walk(BACKUP_DIR):
        for file in files:
            if file.endswith(".html"):
                html_path = os.path.join(root, file)
                base_id = file.split(".html")[0]
                img_folder_path = os.path.join(root, base_id)

                try:
                    with open(html_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f.read(), "html.parser")
                except UnicodeDecodeError:
                    with open(html_path, "r", encoding="cp949") as f:
                        soup = BeautifulSoup(f.read(), "html.parser")

                title_tag = soup.find("h2", class_="post-title")
                date_tag = soup.find("span", class_="time")
                content_tag = soup.find("div", class_="content")

                if not title_tag or not date_tag or not content_tag:
                    continue

                title = title_tag.get_text(strip=True)
                safe_front_matter_title = title.replace('"', '\\"')
                date_str = date_tag.get_text(strip=True)
                date_only = date_str.split(" ")[0]

                physical_images = []
                if os.path.exists(img_folder_path) and os.path.isdir(img_folder_path):
                    for img_file in os.listdir(img_folder_path):
                        if img_file.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                            physical_images.append(img_file)

                used_images = set()

                for img in content_tag.find_all("img"):
                    src = img.get("src")
                    if src:
                        decoded_src = urllib.parse.unquote(src)
                        img_filename = os.path.basename(decoded_src)

                        if img_filename in physical_images:
                            img_local_path = os.path.join(img_folder_path, img_filename)
                            if process_image(img_local_path, img_filename):
                                img["src"] = f"/images/{img_filename}"
                                used_images.add(img_filename)

                markdown_content = md(
                    str(content_tag), strip=["b", "i", "strong", "em"]
                )

                unused_images = [
                    img for img in physical_images if img not in used_images
                ]
                if unused_images:
                    markdown_content += "\n\n---\n\n"
                    for unused_img in unused_images:
                        img_local_path = os.path.join(img_folder_path, unused_img)
                        if process_image(img_local_path, unused_img):
                            markdown_content += f"![첨부이미지](/images/{unused_img})\n"

                front_matter = f"""---
title: "{safe_front_matter_title}"
date: {date_str.replace(' ', 'T')}Z
draft: false
---

"""
                final_content = front_matter + markdown_content.strip()

                # 파일명을 날짜와 고유 ID로 설정하여 URL 안정성 확보
                md_filename = f"{date_only}-{base_id}.md"
                md_filepath = os.path.join(POSTS_DIR, md_filename)

                with open(md_filepath, "w", encoding="utf-8") as f:
                    f.write(final_content)

                processed_count += 1

    print(f"작업 완료. 총 {processed_count}개의 포스트가 생성되었습니다.")


if __name__ == "__main__":
    build_posts()
