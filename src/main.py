from os_work import *
from textnode import TextNode, TextType
from getcontent import *



def main() -> None:
    copy_files_from_folder("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()