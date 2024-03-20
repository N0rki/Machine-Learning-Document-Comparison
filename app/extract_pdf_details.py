import os
import fitz  # PyMuPDF
import re


def extract_abstract(pdf_path):
    pdf_document = fitz.open(pdf_path)

    abstract = None

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()

        abstract_match = re.search(r'(?<=A B S T R A C T).*?(?=1. Introduction)', text, re.IGNORECASE | re.DOTALL)
        if abstract_match:
            abstract = abstract_match.group().strip()
            break

    pdf_document.close()

    return abstract


def extract_author(pdf_path):
    pdf_document = fitz.open(pdf_path)

    metadata = pdf_document.metadata

    author = metadata.get("author", None)

    return author


def extract_title(pdf_path):
    pdf_document = fitz.open(pdf_path)

    metadata = pdf_document.metadata

    name = metadata.get("title", None)

    return name


def extract_references(pdf_path):
    pdf_document = fitz.open(pdf_path)

    references = None

    num_pages = len(pdf_document)

    text = ""
    start_page = max(0, num_pages - 3)
    for page_num in range(start_page, num_pages):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()

    references_match = re.search(r'\bReferences\b\s*(.*)', text, re.IGNORECASE | re.DOTALL)
    if references_match:
        references = references_match.group(1).strip()

    return references


def extract_details(directory):
    pdf_details = {}

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)

            abstract = extract_abstract(file_path)
            author = extract_author(file_path)
            name = extract_title(file_path)
            references = extract_references(file_path)

            pdf_details[filename] = {"author": author, "abstract": abstract,  "name": name, "references": references}

    return pdf_details


directory_path = "../documents"
pdf_details = extract_details(directory_path)


for filename, info in pdf_details.items():

    author = info["author"]
    abstract = info["abstract"]
    references = info["references"]
    name = info["name"]

    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nNext Document:\n")
    print(f"Filename: {filename}\nAuthor: {author}\nName: {name}\nAbstract:\n{abstract}\nReferences:\n{references}\n")
