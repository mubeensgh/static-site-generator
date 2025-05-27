import os
from src.markdown_parser import markdown_to_html_node, extract_title

def generate_page(from_path: str, template_path:str, destpath: str):
    """
    This function genrates a HTML page from markdown
    
    Arguments:
    from_path is the path to the markdown file
    template_path is the path to the html template
    destpat is the path where the HTML page will be created

    Returns:
    None
    """
    print(f"Generating page from {from_path} to {destpath} using {template_path}")
    print(f"  Reading markdown from: {from_path}")
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    print(f"  Reading template from: {template_path}")
    with open(template_path,'r') as g:
        template_content = g.read()

    print("  Converting markdown to HTML...")
    html_node = markdown_to_html_node(markdown_content)
    page_content = html_node.to_html()

    print("  Extracting title...")
    page_title = extract_title(markdown_content)

    print("  Replacing placeholders in template...")
    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", page_content)

    dest_dir = os.path.dirname(destpath)
    if dest_dir:
        print(f"  Ensuring destination directory exists: {dest_dir}")
        os.makedirs(dest_dir, exist_ok = True)

    print(f"  Writing generated HTML to: {destpath}")
    with open(destpath,'w') as h:
        h.write(final_html)
    
    print(f"Page generation complete for {from_path}")