# Wiki XML Dump to PDF

The purpose of this is essentially to extract all the text from the xml is a (somewhat) readable format. 

This was used to create PDF files to upload an entire wiki to [NotebookLM](https://notebooklm.google.com/).

Two python files. 

## Explanation of files

1. [one-pdf.py](one-pdf.py) will convert the xml dump to one large pdf. 
2. [max-word-count.py] will break up the text into multiple PDFs with a maximum of 499,999 words to abide by NotebookLM word limits. [You can edit the word limit here] (max-word-count.py#L43).

### Notes

The script assumes you are using `http://www.mediawiki.org/xml/export-0.11/'  # Example namespace; adjust after printing structure` but it's possible your XML is using a different namespace. 

The script prints out the namespace when running and will throw an error if the namespace is incorrect but in the print it should indicate the correct namespace so you can update the namespace in Line 20 [max-word-count.py#L20] or [one-pdf.py#L20].