
import io
from PyPDF2 import PdfReader

def parse_file(file):
	if file.content_type == "application/pdf":
		return parse_pdf(file.file)
	elif file.content_type == "text/plain":
		return file.file.read().decode("utf-8")
	else:
		raise ValueError("Unsupported file type")

def parse_pdf(file_obj):
	reader = PdfReader(file_obj)
	text = ""
	for page in reader.pages:
		text += page.extract_text() or ""
	return text

def chunk_text(text, chunk_size=400, overlap=100):
	words = text.split()
	chunks = [" ".join(words[((i - overlap) if i > 100 else i):i+chunk_size]) for i in range(0, len(words), chunk_size)]
	return [c for c in chunks if c.strip()]
