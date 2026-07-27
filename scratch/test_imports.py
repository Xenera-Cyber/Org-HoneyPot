try:
    import pypdf
    print("pypdf available")
except ImportError:
    print("pypdf NOT available")

try:
    import PyPDF2
    print("PyPDF2 available")
except ImportError:
    print("PyPDF2 NOT available")

try:
    import fitz # PyMuPDF
    print("PyMuPDF available")
except ImportError:
    print("PyMuPDF NOT available")
