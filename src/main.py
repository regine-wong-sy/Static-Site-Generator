import os
import shutil

from generate_page import generate_page

STATIC_DIR = "static"
PUBLIC_DIR = "public"
CONTENT_PATH = "content/index.md"
TEMPLATE_PATH = "template.html"
DEST_PATH = "public/index.html"


def copy_files_recursive(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            copy_files_recursive(src_path, dst_path)


def main():
    copy_files_recursive(STATIC_DIR, PUBLIC_DIR)
    generate_page(CONTENT_PATH, TEMPLATE_PATH, DEST_PATH)


if __name__ == "__main__":
    main()
