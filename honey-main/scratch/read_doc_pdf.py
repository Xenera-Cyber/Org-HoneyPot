import pypdf
import os

pdf_path = r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\doc of Xynera.pdf"

if os.path.exists(pdf_path):
    print("Found PDF file.")
    try:
        reader = pypdf.PdfReader(pdf_path)
        print(f"Total pages: {len(reader.pages)}")
        
        # Check first 5 pages for any text
        for i in range(min(5, len(reader.pages))):
            text = reader.pages[i].extract_text()
            print(f"\n--- Page {i+1} ---")
            if text:
                print(text[:1000]) # print first 1000 chars of page
            else:
                print("[No text extracted]")
    except Exception as e:
        print("Error reading PDF:", e)
else:
    print("PDF not found at", pdf_path)
