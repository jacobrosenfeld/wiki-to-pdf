import mwparserfromhell
import pdfkit
import xml.etree.ElementTree as ET

# Parse the MediaWiki XML dump
def extract_articles(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    articles = []
    for page in root.findall(".//page"):
        title = page.find("title").text
        text = page.find(".//revision/text").text
        if text:
            articles.append({"title": title, "text": text})
    
    return articles

# Convert MediaWiki syntax to HTML using mwparserfromhell
def convert_wiki_to_html(article):
    parsed_text = mwparserfromhell.parse(article)
    return parsed_text.strip_code()  # Converts to plain text (or use HTML renderer)

# Combine all articles
def combine_articles(articles):
    combined = "<h1>All Articles</h1>"
    for article in articles:
        combined += f"<h2>{article['title']}</h2>"
        combined += f"<p>{convert_wiki_to_html(article['text'])}</p>"
    return combined

# Create a PDF from the combined HTML
def save_pdf(html_content, output_pdf):
    pdfkit.from_string(html_content, output_pdf)

# Main process
def create_pdf_from_wiki_dump(xml_file, output_pdf):
    articles = extract_articles(xml_file)
    combined_html = combine_articles(articles)
    save_pdf(combined_html, output_pdf)

# Run the process
xml_dump_file = "/Users/jacobrosenfeld/Downloads/halac/halachipediacom-20241007-wikidump/halachipediacom-20241007-current.xml"
output_pdf_file = "combined_articles.pdf"
create_pdf_from_wiki_dump(xml_dump_file, output_pdf_file)
