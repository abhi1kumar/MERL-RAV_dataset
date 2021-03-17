"""
    Sample Run:
    python organize_merl_rav_using_aflw_and_our_labels.py

    Organizes landmark points and the images of the original AFLW dataset into
    a common directory.

    Version 1 Abhinav Kumar
"""

from common_functions import *

IMAGE_EXTENSIONS                 = [".jpg"]
LANDMARK_GROUND_TRUTH_EXTENSIONS = [".pts"]

#==============================================================================
# Paths
#==============================================================================
input_folder      = "aflw"                # path to the aflw folder
label_folder      = "merl_rav_labels"     # path to the merl_rav_labels
output_folder     = "merl_rav_organized"  # path to the output folder

# All sub_directories in the label folder
sub_directories   = ["frontal", "left", "lefthalf", "right", "righthalf"]
# Each of the above subdirectories contain the following two folders
sub_directories_2 = ["trainset", "testset"]

images_folder     = "faces"
landmarks_folder  = "labels"

# Grab all the images from the aflw first
input_images_path = []
input_subfolders  = ["0", "2", "3"]

for subfolder in input_subfolders:
    temp                 = [input_folder, "flickr", subfolder]
    input_subfolder_path = os.path.join(*temp)
    image_files_grabbed  = grab_files(input_subfolder_path, IMAGE_EXTENSIONS)
    num_images           = len(image_files_grabbed)
    print("Found {} images in {}".format(num_images, input_subfolder_path))
    input_images_path   += image_files_grabbed

total_input_images = len(input_images_path)
print("")

# Create the output folder
create_folder(output_folder)

# Go to each of the sub-directories
for i in range(len(sub_directories)):

    for j in range(len(sub_directories_2)):
        
        # Get all the landmarks
        temp                      = [label_folder, sub_directories[i], sub_directories_2[j], landmarks_folder]
        input_landmarks_full_path = os.path.join(*temp)
        landmark_files_grabbed    = grab_files(input_landmarks_full_path, LANDMARK_GROUND_TRUTH_EXTENSIONS)
        num_landmarks             = len(landmark_files_grabbed)

        print("\n{:10s}".format(sub_directories[i]))
        print("Landmarks_directory= {:75s} #Landmarks= {}".format(input_landmarks_full_path, num_landmarks))

        temp                      = [output_folder, sub_directories[i], sub_directories_2[j]]
        output_sub_directory_full_path = os.path.join(*temp)
        create_folder(output_sub_directory_full_path)

        # Now search for the corresponding images
        images_files_paths = []
        for m in range(num_landmarks):
            current_landmark           = landmark_files_grabbed[m]
            basename                   = os.path.basename(current_landmark)
            basename_without_extension = basename.split(".")[0]
            key                        = basename_without_extension.split("_")[0]
            
            found    = False
            for n in range(total_input_images):
                current_image          = input_images_path[n]
                current_image_basename = os.path.basename(current_image)
                current_image_extension= current_image_basename.split(".")[1]

                if key in current_image_basename:
                    found = True
                    break

            if found:
                # Copy image files and landmark files to the same output directory
                # Remember to keep the image same as the landmark
                execute("cp " + current_image    + " " + os.path.join(output_sub_directory_full_path, basename_without_extension + "." + current_image_extension))
                execute("cp " + current_landmark + " " + output_sub_directory_full_path)
            else:
                print("{} image not found in AFLW dataset".format(basename_without_extension))

            if (m+1) % 1000 == 0 or m == num_landmarks-1:
                print("{} images-landmarks checked".format(m+1))
