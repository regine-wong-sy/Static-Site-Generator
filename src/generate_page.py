import os

from split_delimiter import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, filename[: -len(".md")] + ".html")
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
