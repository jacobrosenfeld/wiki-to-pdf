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

# Function to count words in a string
def count_words(text):
    return len(text.split())

# Combine articles into segments that max out at 500,000 words per segment
def split_articles_into_segments(articles, max_words=499999):
    segments = []
    current_segment = []
    current_word_count = 0
    
    for article in articles:
        title = article['title']
        text = convert_wiki_to_plain_text(article['text'])
        article_word_count = count_words(text)
        
        if current_word_count + article_word_count > max_words:
            # Start a new segment if adding the article exceeds the word limit
            segments.append(current_segment)
            current_segment = []
            current_word_count = 0
        
        current_segment.append({'title': title, 'text': text})
        current_word_count += article_word_count
    
    # Add the last segment
    if current_segment:
        segments.append(current_segment)
    
    return segments

# Combine articles into a single HTML string for each segment
def combine_articles_to_html(articles_segment):
    combined_html = "<html><body><h1>Articles</h1>"
    for article in articles_segment:
        title = article['title']
        text = article['text']
        combined_html += f"<h2>{title}</h2>"
        combined_html += f"<p>{text}</p>"
    combined_html += "</body></html>"
    return combined_html

# Create a PDF from the combined HTML
def save_pdf(html_content, output_pdf):
    options = {
        'page-size': 'Letter',  # Page size is set to 'Letter'
        'encoding': "UTF-8"
    }
    pdfkit.from_string(html_content, output_pdf, options=options)

# Main process to create PDFs from the MediaWiki XML dump
def create_pdfs_from_wiki_dump(xml_file):
    print("Inspecting XML structure...")
    print_xml_structure(xml_file)  # Debug: Print the structure to see namespace and tags
    
    print("Extracting articles...")
    articles = extract_articles(xml_file)
    
    if not articles:
        print("No articles found. Please check the XML structure.")
        return
    
    print("Splitting articles into segments of 500,000 words...")
    article_segments = split_articles_into_segments(articles)
    
    for idx, segment in enumerate(article_segments):
        combined_html = combine_articles_to_html(segment)
        
        # Generate output PDF file names with part numbers
        output_pdf_file = f"combined_articles_part{idx+1}.pdf"
        
        # Debug: Print out the first part of the HTML to ensure it's correct
        print(f"Generated HTML Preview for part {idx+1}:", combined_html[:500])  # Check the first 500 characters of the HTML
        
        print(f"Saving to PDF... Part {idx+1}")
        save_pdf(combined_html, output_pdf_file)
        print(f"PDF saved as {output_pdf_file}")

# Run the process with user input for the XML dump file location
xml_dump_file = input("Please enter the path to your MediaWiki XML dump file: ")  # Prompt for XML file location

# Create the PDFs from the wiki dump
create_pdfs_from_wiki_dump(xml_dump_file)