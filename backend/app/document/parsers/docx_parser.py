from docx import Document


def parse_docx(file_path):

    doc = Document(file_path)

    text = []

    for para in doc.paragraphs:

        text.append(para.text)

    return "\n".join(text)