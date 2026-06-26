from os_work import *
from getcontent import *
import sys

def main() -> None:
    if len(sys.argv) != 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    copy_files_from_folder("static", "docs")
    generate_pages_recursive("content", "template.html", "public", basepath)


main()
