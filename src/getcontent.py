import os
from markdown_to_html import *
from pathlib import Path


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    f = open(from_path, "r")
    markdown = f.read()
    f.close()

    f = open(template_path, "r")
    template = f.read()
    f.close()

    markdown_blocks = markdown_to_html_node(markdown)
    markdown_html_string = markdown_blocks.to_html()
    title = extract_title(markdown)
    title_template = template.replace("{{ Title }}", title)
    content_template = title_template.replace("{{ Content }}", markdown_html_string)
    content_template_href = content_template.replace('href="/', f'href="{basepath}')
    content_template_src = content_template_href.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f = open(dest_path, "w")
    f.write(content_template_src)
    f.close()

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(src_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(src_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(src_path, template_path, dest_path, basepath)