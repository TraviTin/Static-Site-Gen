import os
import shutil

# copy files from folder works by naming (what files I want to copy, where I want them to go)
def copy_files_from_folder(folder_path: str, destination_path: str) -> None:
    if os.path.exists(destination_path):
        print(f"removing folder {destination_path}")
        shutil.rmtree(destination_path)
    os.makedirs(destination_path)
    print(f"making new folder {destination_path}")
    copy_helper(folder_path, destination_path)




def copy_helper(folder_path: str, destination_path: str) -> None:
    for filename in os.listdir(folder_path):
        src_path = os.path.join(folder_path, filename)
        if os.path.isfile(src_path):
            print(f"copying {src_path} to {destination_path}")
            shutil.copy(src_path, destination_path)
        else:
            os.mkdir(os.path.join(destination_path, filename))
            copy_helper(src_path, os.path.join(destination_path, filename))
