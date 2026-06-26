import os
from markdown_to_html import *
from htmlnode import *

def generate_page(from_path, template_path, dest_path):
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
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f = open(dest_path, "w")
    f.write(content_template)
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path.replace(".md", ".html"))
        else:
            generate_pages_recursive(src_path, template_path, dest_path)