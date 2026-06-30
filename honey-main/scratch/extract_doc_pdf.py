import pypdf
import os

pdf_path = r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\doc of Xynera.pdf"
out_path = r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\doc_pdf_extracted.txt"

if os.path.exists(pdf_path):
    print("Found PDF file. Extracting all text...")
    try:
        reader = pypdf.PdfReader(pdf_path)
        print(f"Total pages: {len(reader.pages)}")
        
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            full_text.append(f"=== PAGE {i+1} ===")
            if text:
                full_text.append(text)
            else:
                full_text.append("[Empty or un-extractable page]")
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(full_text))
        print(f"Extraction complete. Saved to {out_path}")
    except Exception as e:
        print("Error reading PDF:", e)
else:
    print("PDF not found at", pdf_path)
