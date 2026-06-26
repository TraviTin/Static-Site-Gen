from os_work import *
from getcontent import *
import sys



def main() -> None:
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_files_from_folder("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
