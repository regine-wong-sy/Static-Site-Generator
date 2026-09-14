import os
import shutil
import sys

from generate_page import generate_pages_recursive

STATIC_DIR = "static"
DOCS_DIR = "docs"
CONTENT_DIR = "content"
TEMPLATE_PATH = "template.html"


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
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_files_recursive(STATIC_DIR, DOCS_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, DOCS_DIR, basepath)


if __name__ == "__main__":
    main()
