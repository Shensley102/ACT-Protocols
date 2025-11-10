#!/usr/bin/env python3
import argparse, json, os, re
from PyPDF2 import PdfReader

def normalize_ws(s: str) -> str:
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\u00a0", " ", s)
    return s

def derive_category(number: str):
    m = re.search(r"GUID-[0-9\-]+-([A-Z]+)\d+", number, re.IGNORECASE)
    code = m.group(1).upper() if m else ""
    cat_map = {"G":"General","M":"Medical","C":"Cardiac","T":"Trauma","PED":"Pediatric","PR":"Procedures"}
    return code, cat_map.get(code, code or "Unknown")

def build(pdf_path: str):
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        pages.append(normalize_ws(txt))

    pat = re.compile(r"Guideline Title:\s*(.*?)\s*Guideline Number:\s*([A-Za-z0-9\-\s]+)", re.I|re.S)
    protocols = []
    cur = None

    for pageno, txt in enumerate(pages, start=1):
        m = pat.search(txt)
        if m:
            if cur is not None:
                cur["end_page"] = pageno - 1
                start_idx = cur["start_page"] - 1
                end_idx = max(start_idx, pageno - 2)
                cur["content"] = "\n".join(pages[start_idx:end_idx+1])
                protocols.append(cur)
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            number_raw = re.sub(r"\s+", "", m.group(2)).upper()
            mnum = re.search(r"(GUID-[0-9\-]+-[A-Z]+[0-9]+)", number_raw, re.I)
            number = mnum.group(1).upper() if mnum else number_raw[:30]
            code, cat = derive_category(number)
            cur = {
                "title": title,
                "number": number,
                "category_code": code,
                "category": cat,
                "start_page": pageno,
            }

    if cur is not None:
        cur["end_page"] = len(pages)
        cur["content"] = "\n".join(pages[cur["start_page"]-1:])

    index = {"source_pdf": os.path.basename(pdf_path), "num_pages": len(pages), "protocols": []}
    for pr in protocols:
        excerpt = re.sub(r"\s+", " ", pr.get("content",""))[:1000]
        index["protocols"].append({
            "title": pr["title"],
            "number": pr["number"],
            "category": pr["category"],
            "category_code": pr.get("category_code",""),
            "start_page": pr["start_page"],
            "end_page": pr["end_page"],
            "excerpt": excerpt
        })
    return index

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", help="Path to protocols PDF")
    ap.add_argument("--out", default="public/act_protocol_index.json")
    args = ap.parse_args()
    idx = build(args.pdf)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f"Wrote {{len(idx['protocols'])}} protocols -> {{args.out}}")

if __name__ == "__main__":
    main()
