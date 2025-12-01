from bs4 import BeautifulSoup
import os

def prepare_web_html(input_path: str, filename: str, article_slug: str, base_url: str = "https://cyprieninperu.netlify.app/", output_path: str = "content/newsletters"):
    """
    Removes MAIL class elements AND replaces template variables, then saves to output.
    
    Args:
        input_path (str): Path to input HTML file
        filename (str): Newsletter filename for {{FILENAME}}
        article_slug (str): Article slug for {{ARTICLE_SLUG}}
        base_url (optional, str): Website domain for {{BASE_URL}}. Defaults to: "https://cyprieninperu.netlify.app/"
    output_path (optional, str): Directory to save cleaned HTML. Defaults to: "content/newsletters"
    """
    # Validate input file
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Read and replace template variables FIRST
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Template replacements (in order of your original script)
    replacements = {
        '{{BASE_URL}}': base_url,
        '{{FILENAME}}': filename or os.path.basename(input_path),
        '{{ARTICLE_SLUG}}': article_slug
    }
    
    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, value)
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove ALL elements with class="MAIL"
    mail_elements = soup.find_all(class_='MAIL')
    removed_count = len(mail_elements)
    
    for elem in mail_elements:
        elem.decompose()
    
    # Get output filename (same as input)
    input_filename = os.path.basename(input_path)
    output_file = os.path.join(output_path, input_filename)
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Save cleaned HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✓ Replaced {len(replacements)} template variables")
    print(f"✓ Removed {removed_count} MAIL elements")
    print(f"✓ Saved: {output_file}")
    return output_file

# Usage example:
if __name__ == "__main__":
    input_file = "newslettermjml/DE-30-11-2025.html"
    output_dir = "content/newsletters/"
    
    web_html = prepare_web_html(
        input_file, 
        base_url="https://cyprieninperu.netlify.app/",
        filename="DE-30-11-2025.html",
        article_slug="11-hours-later",
        output_path=output_dir
    )
