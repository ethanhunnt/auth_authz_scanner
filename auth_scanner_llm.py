import os
import json
from datetime import datetime
from openai import OpenAI

# -------------------------------
# CONFIG
# -------------------------------
client = OpenAI()
SYSTEM_PROMPT_PATH = "prompts/auth_authz_universal 1.txt"
TARGET_DIRECTORY = "src"
MODEL = "gpt-4o"

# Output directory for reports
OUTPUT_DIR = "reports"


# -------------------------------
# Ensure reports folder exists
# -------------------------------
def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    return OUTPUT_DIR


# -------------------------------
# Load the system prompt
# -------------------------------
def load_prompt():
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------------
# List source files in repo
# -------------------------------
def list_source_files(base_dir):
    code_files = []
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            if name.endswith((
                ".js", ".ts", ".py", ".java", ".go",
                ".cs", ".php", ".rb", ".cpp", ".kt", ".swift",".jsp", ".asp", ".aspx", ".cshtml", ".vbhtml"
            )):
                code_files.append(os.path.join(root, name))
    return code_files


# -------------------------------
# Analyze one file with LLM
# -------------------------------
def analyze_file(filepath, system_prompt):
    with open(filepath, "r", errors="ignore", encoding="utf-8") as f:
        code = f.read()

    print(f"[*] Scanning: {filepath}")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
Analyze this file for authentication and authorization bypass issues.

FILE: {filepath}

CODE:
```{code}```
"""
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error analyzing {filepath}: {str(e)}"


# -------------------------------
# Generate HTML Report
# -------------------------------
def generate_html_report(json_results, output_file):
    html_head = """
    <html>
    <head>
        <title>Auth/AuthZ Scanner Report</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h1 { color: #333; }
            h2 { margin-top: 40px; color: #444; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 8px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Auth/AuthZ LLM Scanner Report</h1>
    """

    html_body = ""
    for entry in json_results:
        html_body += f"""
        <h2>File: {entry['file']}</h2>
        <pre>{entry['report']}</pre>
        """

    html_end = "</body></html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_head + html_body + html_end)


# -------------------------------
# MAIN
# -------------------------------
def main():
    ensure_output_dir()

    system_prompt = load_prompt()
    files = list_source_files(TARGET_DIRECTORY)

    results = []

    for file in files:
        report = analyze_file(file, system_prompt)
        results.append({"file": file, "report": report})

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = os.path.join(OUTPUT_DIR, f"auth_scanner_results_{timestamp}.json")
    html_path = os.path.join(OUTPUT_DIR, f"auth_scanner_report_{timestamp}.html")

    # Write JSON
    with open(json_path, "w", encoding="utf-8") as out:
        json.dump(results, out, indent=4)

    print(f"\n[+] JSON report written to: {json_path}")

    # Write HTML
    generate_html_report(results, html_path)
    print(f"[+] HTML report written to: {html_path}")

    print("\n[✓] Scan complete!")


if __name__ == "__main__":
    main()


