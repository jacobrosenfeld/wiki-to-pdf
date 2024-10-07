import mwparserfromhell
import pdfkit
import xml.etree.ElementTree as ET

# Function to print the XML structure to inspect its elements and attributes
def print_xml_structure(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Print the first few elements to inspect structure
    for elem in root.iter():
        print(elem.tag, elem.attrib)

# Function to extract articles from MediaWiki XML dump, with namespace handling
def extract_articles(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Check if the XML uses a namespace, adjust accordingly
    ns = {'ns': 'http://www.mediawiki.org/xml/export-0.11/'}  # Example namespace; adjust after printing structure

    articles = []
    for page in root.findall(".//ns:page", ns):  # Adjusted to include namespace
        title = page.find("ns:title", ns).text
        revision = page.find(".//ns:revision", ns)
        if revision is not None:
            text_elem = revision.find("ns:text", ns)
            text = text_elem.text if text_elem is not None else ""
            articles.append({"title": title, "text": text})
    
    return articles

# Convert MediaWiki syntax to plain text using mwparserfromhell
def convert_wiki_to_plain_text(article_text):
    wikicode = mwparserfromhell.parse(article_text)
    return wikicode.strip_code()  # Converts to plain text

# Combine all articles into a single HTML string
def combine_articles(articles):
    combined_html = "<html><body><h1>All Articles</h1>"
    for article in articles:
        title = article['title']
        text = convert_wiki_to_plain_text(article['text'])
        combined_html += f"<h2>{title}</h2>"
        combined_html += f"<p>{text}</p>"
    combined_html += "</body></html>"
    return combined_html

# Create a PDF from the combined HTML
def save_pdf(html_content, output_pdf):
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8"
    }
    pdfkit.from_string(html_content, output_pdf, options=options)

# Main process to create PDF from the MediaWiki XML dump
def create_pdf_from_wiki_dump(xml_file, output_pdf):
    print("Inspecting XML structure...")
    print_xml_structure(xml_file)  # Debug: Print the structure to see namespace and tags
    
    print("Extracting articles...")
    articles = extract_articles(xml_file)
    
    if not articles:
        print("No articles found. Please check the XML structure.")
        return
    
    combined_html = combine_articles(articles)
    
    # Debug: Print out the first part of the HTML to ensure it's correct
    print("Generated HTML Preview:", combined_html[:500])  # Check the first 500 characters of the HTML
    
    print("Saving to PDF...")
    save_pdf(combined_html, output_pdf)
    print(f"PDF saved as {output_pdf}")

# Run the process with your XML dump file and desired PDF output path
xml_dump_file = "/Users/jacobrosenfeld/Downloads/halac/halachipediacom-20241007-wikidump/halachipediacom-20241007-current.xml"
output_pdf_file = "combined_articles.pdf"


# Create the PDF from the wiki dump
create_pdf_from_wiki_dump(xml_dump_file, output_pdf_file)

