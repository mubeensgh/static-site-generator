import os
from src.markdown_parser import markdown_to_html_node, extract_title

def _generate_page_from_file(from_file_path: str, template_path: str, dest_file_path: str):

    with open(from_file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    page_content_html = html_node.to_html()

    page_title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", page_content_html)

    dest_dir = os.path.dirname(dest_file_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_file_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Single page generation complete for {from_file_path}")


def generate_page(from_path: str, template_path: str, dest_dir_path: str):

    if os.path.isfile(from_path):
        if not from_path.endswith(".md"):
            print(f"  Skipping non-markdown file: {from_path}")
            return
        
        base_filename = os.path.basename(from_path) # e.g., 'index.md'
        html_filename = os.path.splitext(base_filename)[0] + ".html" # e.g., 'index.html'
        final_dest_html_path = os.path.join(dest_dir_path, html_filename)

        _generate_page_from_file(from_path, template_path, final_dest_html_path)
        return 

    os.makedirs(dest_dir_path, exist_ok=True)

    for item_name in os.listdir(from_path):
        source_item_path = os.path.join(from_path, item_name)
        

        if os.path.isdir(source_item_path):
            next_level_dest_dir_path = os.path.join(dest_dir_path, item_name)
            generate_page(source_item_path, template_path, next_level_dest_dir_path)

        elif os.path.isfile(source_item_path):
            generate_page(source_item_path, template_path, dest_dir_path) # Pass the current dir
        else:
            print(f"  Skipping unknown item type: {source_item_path}")
            
    print(f"--- Finished recursive generation for: {from_path} ---")

