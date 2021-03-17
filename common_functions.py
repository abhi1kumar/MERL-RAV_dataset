import os
import glob

def grab_files(folder_full_path, EXTENSIONS):
    """
        Grabs files in folder with the given extensions
        Returns- list
    """
    files_grabbed = []
    for j in range(len(EXTENSIONS)):
        key = os.path.join(folder_full_path, "*"+EXTENSIONS[j])
        files_grabbed.extend(glob.glob(key))

    return files_grabbed

def copy_files(list_of_files, output_folder_path):
    """
        Copies a list of files to the output folder path
    """
    num_files = len(list_of_files)

   # Iterate over all files
    for j in range(num_files):
        filename = list_of_files[j]

        # Copy the files to new location
        subprocess.call(["cp", filename,  output_folder_path])

def create_folder(output_folder_path):
    """
        Tries to create a folder if folder is not present
    """
    if os.path.exists(output_folder_path):
        print("Directory exists {}".format(output_folder_path))
    else:
        print("Creating directory {}".format(output_folder_path))
        os.makedirs(output_folder_path)

def execute(command, print_flag= False):
    if print_flag:
        print(command)
    os.system(command)
