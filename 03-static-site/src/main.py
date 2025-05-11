import os
import shutil

from .markdown import extract_markdown_title, markdown_to_html


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


def generate_page(md_path: str, html_tmpl_path: str, html_path: str) -> None:
    """
    Create an HTML file from a markdown file with the given HTML template file.
    """
    print(f"Generating page from {md_path} to {html_path} using {html_tmpl_path}")
    with open(md_path, "r") as f:
        md = f.read()
        title = extract_markdown_title(md)
        content = markdown_to_html(md)

    with open(html_tmpl_path, "r") as f:
        tmpl = f.read()

    html = tmpl.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(html_path, "w") as f:
        f.write(html)


def generate_pages_recursive(md_dir: str, html_tmpl_path: str, html_dir: str) -> None:
    """
    Recursively generate HTML files from markdown files under directory
    """
    assert os.path.exists(md_dir)
    os.makedirs(html_dir, exist_ok=True)

    list_dir = os.listdir(md_dir)
    for item in list_dir:
        item_basename, item_ext = os.path.splitext(item)
        item_path = os.path.join(md_dir, item)

        if item_ext == ".md":
            generate_page(
                item_path,
                html_tmpl_path,
                os.path.join(html_dir, item_basename + ".html"),
            )
            continue

        if os.path.isdir(item_path):
            generate_pages_recursive(
                item_path, html_tmpl_path, os.path.join(html_dir, item)
            )


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
    md_path = os.path.join(project_root, "content/")
    tmpl_path = os.path.join(project_root, "template.html")
    generate_pages_recursive(md_path, tmpl_path, public_dir)


if __name__ == "__main__":
    main()
