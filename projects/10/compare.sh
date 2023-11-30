#!/bin/bash

# Specify the source and output directories
source_dir="."
output_dir="output"
exclude_folders="output __pycache__"
text_comparer='../../tools/TextComparer.sh'

# Variable to track whether a failure has occurred
failure_found=false

# Check if a folder name is provided as a command-line argument
if [ $# -eq 1 ]; then
    # Sanitize the folder name using realpath
    target_folder=$(realpath -m --relative-base="$source_dir" "$1")
    target_source_folder="$source_dir/$target_folder"
    target_output_folder="$output_dir/$target_folder"

    # Check if the target folder exists in the source directory
    if [ -d "$target_source_folder" ]; then
        # Construct the corresponding output folder path
        if [ -d "$target_output_folder" ]; then
            # Iterate over XML files in the target source folder
            for source_file in "$target_source_folder"/*.xml; do
                # Extract the file name (without extension)
                filename=$(basename "$source_file" .xml)

                # Construct the corresponding output file path
                output_file="$target_output_folder/$filename.xml"

                # Check if the output file exists
                if [ -e "$output_file" ]; then
                    # Print the program name and file being compared
                    echo "--Checking: $target_folder/$filename"

                    # Compare the XML files
                    sh "$text_comparer" "$source_file" "$output_file"

                    # Check the exit status of the TextComparer
                    if [ $? -ne 0 ]; then
                        echo "Comparison failure in $output_file"
                        failure_found=true
                        break
                    fi
                else
                    echo "--Output file $output_file not found."
                fi
            done
        else
            echo "--Output folder $target_output_folder not found."
        fi
    else
        echo "--Source folder $target_source_folder not found."
    fi
else
    # Iterate over folders in the source directory
    for source_folder in "$source_dir"/*; do
        # Extract the folder name
        folder_name=$(basename "$source_folder")

        # Check if the item is a directory and not in the exclusion list
        if [ -d "$source_folder" ]; then
            should_exclude=false
            for excluded_folder in $exclude_folders; do
                if [ "$folder_name" = "$excluded_folder" ]; then
                    should_exclude=true
                    break
                fi
            done

            if [ "$should_exclude" = false ]; then
                # Construct the corresponding output folder path
                output_folder="$output_dir/$folder_name"

                # Check if the output folder exists
                if [ -d "$output_folder" ]; then
                    # Iterate over XML files in the source folder
                    for source_file in "$source_folder"/*.xml; do
                        # Extract the file name (without extension)
                        filename=$(basename "$source_file" .xml)

                        # Construct the corresponding output file path
                        output_file="$output_folder/$filename.xml"

                        # Check if the output file exists
                        if [ -e "$output_file" ]; then
                            # Print the program name and file being compared
                            echo "--Checking: $folder_name/$filename"

                            # Compare the XML files
                            sh "$text_comparer" "$source_file" "$output_file"

                            # Check the exit status of the TextComparer
                            if [ $? -ne 0 ]; then
                                echo "Comparison failure in $output_file"
                                failure_found=true
                                break
                            fi
                        else
                            echo "--Output file $output_file not found."
                        fi
                    done
                else
                    echo "--Output folder $output_folder not found."
                fi
            fi
        fi

        # Exit the loop if a failure is found
        if [ "$failure_found" = true ]; then
            break
        fi
    done

    # Exit the script with a failure code if a failure is found
    if [ "$failure_found" = true ]; then
        exit 1
    fi
fi
