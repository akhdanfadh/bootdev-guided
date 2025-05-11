import os
import shutil

from .markdown import generate_page


def recursive_copy_directory(source_dir: str, dest_dir: str) -> None:
    """
    Recursively copy a directory from source to destination.
    """
    assert os.path.exists(source_dir)
    os.makedirs(dest_dir, exist_ok=True)

    list_dir = os.listdir(source_dir)
    for item in list_dir:
        item_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_path)
        else:
            recursive_copy_directory(item_path, dest_path)


def main():
    project_root = os.path.split(os.path.dirname(__file__))[0]

    # Source files
    static_dir = os.path.join(project_root, "static/")
    assert os.path.exists(static_dir)

    # Generated files
    public_dir = os.path.join(project_root, "public/")
    shutil.rmtree(public_dir, ignore_errors=True)

    recursive_copy_directory(static_dir, public_dir)

    # Generate HTML
    md_path = os.path.join(project_root, "content/index.md")
    tmpl_path = os.path.join(project_root, "template.html")
    html_path = os.path.join(project_root, "public/index.html")
    generate_page(md_path, tmpl_path, html_path)


if __name__ == "__main__":
    main()
