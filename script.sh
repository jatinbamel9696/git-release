#!/bin/bash

# Get the current version from the latest tag
current_version=$(git describe --tags --abbrev=0 2>/dev/null)

# If no tags are found, start with version 0.1.0
if [ -z "$current_version" ]; then
  current_version="0.1.0"
fi

# Parse the major, minor, and patch versions
version_regex="([0-9]+)\.([0-9]+)\.([0-9]+)"
if [[ $current_version =~ $version_regex ]]; then
  major_version="${BASH_REMATCH[1]}"
  minor_version="${BASH_REMATCH[2]}"
  patch_version="${BASH_REMATCH[3]}"
else
  echo "Error: Unable to parse current version."
  exit 1
fi

# Determine the next version
read -p "Enter the type of release (major, minor, patch): " release_type

case $release_type in
  major)
    new_version="$((major_version + 1)).0.0"
    ;;
  minor)
    new_version="$major_version.$((minor_version + 1)).0"
    ;;
  patch)
    new_version="$major_version.$minor_version.$((patch_version + 1))"
    ;;
  *)
    echo "Error: Invalid release type. Choose 'major', 'minor', or 'patch'."
    exit 1
    ;;
esac

# Confirm the new version
read -p "Confirm release of version $new_version (y/n): " confirm
if [ "$confirm" != "y" ]; then
  echo "Release canceled."
  exit 0
fi

# Create a new tag for the release
git tag "$new_version"

# Push the new tag to the repository
git push origin "$new_version"

echo "Release $new_version created successfully."
