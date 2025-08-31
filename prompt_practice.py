# prompt_practice.py
# A tiny prompt-engineering playground that demonstrates:
# - Bullet summaries
# - Strict JSON extraction
# - Text classification with fixed labels
# - Markdown table generation
# Purpose: Experiment with prompt engineering for structured, business-ready outputs

import os
import json
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader


# Key for local use only, as this was a test/simple practice script I kept my key here
# and removed it once commiting
OPENAI_API_KEY = "openai_key"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

client = OpenAI()

MODEL = "gpt-3.5-turbo"
TEMP_LOW = 0.1  # more deterministic/reliable, less creative


def chat(messages, model=MODEL, temperature=TEMP_LOW):
    return client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
    ).choices[0].message.content

# Summarises given text, into bullet points using an analytical pov
def summarize_to_bullets(text, max_bullets=5):
    system = "You are a concise business analyst. Focus on clarity and action."
    user = f"""Summarize the following text into at most {max_bullets} bullet points.
Use short, direct bullets (max 15 words each).

TEXT:
{text}
"""
    return chat([{"role":"system","content":system},{"role":"user","content":user}])

# Extracts skills from text and returns them in strict JSON format
def extract_skills_json(text):
    system = "You are an information extraction engine. Always return STRICT JSON only."
    user = f"""Extract key AI/engineering skills as strict JSON with this schema:
{{
  "languages": [string],       // e.g., ["Python", "JavaScript"]
  "frameworks": [string],      // e.g., ["LangChain", "React"]
  "cloud": [string],           // e.g., ["Azure", "GCP"]
  "topics": [string]           // e.g., ["RAG", "Prompt Engineering", "LLMs", "SDLC"]
}}

Rules:
- Respond with ONLY a JSON object. No extra text.
- If a field is unknown, return an empty array for that field.

TEXT:
{text}
"""
    raw = chat([{"role":"system","content":system},{"role":"user","content":user}])
    # Best-effort validation
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Try to fix common trailing text issues
        raw = raw.strip().split("\n")[0]
        data = json.loads(raw)
    return json.dumps(data, indent=2)

# Replies in JSON, adheres to strict pre-determined labels
def classify_text(text):
    system = "You are a classifier. Always reply with STRICT JSON only."
    labels = ["Tech", "Business", "Policy", "Other"]
    user = f"""Classify the TEXT into ONE label from this closed set:
{labels}

Return STRICT JSON: {{"label": "<one_of_labels>", "rationale": "<short reason>"}}
Do not include any other fields.

TEXT:
{text}
"""
    raw = chat([{"role":"system","content":system},{"role":"user","content":user}])
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"label": "Other", "rationale": "Could not parse JSON reliably."}
    return json.dumps(data, indent=2)

# Lists skills in Markdown table
def to_markdown_table(rows):
    """
    rows: list of dicts with the SAME keys.
    Example:
      rows = [
        {"Skill":"Python", "Level":"Intermediate", "Notes":"Used for RAG prototype"},
        {"Skill":"JavaScript", "Level":"Basic", "Notes":"Small front-end tweaks"}
      ]
    The model will normalize and emit a Markdown table.
    """
    system = "You are a formatter that outputs ONLY a Markdown table (no backticks, no commentary)."
    user = f"""Given this JSON array of objects, output ONLY a Markdown table with headers inferred from keys:

JSON:
{json.dumps(rows, indent=2)}

Rules:
- Output only the table. No extra text, no code fences.
- Preserve order of columns as they appear in the first object.
"""
    return chat([{"role":"system","content":system},{"role":"user","content":user}])


def demo():
    # Load text from a PDF (e.g., job description, notes, report), I used the job description of the job I was applying for
    # can be changed to suit use case 
    loader = PyPDFLoader("job_description.pdf")
    documents = loader.load()

    # Concatenate pages into one string
    sample_text = "\n".join([doc.page_content for doc in documents])

    print("\n=== 1) Bullet Summary ===")
    print(summarize_to_bullets(sample_text, max_bullets=5))

    print("\n=== 2) JSON Skill Extraction ===")
    print(extract_skills_json(sample_text))

    print("\n=== 3) Classification ===")
    print(classify_text(sample_text))

    print("\n=== 4) Markdown Table ===")
    rows = [
        {"Skill": "Python", "Level": "Intermediate", "Notes": "Built RAG prototype"},
        {"Skill": "JavaScript", "Level": "Basic", "Notes": "Small UI integrations"},
        {"Skill": "Prompt Engineering", "Level": "Intermediate", "Notes": "Structured JSON outputs"},
        {"Skill": "RAG", "Level": "Foundational", "Notes": "Document Q&A with embeddings"},
    ]
    print(to_markdown_table(rows))


if __name__ == "__main__":
    # Quick interactive loop for your own text (optional)
    # Or just run demo() and screenshot outputs.
    print("Prompt Practice")
    print("1) Demo all\n2) Summarize to bullets\n3) Extract skills JSON\n4) Classify text\n5) Markdown table from sample rows")
    choice = input("Choose an option (1-5): ").strip()

    if choice == "1":
        demo()
    elif choice == "2":
        t = input("Paste text to summarize:\n")
        print(summarize_to_bullets(t))
    elif choice == "3":
        t = input("Paste text to extract skills from:\n")
        print(extract_skills_json(t))
    elif choice == "4":
        t = input("Paste text to classify:\n")
        print(classify_text(t))
    else:
        print("Bye!")
