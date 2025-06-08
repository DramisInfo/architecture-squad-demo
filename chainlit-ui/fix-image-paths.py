#!/usr/bin/env python
"""
Fix-image-paths.py - Script to convert image paths in markdown files from /diagrams/ to /public/diagrams/
"""

import sys
import re
import os


def fix_image_paths(content):
    """Convert image paths from /diagrams/ to /public/diagrams/"""
    # Find all markdown image references with /diagrams/ path
    pattern = r'!\[(.*?)\]\(/diagrams/(.*?)\.png\)'
    replacement = r'![\1](/public/diagrams/\2.png)'

    # Replace all matches
    fixed_content = re.sub(pattern, replacement, content)

    return fixed_content


def main():
    """Main function to process input file(s)"""
    if len(sys.argv) < 2:
        print("Usage: fix-image-paths.py <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]

    # If output file not specified, use the same file
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix image paths
    fixed_content = fix_image_paths(content)

    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Successfully updated image paths in {output_file}")


if __name__ == '__main__':
    main()
