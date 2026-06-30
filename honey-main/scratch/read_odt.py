import zipfile
import xml.etree.ElementTree as ET
import os

odt_path = r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\doc of Xynera.odt"

if os.path.exists(odt_path):
    print("Found ODT file. Extracting text...")
    try:
        with zipfile.ZipFile(odt_path) as z:
            content_xml = z.read("content.xml")
            root = ET.fromstring(content_xml)
            
            # Simple text extraction from ODT XML namespace namespaces
            namespaces = {
                'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
            }
            
            texts = []
            for elem in root.findall('.//text:p', namespaces):
                text = "".join(elem.itertext())
                texts.append(text)
            
            full_text = "\n".join(texts)
            print("Extracted", len(texts), "paragraphs.")
            
            # Search for Monday, Tuesday, Wednesday
            for line in full_text.split("\n"):
                if any(day in line for day in ["Monday", "Tuesday", "Wednesday", "Fake Employee", "Ecosystem", "Document"]):
                    print("MATCH:", line)
            
            # Write full text to a file so we can view it easily
            out_path = r"c:\Users\VIDIT RATURI\Downloads\honey-main\honey-main\doc_extracted.txt"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"Saved full text to {out_path}")
            
    except Exception as e:
        print("Error reading ODT:", e)
else:
    print("ODT file not found at", odt_path)
