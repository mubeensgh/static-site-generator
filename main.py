import os

from src.sitegen import copy_static_to_public
from src.pagegenerator import generate_page

def main():
    print("Starting static site generation...")

    current_working_directory = os.getcwd()
    static_content_path = os.path.join(current_working_directory, "static")
    public_output_path = os.path.join(current_working_directory, "public")
    content_input_path = os.path.join(current_working_directory, "content") # This is root
    template_file_path = os.path.join(current_working_directory, "template.html")

    
    copy_static_to_public(static_content_path, public_output_path)

    generate_page(content_input_path, template_file_path, public_output_path)

    print("\nStatic site generation complete.")

if __name__ == "__main__":
    main()