import fitz
import docx
import re
import spacy

nlp = spacy.load("en_core_web_sm")


# -----------------------------
# FILE TEXT EXTRACTION
# -----------------------------

def extract_text(file, file_type):
    text = ""

    if file_type == "pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

    elif file_type == "docx":
        document = docx.Document(file)
        for para in document.paragraphs:
            text += para.text + "\n"

    return text


# -----------------------------
# CLEAN TEXT
# -----------------------------

def clean_text(text):
    text = re.sub(r'\r', '\n', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[•●▪■]', '', text)
    return text.strip()


# -----------------------------
# BASIC DETAILS
# -----------------------------

def extract_email(text):
    match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-]{8,15}', text)
    return match.group(0) if match else None


def extract_name(text):
    doc = nlp(text[:1000])  # first part only
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


# -----------------------------
# SECTION BASED EXTRACTION
# -----------------------------

def extract_section(text, section_keywords):
    lines = text.split("\n")
    section_data = []
    capture = False

    for line in lines:
        line_strip = line.strip().lower()

        if any(keyword in line_strip for keyword in section_keywords):
            capture = True
            continue

        if capture:
            if line_strip == "":
                break
            section_data.append(line.strip())

    return section_data


def extract_skills(text):
    return extract_section(text, ["skills", "technical skills", "core competencies"])


def extract_education(text):
    return extract_section(text, ["education", "academic qualification"])


def extract_experience(text):
    return extract_section(text, ["experience", "work experience", "professional experience"])


# -----------------------------
# MAIN FUNCTION
# -----------------------------

def parse_resume(file, file_type):

    text = extract_text(file, file_type)
    text = clean_text(text)

    parsed_data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }

    return parsed_data