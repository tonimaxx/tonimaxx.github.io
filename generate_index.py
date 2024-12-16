import os

# Directories to exclude from processing
EXCLUDE_DIRS = ['.github/workflows']

def generate_index_for_directory(root_dir):
    index_file = os.path.join(root_dir, 'index.md')

    with open(index_file, 'w') as f:
        f.write("# Index of files\n\n")
        for filename in sorted(os.listdir(root_dir)):
            if filename in ['index.md', '.DS_Store'] or os.path.isdir(os.path.join(root_dir, filename)):
                continue
            f.write(f"- [{filename}]({filename})\n")

def walk_directories_and_generate_index():
    for root, dirs, files in os.walk('.'):
        if any(excl in root for excl in EXCLUDE_DIRS):
            continue  # Skip excluded directories
        generate_index_for_directory(root)

if __name__ == "__main__":
    walk_directories_and_generate_index()
    print("Index.md files have been generated successfully!")