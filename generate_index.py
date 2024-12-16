import os

def generate_index_for_folder(folder_path):
    output_file = os.path.join(folder_path, "index.md")
    with open(output_file, "w") as f:
        f.write(f"# Files in {folder_path}\n\n")
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".md") and file_name != "index.md":
                f.write(f"- [{file_name}]({file_name})\n")

def generate_indexes(root_path="."):
    for subdir, _, _ in os.walk(root_path):
        if subdir == ".git" or "node_modules" in subdir:
            continue
        generate_index_for_folder(subdir)

if __name__ == "__main__":
    generate_indexes()