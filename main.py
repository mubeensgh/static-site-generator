import os
import shutil

from src.markdown_parser import markdown_to_html_node 
from src.sitegen import copy_static_to_public
from src.pagegenerator import generate_page

def main():
    print("Starting static site generation...")

    current_working_directory = os.getcwd()
    static_content_path = os.path.join(current_working_directory, "static")
    public_output_path = os.path.join(current_working_directory, "public")
    content_input_path = os.path.join(current_working_directory, "content")
    template_file_path = os.path.join(current_working_directory, "template.html")

    
    copy_static_to_public(static_content_path, public_output_path)

    source_markdown_file = os.path.join(content_input_path, "index.md")
    destination_html_file = os.path.join(public_output_path, "index.html")
    
    generate_page(source_markdown_file, template_file_path, destination_html_file)

if __name__ == "__main__":
    main()