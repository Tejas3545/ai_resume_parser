import re
import pdfplumber
import docx2txt

# Try to use spaCy if available, otherwise fall back gracefully
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except Exception:
    nlp = None


def _clean_text(text: str) -> str:
    if not text:
        return ""
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text(file_path: str) -> str:
    text = ""
    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
    elif file_path.lower().endswith(".docx"):
        text = docx2txt.process(file_path) or ""
    return _clean_text(text)


EMAIL_REGEX = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"(?:\+?\d[\d\s-]{7,}\d)"

EDU_KEYWORDS = [
    "B.Tech", "B.E", "BE", "BSc", "B.Sc", "M.Tech", "M.E", "ME", "MSc", "M.Sc",
    "MBA", "PhD", "Diploma", "Bachelor", "Master"
]

SKILL_KEYWORDS = [
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript", "SQL", "NoSQL",
    "Flask", "Django", "FastAPI", "Pandas", "NumPy", "scikit-learn",
    "TensorFlow", "Keras", "PyTorch", "OpenCV", "NLTK", "spaCy", "AWS", "GCP",
    "Azure", "Docker", "Kubernetes", "Git", "Linux", "HTML", "CSS", "React",
]


def parse_resume(text: str) -> dict:
    details = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": [],
        "education": [],
        "experience": []
    }

    if not text:
        return details

    # Email
    email_match = re.search(EMAIL_REGEX, text)
    if email_match:
        details["email"] = email_match.group(0)

    # Phone
    phone_match = re.search(PHONE_REGEX, text)
    if phone_match:
        details["phone"] = phone_match.group(0)

    # ---- Improved NAME Extraction ----
    blacklist_words = ["intern", "developer", "engineer", "student", "enthusiast", "specialist"]
    candidate_name = None

    # Try spaCy PERSON detection first
    if nlp is not None:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                if not any(bw in ent.text.lower() for bw in blacklist_words):
                    candidate_name = ent.text.strip()
                    break

    # If spaCy failed, use heuristics
    if not candidate_name:
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if any(bw in line.lower() for bw in blacklist_words):
                continue
            if 2 <= len(line.split()) <= 5:  # reasonable for names
                candidate_name = line
                break

    details["name"] = candidate_name

    # Education
    edu_found = set()
    for kw in EDU_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", text, flags=re.IGNORECASE):
            edu_found.add(kw)
    details["education"] = sorted(edu_found)

    # Skills
    skill_found = set()
    for kw in SKILL_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", text, flags=re.IGNORECASE):
            skill_found.add(kw)
    details["skills"] = sorted(skill_found)

    # Experience (simple heuristic)
    exp_lines = []
    for line in text.splitlines():
        l = line.strip()
        if not l:
            continue
        if re.search(r"experience|worked|intern|years|months", l, flags=re.IGNORECASE):
            exp_lines.append(l)
    details["experience"] = exp_lines[:10]  # avoid huge blobs

    return details
