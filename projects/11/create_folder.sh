#!/bin/bash

# Create 'xml' and 'output' directories if they don't exist
mkdir -p xml output

# Iterate over subdirectories in the current directory
for subdir in */; do
    # Extract the directory name
    dir_name=$(basename "$subdir")

    # Create empty directories with the same name in 'xml' and 'output'
    mkdir -p "xml/$dir_name" "output/$dir_name"
done