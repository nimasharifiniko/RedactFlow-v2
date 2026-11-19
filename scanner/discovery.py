import os
from concurrent.futures import ThreadPoolExecutor
from core.extractors import extract_text
from core.merger import scan_document

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def scan_file(filepath: str) -> dict:
    try:
        text = extract_text(filepath)
        findings = scan_document(text, use_llm=False)

        if findings:
            breakdown = {}
            for f in findings:
                t = f["type"]
                breakdown[t] = breakdown.get(t, 0) + 1
            return {
                "filepath": filepath,
                "breakdown": breakdown,
                "total": len(findings)
            }
    except Exception:
        pass
    return None


def scan_directory(directory_path: str) -> list:
    files_to_scan = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                files_to_scan.append(os.path.join(root, file))

    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for res in executor.map(scan_file, files_to_scan):
            if res:
                results.append(res)

    return results
