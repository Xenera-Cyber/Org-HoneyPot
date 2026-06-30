import os
import pypdf

pdf_files = [
    # Parent directory PDFs
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\Xynera_Architecture_Analysis_Report.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\Xynera_Code_Optimization_Report.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\Xynera_Deception_Prompt_Refinement_Report.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\Xynera_System_Architecture_Report.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\Xynera_Upgrade_History_and_Benefits_Report.pdf",
    # Subdirectory PDFs
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\doc of Xynera.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\xynera-ai\Xynera_Attack_Deception_Report.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\xynera-ai\Xynera_Knowledge_Base.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\xynera-ai\Xynera_Vector_Store_Optimization_Report.pdf",
    r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\xynera-ai\evaluation_report.pdf",
]

search_terms = ["monday", "tuesday", "wednesday", "employee", "ecosystem", "incident", "client", "vendor"]

for pdf_path in pdf_files:
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        continue
    
    print(f"\nScanning: {os.path.basename(pdf_path)}...")
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                line_lower = line.lower()
                for term in search_terms:
                    if term in line_lower:
                        print(f"  [Page {page_num+1}] Match for '{term}': {line.strip()}")
                        break
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
